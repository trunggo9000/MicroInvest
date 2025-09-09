import pytest
from backend.ai.advisor import InvestmentAdvisor

class TestInvestmentAdvisor:
    """Test suite for the InvestmentAdvisor class."""
    
    @pytest.fixture
    def advisor(self):
        """Create an InvestmentAdvisor instance for testing."""
        return InvestmentAdvisor()
    
    def test_initialization(self, advisor):
        """Test that advisor initializes correctly."""
        assert hasattr(advisor, 'portfolio_templates')
        assert hasattr(advisor, 'educational_content')
        assert hasattr(advisor, 'risk_explanations')
        assert isinstance(advisor.portfolio_templates, dict)
        assert isinstance(advisor.educational_content, dict)
        assert isinstance(advisor.risk_explanations, dict)
    
    def test_explain_portfolio_aggressive(self, advisor):
        """Test portfolio explanation for aggressive allocation."""
        allocation = {'Stocks': 80, 'Bonds': 20}
        risk_tolerance = 'high'
        investment_goal = 'retirement'
        time_horizon = '20+ years'
        
        result = advisor.explain_portfolio(allocation, risk_tolerance, investment_goal, time_horizon)
        
        # Check the result
        assert isinstance(result, str)
        assert 'aggressive growth' in result
        assert '80% Stocks' in result
        assert '20% Bonds' in result
        assert 'retirement' in result
    
    def test_explain_portfolio_conservative(self, advisor):
        """Test portfolio explanation for conservative allocation."""
        allocation = {'Stocks': 30, 'Bonds': 70}
        risk_tolerance = 'low'
        investment_goal = 'emergency fund'
        time_horizon = '3-5 years'
        
        result = advisor.explain_portfolio(allocation, risk_tolerance, investment_goal, time_horizon)
        
        assert isinstance(result, str)
        assert 'conservative' in result
        assert '30% Stocks' in result
        assert '70% Bonds' in result
    
    def test_answer_contribution_question(self, advisor):
        """Test answering contribution-related questions."""
        question = "Should I increase my monthly contribution?"
        portfolio_context = {'allocation': {'Stocks': 60, 'Bonds': 40}}
        financial_context = {'monthly_contribution': 100}
        
        result = advisor.answer_question(question, portfolio_context, financial_context)
        
        assert isinstance(result, str)
        assert 'contribution' in result.lower()
        assert 'compound' in result.lower() or 'growth' in result.lower()
    
    def test_answer_risk_question(self, advisor):
        """Test answering risk-related questions."""
        question = "How can I reduce risk in my portfolio?"
        portfolio_context = {'allocation': {'Stocks': 80, 'Bonds': 20}}
        
        result = advisor.answer_question(question, portfolio_context)
        
        assert isinstance(result, str)
        assert 'risk' in result.lower()
        assert 'bond' in result.lower() or 'diversif' in result.lower()
    
    def test_answer_rebalancing_question(self, advisor):
        """Test answering rebalancing questions."""
        question = "When should I rebalance my portfolio?"
        portfolio_context = {'allocation': {'Stocks': 60, 'Bonds': 40}}
        
        result = advisor.answer_question(question, portfolio_context)
        
        assert isinstance(result, str)
        assert 'rebalanc' in result.lower()
        assert 'quarterly' in result.lower() or 'target' in result.lower()
    
    def test_simulate_what_if_contribution_increase(self, advisor):
        """Test what-if simulation for contribution increase."""
        scenario = "Increase monthly contribution by $50"
        current_portfolio = {'Stocks': 60, 'Bonds': 40}
        proposed_changes = {'monthly_contribution': 150}
        financial_context = {'monthly_contribution': 100}
        
        result = advisor.simulate_what_if(scenario, current_portfolio, proposed_changes, financial_context)
        
        assert isinstance(result, dict)
        assert 'impact' in result
        assert 'risks' in result
        assert 'recommendation' in result
        assert 'Positive' in result['impact']
    
    def test_simulate_what_if_risk_increase(self, advisor):
        """Test what-if simulation for risk increase."""
        scenario = "Switch to higher risk aggressive portfolio"
        current_portfolio = {'Stocks': 40, 'Bonds': 60}
        proposed_changes = {'risk_level': 'aggressive'}
        financial_context = {}
        
        result = advisor.simulate_what_if(scenario, current_portfolio, proposed_changes, financial_context)
        
        assert isinstance(result, dict)
        assert 'impact' in result
        assert 'risks' in result
        assert 'recommendation' in result
        assert 'volatility' in result['impact'].lower() or 'return' in result['impact'].lower()
    
    def test_load_templates(self, advisor):
        """Test that templates are loaded correctly."""
        templates = advisor._load_portfolio_templates()
        assert 'aggressive' in templates
        assert 'moderate' in templates
        assert 'conservative' in templates
        
        educational = advisor._load_educational_content()
        assert 'diversification' in educational
        assert 'compound_interest' in educational
        
        risk_explanations = advisor._load_risk_explanations()
        assert 'low' in risk_explanations
        assert 'medium' in risk_explanations
        assert 'high' in risk_explanations
    
    def test_answer_diversification_question(self, advisor):
        """Test answering diversification questions."""
        question = "How can I diversify my portfolio better?"
        portfolio_context = {'allocation': {'Stocks': 100}}
        
        result = advisor.answer_question(question, portfolio_context)
        
        assert isinstance(result, str)
        assert 'diversif' in result.lower()
        assert 'asset' in result.lower() or 'class' in result.lower()
    
    def test_answer_general_question(self, advisor):
        """Test answering general questions."""
        question = "What should I do with my investments?"
        portfolio_context = {'allocation': {'Stocks': 60, 'Bonds': 40}}
        
        result = advisor.answer_question(question, portfolio_context)
        
        assert isinstance(result, str)
        assert len(result) > 50  # Should provide substantial advice
        assert 'contribution' in result.lower() or 'diversif' in result.lower()
