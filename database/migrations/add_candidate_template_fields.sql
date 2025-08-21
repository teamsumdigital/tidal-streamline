-- Migration: Add fields needed for template variable export
-- Date: 2025-01-18
-- Purpose: Support 45+ candidate template variables for Canva integration

-- Add missing critical fields for template variables
ALTER TABLE candidate_profiles 
-- Note: video_url already exists in schema, keeping for reference
ADD COLUMN IF NOT EXISTS capabilities TEXT,
ADD COLUMN IF NOT EXISTS monthly_salary_min INTEGER,
ADD COLUMN IF NOT EXISTS monthly_salary_max INTEGER,
ADD COLUMN IF NOT EXISTS working_hours VARCHAR(50),
ADD COLUMN IF NOT EXISTS tech_stack JSONB,
ADD COLUMN IF NOT EXISTS experience_breakdown JSONB,
ADD COLUMN IF NOT EXISTS onboarded_date DATE,
ADD COLUMN IF NOT EXISTS availability_type VARCHAR(20) DEFAULT 'Full-Time',
ADD COLUMN IF NOT EXISTS country_code VARCHAR(3),
ADD COLUMN IF NOT EXISTS responsibilities TEXT;

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_candidate_monthly_salary ON candidate_profiles (monthly_salary_min, monthly_salary_max);
CREATE INDEX IF NOT EXISTS idx_candidate_country ON candidate_profiles (country_code);
CREATE INDEX IF NOT EXISTS idx_candidate_availability_type ON candidate_profiles (availability_type);

-- Update existing data with sample values (update these with real data)
UPDATE candidate_profiles SET 
  availability_type = 'Full-Time',
  working_hours = CASE 
    WHEN timezone = 'EST' THEN '9am - 5pm EST'
    WHEN timezone = 'PST' THEN '9am - 5pm PST'  
    ELSE '9am - 5pm ' || COALESCE(timezone, 'UTC')
  END,
  country_code = CASE 
    WHEN region ILIKE '%argentina%' THEN 'ARG'
    WHEN region ILIKE '%brazil%' THEN 'BRA'
    WHEN region ILIKE '%south africa%' THEN 'ZAF'
    WHEN region ILIKE '%philippines%' THEN 'PHL'
    WHEN region ILIKE '%mexico%' THEN 'MEX'
    WHEN region ILIKE '%colombia%' THEN 'COL'
    ELSE 'UNK'
  END
WHERE capabilities IS NULL;

-- Add comments for documentation  
COMMENT ON COLUMN candidate_profiles.video_url IS 'Video profile URL for template display (will be uploaded to CDN separately)';
COMMENT ON COLUMN candidate_profiles.capabilities IS 'Detailed capabilities description for template bio section';
COMMENT ON COLUMN candidate_profiles.monthly_salary_min IS 'Minimum monthly salary in USD for template salary ranges';
COMMENT ON COLUMN candidate_profiles.monthly_salary_max IS 'Maximum monthly salary in USD for template salary ranges';
COMMENT ON COLUMN candidate_profiles.working_hours IS 'Formatted working hours display for templates (e.g., "9am - 5pm EST")';
COMMENT ON COLUMN candidate_profiles.tech_stack IS 'Structured tech skills grouped for template display {"primary": ["tool1"], "secondary": ["tool2"]}';
COMMENT ON COLUMN candidate_profiles.experience_breakdown IS 'Experience by category {"freelancing": "9+ Yrs", "marketing": "10+ Yrs"}';
COMMENT ON COLUMN candidate_profiles.onboarded_date IS 'Date when candidate joined Tidal talent pool';
COMMENT ON COLUMN candidate_profiles.availability_type IS 'Full-Time, Part-Time, or Contract availability';
COMMENT ON COLUMN candidate_profiles.country_code IS 'ISO country code for flag display in templates';
COMMENT ON COLUMN candidate_profiles.responsibilities IS 'Key responsibilities bullets for role display in templates';