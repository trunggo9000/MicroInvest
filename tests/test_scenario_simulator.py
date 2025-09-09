import pytest
import numpy as np
import pandas as pd
from backend.services.scenario_simulator import ScenarioSimulator
from backend.services.investment_engine import InvestmentEngine

class TestScenarioSimulator:
    """Test suite for the ScenarioSimulator class."""
    
    @pytest.fixture
    def sample_returns(self):
        """Create sample historical returns data for testing."""
        np.random.seed(42)
        dates = pd.date_range('2020-01-01', periods=252, freq='D')
        returns = pd.DataFrame({
            'Stocks': np.random.normal(0.0008, 0.02, 252),
            'Bonds': np.random.normal(0.0003, 0.005, 252),
            'Real Estate': np.random.normal(0.0005, 0.015, 252),
        }, index=dates)
        return returns
    
    @pytest.fixture
    def investment_engine(self, sample_returns):
        """Create an InvestmentEngine instance for testing."""
        return InvestmentEngine(sample_returns)
    
    @pytest.fixture
    def simulator(self, investment_engine):
        """Create a ScenarioSimulator instance for testing."""
        return ScenarioSimulator(investment_engine)
    
    @pytest.fixture
    def base_scenario(self):
        """Create a base scenario for testing."""
        return {
            'allocation': {'Stocks': 0.6, 'Bonds': 0.4},
            'initial_investment': 1000,
            'monthly_contribution': 100,
            'expected_return': 0.07,
            'volatility': 0.15
        }
    
    def test_single_scenario_simulation(self, simulator, base_scenario):
        """Test simulation of a single scenario."""
        result = simulator._simulate_single_scenario(base_scenario, years=5, simulations=100)
        
        # Check that result contains expected keys
        expected_keys = [
            'scenario_params', 'final_values', 'mean_final_value', 'median_final_value',
            'std_final_value', 'percentiles', 'total_contributions', 'mean_profit',
            'probability_of_loss', 'max_value', 'min_value'
        ]
        for key in expected_keys:
            assert key in result
        
        # Check data types and values
        assert isinstance(result['final_values'], np.ndarray)
        assert len(result['final_values']) == 100
        assert result['mean_final_value'] > 0
        assert result['total_contributions'] == 1000 + (100 * 5 * 12)  # Initial + monthly contributions
        assert 0 <= result['probability_of_loss'] <= 100
        
        # Check percentiles
        assert len(result['percentiles']) == 4
        assert result['percentiles']['10th'] <= result['percentiles']['25th']
        assert result['percentiles']['25th'] <= result['percentiles']['75th']
        assert result['percentiles']['75th'] <= result['percentiles']['90th']
    
    def test_what_if_simulation(self, simulator, base_scenario):
        """Test what-if scenario simulation."""
        alternative_scenarios = [
            {
                **base_scenario,
                'monthly_contribution': 150  # Increased contribution
            },
            {
                **base_scenario,
                'expected_return': 0.09,  # Higher return
                'volatility': 0.20
            }
        ]
        
        results = simulator.simulate_what_if(base_scenario, alternative_scenarios, years=5, simulations=50)
        
        # Check that results contain all scenarios
        assert 'base' in results
        assert 'alternative_1' in results
        assert 'alternative_2' in results
        assert 'comparison' in results
        
        # Check comparison results
        comparison = results['comparison']
        assert 'alternative_1' in comparison
        assert 'alternative_2' in comparison
        
        # Check comparison metrics
        for alt_key in ['alternative_1', 'alternative_2']:
            comp = comparison[alt_key]
            assert 'mean_value_difference' in comp
            assert 'mean_value_percentage_change' in comp
            assert 'risk_difference' in comp
            assert 'probability_of_loss_difference' in comp
            assert 'better_outcome_probability' in comp
            
            # Check that probability is between 0 and 100
            assert 0 <= comp['better_outcome_probability'] <= 100
    
    def test_contribution_changes_simulation(self, simulator, base_scenario):
        """Test simulation of different contribution amounts."""
        contribution_changes = [50, 150, 200]
        
        results = simulator.simulate_contribution_changes(
            base_monthly_contribution=100,
            contribution_changes=contribution_changes,
            portfolio_params=base_scenario,
            years=5
        )
        
        # Check that results contain base and alternatives
        assert 'base' in results
        assert 'alternative_1' in results  # $50
        assert 'alternative_2' in results  # $150
        assert 'alternative_3' in results  # $200
        
        # Check that higher contributions generally lead to higher final values
        base_value = results['base']['mean_final_value']
        alt2_value = results['alternative_2']['mean_final_value']  # $150 contribution
        assert alt2_value > base_value  # Higher contribution should yield higher value
    
    def test_risk_tolerance_simulation(self, simulator, base_scenario):
        """Test simulation of different risk tolerance levels."""
        risk_levels = ['conservative', 'moderate', 'aggressive']
        
        results = simulator.simulate_risk_tolerance_changes(
            base_allocation={'Stocks': 0.6, 'Bonds': 0.4},
            risk_levels=risk_levels,
            portfolio_params=base_scenario,
            years=5
        )
        
        # Check that results contain all risk levels
        assert 'base' in results
        assert len([k for k in results.keys() if k.startswith('alternative_')]) == 3
        
        # Check that aggressive portfolios generally have higher volatility
        # (This is a general expectation, though not guaranteed in all simulations)
        conservative_result = results['alternative_1']  # First alternative should be conservative
        aggressive_result = results['alternative_3']   # Third alternative should be aggressive
        
        # Conservative should generally have lower standard deviation
        assert conservative_result['std_final_value'] <= aggressive_result['std_final_value'] * 1.5  # Allow some variance
    
    def test_time_horizon_impact(self, simulator, base_scenario):
        """Test simulation of different time horizons."""
        time_horizons = [1, 5, 10]
        
        results = simulator.simulate_time_horizon_impact(base_scenario, time_horizons)
        
        # Check that results contain all time horizons
        assert '1_years' in results
        assert '5_years' in results
        assert '10_years' in results
        
        # Check that longer time horizons generally lead to higher values
        one_year_value = results['1_years']['mean_final_value']
        ten_year_value = results['10_years']['mean_final_value']
        assert ten_year_value > one_year_value
    
    def test_scenario_insights_generation(self, simulator, base_scenario):
        """Test generation of scenario insights."""
        alternative_scenarios = [
            {
                **base_scenario,
                'monthly_contribution': 200  # Significantly higher contribution
            }
        ]
        
        results = simulator.simulate_what_if(base_scenario, alternative_scenarios, years=5, simulations=50)
        insights = simulator.generate_scenario_insights(results)
        
        # Check that insights are generated
        assert isinstance(insights, list)
        
        # If insights are generated, check their structure
        if insights:
            for insight in insights:
                assert 'title' in insight
                assert 'description' in insight
                assert 'priority' in insight
                assert 'type' in insight
                assert insight['priority'] in ['High', 'Medium', 'Low']
                assert insight['type'] in ['opportunity', 'risk', 'warning']
    
    def test_edge_cases(self, simulator):
        """Test edge cases and error handling."""
        # Test with minimal scenario
        minimal_scenario = {
            'allocation': {'Stocks': 1.0},
            'initial_investment': 100,
            'monthly_contribution': 10,
            'expected_return': 0.05,
            'volatility': 0.10
        }
        
        result = simulator._simulate_single_scenario(minimal_scenario, years=1, simulations=10)
        assert 'final_values' in result
        assert len(result['final_values']) == 10
        
        # Test with zero contributions
        zero_contrib_scenario = {
            **minimal_scenario,
            'monthly_contribution': 0
        }
        
        result = simulator._simulate_single_scenario(zero_contrib_scenario, years=1, simulations=10)
        assert 'final_values' in result
        
        # Test with very high volatility
        high_vol_scenario = {
            **minimal_scenario,
            'volatility': 0.50
        }
        
        result = simulator._simulate_single_scenario(high_vol_scenario, years=1, simulations=10)
        assert 'final_values' in result
        assert result['std_final_value'] > 0
