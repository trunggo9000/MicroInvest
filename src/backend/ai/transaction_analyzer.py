"""
ML-powered Transaction Analysis and Categorization
"""
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import re
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)

class TransactionAnalyzer:
    """ML-powered transaction analyzer for spending insights and predictions."""
    
    def __init__(self):
        self.categorizer = RandomForestClassifier(n_estimators=100, random_state=42)
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.scaler = StandardScaler()
        self.spending_clusters = KMeans(n_clusters=5, random_state=42)
        self.is_trained = False
        
        # Predefined category mappings for better accuracy
        self.category_keywords = {
            'Food and Drink': ['restaurant', 'cafe', 'food', 'grocery', 'starbucks', 'mcdonalds', 'pizza', 'bar'],
            'Transportation': ['uber', 'lyft', 'gas', 'fuel', 'parking', 'metro', 'bus', 'taxi', 'car'],
            'Entertainment': ['movie', 'netflix', 'spotify', 'game', 'concert', 'theater', 'gym', 'fitness'],
            'Shopping': ['amazon', 'target', 'walmart', 'store', 'shop', 'clothing', 'electronics'],
            'Healthcare': ['pharmacy', 'doctor', 'medical', 'hospital', 'dentist', 'health'],
            'Education': ['tuition', 'book', 'school', 'university', 'course', 'textbook'],
            'Bills': ['electric', 'water', 'internet', 'phone', 'rent', 'insurance', 'utility']
        }
    
    def analyze_transactions(self, transactions_df: pd.DataFrame) -> Dict:
        """Comprehensive transaction analysis with ML insights."""
        if transactions_df.empty:
            return self._empty_analysis()
        
        # Enhanced categorization
        categorized_df = self.categorize_transactions(transactions_df)
        
        # Spending pattern analysis
        spending_patterns = self._analyze_spending_patterns(categorized_df)
        
        # Anomaly detection
        anomalies = self._detect_spending_anomalies(categorized_df)
        
        # Seasonal analysis
        seasonal_insights = self._analyze_seasonal_patterns(categorized_df)
        
        # Investment capacity prediction
        investment_capacity = self._predict_investment_capacity(categorized_df)
        
        # Spending optimization suggestions
        optimization_tips = self._generate_optimization_tips(categorized_df, spending_patterns)
        
        return {
            'categorized_transactions': categorized_df,
            'spending_patterns': spending_patterns,
            'anomalies': anomalies,
            'seasonal_insights': seasonal_insights,
            'investment_capacity': investment_capacity,
            'optimization_tips': optimization_tips,
            'summary_stats': self._calculate_summary_stats(categorized_df)
        }
    
    def categorize_transactions(self, transactions_df: pd.DataFrame) -> pd.DataFrame:
        """Enhanced ML-powered transaction categorization."""
        df = transactions_df.copy()
        
        # If no existing categories or we want to improve them
        if 'category' not in df.columns or df['category'].isna().sum() > len(df) * 0.5:
            df['predicted_category'] = df.apply(self._predict_category, axis=1)
            df['category'] = df['predicted_category']
        else:
            df['predicted_category'] = df['category']
        
        # Add subcategory predictions
        df['subcategory'] = df.apply(self._predict_subcategory, axis=1)
        
        # Add spending type (essential vs discretionary)
        df['spending_type'] = df['category'].apply(self._classify_spending_type)
        
        # Add merchant analysis
        df['merchant_type'] = df.apply(self._analyze_merchant, axis=1)
        
        return df
    
    def _predict_category(self, transaction: pd.Series) -> str:
        """Predict transaction category using ML and rules."""
        text = f"{transaction.get('name', '')} {transaction.get('merchant_name', '')}".lower()
        
        # Rule-based categorization using keywords
        for category, keywords in self.category_keywords.items():
            if any(keyword in text for keyword in keywords):
                return category
        
        # Amount-based heuristics
        amount = abs(transaction.get('amount', 0))
        
        if amount > 1000:
            return 'Bills'
        elif amount < 5:
            return 'Food and Drink'
        elif 'transfer' in text or 'deposit' in text:
            return 'Transfer'
        elif any(word in text for word in ['atm', 'withdrawal', 'cash']):
            return 'Cash'
        
        return 'Other'
    
    def _predict_subcategory(self, transaction: pd.Series) -> str:
        """Predict transaction subcategory."""
        category = transaction.get('category', 'Other')
        text = f"{transaction.get('name', '')} {transaction.get('merchant_name', '')}".lower()
        
        subcategory_map = {
            'Food and Drink': {
                'restaurant': ['restaurant', 'cafe', 'bar', 'diner'],
                'grocery': ['grocery', 'supermarket', 'market', 'food store'],
                'fast_food': ['mcdonalds', 'burger', 'pizza', 'subway', 'kfc'],
                'coffee': ['starbucks', 'coffee', 'dunkin']
            },
            'Transportation': {
                'rideshare': ['uber', 'lyft'],
                'fuel': ['gas', 'fuel', 'shell', 'exxon'],
                'parking': ['parking', 'meter'],
                'public_transit': ['metro', 'bus', 'train']
            },
            'Shopping': {
                'online': ['amazon', 'ebay', 'online'],
                'clothing': ['clothing', 'apparel', 'fashion'],
                'electronics': ['electronics', 'tech', 'computer'],
                'general': ['target', 'walmart', 'store']
            }
        }
        
        if category in subcategory_map:
            for subcat, keywords in subcategory_map[category].items():
                if any(keyword in text for keyword in keywords):
                    return subcat
        
        return 'general'
    
    def _classify_spending_type(self, category: str) -> str:
        """Classify spending as essential or discretionary."""
        essential_categories = ['Food and Drink', 'Transportation', 'Bills', 'Healthcare', 'Education']
        return 'essential' if category in essential_categories else 'discretionary'
    
    def _analyze_merchant(self, transaction: pd.Series) -> str:
        """Analyze merchant type and patterns."""
        merchant = transaction.get('merchant_name', '').lower()
        
        if not merchant:
            return 'unknown'
        
        merchant_types = {
            'chain_restaurant': ['mcdonalds', 'starbucks', 'subway', 'chipotle'],
            'big_box_retail': ['walmart', 'target', 'costco', 'amazon'],
            'tech_service': ['netflix', 'spotify', 'apple', 'google'],
            'financial': ['bank', 'credit', 'loan', 'insurance'],
            'local_business': []  # Default for unrecognized merchants
        }
        
        for merchant_type, keywords in merchant_types.items():
            if any(keyword in merchant for keyword in keywords):
                return merchant_type
        
        return 'local_business'
    
    def _analyze_spending_patterns(self, df: pd.DataFrame) -> Dict:
        """Analyze spending patterns using ML."""
        spending_df = df[df['amount'] > 0].copy()
        
        if spending_df.empty:
            return {}
        
        # Convert date to datetime
        spending_df['date'] = pd.to_datetime(spending_df['date'])
        
        # Daily patterns
        spending_df['day_of_week'] = spending_df['date'].dt.day_name()
        spending_df['hour'] = spending_df['date'].dt.hour
        spending_df['is_weekend'] = spending_df['date'].dt.weekday >= 5
        
        patterns = {
            'daily_average': spending_df['amount'].mean(),
            'spending_by_day': spending_df.groupby('day_of_week')['amount'].sum().to_dict(),
            'spending_by_category': spending_df.groupby('category')['amount'].sum().to_dict(),
            'weekend_vs_weekday': {
                'weekend': spending_df[spending_df['is_weekend']]['amount'].sum(),
                'weekday': spending_df[~spending_df['is_weekend']]['amount'].sum()
            },
            'transaction_frequency': len(spending_df) / max(1, (spending_df['date'].max() - spending_df['date'].min()).days),
            'top_merchants': spending_df.groupby('merchant_name')['amount'].sum().nlargest(5).to_dict(),
            'spending_volatility': spending_df['amount'].std()
        }
        
        # Cluster spending behavior
        if len(spending_df) > 10:
            features = spending_df[['amount']].values
            spending_df['spending_cluster'] = self.spending_clusters.fit_predict(features)
            patterns['spending_clusters'] = spending_df.groupby('spending_cluster')['amount'].agg(['mean', 'count']).to_dict()
        
        return patterns
    
    def _detect_spending_anomalies(self, df: pd.DataFrame) -> List[Dict]:
        """Detect unusual spending patterns."""
        spending_df = df[df['amount'] > 0].copy()
        
        if len(spending_df) < 10:
            return []
        
        anomalies = []
        
        # Statistical anomaly detection
        mean_amount = spending_df['amount'].mean()
        std_amount = spending_df['amount'].std()
        threshold = mean_amount + 2 * std_amount
        
        unusual_transactions = spending_df[spending_df['amount'] > threshold]
        
        for _, transaction in unusual_transactions.iterrows():
            anomalies.append({
                'type': 'high_amount',
                'transaction_id': transaction.get('transaction_id', ''),
                'amount': transaction['amount'],
                'date': transaction['date'],
                'merchant': transaction.get('merchant_name', ''),
                'description': f"Unusually high transaction: ${transaction['amount']:.2f} (avg: ${mean_amount:.2f})",
                'severity': 'medium' if transaction['amount'] < threshold * 1.5 else 'high'
            })
        
        # Category-based anomalies
        category_stats = spending_df.groupby('category')['amount'].agg(['mean', 'std']).fillna(0)
        
        for category, stats in category_stats.iterrows():
            cat_transactions = spending_df[spending_df['category'] == category]
            cat_threshold = stats['mean'] + 2 * stats['std']
            
            unusual_cat_transactions = cat_transactions[cat_transactions['amount'] > cat_threshold]
            
            for _, transaction in unusual_cat_transactions.iterrows():
                if transaction['amount'] <= threshold:  # Don't duplicate global anomalies
                    anomalies.append({
                        'type': 'category_anomaly',
                        'transaction_id': transaction.get('transaction_id', ''),
                        'amount': transaction['amount'],
                        'category': category,
                        'date': transaction['date'],
                        'description': f"Unusual {category} spending: ${transaction['amount']:.2f}",
                        'severity': 'low'
                    })
        
        return sorted(anomalies, key=lambda x: x['amount'], reverse=True)[:10]
    
    def _analyze_seasonal_patterns(self, df: pd.DataFrame) -> Dict:
        """Analyze seasonal spending patterns."""
        spending_df = df[df['amount'] > 0].copy()
        
        if spending_df.empty:
            return {}
        
        spending_df['date'] = pd.to_datetime(spending_df['date'])
        spending_df['month'] = spending_df['date'].dt.month
        spending_df['quarter'] = spending_df['date'].dt.quarter
        
        seasonal_patterns = {
            'monthly_spending': spending_df.groupby('month')['amount'].sum().to_dict(),
            'quarterly_spending': spending_df.groupby('quarter')['amount'].sum().to_dict(),
            'seasonal_categories': {}
        }
        
        # Analyze category seasonality
        for category in spending_df['category'].unique():
            cat_data = spending_df[spending_df['category'] == category]
            if len(cat_data) > 5:
                monthly_cat = cat_data.groupby('month')['amount'].sum()
                seasonal_patterns['seasonal_categories'][category] = {
                    'peak_month': monthly_cat.idxmax(),
                    'low_month': monthly_cat.idxmin(),
                    'variation': monthly_cat.std() / monthly_cat.mean() if monthly_cat.mean() > 0 else 0
                }
        
        return seasonal_patterns
    
    def _predict_investment_capacity(self, df: pd.DataFrame) -> Dict:
        """Predict investment capacity using ML analysis."""
        spending_df = df[df['amount'] > 0].copy()
        income_df = df[df['amount'] < 0].copy()  # Deposits/income
        
        if spending_df.empty:
            return {'recommended_investment': 0, 'confidence': 0}
        
        # Calculate financial metrics
        total_spending = spending_df['amount'].sum()
        total_income = abs(income_df['amount'].sum()) if not income_df.empty else total_spending * 1.2
        
        # Categorize spending
        essential_spending = spending_df[spending_df['spending_type'] == 'essential']['amount'].sum()
        discretionary_spending = spending_df[spending_df['spending_type'] == 'discretionary']['amount'].sum()
        
        # Calculate savings rate
        net_income = total_income - total_spending
        savings_rate = net_income / total_income if total_income > 0 else 0
        
        # ML-based investment capacity prediction
        features = np.array([
            total_income,
            essential_spending,
            discretionary_spending,
            savings_rate,
            len(spending_df),  # Transaction frequency
            spending_df['amount'].std()  # Spending volatility
        ]).reshape(1, -1)
        
        # Simple heuristic-based prediction (can be replaced with trained model)
        if discretionary_spending > 0:
            # Recommend 20-30% of discretionary spending for investment
            base_recommendation = discretionary_spending * 0.25
        else:
            # Conservative recommendation based on income
            base_recommendation = total_income * 0.05
        
        # Adjust based on savings rate
        if savings_rate > 0.2:  # Good saver
            investment_multiplier = 1.2
        elif savings_rate < 0:  # Spending more than earning
            investment_multiplier = 0.3
        else:
            investment_multiplier = 1.0
        
        recommended_investment = max(10, base_recommendation * investment_multiplier)
        
        # Calculate confidence based on data quality
        confidence = min(95, len(df) * 2 + (30 if not income_df.empty else 0))
        
        return {
            'recommended_monthly_investment': recommended_investment,
            'current_savings_rate': savings_rate,
            'total_income': total_income,
            'essential_spending': essential_spending,
            'discretionary_spending': discretionary_spending,
            'confidence': confidence,
            'investment_rationale': self._generate_investment_rationale(
                recommended_investment, savings_rate, discretionary_spending
            )
        }
    
    def _generate_optimization_tips(self, df: pd.DataFrame, patterns: Dict) -> List[Dict]:
        """Generate ML-powered spending optimization tips."""
        tips = []
        
        spending_by_category = patterns.get('spending_by_category', {})
        total_spending = sum(spending_by_category.values())
        
        if not spending_by_category:
            return tips
        
        # Find highest spending categories
        sorted_categories = sorted(spending_by_category.items(), key=lambda x: x[1], reverse=True)
        
        for category, amount in sorted_categories[:3]:
            percentage = (amount / total_spending) * 100 if total_spending > 0 else 0
            
            if percentage > 30:
                tips.append({
                    'type': 'high_category_spending',
                    'category': category,
                    'amount': amount,
                    'percentage': percentage,
                    'priority': 'high',
                    'suggestion': f"Your {category} spending is {percentage:.1f}% of total expenses. Consider setting a budget limit.",
                    'potential_savings': amount * 0.1  # 10% reduction potential
                })
        
        # Analyze merchant patterns
        top_merchants = patterns.get('top_merchants', {})
        for merchant, amount in list(top_merchants.items())[:3]:
            if amount > total_spending * 0.1:  # More than 10% at single merchant
                tips.append({
                    'type': 'merchant_concentration',
                    'merchant': merchant,
                    'amount': amount,
                    'priority': 'medium',
                    'suggestion': f"You spend ${amount:.2f} at {merchant}. Look for alternatives or bulk discounts.",
                    'potential_savings': amount * 0.05
                })
        
        # Weekend vs weekday analysis
        weekend_weekday = patterns.get('weekend_vs_weekday', {})
        if weekend_weekday:
            weekend_spending = weekend_weekday.get('weekend', 0)
            weekday_spending = weekend_weekday.get('weekday', 0)
            
            if weekend_spending > weekday_spending * 0.4:  # High weekend spending
                tips.append({
                    'type': 'weekend_spending',
                    'weekend_amount': weekend_spending,
                    'weekday_amount': weekday_spending,
                    'priority': 'low',
                    'suggestion': "High weekend spending detected. Plan weekend activities with a budget.",
                    'potential_savings': weekend_spending * 0.15
                })
        
        return sorted(tips, key=lambda x: x.get('potential_savings', 0), reverse=True)
    
    def _generate_investment_rationale(self, recommended_amount: float, savings_rate: float, discretionary_spending: float) -> str:
        """Generate explanation for investment recommendation."""
        if savings_rate > 0.2:
            return f"With a strong savings rate of {savings_rate:.1%}, you can comfortably invest ${recommended_amount:.0f} monthly."
        elif savings_rate > 0:
            return f"Your current savings rate allows for ${recommended_amount:.0f} monthly investment while maintaining financial stability."
        else:
            return f"Focus on reducing discretionary spending (${discretionary_spending:.0f}) to enable ${recommended_amount:.0f} monthly investment."
    
    def _calculate_summary_stats(self, df: pd.DataFrame) -> Dict:
        """Calculate comprehensive summary statistics."""
        spending_df = df[df['amount'] > 0]
        
        if spending_df.empty:
            return {}
        
        return {
            'total_transactions': len(df),
            'spending_transactions': len(spending_df),
            'total_spending': spending_df['amount'].sum(),
            'average_transaction': spending_df['amount'].mean(),
            'median_transaction': spending_df['amount'].median(),
            'largest_transaction': spending_df['amount'].max(),
            'categories_count': spending_df['category'].nunique(),
            'merchants_count': spending_df['merchant_name'].nunique(),
            'date_range': {
                'start': df['date'].min(),
                'end': df['date'].max(),
                'days': (pd.to_datetime(df['date'].max()) - pd.to_datetime(df['date'].min())).days
            }
        }
    
    def _empty_analysis(self) -> Dict:
        """Return empty analysis structure."""
        return {
            'categorized_transactions': pd.DataFrame(),
            'spending_patterns': {},
            'anomalies': [],
            'seasonal_insights': {},
            'investment_capacity': {'recommended_investment': 0, 'confidence': 0},
            'optimization_tips': [],
            'summary_stats': {}
        }
