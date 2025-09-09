import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import requests
import time

class MarketDataService:
    """
    Service to fetch real market data from various sources.
    Uses Yahoo Finance as the primary data source.
    """
    
    def __init__(self):
        """Initialize the market data service."""
        self.cache = {}
        self.cache_expiry = {}
        self.cache_duration = 3600  # 1 hour cache
        
        # Define common investment assets
        self.asset_symbols = {
            'US_STOCKS': 'VTI',      # Vanguard Total Stock Market ETF
            'INTL_STOCKS': 'VTIAX',  # Vanguard Total International Stock Index
            'BONDS': 'BND',          # Vanguard Total Bond Market ETF
            'REAL_ESTATE': 'VNQ',    # Vanguard Real Estate ETF
            'COMMODITIES': 'VDE',    # Vanguard Energy ETF
            'EMERGING_MARKETS': 'VWO', # Vanguard Emerging Markets ETF
            'SMALL_CAP': 'VB',       # Vanguard Small-Cap ETF
            'TECH': 'VGT',           # Vanguard Information Technology ETF
            'HEALTHCARE': 'VHT',     # Vanguard Health Care ETF
            'TREASURY': 'VGIT'       # Vanguard Intermediate-Term Treasury ETF
        }
    
    def _is_cache_valid(self, key: str) -> bool:
        """Check if cached data is still valid."""
        if key not in self.cache or key not in self.cache_expiry:
            return False
        return datetime.now() < self.cache_expiry[key]
    
    def _cache_data(self, key: str, data: any) -> None:
        """Cache data with expiry time."""
        self.cache[key] = data
        self.cache_expiry[key] = datetime.now() + timedelta(seconds=self.cache_duration)
    
    def get_historical_data(
        self, 
        symbols: List[str] = None, 
        period: str = '5y',
        interval: str = '1d'
    ) -> pd.DataFrame:
        """
        Fetch historical price data for given symbols.
        
        Args:
            symbols: List of ticker symbols (defaults to common investment assets)
            period: Time period ('1y', '2y', '5y', '10y', 'max')
            interval: Data interval ('1d', '1wk', '1mo')
            
        Returns:
            DataFrame with historical returns for each asset
        """
        if symbols is None:
            symbols = list(self.asset_symbols.values())
        
        cache_key = f"historical_{'-'.join(symbols)}_{period}_{interval}"
        
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]
        
        try:
            # Fetch data for all symbols
            data = yf.download(symbols, period=period, interval=interval, progress=False)
            
            if len(symbols) == 1:
                # Single symbol case
                prices = data['Adj Close'].dropna()
                returns = prices.pct_change().dropna()
                result = pd.DataFrame({symbols[0]: returns})
            else:
                # Multiple symbols case
                prices = data['Adj Close'].dropna()
                returns = prices.pct_change().dropna()
                result = returns
            
            # Cache the result
            self._cache_data(cache_key, result)
            return result
            
        except Exception as e:
            print(f"Error fetching historical data: {e}")
            # Return mock data as fallback
            return self._get_mock_historical_data(symbols, period)
    
    def get_current_prices(self, symbols: List[str] = None) -> Dict[str, float]:
        """
        Get current prices for given symbols.
        
        Args:
            symbols: List of ticker symbols
            
        Returns:
            Dictionary mapping symbols to current prices
        """
        if symbols is None:
            symbols = list(self.asset_symbols.values())
        
        cache_key = f"current_prices_{'-'.join(symbols)}"
        
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]
        
        try:
            prices = {}
            for symbol in symbols:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                prices[symbol] = info.get('regularMarketPrice', info.get('previousClose', 100.0))
            
            self._cache_data(cache_key, prices)
            return prices
            
        except Exception as e:
            print(f"Error fetching current prices: {e}")
            # Return mock prices as fallback
            return {symbol: 100.0 for symbol in symbols}
    
    def get_asset_info(self, symbol: str) -> Dict:
        """
        Get detailed information about an asset.
        
        Args:
            symbol: Ticker symbol
            
        Returns:
            Dictionary with asset information
        """
        cache_key = f"asset_info_{symbol}"
        
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]
        
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            result = {
                'name': info.get('longName', symbol),
                'sector': info.get('sector', 'Unknown'),
                'expense_ratio': info.get('annualReportExpenseRatio', 0.0),
                'dividend_yield': info.get('dividendYield', 0.0),
                'market_cap': info.get('marketCap', 0),
                'beta': info.get('beta', 1.0),
                'pe_ratio': info.get('trailingPE', None),
                'description': info.get('longBusinessSummary', '')[:200] + '...' if info.get('longBusinessSummary') else ''
            }
            
            self._cache_data(cache_key, result)
            return result
            
        except Exception as e:
            print(f"Error fetching asset info for {symbol}: {e}")
            return {
                'name': symbol,
                'sector': 'Unknown',
                'expense_ratio': 0.0,
                'dividend_yield': 0.0,
                'market_cap': 0,
                'beta': 1.0,
                'pe_ratio': None,
                'description': 'Information not available'
            }
    
    def get_investment_options(self, risk_tolerance: str = 'moderate') -> List[Dict]:
        """
        Get recommended investment options based on risk tolerance.
        
        Args:
            risk_tolerance: 'conservative', 'moderate', or 'aggressive'
            
        Returns:
            List of investment option dictionaries
        """
        if risk_tolerance.lower() == 'conservative':
            symbols = ['BND', 'VGIT', 'VTI', 'VTIAX']
            allocations = [0.4, 0.2, 0.3, 0.1]
        elif risk_tolerance.lower() == 'aggressive':
            symbols = ['VTI', 'VGT', 'VWO', 'VNQ']
            allocations = [0.4, 0.3, 0.2, 0.1]
        else:  # moderate
            symbols = ['VTI', 'VTIAX', 'BND', 'VNQ']
            allocations = [0.4, 0.2, 0.3, 0.1]
        
        options = []
        for symbol, allocation in zip(symbols, allocations):
            info = self.get_asset_info(symbol)
            current_price = self.get_current_prices([symbol])[symbol]
            
            options.append({
                'symbol': symbol,
                'name': info['name'],
                'allocation': allocation,
                'current_price': current_price,
                'expense_ratio': info['expense_ratio'],
                'dividend_yield': info['dividend_yield'],
                'sector': info['sector'],
                'description': info['description']
            })
        
        return options
    
    def calculate_portfolio_metrics(self, allocation: Dict[str, float], period: str = '1y') -> Dict:
        """
        Calculate portfolio metrics based on allocation and historical data.
        
        Args:
            allocation: Dictionary mapping symbols to allocation percentages
            period: Historical period to analyze
            
        Returns:
            Dictionary with portfolio metrics
        """
        symbols = list(allocation.keys())
        weights = np.array(list(allocation.values()))
        
        # Get historical returns
        returns_data = self.get_historical_data(symbols, period=period)
        
        if returns_data.empty:
            return self._get_mock_portfolio_metrics()
        
        # Calculate portfolio returns
        portfolio_returns = (returns_data * weights).sum(axis=1)
        
        # Calculate metrics
        annual_return = (1 + portfolio_returns.mean()) ** 252 - 1
        annual_volatility = portfolio_returns.std() * np.sqrt(252)
        sharpe_ratio = (annual_return - 0.02) / annual_volatility if annual_volatility > 0 else 0
        
        # Calculate maximum drawdown
        cumulative_returns = (1 + portfolio_returns).cumprod()
        rolling_max = cumulative_returns.expanding().max()
        drawdown = (cumulative_returns - rolling_max) / rolling_max
        max_drawdown = drawdown.min()
        
        return {
            'annual_return': annual_return,
            'annual_volatility': annual_volatility,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'total_return': cumulative_returns.iloc[-1] - 1,
            'best_month': portfolio_returns.max(),
            'worst_month': portfolio_returns.min()
        }
    
    def _get_mock_historical_data(self, symbols: List[str], period: str) -> pd.DataFrame:
        """Generate mock historical data as fallback."""
        days = {'1y': 252, '2y': 504, '5y': 1260, '10y': 2520}.get(period, 1260)
        dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
        
        data = {}
        for symbol in symbols:
            # Generate realistic returns based on asset type
            if 'BND' in symbol or 'VGIT' in symbol:  # Bonds
                returns = np.random.normal(0.0002, 0.005, days)  # Low volatility
            elif 'VTI' in symbol or 'VTIAX' in symbol:  # Stocks
                returns = np.random.normal(0.0004, 0.015, days)  # Medium volatility
            else:  # Other assets
                returns = np.random.normal(0.0003, 0.012, days)
            
            data[symbol] = returns
        
        return pd.DataFrame(data, index=dates)
    
    def _get_mock_portfolio_metrics(self) -> Dict:
        """Generate mock portfolio metrics as fallback."""
        return {
            'annual_return': 0.08,
            'annual_volatility': 0.12,
            'sharpe_ratio': 0.5,
            'max_drawdown': -0.15,
            'total_return': 0.08,
            'best_month': 0.05,
            'worst_month': -0.04
        }
