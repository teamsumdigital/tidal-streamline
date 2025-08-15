-- Tidal Streamline Database Schema
-- Market Scan Automation System

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Market Scans Table
CREATE TABLE market_scans (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_name VARCHAR(100) NOT NULL,
    client_email VARCHAR(255) NOT NULL,
    company_domain VARCHAR(100) NOT NULL,
    job_title VARCHAR(200) NOT NULL,
    job_description TEXT NOT NULL,
    hiring_challenges TEXT,
    
    -- Analysis Results (stored as JSONB for flexibility)
    job_analysis JSONB,
    salary_recommendations JSONB,
    skills_recommendations JSONB,
    
    -- Metadata
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'analyzing', 'completed', 'failed')),
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    processing_time_seconds REAL,
    similar_scans_count INTEGER DEFAULT 0,
    confidence_score REAL CHECK (confidence_score >= 0 AND confidence_score <= 1),
    
    -- Searchable fields extracted from analysis
    role_category VARCHAR(100),
    experience_level VARCHAR(20),
    recommended_regions TEXT[],
    complexity_score INTEGER CHECK (complexity_score >= 1 AND complexity_score <= 10)
);

-- Roles and Title Mappings Table
CREATE TABLE roles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    core_role VARCHAR(100) NOT NULL UNIQUE,
    common_titles TEXT[] NOT NULL,
    description TEXT,
    category VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Salary Benchmarks Table
CREATE TABLE salary_benchmarks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    role_category VARCHAR(100) NOT NULL,
    region VARCHAR(50) NOT NULL,
    experience_level VARCHAR(20) NOT NULL,
    salary_low INTEGER NOT NULL,
    salary_mid INTEGER NOT NULL,
    salary_high INTEGER NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    period VARCHAR(10) DEFAULT 'monthly',
    savings_vs_us INTEGER CHECK (savings_vs_us >= 0 AND savings_vs_us <= 100),
    data_source VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(role_category, region, experience_level)
);

-- Candidate Profiles Table
CREATE TABLE candidate_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    role_category VARCHAR(100) NOT NULL,
    experience_years VARCHAR(20),
    region VARCHAR(50) NOT NULL,
    skills TEXT[] NOT NULL,
    bio TEXT,
    video_url VARCHAR(500),
    resume_url VARCHAR(500),
    portfolio_url VARCHAR(500),
    hourly_rate INTEGER,
    availability VARCHAR(50) DEFAULT 'Available',
    english_proficiency VARCHAR(20) DEFAULT 'Fluent',
    timezone VARCHAR(10),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Skills Catalog Table
CREATE TABLE skills (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    skill_name VARCHAR(100) NOT NULL UNIQUE,
    category VARCHAR(50),
    description TEXT,
    frequency_score REAL DEFAULT 0,
    is_technical BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Historical Market Scans Import Table
CREATE TABLE historical_scans (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    original_scan_id VARCHAR(100),
    job_title VARCHAR(200) NOT NULL,
    job_description TEXT,
    role_category VARCHAR(100),
    region VARCHAR(50),
    salary_range VARCHAR(100),
    skills_required TEXT[],
    date_created DATE,
    client_name VARCHAR(100),
    import_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    processed BOOLEAN DEFAULT false
);

-- Client Requests Log Table
CREATE TABLE client_requests (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_email VARCHAR(255) NOT NULL,
    company_domain VARCHAR(100),
    request_type VARCHAR(50) NOT NULL,
    request_data JSONB,
    response_data JSONB,
    status VARCHAR(20) DEFAULT 'pending',
    processing_time_seconds REAL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    user_agent TEXT,
    ip_address INET
);

-- Indexes for Performance
CREATE INDEX idx_market_scans_status ON market_scans(status);
CREATE INDEX idx_market_scans_created_at ON market_scans(created_at DESC);
CREATE INDEX idx_market_scans_role_category ON market_scans(role_category);
CREATE INDEX idx_market_scans_client_email ON market_scans(client_email);
CREATE INDEX idx_market_scans_company_domain ON market_scans(company_domain);

CREATE INDEX idx_salary_benchmarks_role_region ON salary_benchmarks(role_category, region);
CREATE INDEX idx_candidate_profiles_role ON candidate_profiles(role_category);
CREATE INDEX idx_candidate_profiles_region ON candidate_profiles(region);
CREATE INDEX idx_candidate_profiles_active ON candidate_profiles(is_active) WHERE is_active = true;

CREATE INDEX idx_historical_scans_processed ON historical_scans(processed) WHERE processed = false;
CREATE INDEX idx_client_requests_created_at ON client_requests(created_at DESC);

-- Full-text search indexes
CREATE INDEX idx_market_scans_job_title_fts ON market_scans USING GIN(to_tsvector('english', job_title));
CREATE INDEX idx_market_scans_job_description_fts ON market_scans USING GIN(to_tsvector('english', job_description));

-- Updated timestamp trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply updated_at triggers
CREATE TRIGGER update_market_scans_updated_at BEFORE UPDATE ON market_scans
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_roles_updated_at BEFORE UPDATE ON roles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_salary_benchmarks_updated_at BEFORE UPDATE ON salary_benchmarks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_candidate_profiles_updated_at BEFORE UPDATE ON candidate_profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert default role mappings
INSERT INTO roles (core_role, common_titles, description, category) VALUES
('Brand Marketing Manager', 
 ARRAY['Creative Project Manager', 'Marketing Project Manager', 'Production Manager', 'Marketing Operations Manager'],
 'Manages brand marketing campaigns and creative projects',
 'Marketing'),

('Community Manager',
 ARRAY['Social Media Manager', 'Influencer Coordinator', 'Affiliate Manager', 'Partnerships Coordinator'],
 'Manages online communities and social media presence',
 'Marketing'),

('Content Marketer',
 ARRAY['Brand Content Manager', 'Content Strategist', 'Digital Content Manager', 'Creative Content Manager'],
 'Creates and manages content marketing strategies',
 'Marketing'),

('Retention Manager',
 ARRAY['Email Marketing Manager', 'Lifecycle Marketing Manager', 'CRM Manager'],
 'Focuses on customer retention and lifecycle marketing',
 'Marketing'),

('Ecommerce Manager',
 ARRAY['E-commerce Manager', 'Shopify Manager', 'E-commerce Operations Manager', 'E-commerce Project Manager', 'Digital Commerce Manager'],
 'Manages online store operations and e-commerce strategy',
 'Operations'),

('Sales Operations Manager',
 ARRAY['Operations Manager', 'RevOps Manager', 'Amazon/Shopify/Sales Channel Manager'],
 'Optimizes sales processes and revenue operations',
 'Operations'),

('Data Analyst',
 ARRAY['Data Engineer', 'Marketing Data Analyst', 'Business Intelligence Analyst', 'Digital Analytics Specialist', 'Reporting Analyst', 'Performance Marketing Analyst'],
 'Analyzes data to drive business insights and decisions',
 'Analytics'),

('Logistics Manager',
 ARRAY['Supply Chain Coordinator', 'Operations Manager', 'Fulfillment Operations Manager', 'Freight Coordinator', 'EDI/ERP Coordinator'],
 'Manages supply chain and logistics operations',
 'Operations');

-- Insert default salary benchmarks
INSERT INTO salary_benchmarks (role_category, region, experience_level, salary_low, salary_mid, salary_high, savings_vs_us) VALUES
-- United States baseline
('Brand Marketing Manager', 'United States', '2-4 years', 5000, 6000, 7000, 0),
('Brand Marketing Manager', 'United States', '5-8 years', 6000, 7000, 8000, 0),
('Brand Marketing Manager', 'United States', '9+ years', 7000, 8000, 9000, 0),

-- Philippines
('Brand Marketing Manager', 'Philippines', '2-4 years', 1500, 1750, 2000, 71),
('Brand Marketing Manager', 'Philippines', '5-8 years', 1750, 2000, 2250, 71),
('Brand Marketing Manager', 'Philippines', '9+ years', 2000, 2250, 2500, 71),

-- Latin America
('Brand Marketing Manager', 'Latin America', '2-4 years', 2200, 2500, 2800, 58),
('Brand Marketing Manager', 'Latin America', '5-8 years', 2500, 2800, 3100, 58),
('Brand Marketing Manager', 'Latin America', '9+ years', 2800, 3100, 3400, 58),

-- South Africa
('Brand Marketing Manager', 'South Africa', '2-4 years', 2800, 3000, 3200, 48),
('Brand Marketing Manager', 'South Africa', '5-8 years', 3200, 3500, 3800, 48),
('Brand Marketing Manager', 'South Africa', '9+ years', 3600, 4000, 4400, 48),

-- Ecommerce Manager
('Ecommerce Manager', 'United States', '2-4 years', 4500, 5500, 6500, 0),
('Ecommerce Manager', 'Philippines', '2-4 years', 1400, 1600, 1800, 71),
('Ecommerce Manager', 'Latin America', '2-4 years', 2000, 2300, 2600, 58),
('Ecommerce Manager', 'South Africa', '2-4 years', 2600, 2900, 3200, 48),

-- Data Analyst
('Data Analyst', 'United States', '2-4 years', 4000, 5000, 6000, 0),
('Data Analyst', 'Philippines', '2-4 years', 1200, 1450, 1700, 71),
('Data Analyst', 'Latin America', '2-4 years', 1800, 2100, 2400, 58),
('Data Analyst', 'South Africa', '2-4 years', 2400, 2600, 2800, 48);

-- Insert sample candidate profiles
INSERT INTO candidate_profiles (name, role_category, experience_years, region, skills, bio, hourly_rate, timezone) VALUES
('Maria Santos', 'Ecommerce Manager', '5-8 years', 'Philippines', 
 ARRAY['Shopify Admin', 'Google Analytics', 'Email Marketing', 'Project Management'],
 'Experienced e-commerce manager with 6 years of experience managing Shopify stores for US-based brands. Specialized in conversion optimization and customer retention strategies.',
 15, 'GMT+8'),

('Carlos Rodriguez', 'Data Analyst', '3-6 years', 'Latin America',
 ARRAY['Excel Advanced', 'SQL', 'Python', 'Tableau', 'Google Analytics'],
 'Data analyst with strong background in e-commerce analytics and reporting. Experience with large datasets and automated reporting systems.',
 18, 'GMT-3'),

('Thandiwe Mokwena', 'Content Marketer', '2-4 years', 'South Africa',
 ARRAY['Content Creation', 'Social Media', 'SEO', 'Adobe Creative Suite'],
 'Creative content marketer with experience in B2C brands. Strong background in social media content and email marketing campaigns.',
 20, 'GMT+2'),

('Sofia Mendoza', 'Brand Marketing Manager', '5-8 years', 'Latin America',
 ARRAY['Project Management', 'Creative Direction', 'Marketing Automation', 'Adobe Creative Suite'],
 'Brand marketing manager with extensive experience in campaign management and creative coordination for international brands.',
 22, 'GMT-5'),

('Jin Watanabe', 'Data Analyst', '9+ years', 'Philippines',
 ARRAY['Advanced Excel', 'SQL', 'Python', 'Power BI', 'Statistical Analysis'],
 'Senior data analyst with expertise in marketing analytics and business intelligence. Experience with complex data modeling and automated reporting.',
 25, 'GMT+8');

-- Insert common skills
INSERT INTO skills (skill_name, category, is_technical) VALUES
('Excel/Google Sheets (Advanced)', 'Technical', true),
('Shopify Admin Experience', 'Technical', true),
('Google Analytics', 'Technical', true),
('SQL/Database Knowledge', 'Technical', true),
('Project Management', 'Soft Skills', false),
('Data Analysis & Reporting', 'Technical', true),
('Email Marketing', 'Marketing', false),
('Social Media Management', 'Marketing', false),
('Adobe Creative Suite', 'Technical', true),
('Content Creation', 'Creative', false),
('SEO', 'Marketing', true),
('Python/R Programming', 'Technical', true),
('Inventory Management Systems', 'Technical', true),
('Customer Support Tools', 'Technical', true),
('Communication Skills', 'Soft Skills', false);

-- Row Level Security (RLS) - Optional for multi-tenant setup
-- ALTER TABLE market_scans ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE client_requests ENABLE ROW LEVEL SECURITY;

-- Create policy for client access to their own data
-- CREATE POLICY "Clients can view their own market scans" ON market_scans
--     FOR SELECT USING (client_email = current_setting('app.current_user_email'));

COMMENT ON TABLE market_scans IS 'Main table storing market scan requests and analysis results';
COMMENT ON TABLE roles IS 'Role standardization and title mapping data';
COMMENT ON TABLE salary_benchmarks IS 'Regional salary benchmark data by role and experience';
COMMENT ON TABLE candidate_profiles IS 'Example candidate profiles for client reference';
COMMENT ON TABLE historical_scans IS 'Imported historical market scan data for training and analysis';
COMMENT ON TABLE client_requests IS 'Log of all client API requests for analytics and debugging';