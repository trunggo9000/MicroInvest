#!/usr/bin/env python3
"""
Test script to verify the real market data integration is working properly.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_market_data_service():
    """Test the market data service functionality."""
    print("Testing Market Data Service...")
    
    try:
        from services.market_data_service import MarketDataService
        
        # Initialize service
        market_service = MarketDataService()
        print("✅ Market data service initialized successfully")
        
        # Test getting investment options
        conservative_options = market_service.get_investment_options('conservative')
        print(f"✅ Conservative investment options: {len(conservative_options)} assets")
        
        moderate_options = market_service.get_investment_options('moderate')
        print(f"✅ Moderate investment options: {len(moderate_options)} assets")
        
        aggressive_options = market_service.get_investment_options('aggressive')
        print(f"✅ Aggressive investment options: {len(aggressive_options)} assets")
        
        # Test getting asset info
        if conservative_options:
            symbol = conservative_options[0]['symbol']
            asset_info = market_service.get_asset_info(symbol)
            print(f"✅ Asset info for {symbol}: {asset_info['name']}")
        
        # Test portfolio metrics calculation
        test_allocation = {'VTI': 0.6, 'BND': 0.4}
        metrics = market_service.calculate_portfolio_metrics(test_allocation)
        print(f"✅ Portfolio metrics calculated - Annual Return: {metrics['annual_return']:.2%}")
        
        return True
        
    except Exception as e:
        print(f"❌ Market data service test failed: {e}")
        return False

def test_investment_engine():
    """Test the investment engine functionality."""
    print("\nTesting Investment Engine...")
    
    try:
        from services.investment_engine import InvestmentEngine
        from services.market_data_service import MarketDataService
        
        # Initialize engine
        market_service = MarketDataService()
        engine = InvestmentEngine(market_service)
        print("✅ Investment engine initialized successfully")
        
        # Test portfolio recommendation generation
        portfolio = engine.generate_portfolio_recommendation(
            monthly_investment=100,
            risk_tolerance='Balanced (Medium Risk)',
            time_horizon='5-10 years',
            investment_goal='Long-term wealth building'
        )
        
        print(f"✅ Portfolio recommendation generated:")
        print(f"   - Monthly Amount: ${portfolio['monthlyAmount']}")
        print(f"   - Expected Return: {portfolio['totalExpectedReturn']:.1f}%")
        print(f"   - Projected Value: ${portfolio['projectedValue']:,.0f}")
        print(f"   - Number of investments: {len(portfolio['investments'])}")
        
        # Test Monte Carlo simulation
        if 'allocation' in portfolio:
            simulation = engine.run_monte_carlo_with_contributions(
                allocation=portfolio['allocation'],
                monthly_contribution=100,
                years=5,
                simulations=100  # Reduced for faster testing
            )
            print(f"✅ Monte Carlo simulation completed:")
            print(f"   - Mean final value: ${simulation['mean_value']:,.0f}")
            print(f"   - Probability of profit: {simulation['probability_of_profit']:.1f}%")
        
        return True
        
    except Exception as e:
        print(f"❌ Investment engine test failed: {e}")
        return False

def test_app_integration():
    """Test the Streamlit app integration."""
    print("\nTesting App Integration...")
    
    try:
        # Test importing the app modules
        sys.path.append('frontend')
        
        # Test the portfolio generation function
        import importlib.util
        spec = importlib.util.spec_from_file_location("app", "frontend/app.py")
        app_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(app_module)
        
        print("✅ App module imported successfully")
        
        # Test portfolio generation
        portfolio = app_module.generate_react_style_portfolio(
            monthly_budget=50,
            risk_tolerance='Conservative (Low Risk)',
            time_horizon='3-5 years',
            investment_goal='Emergency fund'
        )
        
        print(f"✅ Portfolio generation test:")
        print(f"   - Monthly Amount: ${portfolio['monthlyAmount']}")
        print(f"   - Expected Return: {portfolio['totalExpectedReturn']:.1f}%")
        print(f"   - Time Horizon: {portfolio['timeHorizon']} years")
        
        return True
        
    except Exception as e:
        print(f"❌ App integration test failed: {e}")
        return False

def main():
    """Run all integration tests."""
    print("🚀 Starting MicroInvest Integration Tests\n")
    
    tests = [
        test_market_data_service,
        test_investment_engine,
        test_app_integration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All integration tests passed! The real market data integration is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the error messages above.")
    
    return passed == total

if __name__ == "__main__":
    main()
