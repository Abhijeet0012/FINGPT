from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, DECIMAL, ForeignKey, Date, func
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    is_active = Column(Boolean, default=True)
    profile = relationship('UserProfile', back_populates='user', uselist=False)
    query_logs = relationship('QueryLog', back_populates='user')

class UserProfile(Base):
    __tablename__ = 'user_profiles'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    name = Column(String(255), nullable=False)
    age = Column(Integer, nullable=False)
    income = Column(DECIMAL(12,2), nullable=False)
    employment_type = Column(String(50), nullable=False)
    risk_appetite = Column(String(50), nullable=False)
    financial_goals = Column(String(255), nullable=False)
    credit_score = Column(Integer, nullable=False)
    kyc_verified = Column(String(5), nullable=False)
    user = relationship('User', back_populates='profile')

class FinancialProduct(Base):
    __tablename__ = 'financial_products'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)
    interest_rate = Column(String(20))
    min_amount = Column(DECIMAL(12,2), nullable=False)
    risk_level = Column(String(50), nullable=False)
    tenure_months = Column(Integer)
    eligibility = Column(String(255))

class QueryLog(Base):
    __tablename__ = 'query_logs'
    id = Column(Integer, primary_key=True)
    trace_id = Column(String(255), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user_name = Column(String(255), nullable=False)
    query = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    confidence_score = Column(DECIMAL(3,2), nullable=False)
    processing_time = Column(DECIMAL(8,3), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    user = relationship('User', back_populates='query_logs')

class Offer(Base):
    __tablename__ = 'offers'
    id = Column(Integer, primary_key=True)
    product_name = Column(String(255), nullable=False)
    promo_interest_rate = Column(String(20))
    signup_bonus = Column(String(255))
    valid_till = Column(Date, nullable=False) 