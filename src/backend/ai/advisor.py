from typing import Dict, Any, Optional
import json
import random

class InvestmentAdvisor:
    """
    Rule-based investment advisor that provides personalized recommendations
    and explanations using predefined templates and logic.
    """
    
    def __init__(self):
        """Initialize the investment advisor with rule-based templates."""
        self.portfolio_templates = self._load_portfolio_templates()
        self.educational_content = self._load_educational_content()
        self.risk_explanations = self._load_risk_explanations()
    
    def explain_portfolio(
        self, 
        allocation: Dict[str, float],
        risk_tolerance: str,
        investment_goal: str,
        time_horizon: str,
        context: Dict[str, Any] = None
    ) -> str:
        """
        Generate a human-readable explanation of the recommended portfolio.
        
        Args:
            allocation: Dictionary of asset allocations (e.g., {'Stocks': 60, 'Bonds': 40})
            risk_tolerance: User's risk tolerance level (e.g., 'low', 'medium', 'high')
            investment_goal: User's investment goal (e.g., 'retirement', 'buying a house')
            time_horizon: Investment time horizon (e.g., '5 years', '10+ years')
            context: Additional context about the user's financial situation
            
        Returns:
            String containing the generated explanation
        """
        # Determine portfolio type based on allocation
        stocks_pct = allocation.get('Stocks', 0)
        bonds_pct = allocation.get('Bonds', 0)
        
        if stocks_pct >= 80:
            portfolio_type = "aggressive growth"
        elif stocks_pct >= 60:
            portfolio_type = "moderate growth"
        elif stocks_pct >= 40:
            portfolio_type = "balanced"
        else:
            portfolio_type = "conservative"
        
        # Build explanation based on portfolio characteristics
        explanation = f"Your {portfolio_type} portfolio is designed for {investment_goal.lower()} with a {time_horizon} investment horizon.\n\n"
        
        # Add allocation explanation
        if stocks_pct > 0:
            explanation += f"• **{stocks_pct}% Stocks**: Provides growth potential for long-term wealth building. "
            if stocks_pct >= 70:
                explanation += "This high allocation aims for maximum growth but comes with higher volatility.\n"
            elif stocks_pct >= 50:
                explanation += "This moderate allocation balances growth with stability.\n"
            else:
                explanation += "This conservative allocation prioritizes stability over growth.\n"
        
        if bonds_pct > 0:
            explanation += f"• **{bonds_pct}% Bonds**: Provides stability and regular income. "
            if bonds_pct >= 50:
                explanation += "This high allocation reduces portfolio volatility and provides steady returns.\n"
            else:
                explanation += "This allocation helps cushion against stock market volatility.\n"
        
        # Add risk tolerance explanation
        risk_explanation = self.risk_explanations.get(risk_tolerance.lower(), "")
        if risk_explanation:
            explanation += f"\n{risk_explanation}"
        
        return explanation
    
    def answer_question(
        self, 
        question: str,
        portfolio_context: Dict[str, Any],
        financial_context: Dict[str, Any] = None
    ) -> str:
        """
        Answer a user's investment-related question with personalized advice.
        
        Args:
            question: The user's question
            portfolio_context: Information about the user's current portfolio
            financial_context: Additional financial context about the user
            
        Returns:
            String containing the generated answer
        """
        question_lower = question.lower()
        
        # Common question patterns and responses
        if "increase" in question_lower and ("contribution" in question_lower or "invest" in question_lower):
            return self._answer_contribution_question(portfolio_context, financial_context)
        elif "risk" in question_lower and ("reduce" in question_lower or "lower" in question_lower):
            return self._answer_risk_reduction_question(portfolio_context)
        elif "rebalance" in question_lower:
            return self._answer_rebalancing_question(portfolio_context)
        elif "diversif" in question_lower:
            return self._answer_diversification_question(portfolio_context)
        else:
            return self._answer_general_question(question, portfolio_context)
    
    def simulate_what_if(
        self,
        scenario: str,
        current_portfolio: Dict[str, float],
        proposed_changes: Dict[str, Any],
        financial_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze a 'what-if' investment scenario and provide insights.
        
        Args:
            scenario: Description of the scenario to analyze
            current_portfolio: Current asset allocation
            proposed_changes: Proposed changes to the portfolio
            financial_context: User's financial context
            
        Returns:
            Dictionary containing analysis and recommendations
        """
        analysis = {
            "impact": "Neutral",
            "risks": "Moderate",
            "recommendation": "Consider your risk tolerance"
        }
        
        # Analyze contribution changes
        if "contribution" in scenario.lower():
            current_contrib = financial_context.get('monthly_contribution', 100)
            new_contrib = proposed_changes.get('monthly_contribution', current_contrib)
            
            if new_contrib > current_contrib:
                analysis["impact"] = "Positive - Higher contributions will accelerate your goal achievement"
                analysis["risks"] = "Low - Ensure you can maintain the higher contribution consistently"
                analysis["recommendation"] = "Increase gradually and maintain an emergency fund"
            else:
                analysis["impact"] = "Negative - Lower contributions will delay goal achievement"
                analysis["risks"] = "Moderate - May not reach financial goals on time"
                analysis["recommendation"] = "Consider reducing expenses elsewhere to maintain contributions"
        
        # Analyze risk level changes
        elif "risk" in scenario.lower():
            if "higher" in scenario.lower() or "aggressive" in scenario.lower():
                analysis["impact"] = "Higher potential returns but increased volatility"
                analysis["risks"] = "High - Greater chance of short-term losses"
                analysis["recommendation"] = "Only suitable if you have a long time horizon and can handle volatility"
            else:
                analysis["impact"] = "Lower volatility but reduced growth potential"
                analysis["risks"] = "Low - More stable but may not beat inflation long-term"
                analysis["recommendation"] = "Suitable for short-term goals or risk-averse investors"
        
        return analysis
    
    def _load_portfolio_templates(self) -> Dict[str, str]:
        """Load portfolio explanation templates."""
        return {
            "aggressive": "This aggressive portfolio prioritizes growth over stability, suitable for long-term investors who can tolerate significant volatility.",
            "moderate": "This balanced portfolio provides a mix of growth and stability, appropriate for investors with moderate risk tolerance.",
            "conservative": "This conservative portfolio emphasizes capital preservation and steady income, ideal for risk-averse investors or those nearing their goals."
        }
    
    def _load_educational_content(self) -> Dict[str, str]:
        """Load educational content snippets."""
        return {
            "diversification": "Diversification helps reduce risk by spreading investments across different asset classes that may perform differently in various market conditions.",
            "compound_interest": "Compound interest is the eighth wonder of the world. Starting early gives your money more time to grow exponentially.",
            "dollar_cost_averaging": "Investing the same amount regularly (dollar-cost averaging) helps reduce the impact of market volatility on your investments.",
            "emergency_fund": "Always maintain 3-6 months of expenses in an emergency fund before investing significant amounts in the market."
        }
    
    def _load_risk_explanations(self) -> Dict[str, str]:
        """Load risk tolerance explanations."""
        return {
            "low": "Your conservative approach prioritizes capital preservation. This strategy is suitable for short-term goals or if you're uncomfortable with market volatility.",
            "medium": "Your moderate risk tolerance allows for balanced growth while maintaining reasonable stability. This approach is suitable for most long-term investors.",
            "high": "Your aggressive approach maximizes growth potential. This strategy is suitable for long-term goals where you can ride out market fluctuations."
        }
    
    def _answer_contribution_question(self, portfolio_context: Dict[str, Any], financial_context: Dict[str, Any]) -> str:
        """Answer questions about increasing contributions."""
        return ("Increasing your monthly contributions is one of the most effective ways to reach your financial goals faster. "
                "Even small increases can have a significant impact due to compound growth. "
                "Consider increasing by 10-20% initially, and review your budget to ensure sustainability. "
                "Remember to maintain your emergency fund while increasing investments.")
    
    def _answer_risk_reduction_question(self, portfolio_context: Dict[str, Any]) -> str:
        """Answer questions about reducing risk."""
        current_stocks = portfolio_context.get('allocation', {}).get('Stocks', 0)
        if current_stocks > 60:
            return ("To reduce risk, consider increasing your bond allocation to 40-50% of your portfolio. "
                    "This will provide more stability but may reduce long-term growth potential. "
                    "Also consider diversifying across different asset classes and geographic regions.")
        else:
            return ("Your current allocation is already relatively conservative. "
                    "To further reduce risk, you could increase cash holdings or consider Treasury bills, "
                    "but be aware this may not keep pace with inflation over time.")
    
    def _answer_rebalancing_question(self, portfolio_context: Dict[str, Any]) -> str:
        """Answer questions about rebalancing."""
        return ("Rebalancing helps maintain your target asset allocation as market movements change your portfolio mix. "
                "Consider rebalancing quarterly or when any asset class deviates more than 5% from your target. "
                "This disciplined approach helps you 'buy low and sell high' automatically.")
    
    def _answer_diversification_question(self, portfolio_context: Dict[str, Any]) -> str:
        """Answer questions about diversification."""
        return ("Diversification is key to managing investment risk. Consider spreading investments across: "
                "different asset classes (stocks, bonds, real estate), geographic regions (domestic and international), "
                "and company sizes (large-cap, mid-cap, small-cap). "
                "Index funds and ETFs are excellent tools for instant diversification.")
    
    def _answer_general_question(self, question: str, portfolio_context: Dict[str, Any]) -> str:
        """Answer general investment questions."""
        return ("Based on your current portfolio and investment profile, I recommend focusing on: "
                "1) Consistent monthly contributions, 2) Maintaining proper diversification, "
                "3) Regular portfolio reviews, and 4) Staying disciplined during market volatility. "
                "For specific questions about your situation, consider consulting with a financial advisor.")
