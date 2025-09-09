import pytest
import numpy as np
import pandas as pd
from backend.services.investment_engine import InvestmentEngine

class TestInvestmentEngine:
    """Test suite for the InvestmentEngine class."""
    
    @pytest.fixture
    def sample_returns(self):
        """Create sample historical returns data for testing."""
        np.random.seed(42)  # For reproducible tests
        dates = pd.date_range('2020-01-01', periods=252, freq='D')
        returns = pd.DataFrame({
            'Stocks': np.random.normal(0.0008, 0.02, 252),  # ~8% annual return, 20% volatility
            'Bonds': np.random.normal(0.0003, 0.005, 252),  # ~3% annual return, 5% volatility
            'Real Estate': np.random.normal(0.0005, 0.015, 252),  # ~5% annual return, 15% volatility
        }, index=dates)
        return returns
    
    @pytest.fixture
    def engine(self, sample_returns):
        """Create an InvestmentEngine instance for testing."""
        return InvestmentEngine(sample_returns)
    
    def test_initialization(self, sample_returns):
        """Test that the engine initializes correctly."""
        engine = InvestmentEngine(sample_returns)
        
        assert engine.assets == ['Stocks', 'Bonds', 'Real Estate']
        assert len(engine.expected_returns) == 3
        assert engine.cov_matrix.shape == (3, 3)
    
    def test_monte_carlo_simulation(self, engine):
        """Test Monte Carlo simulation functionality."""
        allocation = {'Stocks': 0.6, 'Bonds': 0.3, 'Real Estate': 0.1}
        
        results = engine.monte_carlo_simulation(allocation, years=5, simulations=100)
        
        # Check that results contain expected keys
        expected_keys = ['paths', 'final_values', 'mean_return', 'volatility', 'sharpe_ratio', 'percentiles']
        for key in expected_keys:
            assert key in results
        
        # Check data types and shapes
        assert isinstance(results['final_values'], np.ndarray)
        assert len(results['final_values']) == 100
        assert results['paths'].shape == (100, 5 * 252)
        assert len(results['percentiles']) == 5
        
        # Check that values are reasonable
        assert results['mean_return'] > -1 and results['mean_return'] < 1
        assert results['volatility'] > 0
        assert isinstance(results['sharpe_ratio'], float)
    
    def test_portfolio_optimization(self, engine):
        """Test portfolio optimization functionality."""
        optimized_allocation = engine.optimize_portfolio(risk_tolerance=0.5)
        
        # Check that allocation sums to 1 (within tolerance)
        total_allocation = sum(optimized_allocation.values())
        assert abs(total_allocation - 1.0) < 0.01
        
        # Check that all allocations are non-negative
        for allocation in optimized_allocation.values():
            assert allocation >= 0
        
        # Check that we get allocations for all assets
        assert len(optimized_allocation) == len(engine.assets)
    
    def test_sharpe_ratio_calculation(self, engine):
        """Test Sharpe ratio calculation."""
        # Test with known values
        sharpe = engine._calculate_sharpe_ratio(0.08, 0.15, 0.02)
        expected_sharpe = (0.08 - 0.02) / 0.15
        assert abs(sharpe - expected_sharpe) < 0.001
        
        # Test edge case with zero volatility
        sharpe_zero_vol = engine._calculate_sharpe_ratio(0.08, 0.0, 0.02)
        assert sharpe_zero_vol > 0  # Should handle division by zero
    
    def test_efficient_frontier(self, engine):
        """Test efficient frontier generation."""
        volatilities, returns, sharpe_ratios = engine.get_efficient_frontier(num_portfolios=50)
        
        # Check that we get the right number of portfolios
        assert len(volatilities) == 50
        assert len(returns) == 50
        assert len(sharpe_ratios) == 50
        
        # Check that values are reasonable
        assert all(vol >= 0 for vol in volatilities)
        assert all(ret > -1 and ret < 1 for ret in returns)
    
    def test_allocation_edge_cases(self, engine):
        """Test edge cases for portfolio allocation."""
        # Test with empty allocation
        empty_allocation = {}
        results = engine.monte_carlo_simulation(empty_allocation, years=1, simulations=10)
        assert 'final_values' in results
        
        # Test with single asset allocation
        single_allocation = {'Stocks': 1.0}
        results = engine.monte_carlo_simulation(single_allocation, years=1, simulations=10)
        assert len(results['final_values']) == 10
        
        # Test with partial allocation (doesn't sum to 1)
        partial_allocation = {'Stocks': 0.5, 'Bonds': 0.3}
        results = engine.monte_carlo_simulation(partial_allocation, years=1, simulations=10)
        assert 'final_values' in results
