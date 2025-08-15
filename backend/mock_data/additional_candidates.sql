-- Additional Candidate Profiles for Testing Market Scan Matching
-- 15 more diverse candidates across all regions and roles

INSERT INTO candidate_profiles (name, role_category, experience_years, region, skills, bio, hourly_rate, timezone, availability, english_proficiency) VALUES

-- Philippines Candidates (5 more)
('Ana Reyes', 'Brand Marketing Manager', '5-8 years', 'Philippines',
 ARRAY['Creative Direction', 'Shopify Admin', 'Email Marketing', 'Adobe Creative Suite', 'Project Management', 'Influencer Marketing'],
 'Brand marketing manager with 6 years of experience in fitness and lifestyle brands. Led successful influencer campaigns and managed creative teams across multiple time zones. Expert in Shopify optimization and conversion tracking.',
 22, 'GMT+8', 'Available immediately', 'Native'),

('Miguel Santos', 'Ecommerce Manager', '3-6 years', 'Philippines',
 ARRAY['Shopify Expert', 'Inventory Management', 'Order Processing', 'App Integration', 'Customer Service', 'Data Analysis'],
 'Shopify operations specialist with 4 years managing high-volume e-commerce stores. Experience with 3PL coordination, international shipping, and inventory optimization. Managed stores doing $2M+ annual revenue.',
 18, 'GMT+8', 'Available immediately', 'Fluent'),

('Isabella Cruz', 'Content Marketer', '2-4 years', 'Philippines', 
 ARRAY['Content Creation', 'Video Editing', 'Social Media Strategy', 'Copywriting', 'Pinterest Marketing', 'Instagram Marketing'],
 'Creative content creator specializing in beauty and lifestyle brands. Experience with UGC campaigns, influencer coordination, and sustainable brand messaging. Strong video editing and photography skills.',
 16, 'GMT+8', 'Available in 2 weeks', 'Fluent'),

('Ricardo Dela Cruz', 'Data Analyst', '5-8 years', 'Philippines',
 ARRAY['Advanced SQL', 'Python', 'Google Analytics 4', 'Facebook Ads Analysis', 'Excel Modeling', 'Tableau', 'Statistical Analysis'],
 'Senior marketing data analyst with expertise in e-commerce attribution and customer lifetime value analysis. Built automated reporting systems for multiple D2C brands. Strong background in A/B testing and conversion optimization.',
 28, 'GMT+8', 'Available immediately', 'Native'),

('Grace Bautista', 'Retention Manager', '3-6 years', 'Philippines',
 ARRAY['Email Marketing', 'Klaviyo Expert', 'Customer Segmentation', 'Lifecycle Marketing', 'Data Analysis', 'Customer Support'],
 'Customer retention specialist with proven track record of improving customer LTV. Expert in email marketing automation, customer journey mapping, and retention strategy development. Experience with pet and beauty brands.',
 20, 'GMT+8', 'Available immediately', 'Fluent'),

-- Latin America Candidates (5 more)
('Diego Morales', 'Brand Marketing Manager', '9+ years', 'Latin America',
 ARRAY['Campaign Strategy', 'Team Leadership', 'Brand Development', 'Market Research', 'Adobe Creative Suite', 'Marketing Automation'],
 'Senior brand marketing manager with 10+ years leading marketing teams for international e-commerce brands. Specializes in market entry strategies and cross-cultural brand development. Fluent in English, Spanish, and Portuguese.',
 32, 'GMT-3', 'Available in 1 month', 'Native'),

('Valentina Rodriguez', 'Data Analyst', '2-4 years', 'Latin America',
 ARRAY['Google Analytics', 'SQL', 'Facebook Ads', 'Google Ads', 'Excel Advanced', 'Data Visualization', 'A/B Testing'],
 'Performance marketing analyst with strong background in paid advertising analysis. Experience with tech and gadget e-commerce brands. Specialized in attribution modeling and campaign optimization.',
 21, 'GMT-5', 'Available immediately', 'Fluent'),

('Alejandro Gutierrez', 'Sales Operations Manager', '5-8 years', 'Latin America',
 ARRAY['Operations Management', 'Process Optimization', 'Team Coordination', 'Vendor Management', 'Logistics', 'Amazon FBA'],
 'Operations manager with extensive experience in e-commerce fulfillment and vendor coordination. Managed international supply chains and optimized order processing workflows. Strong in vendor negotiations.',
 26, 'GMT-6', 'Available in 2 weeks', 'Fluent'),

('Camila Silva', 'Content Marketer', '3-6 years', 'Latin America',
 ARRAY['Content Strategy', 'SEO Writing', 'Blog Management', 'Email Copywriting', 'Social Media', 'Beauty Industry Knowledge'],
 'Content strategist with deep knowledge of beauty and wellness industries. Experience creating educational content for sustainable brands. Strong background in SEO and email marketing copywriting.',
 19, 'GMT-3', 'Available immediately', 'Native'),

('Sebastian Torres', 'Ecommerce Manager', '5-8 years', 'Latin America',
 ARRAY['Shopify Plus', 'Team Management', 'International Expansion', 'Payment Processing', 'Customer Experience', 'Analytics'],
 'Senior e-commerce manager with experience scaling D2C brands internationally. Led teams managing multi-million dollar Shopify stores. Expert in payment processing, international shipping, and customer experience optimization.',
 29, 'GMT-4', 'Available in 3 weeks', 'Fluent'),

-- South Africa Candidates (5 more)  
('Nomsa Mbeki', 'Brand Marketing Manager', '3-6 years', 'South Africa',
 ARRAY['Brand Strategy', 'Creative Campaigns', 'Digital Marketing', 'Project Management', 'Market Analysis', 'Team Leadership'],
 'Brand marketing professional with experience in fitness and lifestyle sectors. Led successful product launch campaigns and brand repositioning projects. Strong background in African market dynamics and consumer behavior.',
 24, 'GMT+2', 'Available immediately', 'Native'),

('Thabo Mthembu', 'Data Analyst', '9+ years', 'South Africa',
 ARRAY['Advanced Analytics', 'SQL Server', 'Python', 'R', 'Business Intelligence', 'Machine Learning', 'Statistical Modeling'],
 'Senior data scientist with expertise in customer analytics and predictive modeling. Built machine learning models for customer churn prediction and lifetime value optimization. PhD in Statistics with industry focus.',
 35, 'GMT+2', 'Available in 1 month', 'Native'),

('Lerato Nkomo', 'Community Manager', '2-4 years', 'South Africa',
 ARRAY['Social Media Management', 'Community Building', 'Customer Support', 'Content Moderation', 'Influencer Relations', 'Crisis Management'],
 'Community manager with strong background in building engaged online communities. Experience with beauty and wellness brands. Excellent at managing customer relationships and handling sensitive communications.',
 17, 'GMT+2', 'Available immediately', 'Native'),

('Sipho Ndlovu', 'Operations Manager', '5-8 years', 'South Africa', 
 ARRAY['Supply Chain Management', 'Logistics Coordination', 'Vendor Relations', 'Quality Control', 'Process Improvement', 'Team Management'],
 'Operations manager with extensive supply chain and logistics experience. Managed complex fulfillment operations for African and European markets. Strong in process optimization and vendor relationship management.',
 27, 'GMT+2', 'Available in 2 weeks', 'Fluent'),

('Zandi Dlamini', 'Content Marketer', '5-8 years', 'South Africa',
 ARRAY['Content Strategy', 'Brand Storytelling', 'Video Production', 'Social Impact Marketing', 'Sustainable Brands', 'Market Research'],
 'Senior content strategist specializing in purpose-driven and sustainable brands. Experience creating authentic brand narratives that resonate with socially conscious consumers. Strong video production and storytelling skills.',
 25, 'GMT+2', 'Available immediately', 'Native');