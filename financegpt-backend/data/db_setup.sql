-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- User Profiles table
CREATE TABLE IF NOT EXISTS user_profiles (
    user_id INTEGER PRIMARY KEY REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    age INTEGER NOT NULL,
    income NUMERIC(12,2) NOT NULL,
    employment_type VARCHAR(50) NOT NULL,
    risk_appetite VARCHAR(50) NOT NULL,
    financial_goals VARCHAR(255) NOT NULL,
    credit_score INTEGER NOT NULL,
    kyc_verified VARCHAR(5) NOT NULL
);

-- Financial Products table
CREATE TABLE IF NOT EXISTS financial_products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,
    interest_rate VARCHAR(20),
    min_amount NUMERIC(12,2) NOT NULL,
    risk_level VARCHAR(50) NOT NULL,
    tenure_months INTEGER,
    eligibility VARCHAR(255)
);

-- Query Logs table
CREATE TABLE IF NOT EXISTS query_logs (
    id SERIAL PRIMARY KEY,
    trace_id VARCHAR(255) UNIQUE NOT NULL,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    user_name VARCHAR(255) NOT NULL,
    query TEXT NOT NULL,
    answer TEXT NOT NULL,
    confidence_score NUMERIC(3,2) NOT NULL,
    processing_time NUMERIC(8,3) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Offers table
CREATE TABLE IF NOT EXISTS offers (
    id SERIAL PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    promo_interest_rate VARCHAR(20),
    signup_bonus VARCHAR(255),
    valid_till DATE NOT NULL
);

-- Sample data
-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- User Profiles table
CREATE TABLE IF NOT EXISTS user_profiles (
    user_id INTEGER PRIMARY KEY REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    age INTEGER NOT NULL,
    income NUMERIC(12,2) NOT NULL,
    employment_type VARCHAR(50) NOT NULL,
    risk_appetite VARCHAR(50) NOT NULL,
    financial_goals VARCHAR(255) NOT NULL,
    credit_score INTEGER NOT NULL,
    kyc_verified VARCHAR(5) NOT NULL
);

-- Financial Products table
CREATE TABLE IF NOT EXISTS financial_products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,
    interest_rate VARCHAR(20),
    min_amount NUMERIC(12,2) NOT NULL,
    risk_level VARCHAR(50) NOT NULL,
    tenure_months INTEGER,
    eligibility VARCHAR(255)
);

-- Query Logs table
CREATE TABLE IF NOT EXISTS query_logs (
    id SERIAL PRIMARY KEY,
    trace_id VARCHAR(255) UNIQUE NOT NULL,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    user_name VARCHAR(255) NOT NULL,
    query TEXT NOT NULL,
    answer TEXT NOT NULL,
    confidence_score NUMERIC(3,2) NOT NULL,
    processing_time NUMERIC(8,3) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Offers table
CREATE TABLE IF NOT EXISTS offers (
    id SERIAL PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    promo_interest_rate VARCHAR(20),
    signup_bonus VARCHAR(255),
    valid_till DATE NOT NULL
);

-- Sample data
INSERT INTO public.financial_products 
(id, name, type, interest_rate, min_amount, risk_level, tenure_months, eligibility)
VALUES
(1, 'Secure FD Plus', 'Fixed Deposit', '7.2%', 5000.00, 'Low', 24, 'Age > 18'),
(2, 'Ultra Growth Fund', 'Mutual Fund', '~12%', 1000.00, 'High', NULL, 'KYC Verified'),
(3, 'HealthShield', 'Insurance', 'NA', 3000.00, 'Low', 12, 'Age 18–55'),
(4, 'Cashback Credit', 'Credit Card', 'NA', 0.00, 'Medium', NULL, 'Credit Score > 700'),
(5, 'Wealth Builder FD', 'Fixed Deposit', '6.8%', 10000.00, 'Low', 36, 'Senior Citizen'),
(6, 'Equity Advantage Fund', 'Mutual Fund', '~14%', 1500.00, 'High', NULL, 'KYC Verified'),
(7, 'LifeCare Policy', 'Insurance', 'NA', 5000.00, 'Low', 60, 'Age 25–60'),
(8, 'Gold Saver Plan', 'Savings Scheme', '6.5%', 2000.00, 'Medium', 12, 'All Residents'),
(9, 'Travel Freedom Card', 'Credit Card', 'NA', 0.00, 'Medium', NULL, 'Salary > ₹30,000'),
(10, 'Smart EMI Loan', 'Loan', '10.5%', 25000.00, 'Medium', 24, 'Credit Score > 650'),
(11, 'Green Energy Bond', 'Bond', '8.0%', 10000.00, 'Medium', 60, 'KYC Verified'),
(12, 'Digital Gold Account', 'Commodity Investment', 'NA', 100.00, 'Low', NULL, 'KYC Verified'),
(13, 'Secure Child Plan', 'Insurance', 'NA', 4000.00, 'Low', 180, 'Parents Age 25–45'),
(14, 'Balanced Income Fund', 'Mutual Fund', '~9%', 2000.00, 'Medium', NULL, 'KYC Verified'),
(15, 'Premium Salary Account', 'Savings Account', '3.5%', 0.00, 'Low', NULL, 'Salaried Individual'),
(16, 'Flexi Recurring Deposit', 'Recurring Deposit', '6.9%', 500.00, 'Low', 12, 'Age > 18'),
(17, 'Startup Equity Plan', 'Mutual Fund', '~16%', 5000.00, 'High', NULL, 'KYC + PAN'),
(18, 'Zero Fee Credit Card', 'Credit Card', 'NA', 0.00, 'Medium', NULL, 'Credit Score > 680'),
(19, 'Pension Plus', 'Retirement Fund', '7.5%', 3000.00, 'Low', 240, 'Age 30–55'),
(20, 'Auto Loan Express', 'Loan', '9.8%', 50000.00, 'Medium', 60, 'Vehicle Quotation + Credit Score > 700'),
(21, 'Senior Advantage FD', 'Fixed Deposit', '7.75%', 5000.00, 'Low', 36, 'Age > 60'),
(22, 'Home Protect Insurance', 'Insurance', 'NA', 6000.00, 'Low', 120, 'Property Owner'),
(23, 'Index Tracker Fund', 'Mutual Fund', '~10%', 1000.00, 'Medium', NULL, 'KYC Verified'),
(24, 'Digital Savings Lite', 'Savings Account', '3.0%', 0.00, 'Low', NULL, 'Aadhaar + Mobile Verified');


INSERT INTO public.offers 
(id, product_name, promo_interest_rate, signup_bonus, valid_till)
VALUES
(5, 'Secure FD Plus', '7.8%', '₹750 bonus for deposits above ₹1L', '2025-12-31'),
(6, 'Ultra Growth Fund', '13%', 'Zero processing fee + ₹500 investment bonus', '2025-10-31'),
(7, 'Cashback Credit', NULL, '2X cashback for first 3 months', '2025-09-30'),
(8, 'LifeCare Policy', NULL, '₹1000 bonus on annual premium > ₹50,000', '2026-01-15'),
(9, 'HealthShield', NULL, 'Flat 15% discount on premiums', '2025-12-15'),
(10, 'Smart EMI Loan', '9.5%', 'No processing fee + free credit report', '2025-11-30'),

