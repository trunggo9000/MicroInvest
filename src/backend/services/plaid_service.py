"""
Plaid Integration Service for Real-time Transaction Data
"""
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging
from plaid.api import plaid_api
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.country_code import CountryCode
from plaid.model.products import Products
from plaid.configuration import Configuration
from plaid.api_client import ApiClient
import pandas as pd

logger = logging.getLogger(__name__)

class PlaidService:
    """Service for integrating with Plaid API to fetch real-time transaction data."""
    
    def __init__(self):
        """Initialize Plaid client with environment variables."""
        self.client_id = os.getenv('PLAID_CLIENT_ID')
        self.secret = os.getenv('PLAID_SECRET')
        self.environment = os.getenv('PLAID_ENV', 'sandbox')  # sandbox, development, production
        
        if not self.client_id or not self.secret:
            logger.warning("Plaid credentials not found. Using mock data.")
            self.client = None
            return
        
        # Configure Plaid client
        configuration = Configuration(
            host=getattr(plaid_api.Environment, self.environment),
            api_key={
                'clientId': self.client_id,
                'secret': self.secret
            }
        )
        api_client = ApiClient(configuration)
        self.client = plaid_api.PlaidApi(api_client)
    
    def create_link_token(self, user_id: str) -> Optional[str]:
        """Create a link token for Plaid Link initialization."""
        if not self.client:
            return None
        
        try:
            request = LinkTokenCreateRequest(
                products=[Products('transactions')],
                client_name="MicroInvest",
                country_codes=[CountryCode('US')],
                language='en',
                user=LinkTokenCreateRequestUser(client_user_id=user_id)
            )
            response = self.client.link_token_create(request)
            return response['link_token']
        except Exception as e:
            logger.error(f"Error creating link token: {e}")
            return None
    
    def exchange_public_token(self, public_token: str) -> Optional[str]:
        """Exchange public token for access token."""
        if not self.client:
            return None
        
        try:
            request = ItemPublicTokenExchangeRequest(public_token=public_token)
            response = self.client.item_public_token_exchange(request)
            return response['access_token']
        except Exception as e:
            logger.error(f"Error exchanging public token: {e}")
            return None
    
    def get_accounts(self, access_token: str) -> List[Dict]:
        """Get user's bank accounts."""
        if not self.client:
            return self._get_mock_accounts()
        
        try:
            request = AccountsGetRequest(access_token=access_token)
            response = self.client.accounts_get(request)
            
            accounts = []
            for account in response['accounts']:
                accounts.append({
                    'account_id': account['account_id'],
                    'name': account['name'],
                    'type': account['type'],
                    'subtype': account['subtype'],
                    'balance': account['balances']['current'],
                    'available_balance': account['balances']['available']
                })
            return accounts
        except Exception as e:
            logger.error(f"Error fetching accounts: {e}")
            return self._get_mock_accounts()
    
    def get_transactions(self, access_token: str, days: int = 30) -> pd.DataFrame:
        """Get recent transactions from user's accounts."""
        if not self.client:
            return self._get_mock_transactions(days)
        
        try:
            start_date = datetime.now() - timedelta(days=days)
            end_date = datetime.now()
            
            request = TransactionsGetRequest(
                access_token=access_token,
                start_date=start_date.date(),
                end_date=end_date.date()
            )
            response = self.client.transactions_get(request)
            
            transactions = []
            for transaction in response['transactions']:
                transactions.append({
                    'transaction_id': transaction['transaction_id'],
                    'account_id': transaction['account_id'],
                    'amount': transaction['amount'],
                    'date': transaction['date'],
                    'name': transaction['name'],
                    'merchant_name': transaction.get('merchant_name', ''),
                    'category': transaction['category'][0] if transaction['category'] else 'Other',
                    'subcategory': transaction['category'][1] if len(transaction['category']) > 1 else '',
                    'account_owner': transaction.get('account_owner', '')
                })
            
            return pd.DataFrame(transactions)
        except Exception as e:
            logger.error(f"Error fetching transactions: {e}")
            return self._get_mock_transactions(days)
    
    def analyze_spending_patterns(self, transactions_df: pd.DataFrame) -> Dict:
        """Analyze spending patterns from transaction data."""
        if transactions_df.empty:
            return {}
        
        # Convert date column to datetime
        transactions_df['date'] = pd.to_datetime(transactions_df['date'])
        
        # Filter out deposits (negative amounts in Plaid represent money going out)
        spending_df = transactions_df[transactions_df['amount'] > 0].copy()
        
        analysis = {
            'total_spending': spending_df['amount'].sum(),
            'avg_daily_spending': spending_df['amount'].sum() / len(spending_df['date'].dt.date.unique()),
            'transaction_count': len(spending_df),
            'avg_transaction_amount': spending_df['amount'].mean(),
            'spending_by_category': spending_df.groupby('category')['amount'].sum().to_dict(),
            'monthly_trend': spending_df.groupby(spending_df['date'].dt.to_period('M'))['amount'].sum().to_dict(),
            'top_merchants': spending_df.groupby('merchant_name')['amount'].sum().nlargest(10).to_dict()
        }
        
        return analysis
    
    def get_investment_capacity(self, transactions_df: pd.DataFrame) -> Dict:
        """Calculate potential investment capacity based on spending patterns."""
        if transactions_df.empty:
            return {'recommended_monthly_investment': 0, 'confidence': 0}
        
        analysis = self.analyze_spending_patterns(transactions_df)
        
        # Calculate income (deposits)
        income_df = transactions_df[transactions_df['amount'] < 0].copy()
        monthly_income = abs(income_df['amount'].sum()) / (len(transactions_df) / 30)
        
        # Calculate essential vs discretionary spending
        essential_categories = ['Food and Drink', 'Transportation', 'Shops', 'Payment', 'Transfer']
        essential_spending = sum([analysis['spending_by_category'].get(cat, 0) for cat in essential_categories])
        total_spending = analysis['total_spending']
        discretionary_spending = total_spending - essential_spending
        
        # Recommend 10-20% of discretionary spending for investment
        recommended_investment = min(discretionary_spending * 0.15, monthly_income * 0.1)
        
        # Calculate confidence based on data quality
        confidence = min(100, len(transactions_df) * 2)  # Higher confidence with more data
        
        return {
            'recommended_monthly_investment': max(10, recommended_investment),  # Minimum $10
            'monthly_income': monthly_income,
            'essential_spending': essential_spending,
            'discretionary_spending': discretionary_spending,
            'confidence': confidence,
            'spending_analysis': analysis
        }
    
    def _get_mock_accounts(self) -> List[Dict]:
        """Generate mock account data for testing."""
        return [
            {
                'account_id': 'mock_checking_001',
                'name': 'Student Checking',
                'type': 'depository',
                'subtype': 'checking',
                'balance': 1250.50,
                'available_balance': 1200.50
            },
            {
                'account_id': 'mock_savings_001',
                'name': 'Emergency Savings',
                'type': 'depository',
                'subtype': 'savings',
                'balance': 850.00,
                'available_balance': 850.00
            }
        ]
    
    def _get_mock_transactions(self, days: int = 30) -> pd.DataFrame:
        """Generate mock transaction data for testing."""
        import random
        
        transactions = []
        start_date = datetime.now() - timedelta(days=days)
        
        # Mock transaction categories and amounts
        categories = [
            ('Food and Drink', 15, 45),
            ('Transportation', 5, 25),
            ('Shops', 20, 80),
            ('Entertainment', 10, 50),
            ('Transfer', -500, -200),  # Income
            ('Payment', 50, 200),
            ('Healthcare', 20, 100)
        ]
        
        for i in range(days * 3):  # ~3 transactions per day
            category, min_amt, max_amt = random.choice(categories)
            amount = random.uniform(min_amt, max_amt)
            date = start_date + timedelta(days=random.randint(0, days-1))
            
            transactions.append({
                'transaction_id': f'mock_txn_{i:04d}',
                'account_id': 'mock_checking_001',
                'amount': amount,
                'date': date.date(),
                'name': f'Mock Transaction {i}',
                'merchant_name': f'Mock Merchant {random.randint(1, 20)}',
                'category': category,
                'subcategory': '',
                'account_owner': 'student'
            })
        
        return pd.DataFrame(transactions)
