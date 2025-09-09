import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

class ScenarioSimulator:
    """
    Scenario simulator for what-if analysis of investment portfolios.
    Allows users to simulate different investment scenarios and compare outcomes.
    """
    
    def __init__(self, investment_engine):
        """
        Initialize the scenario simulator with an investment engine.
        
        Args:
            investment_engine: InvestmentEngine instance for portfolio calculations
        """
        self.investment_engine = investment_engine
    
    def simulate_what_if(
        self,
        base_scenario: Dict[str, Any],
        alternative_scenarios: List[Dict[str, Any]],
        years: int = 10,
        simulations: int = 1000
    ) -> Dict[str, Any]:
        """
        Simulate multiple what-if scenarios and compare outcomes.
        
        Args:
            base_scenario: Base scenario parameters
            alternative_scenarios: List of alternative scenarios to compare
            years: Number of years to simulate
            simulations: Number of Monte Carlo simulations per scenario
            
        Returns:
            Dictionary containing simulation results for all scenarios
        """
        results = {}
        
        # Simulate base scenario
        results['base'] = self._simulate_single_scenario(base_scenario, years, simulations)
        
        # Simulate alternative scenarios
        for i, scenario in enumerate(alternative_scenarios):
            results[f'alternative_{i+1}'] = self._simulate_single_scenario(scenario, years, simulations)
        
        # Calculate comparisons
        results['comparison'] = self._compare_scenarios(results)
        
        return results
    
    def _simulate_single_scenario(
        self, 
        scenario: Dict[str, Any], 
        years: int, 
        simulations: int
    ) -> Dict[str, Any]:
        """
        Simulate a single investment scenario.
        
        Args:
            scenario: Scenario parameters including allocation, contributions, etc.
            years: Number of years to simulate
            simulations: Number of simulation paths
            
        Returns:
            Dictionary containing simulation results
        """
        # Extract scenario parameters
        allocation = scenario.get('allocation', {})
        initial_investment = scenario.get('initial_investment', 1000)
        monthly_contribution = scenario.get('monthly_contribution', 100)
        expected_return = scenario.get('expected_return', 0.07)
        volatility = scenario.get('volatility', 0.15)
        
        # Generate simulation paths
        months = years * 12
        final_values = []
        
        for _ in range(simulations):
            # Generate random monthly returns
            monthly_returns = np.random.normal(
                (1 + expected_return) ** (1/12) - 1,
                volatility / np.sqrt(12),
                months
            )
            
            # Calculate portfolio value over time
            value = initial_investment
            for monthly_return in monthly_returns:
                value = (value + monthly_contribution) * (1 + monthly_return)
            
            final_values.append(value)
        
        final_values = np.array(final_values)
        
        # Calculate statistics
        total_contributions = initial_investment + (monthly_contribution * months)
        
        return {
            'scenario_params': scenario,
            'final_values': final_values,
            'mean_final_value': np.mean(final_values),
            'median_final_value': np.median(final_values),
            'std_final_value': np.std(final_values),
            'percentiles': {
                '10th': np.percentile(final_values, 10),
                '25th': np.percentile(final_values, 25),
                '75th': np.percentile(final_values, 75),
                '90th': np.percentile(final_values, 90)
            },
            'total_contributions': total_contributions,
            'mean_profit': np.mean(final_values) - total_contributions,
            'probability_of_loss': np.mean(final_values < total_contributions) * 100,
            'max_value': np.max(final_values),
            'min_value': np.min(final_values)
        }
    
    def _compare_scenarios(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compare scenarios and generate insights.
        
        Args:
            results: Dictionary containing results for all scenarios
            
        Returns:
            Dictionary containing comparison metrics and insights
        """
        base_result = results['base']
        comparisons = {}
        
        # Compare each alternative to base
        for key, result in results.items():
            if key.startswith('alternative_'):
                comparison = {
                    'mean_value_difference': result['mean_final_value'] - base_result['mean_final_value'],
                    'mean_value_percentage_change': ((result['mean_final_value'] / base_result['mean_final_value']) - 1) * 100,
                    'risk_difference': result['std_final_value'] - base_result['std_final_value'],
                    'probability_of_loss_difference': result['probability_of_loss'] - base_result['probability_of_loss'],
                    'better_outcome_probability': np.mean(
                        result['final_values'] > base_result['final_values']
                    ) * 100
                }
                comparisons[key] = comparison
        
        return comparisons
    
    def simulate_contribution_changes(
        self,
        base_monthly_contribution: float,
        contribution_changes: List[float],
        portfolio_params: Dict[str, Any],
        years: int = 10
    ) -> Dict[str, Any]:
        """
        Simulate the impact of different monthly contribution amounts.
        
        Args:
            base_monthly_contribution: Current monthly contribution
            contribution_changes: List of alternative contribution amounts
            portfolio_params: Portfolio parameters (allocation, returns, etc.)
            years: Number of years to simulate
            
        Returns:
            Dictionary containing results for each contribution level
        """
        scenarios = []
        
        # Create base scenario
        base_scenario = {
            **portfolio_params,
            'monthly_contribution': base_monthly_contribution
        }
        
        # Create alternative scenarios
        for contribution in contribution_changes:
            scenario = {
                **portfolio_params,
                'monthly_contribution': contribution
            }
            scenarios.append(scenario)
        
        return self.simulate_what_if(base_scenario, scenarios, years)
    
    def simulate_risk_tolerance_changes(
        self,
        base_allocation: Dict[str, float],
        risk_levels: List[str],
        portfolio_params: Dict[str, Any],
        years: int = 10
    ) -> Dict[str, Any]:
        """
        Simulate the impact of different risk tolerance levels.
        
        Args:
            base_allocation: Current portfolio allocation
            risk_levels: List of risk levels ('conservative', 'moderate', 'aggressive')
            portfolio_params: Portfolio parameters
            years: Number of years to simulate
            
        Returns:
            Dictionary containing results for each risk level
        """
        # Define risk-based allocations and expected returns
        risk_profiles = {
            'conservative': {
                'allocation': {'Stocks': 30, 'Bonds': 60, 'Cash': 10},
                'expected_return': 0.05,
                'volatility': 0.08
            },
            'moderate': {
                'allocation': {'Stocks': 60, 'Bonds': 35, 'Cash': 5},
                'expected_return': 0.07,
                'volatility': 0.12
            },
            'aggressive': {
                'allocation': {'Stocks': 85, 'Bonds': 15, 'Cash': 0},
                'expected_return': 0.10,
                'volatility': 0.18
            }
        }
        
        scenarios = []
        base_scenario = {
            **portfolio_params,
            'allocation': base_allocation
        }
        
        # Create scenarios for each risk level
        for risk_level in risk_levels:
            if risk_level in risk_profiles:
                scenario = {
                    **portfolio_params,
                    **risk_profiles[risk_level]
                }
                scenarios.append(scenario)
        
        return self.simulate_what_if(base_scenario, scenarios, years)
    
    def simulate_time_horizon_impact(
        self,
        portfolio_params: Dict[str, Any],
        time_horizons: List[int]
    ) -> Dict[str, Any]:
        """
        Simulate the impact of different investment time horizons.
        
        Args:
            portfolio_params: Portfolio parameters
            time_horizons: List of time horizons in years
            
        Returns:
            Dictionary containing results for each time horizon
        """
        results = {}
        
        for years in time_horizons:
            result = self._simulate_single_scenario(portfolio_params, years, 1000)
            results[f'{years}_years'] = result
        
        return results
    
    def generate_scenario_insights(self, simulation_results: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Generate human-readable insights from simulation results.
        
        Args:
            simulation_results: Results from scenario simulation
            
        Returns:
            List of insight dictionaries with title, description, and priority
        """
        insights = []
        
        if 'comparison' in simulation_results:
            comparisons = simulation_results['comparison']
            
            for scenario_key, comparison in comparisons.items():
                # Analyze mean value difference
                value_change = comparison['mean_value_percentage_change']
                
                if value_change > 10:
                    insights.append({
                        'title': f'Significant Improvement Potential',
                        'description': f'This scenario could increase your expected portfolio value by {value_change:.1f}%.',
                        'priority': 'High',
                        'type': 'opportunity'
                    })
                elif value_change < -10:
                    insights.append({
                        'title': f'Potential Downside Risk',
                        'description': f'This scenario could decrease your expected portfolio value by {abs(value_change):.1f}%.',
                        'priority': 'High',
                        'type': 'risk'
                    })
                
                # Analyze risk changes
                better_outcome_prob = comparison['better_outcome_probability']
                
                if better_outcome_prob > 70:
                    insights.append({
                        'title': f'High Success Probability',
                        'description': f'This scenario has a {better_outcome_prob:.1f}% chance of outperforming your current plan.',
                        'priority': 'Medium',
                        'type': 'opportunity'
                    })
                elif better_outcome_prob < 30:
                    insights.append({
                        'title': f'Lower Success Probability',
                        'description': f'This scenario has only a {better_outcome_prob:.1f}% chance of outperforming your current plan.',
                        'priority': 'Medium',
                        'type': 'warning'
                    })
        
        return insights
