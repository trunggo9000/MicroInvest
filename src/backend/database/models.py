from datetime import datetime
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, Session as DBSession
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment variables or use SQLite as default
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./microinvest.db")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class User(Base):
    """User model to store user information and authentication"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    date_of_birth = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    profiles = relationship("UserProfile", back_populates="user", uselist=False)
    portfolios = relationship("Portfolio", back_populates="user")
    goals = relationship("InvestmentGoal", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"


class UserProfile(Base):
    """Extended user profile with financial information"""
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    
    # Financial information
    annual_income = Column(Float, nullable=True)
    monthly_savings = Column(Float, nullable=True)
    risk_tolerance = Column(String, default="medium")  # low, medium, high
    investment_experience = Column(String, nullable=True)  # beginner, intermediate, advanced
    
    # Preferences
    investment_style = Column(String, nullable=True)  # growth, income, balanced
    preferred_assets = Column(JSON, default=list)  # List of preferred asset classes
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="profiles")
    
    def __repr__(self):
        return f"<UserProfile(user_id={self.user_id}, risk_tolerance={self.risk_tolerance})>"


class Portfolio(Base):
    """Portfolio model to store user investment portfolios"""
    __tablename__ = "portfolios"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, default="My Portfolio")
    description = Column(String, nullable=True)
    
    # Portfolio allocation (stored as JSON for flexibility)
    allocation = Column(JSON, default=dict)  # e.g., {"stocks": 0.6, "bonds": 0.4}
    
    # Performance metrics
    expected_return = Column(Float, nullable=True)
    volatility = Column(Float, nullable=True)
    sharpe_ratio = Column(Float, nullable=True)
    
    # Metadata
    is_primary = Column(Integer, default=0)  # 0 or 1 to indicate primary portfolio
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="portfolios")
    goals = relationship("InvestmentGoal", back_populates="portfolio")
    
    def __repr__(self):
        return f"<Portfolio(id={self.id}, name='{self.name}')>"


class InvestmentGoal(Base):
    """Investment goals and targets for users"""
    __tablename__ = "investment_goals"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=True)
    
    # Goal details
    name = Column(String, nullable=False)  # e.g., "Retirement", "Buy a House"
    target_amount = Column(Float, nullable=False)
    current_amount = Column(Float, default=0.0)
    target_date = Column(DateTime, nullable=True)
    
    # Risk preferences for this specific goal
    risk_tolerance = Column(String, default="medium")  # low, medium, high
    
    # Status
    status = Column(String, default="active")  # active, completed, on_hold, cancelled
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="goals")
    portfolio = relationship("Portfolio", back_populates="goals")
    
    def __repr__(self):
        return f"<InvestmentGoal(id={self.id}, name='{self.name}', target_amount={self.target_amount})>"


class Transaction(Base):
    """Investment transactions (deposits, withdrawals, rebalancing)"""
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=False)
    
    # Transaction details
    type = Column(String, nullable=False)  # deposit, withdrawal, buy, sell, rebalance
    asset = Column(String, nullable=False)  # e.g., "stocks", "bonds"
    amount = Column(Float, nullable=False)
    price_per_unit = Column(Float, nullable=True)
    
    # Metadata
    notes = Column(String, nullable=True)
    transaction_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, type='{self.type}', amount={self.amount})>"


# Create all tables
def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    # Create tables
    init_db()
    print("Database tables created successfully.")
