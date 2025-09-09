import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from scipy.optimize import minimize
from .market_data_service import MarketDataService

class InvestmentEngine:
    """
    Core investment engine that handles portfolio optimization and Monte Carlo simulations.
    """
    
    def __init__(self, market_data_service: Optional[MarketDataService] = None):
        """
        Initialize the investment engine with market data service.
        
        Args:
            market_data_service: Service to fetch real market data (optional)
        """
        self.market_data_service = market_data_service or MarketDataService()
        self.historical_returns = None
        self.assets = []
        self.expected_returns = None
        self.cov_matrix = None
    
    def initialize_with_assets(self, symbols: List[str], period: str = '5y'):
        """
        Initialize the engine with specific assets and fetch their historical data.
        
        Args:
            symbols: List of asset symbols to include
            period: Historical period to fetch ('1y', '2y', '5y', '10y')
        """
        self.historical_returns = self.market_data_service.get_historical_data(symbols, period=period)
        self.assets = self.historical_returns.columns.tolist()
        self.expected_returns = self._calculate_expected_returns()
        self.cov_matrix = self._calculate_covariance_matrix()
    
    def _calculate_expected_returns(self) -> np.ndarray:
        """Calculate annualized expected returns for each asset."""
        return (1 + self.historical_returns.mean()) ** 252 - 1
    
    def _calculate_covariance_matrix(self) -> np.ndarray:
        """Calculate annualized covariance matrix of asset returns."""
        return self.historical_returns.cov() * 252
    
    def monte_carlo_simulation(
        self, 
        allocation: Dict[str, float],
        years: int = 10,
        simulations: int = 1000
    ) -> Dict[str, np.ndarray]:
        """
        Run Monte Carlo simulation for portfolio growth.
        
        Args:
            allocation: Dictionary of asset allocations (e.g., {'stocks': 0.6, 'bonds': 0.4})
            years: Number of years to simulate
            simulations: Number of simulation paths
            
        Returns:
            Dictionary with simulation results including paths and statistics
        """
        # Convert allocation to array in the order of self.assets
        weights = np.array([allocation.get(asset, 0) for asset in self.assets])
        
        # Calculate portfolio expected return and volatility
        port_return = np.sum(self.expected_returns * weights)
        port_volatility = np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix, weights)))
        
        # Generate random returns based on normal distribution
        daily_returns = np.random.normal(
            (1 + port_return) ** (1/252) - 1,
            port_volatility / np.sqrt(252),
            (simulations, years * 252)
        )
        
        # Calculate cumulative returns
        portfolio_paths = np.cumprod(1 + daily_returns, axis=1)
        
        # Calculate statistics
        final_values = portfolio_paths[:, -1]
        percentiles = np.percentile(final_values, [5, 25, 50, 75, 95])
        
        return {
            'paths': portfolio_paths,
            'final_values': final_values,
            'mean_return': port_return,
            'volatility': port_volatility,
            'sharpe_ratio': self._calculate_sharpe_ratio(port_return, port_volatility),
            'percentiles': percentiles
        }
    
    def optimize_portfolio(
        self, 
        risk_tolerance: float,
        target_return: float = None,
        max_volatility: float = None
    ) -> Dict[str, float]:
        """
        Optimize portfolio allocation based on risk tolerance and constraints.
        
        Args:
            risk_tolerance: Float between 0 (low risk) and 1 (high risk)
            target_return: Optional target return to achieve
            max_volatility: Optional maximum volatility constraint
            
        Returns:
            Dictionary of optimized asset allocations
        """
        n_assets = len(self.assets)
        
        # Define objective function (minimize negative Sharpe ratio)
        def objective(weights):
            port_return = np.sum(self.expected_returns * weights)
            port_volatility = np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix, weights)))
            return -self._calculate_sharpe_ratio(port_return, port_volatility)
        
        # Constraints
        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}  # Sum of weights = 1
        ]
        
        if target_return is not None:
            constraints.append(
                {'type': 'ineq', 'fun': lambda x: np.sum(self.expected_returns * x) - target_return}
            )
        
        if max_volatility is not None:
            constraints.append(
                {'type': 'ineq', 'fun': lambda x: max_volatility - np.sqrt(np.dot(x.T, np.dot(self.cov_matrix, x)))}
            )
        
        # Bounds (0 <= weight <= 1)
        bounds = tuple((0, 1) for _ in range(n_assets))
        
        # Initial guess (equal weights)
        init_weights = np.array([1/n_assets] * n_assets)
        
        # Optimize
        result = minimize(
            objective,
            init_weights,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        
        # Return optimized allocation as dictionary
        return {asset: weight for asset, weight in zip(self.assets, result.x)}
    
    def _calculate_sharpe_ratio(self, expected_return: float, volatility: float, risk_free_rate: float = 0.02) -> float:
        """Calculate Sharpe ratio for given return and volatility."""
        return (expected_return - risk_free_rate) / (volatility + 1e-10)  # Add small number to avoid division by zero
    
    def get_efficient_frontier(self, num_portfolios: int = 100) -> Tuple[np.ndarray, np.ndarray]:
        """Generate points on the efficient frontier."""
        results = np.zeros((3, num_portfolios))
        
        for i in range(num_portfolios):
            weights = np.random.random(len(self.assets))
            weights /= np.sum(weights)
            
            port_return = np.sum(self.expected_returns * weights)
            port_volatility = np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix, weights)))
            sharpe = self._calculate_sharpe_ratio(port_return, port_volatility)
            
            results[0, i] = port_volatility
            results[1, i] = port_return
            results[2, i] = sharpe
            
        return results[0], results[1], results[2]
    
    def generate_portfolio_recommendation(
        self, 
        monthly_investment: float,
        risk_tolerance: str,
        time_horizon: str,
        investment_goal: str
    ) -> Dict:
        """
        Generate a complete portfolio recommendation based on user preferences.
        
        Args:
            monthly_investment: Monthly investment amount
            risk_tolerance: 'Conservative', 'Balanced', or 'Growth-Focused'
            time_horizon: Investment time horizon
            investment_goal: Primary investment goal
            
        Returns:
            Dictionary with complete portfolio recommendation
        """
        # Map risk tolerance to asset allocation strategy
        risk_mapping = {
            'Conservative (Low Risk)': 'conservative',
            'Balanced (Medium Risk)': 'moderate', 
            'Growth-Focused (High Risk)': 'aggressive'
        }
        
        # Also handle cases where the exact string might not match
        if 'Conservative' in risk_tolerance:
            risk_level = 'conservative'
        elif 'Balanced' in risk_tolerance:
            risk_level = 'moderate'
        elif 'Growth' in risk_tolerance:
            risk_level = 'aggressive'
        else:
            risk_level = risk_mapping.get(risk_tolerance, 'moderate')
        
        # Get recommended investment options
        investment_options = self.market_data_service.get_investment_options(risk_level)
        
        # Initialize engine with the recommended symbols
        symbols = [option['symbol'] for option in investment_options]
        self.initialize_with_assets(symbols)
        
        # Create allocation dictionary
        allocation = {option['symbol']: option['allocation'] for option in investment_options}
        
        # Calculate portfolio metrics
        portfolio_metrics = self.market_data_service.calculate_portfolio_metrics(allocation)
        
        # Calculate projected value based on time horizon
        years = self._parse_time_horizon(time_horizon)
        monthly_return = portfolio_metrics['annual_return'] / 12
        months = years * 12
        
        # For very short time horizons (less than 1 year), use simple calculation
        if years < 1:
            # For short-term, minimal compound growth - mostly just contributions
            projected_value = monthly_investment * months * (1 + portfolio_metrics['annual_return'] * years)
        elif monthly_return > 0:
            # Future value of annuity formula for longer terms
            projected_value = monthly_investment * (((1 + monthly_return) ** months - 1) / monthly_return)
        else:
            projected_value = monthly_investment * months
        
        # Calculate total contributions
        total_contributions = monthly_investment * months
        
        return {
            'monthlyAmount': monthly_investment,
            'investments': investment_options,
            'allocation': allocation,
            'totalExpectedReturn': portfolio_metrics['annual_return'] * 100,
            'projectedValue': projected_value,
            'totalContributions': total_contributions,
            'projectedGains': projected_value - total_contributions,
            'timeHorizon': years,
            'riskLevel': risk_level,
            'portfolioMetrics': portfolio_metrics,
            'sharpeRatio': portfolio_metrics['sharpe_ratio'],
            'volatility': portfolio_metrics['annual_volatility'] * 100,
            'maxDrawdown': portfolio_metrics['max_drawdown'] * 100
        }
    
    def _parse_time_horizon(self, time_horizon: str) -> float:
        """Parse time horizon string to years."""
        horizon_mapping = {
            '1-2 years': 1.5,
            '3-5 years': 4,
            '5-10 years': 7,
            '10+ years': 15,
            'Less than 1 year': 0.25,
            '3 months': 0.25,
            '1-3 years': 2,
            '3-7 years': 5,
            '7-15 years': 10,
            '15+ years': 20
        }
        return horizon_mapping.get(time_horizon, 10)
    
    def run_monte_carlo_with_contributions(
        self,
        allocation: Dict[str, float],
        monthly_contribution: float,
        years: int = 10,
        simulations: int = 1000
    ) -> Dict:
        """
        Run Monte Carlo simulation including monthly contributions.
        
        Args:
            allocation: Asset allocation dictionary
            monthly_contribution: Monthly contribution amount
            years: Investment period in years
            simulations: Number of simulation runs
            
        Returns:
            Dictionary with simulation results
        """
        if not self.assets:
            symbols = list(allocation.keys())
            self.initialize_with_assets(symbols)
        
        # Convert allocation to weights array
        weights = np.array([allocation.get(asset, 0) for asset in self.assets])
        
        # Calculate portfolio expected return and volatility
        port_return = np.sum(self.expected_returns * weights)
        port_volatility = np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix, weights)))
        
        months = years * 12
        simulation_results = []
        
        for _ in range(simulations):
            portfolio_value = 0
            
            for month in range(months):
                # Add monthly contribution
                portfolio_value += monthly_contribution
                
                # Apply monthly return (with volatility)
                monthly_return = np.random.normal(
                    (1 + port_return) ** (1/12) - 1,
                    port_volatility / np.sqrt(12)
                )
                portfolio_value *= (1 + monthly_return)
            
            simulation_results.append(max(0, portfolio_value))
        
        simulation_results = np.array(simulation_results)
        
        return {
            'final_values': simulation_results,
            'mean_value': np.mean(simulation_results),
            'median_value': np.median(simulation_results),
            'percentile_10': np.percentile(simulation_results, 10),
            'percentile_90': np.percentile(simulation_results, 90),
            'best_case': np.max(simulation_results),
            'worst_case': np.min(simulation_results),
            'total_contributions': monthly_contribution * months,
            'probability_of_profit': np.mean(simulation_results > monthly_contribution * months) * 100
        }
