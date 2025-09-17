"""
Machine Learning Investment Advisor
Uses ML algorithms to predict optimal investment strategies and market trends
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingClassifier
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score
import xgboost as xgb
import joblib
import os
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class MLInvestmentAdvisor:
    """ML-powered investment advisor for personalized recommendations."""
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.encoders = {}
        self.model_dir = os.path.join(os.path.dirname(__file__), 'models')
        os.makedirs(self.model_dir, exist_ok=True)
        
        # Initialize models
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize ML models for different prediction tasks."""
        self.models = {
            'risk_predictor': RandomForestRegressor(n_estimators=100, random_state=42),
            'return_predictor': GradientBoostingClassifier(n_estimators=100, random_state=42),
            'allocation_optimizer': xgb.XGBRegressor(n_estimators=100, random_state=42),
            'spending_predictor': LinearRegression(),
            'market_trend': RandomForestRegressor(n_estimators=150, random_state=42)
        }
        
        self.scalers = {
            'features': StandardScaler(),
            'financial': StandardScaler()
        }
        
        self.encoders = {
            'categorical': LabelEncoder()
        }
    
    def predict_optimal_allocation(self, user_profile: Dict, transaction_data: pd.DataFrame) -> Dict:
        """Predict optimal portfolio allocation using ML."""
        try:
            # Extract features from user profile and transaction data
            features = self._extract_user_features(user_profile, transaction_data)
            
            # Use pre-trained model or create prediction based on features
            if self._model_exists('allocation_optimizer'):
                allocation = self._predict_with_model('allocation_optimizer', features)
            else:
                allocation = self._rule_based_allocation(user_profile, features)
            
            return {
                'stocks': max(0.1, min(0.8, allocation.get('stocks', 0.6))),
                'bonds': max(0.1, min(0.5, allocation.get('bonds', 0.3))),
                'alternatives': max(0.0, min(0.2, allocation.get('alternatives', 0.1))),
                'confidence_score': features.get('confidence', 0.7),
                'reasoning': self._generate_allocation_reasoning(allocation, user_profile)
            }
        except Exception as e:
            logger.error(f"Error in allocation prediction: {e}")
            return self._fallback_allocation(user_profile)
    
    def predict_investment_returns(self, portfolio: Dict, market_conditions: Dict) -> Dict:
        """Predict expected returns using ML models."""
        try:
            # Create feature vector
            features = np.array([
                portfolio.get('stocks', 0.6),
                portfolio.get('bonds', 0.3),
                portfolio.get('alternatives', 0.1),
                market_conditions.get('volatility', 0.15),
                market_conditions.get('interest_rate', 0.05),
                market_conditions.get('inflation', 0.03)
            ]).reshape(1, -1)
            
            # Scale features
            if hasattr(self.scalers['features'], 'mean_'):
                features_scaled = self.scalers['features'].transform(features)
            else:
                features_scaled = features
            
            # Predict returns
            if self._model_exists('return_predictor'):
                predicted_class = self.models['return_predictor'].predict(features_scaled)[0]
                return_ranges = {0: (0.04, 0.06), 1: (0.06, 0.08), 2: (0.08, 0.12), 3: (0.12, 0.16)}
                expected_return = np.mean(return_ranges.get(predicted_class, (0.08, 0.10)))
            else:
                # Rule-based prediction
                expected_return = (
                    portfolio.get('stocks', 0.6) * 0.10 +
                    portfolio.get('bonds', 0.3) * 0.04 +
                    portfolio.get('alternatives', 0.1) * 0.08
                )
            
            # Calculate risk metrics
            volatility = self._calculate_portfolio_volatility(portfolio, market_conditions)
            sharpe_ratio = (expected_return - 0.02) / volatility if volatility > 0 else 0
            
            return {
                'expected_annual_return': expected_return,
                'volatility': volatility,
                'sharpe_ratio': sharpe_ratio,
                'confidence_interval': (expected_return - 0.02, expected_return + 0.02),
                'risk_level': self._categorize_risk(volatility)
            }
        except Exception as e:
            logger.error(f"Error predicting returns: {e}")
            return self._fallback_return_prediction()
    
    def predict_spending_patterns(self, transaction_data: pd.DataFrame) -> Dict:
        """Predict future spending patterns using ML."""
        try:
            if transaction_data.empty:
                return self._generate_mock_spending_prediction()
            
            # Prepare time series data
            daily_spending = self._prepare_spending_timeseries(transaction_data)
            
            # Extract features for prediction
            features = self._extract_spending_features(daily_spending)
            
            # Predict next month's spending
            if len(features) > 10:  # Need sufficient data
                X = features[:-1]
                y = features[1:]
                
                # Train simple model
                self.models['spending_predictor'].fit(X.reshape(-1, 1), y)
                
                # Predict next values
                last_value = features[-1]
                predictions = []
                for _ in range(30):  # Predict 30 days
                    pred = self.models['spending_predictor'].predict([[last_value]])[0]
                    predictions.append(max(0, pred))
                    last_value = pred
                
                predicted_monthly = sum(predictions)
            else:
                # Fallback to average
                predicted_monthly = transaction_data[transaction_data['amount'] > 0]['amount'].sum()
            
            # Calculate spending insights
            category_predictions = self._predict_category_spending(transaction_data)
            
            return {
                'predicted_monthly_spending': predicted_monthly,
                'category_breakdown': category_predictions,
                'spending_trend': 'increasing' if predicted_monthly > transaction_data['amount'].mean() * 30 else 'stable',
                'confidence': min(100, len(transaction_data) * 2),
                'recommendations': self._generate_spending_recommendations(predicted_monthly, category_predictions)
            }
        except Exception as e:
            logger.error(f"Error predicting spending: {e}")
            return self._generate_mock_spending_prediction()
    
    def predict_market_trends(self, historical_data: pd.DataFrame) -> Dict:
        """Predict market trends using ML algorithms."""
        try:
            # Generate synthetic market data if none provided
            if historical_data.empty:
                historical_data = self._generate_synthetic_market_data()
            
            # Extract technical indicators
            features = self._extract_market_features(historical_data)
            
            # Predict trend direction
            if len(features) > 50:
                X = features[:-10]
                y = np.where(features[10:] > features[:-10], 1, 0)  # 1 for up, 0 for down
                
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                
                # Train trend prediction model
                self.models['market_trend'].fit(X_train.reshape(-1, 1), y_train)
                
                # Make predictions
                trend_prob = self.models['market_trend'].predict_proba(features[-10:].reshape(-1, 1))
                bullish_prob = np.mean(trend_prob[:, 1]) if trend_prob.shape[1] > 1 else 0.5
            else:
                bullish_prob = 0.55  # Slightly bullish default
            
            # Generate market outlook
            outlook = self._generate_market_outlook(bullish_prob, features)
            
            return {
                'bullish_probability': bullish_prob,
                'trend_direction': 'bullish' if bullish_prob > 0.6 else 'bearish' if bullish_prob < 0.4 else 'neutral',
                'confidence': min(95, len(historical_data) * 0.5),
                'outlook': outlook,
                'recommended_actions': self._generate_market_recommendations(bullish_prob)
            }
        except Exception as e:
            logger.error(f"Error predicting market trends: {e}")
            return self._fallback_market_prediction()
    
    def _extract_user_features(self, user_profile: Dict, transaction_data: pd.DataFrame) -> Dict:
        """Extract features from user profile and transaction data."""
        features = {
            'age': user_profile.get('age', 25),
            'income': user_profile.get('monthly_income', 1000),
            'investment_amount': user_profile.get('monthly_investment', 100),
            'risk_tolerance': self._encode_risk_tolerance(user_profile.get('risk_tolerance', 'Balanced')),
            'time_horizon': user_profile.get('time_horizon_years', 5),
            'experience': self._encode_experience(user_profile.get('investment_experience', 'Beginner'))
        }
        
        if not transaction_data.empty:
            spending_features = self._analyze_spending_behavior(transaction_data)
            features.update(spending_features)
        
        features['confidence'] = min(1.0, len(transaction_data) / 100) if not transaction_data.empty else 0.5
        
        return features
    
    def _analyze_spending_behavior(self, transaction_data: pd.DataFrame) -> Dict:
        """Analyze spending behavior from transaction data."""
        spending_df = transaction_data[transaction_data['amount'] > 0]
        
        return {
            'avg_transaction': spending_df['amount'].mean() if not spending_df.empty else 0,
            'spending_volatility': spending_df['amount'].std() if not spending_df.empty else 0,
            'transaction_frequency': len(spending_df) / 30,  # per day
            'discretionary_ratio': self._calculate_discretionary_ratio(spending_df)
        }
    
    def _calculate_discretionary_ratio(self, spending_df: pd.DataFrame) -> float:
        """Calculate ratio of discretionary to essential spending."""
        if spending_df.empty:
            return 0.3
        
        essential_categories = ['Food and Drink', 'Transportation', 'Payment', 'Healthcare']
        essential_spending = spending_df[spending_df['category'].isin(essential_categories)]['amount'].sum()
        total_spending = spending_df['amount'].sum()
        
        return 1 - (essential_spending / total_spending) if total_spending > 0 else 0.3
    
    def _rule_based_allocation(self, user_profile: Dict, features: Dict) -> Dict:
        """Rule-based allocation when ML model is not available."""
        age = features.get('age', 25)
        risk_tolerance = user_profile.get('risk_tolerance', 'Balanced')
        time_horizon = features.get('time_horizon', 5)
        
        # Age-based allocation (100 - age rule, modified for students)
        base_stock_allocation = min(0.8, max(0.4, (120 - age) / 100))
        
        # Adjust for risk tolerance
        if 'Conservative' in risk_tolerance:
            stock_allocation = base_stock_allocation * 0.7
        elif 'Growth' in risk_tolerance:
            stock_allocation = min(0.8, base_stock_allocation * 1.2)
        else:
            stock_allocation = base_stock_allocation
        
        # Adjust for time horizon
        if time_horizon < 2:
            stock_allocation *= 0.6
        elif time_horizon > 10:
            stock_allocation = min(0.8, stock_allocation * 1.1)
        
        bond_allocation = min(0.5, 1 - stock_allocation - 0.1)
        alternatives_allocation = max(0, 1 - stock_allocation - bond_allocation)
        
        return {
            'stocks': stock_allocation,
            'bonds': bond_allocation,
            'alternatives': alternatives_allocation
        }
    
    def _generate_allocation_reasoning(self, allocation: Dict, user_profile: Dict) -> str:
        """Generate human-readable reasoning for allocation."""
        stock_pct = allocation.get('stocks', 0.6) * 100
        bond_pct = allocation.get('bonds', 0.3) * 100
        
        reasoning = f"Based on your profile, we recommend {stock_pct:.0f}% stocks and {bond_pct:.0f}% bonds. "
        
        if stock_pct > 70:
            reasoning += "This growth-focused allocation maximizes long-term potential."
        elif stock_pct < 40:
            reasoning += "This conservative allocation prioritizes capital preservation."
        else:
            reasoning += "This balanced allocation provides growth with stability."
        
        return reasoning
    
    def _calculate_portfolio_volatility(self, portfolio: Dict, market_conditions: Dict) -> float:
        """Calculate expected portfolio volatility."""
        stock_vol = 0.16
        bond_vol = 0.04
        alt_vol = 0.12
        
        # Adjust for market conditions
        market_vol = market_conditions.get('volatility', 0.15)
        vol_multiplier = market_vol / 0.15
        
        portfolio_vol = (
            portfolio.get('stocks', 0.6) * stock_vol * vol_multiplier +
            portfolio.get('bonds', 0.3) * bond_vol +
            portfolio.get('alternatives', 0.1) * alt_vol
        )
        
        return portfolio_vol
    
    def _categorize_risk(self, volatility: float) -> str:
        """Categorize risk level based on volatility."""
        if volatility < 0.08:
            return 'Low'
        elif volatility < 0.15:
            return 'Medium'
        else:
            return 'High'
    
    def _prepare_spending_timeseries(self, transaction_data: pd.DataFrame) -> pd.Series:
        """Prepare daily spending time series."""
        transaction_data['date'] = pd.to_datetime(transaction_data['date'])
        spending_df = transaction_data[transaction_data['amount'] > 0]
        
        daily_spending = spending_df.groupby('date')['amount'].sum()
        
        # Fill missing dates with 0
        date_range = pd.date_range(start=daily_spending.index.min(), 
                                 end=daily_spending.index.max(), freq='D')
        daily_spending = daily_spending.reindex(date_range, fill_value=0)
        
        return daily_spending
    
    def _extract_spending_features(self, daily_spending: pd.Series) -> np.ndarray:
        """Extract features from spending time series."""
        # Simple moving average as features
        return daily_spending.rolling(window=7, min_periods=1).mean().values
    
    def _predict_category_spending(self, transaction_data: pd.DataFrame) -> Dict:
        """Predict spending by category."""
        spending_df = transaction_data[transaction_data['amount'] > 0]
        category_spending = spending_df.groupby('category')['amount'].sum()
        
        # Simple prediction: assume similar pattern continues
        total_days = (transaction_data['date'].max() - transaction_data['date'].min()).days
        daily_multiplier = 30 / max(1, total_days)
        
        predictions = {}
        for category, amount in category_spending.items():
            predictions[category] = amount * daily_multiplier
        
        return predictions
    
    def _generate_spending_recommendations(self, predicted_spending: float, category_breakdown: Dict) -> List[str]:
        """Generate spending recommendations."""
        recommendations = []
        
        # Find highest spending categories
        sorted_categories = sorted(category_breakdown.items(), key=lambda x: x[1], reverse=True)
        
        if sorted_categories:
            top_category, top_amount = sorted_categories[0]
            if top_amount > predicted_spending * 0.3:
                recommendations.append(f"Consider reducing {top_category} spending - it's {top_amount/predicted_spending*100:.0f}% of your budget")
        
        if predicted_spending > 2000:
            recommendations.append("Your spending is quite high. Look for opportunities to save and invest more.")
        
        recommendations.append("Track your spending regularly to identify patterns and opportunities for savings.")
        
        return recommendations
    
    def _generate_synthetic_market_data(self) -> pd.DataFrame:
        """Generate synthetic market data for testing."""
        dates = pd.date_range(start='2020-01-01', end='2024-12-31', freq='D')
        np.random.seed(42)
        
        # Generate realistic market data with trends
        returns = np.random.normal(0.0008, 0.02, len(dates))  # Daily returns
        prices = [100]
        
        for ret in returns:
            prices.append(prices[-1] * (1 + ret))
        
        return pd.DataFrame({
            'date': dates,
            'price': prices[:-1],
            'volume': np.random.lognormal(15, 1, len(dates))
        })
    
    def _extract_market_features(self, market_data: pd.DataFrame) -> np.ndarray:
        """Extract technical indicators from market data."""
        prices = market_data['price'].values
        
        # Simple moving averages
        sma_20 = pd.Series(prices).rolling(20).mean().fillna(method='bfill').values
        sma_50 = pd.Series(prices).rolling(50).mean().fillna(method='bfill').values
        
        # Price momentum
        momentum = prices / np.roll(prices, 10) - 1
        momentum[np.isnan(momentum)] = 0
        
        # Combine features
        features = sma_20 / sma_50  # Trend indicator
        
        return features
    
    def _generate_market_outlook(self, bullish_prob: float, features: np.ndarray) -> str:
        """Generate market outlook description."""
        if bullish_prob > 0.7:
            return "Strong bullish signals suggest favorable market conditions for growth investments."
        elif bullish_prob > 0.6:
            return "Moderately bullish outlook with good opportunities for balanced portfolios."
        elif bullish_prob < 0.3:
            return "Bearish signals suggest focusing on defensive investments and capital preservation."
        elif bullish_prob < 0.4:
            return "Cautious outlook recommends reducing risk exposure and maintaining liquidity."
        else:
            return "Neutral market conditions suggest maintaining current allocation strategy."
    
    def _generate_market_recommendations(self, bullish_prob: float) -> List[str]:
        """Generate actionable market recommendations."""
        recommendations = []
        
        if bullish_prob > 0.65:
            recommendations.extend([
                "Consider increasing equity allocation within your risk tolerance",
                "Look for growth-oriented investments",
                "Dollar-cost averaging into index funds could be beneficial"
            ])
        elif bullish_prob < 0.35:
            recommendations.extend([
                "Consider increasing bond allocation for stability",
                "Maintain higher cash reserves",
                "Focus on dividend-paying stocks for income"
            ])
        else:
            recommendations.extend([
                "Maintain current balanced allocation",
                "Continue regular investment schedule",
                "Monitor market conditions for changes"
            ])
        
        return recommendations
    
    def _encode_risk_tolerance(self, risk_tolerance: str) -> float:
        """Encode risk tolerance as numerical value."""
        mapping = {
            'Conservative': 0.2,
            'Balanced': 0.5,
            'Growth': 0.8,
            'Aggressive': 1.0
        }
        
        for key in mapping:
            if key in risk_tolerance:
                return mapping[key]
        
        return 0.5  # Default to balanced
    
    def _encode_experience(self, experience: str) -> float:
        """Encode investment experience as numerical value."""
        mapping = {
            'Beginner': 0.2,
            'Some': 0.5,
            'Experienced': 0.8,
            'Expert': 1.0
        }
        
        for key in mapping:
            if key in experience:
                return mapping[key]
        
        return 0.2  # Default to beginner
    
    def _model_exists(self, model_name: str) -> bool:
        """Check if trained model exists."""
        model_path = os.path.join(self.model_dir, f'{model_name}.joblib')
        return os.path.exists(model_path)
    
    def _predict_with_model(self, model_name: str, features: Dict) -> Dict:
        """Make prediction using trained model."""
        try:
            model_path = os.path.join(self.model_dir, f'{model_name}.joblib')
            model = joblib.load(model_path)
            
            # Convert features to array (simplified)
            feature_array = np.array(list(features.values())).reshape(1, -1)
            prediction = model.predict(feature_array)[0]
            
            return {'stocks': prediction, 'bonds': 1-prediction-0.1, 'alternatives': 0.1}
        except Exception as e:
            logger.error(f"Error loading model {model_name}: {e}")
            return {}
    
    def _fallback_allocation(self, user_profile: Dict) -> Dict:
        """Fallback allocation when ML fails."""
        return {
            'stocks': 0.6,
            'bonds': 0.3,
            'alternatives': 0.1,
            'confidence_score': 0.5,
            'reasoning': "Using balanced default allocation due to insufficient data."
        }
    
    def _fallback_return_prediction(self) -> Dict:
        """Fallback return prediction."""
        return {
            'expected_annual_return': 0.08,
            'volatility': 0.12,
            'sharpe_ratio': 0.5,
            'confidence_interval': (0.06, 0.10),
            'risk_level': 'Medium'
        }
    
    def _generate_mock_spending_prediction(self) -> Dict:
        """Generate mock spending prediction."""
        return {
            'predicted_monthly_spending': 800,
            'category_breakdown': {
                'Food and Drink': 300,
                'Transportation': 150,
                'Entertainment': 200,
                'Shops': 150
            },
            'spending_trend': 'stable',
            'confidence': 60,
            'recommendations': [
                "Track your spending to get personalized insights",
                "Connect your bank account for better predictions"
            ]
        }
    
    def _fallback_market_prediction(self) -> Dict:
        """Fallback market prediction."""
        return {
            'bullish_probability': 0.55,
            'trend_direction': 'neutral',
            'confidence': 50,
            'outlook': "Market conditions appear neutral with slight positive bias.",
            'recommended_actions': [
                "Maintain balanced portfolio allocation",
                "Continue regular investment schedule"
            ]
        }
