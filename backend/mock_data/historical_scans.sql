-- Historical Market Scans Data for Training AI Models
-- Simulating 20 past market scans to build intelligence

INSERT INTO historical_scans (original_scan_id, job_title, job_description, role_category, region, salary_range, skills_required, date_created, client_name, processed) VALUES

-- Historical Data - Brand Marketing Managers
('HS001', 'Brand Marketing Manager - Fitness Apparel', 
 'Leading creative campaigns for premium activewear brand. Managing influencer partnerships and social media strategy.',
 'Brand Marketing Manager', 'Philippines', '$1,700-2,200/month', 
 ARRAY['Creative Direction', 'Influencer Marketing', 'Social Media', 'Adobe Creative Suite'], 
 '2024-01-15', 'ActiveWear Co', false),

('HS002', 'Marketing Project Manager - Beauty Brand',
 'Coordinating marketing campaigns across multiple channels for luxury skincare brand.',
 'Brand Marketing Manager', 'Latin America', '$2,400-2,900/month',
 ARRAY['Project Management', 'Campaign Management', 'Brand Strategy', 'Marketing Automation'],
 '2024-02-03', 'LuxeSkin Beauty', false),

('HS003', 'Creative Marketing Manager - Home Decor',
 'Managing creative projects and brand campaigns for high-end furniture e-commerce.',
 'Brand Marketing Manager', 'South Africa', '$2,800-3,400/month',
 ARRAY['Creative Direction', 'Brand Management', 'E-commerce Marketing', 'Project Management'],
 '2024-01-28', 'ModernHome Design', false),

-- Historical Data - E-commerce Managers  
('HS004', 'Shopify Operations Manager - Pet Products',
 'Managing day-to-day Shopify operations for growing pet accessories brand.',
 'Ecommerce Manager', 'Philippines', '$1,500-1,900/month',
 ARRAY['Shopify Admin', 'Inventory Management', 'Order Processing', 'Customer Service'],
 '2024-02-10', 'PetJoy Products', false),

('HS005', 'E-commerce Manager - Tech Gadgets', 
 'Overseeing online store operations and international expansion for electronics brand.',
 'Ecommerce Manager', 'Latin America', '$2,100-2,700/month',
 ARRAY['Shopify Plus', 'International Shipping', 'Vendor Management', 'Analytics'],
 '2024-01-22', 'TechNova Gadgets', false),

('HS006', 'Digital Commerce Manager - Fashion',
 'Managing multi-platform e-commerce operations for sustainable fashion brand.',
 'Ecommerce Manager', 'South Africa', '$2,600-3,100/month',
 ARRAY['Multi-platform Management', 'Sustainability', 'Fashion Industry', 'Customer Experience'],
 '2024-02-05', 'EcoFashion Hub', false),

-- Historical Data - Data Analysts
('HS007', 'Marketing Data Analyst - SaaS',
 'Analyzing marketing performance and customer acquisition for B2B software company.',
 'Data Analyst', 'Philippines', '$1,300-1,800/month',
 ARRAY['SQL', 'Google Analytics', 'Excel Advanced', 'Marketing Attribution', 'B2B Analytics'],
 '2024-01-18', 'CloudTech Solutions', false),

('HS008', 'Performance Marketing Analyst - E-commerce',
 'Optimizing paid advertising campaigns across multiple channels for D2C brand.',
 'Data Analyst', 'Latin America', '$1,900-2,500/month',
 ARRAY['Facebook Ads', 'Google Ads', 'Attribution Modeling', 'A/B Testing', 'Python'],
 '2024-02-12', 'DirectBrand Co', false),

('HS009', 'Business Intelligence Analyst - Retail',
 'Building dashboards and analyzing sales data for multi-location retail chain.',
 'Data Analyst', 'South Africa', '$2,200-2,800/month',
 ARRAY['Power BI', 'SQL Server', 'Retail Analytics', 'Dashboard Development', 'Statistical Analysis'],
 '2024-01-30', 'RetailMax Stores', false),

-- Historical Data - Content Marketers
('HS010', 'Content Marketing Manager - Wellness',
 'Creating content strategy and managing blog for holistic wellness brand.',
 'Content Marketer', 'Philippines', '$1,200-1,600/month',
 ARRAY['Content Strategy', 'SEO Writing', 'Wellness Industry', 'Email Marketing', 'Social Media'],
 '2024-02-08', 'WellnessWay Brand', false),

('HS011', 'Social Media Content Creator - Beauty',
 'Developing social media content and managing community for clean beauty brand.',
 'Content Marketer', 'Latin America', '$1,600-2,100/month', 
 ARRAY['Social Media Strategy', 'Content Creation', 'Beauty Industry', 'Community Management', 'Influencer Coordination'],
 '2024-01-25', 'CleanGlow Beauty', false),

('HS012', 'Digital Content Manager - Fitness',
 'Managing content across multiple platforms for fitness equipment brand.',
 'Content Marketer', 'South Africa', '$1,900-2,400/month',
 ARRAY['Multi-platform Content', 'Fitness Industry', 'Video Creation', 'Content Calendar', 'Brand Voice'],
 '2024-02-14', 'FitGear Pro', false),

-- Historical Data - Operations Roles
('HS013', 'Customer Success Manager - SaaS',
 'Managing customer onboarding and retention for project management software.',
 'Retention Manager', 'Philippines', '$1,400-1,800/month',
 ARRAY['Customer Success', 'SaaS Industry', 'Onboarding', 'Retention Strategy', 'Technical Support'],
 '2024-01-20', 'ProjectFlow Software', false),

('HS014', 'Email Marketing Specialist - E-commerce',
 'Developing email campaigns and automation flows for fashion e-commerce.',
 'Retention Manager', 'Latin America', '$1,700-2,200/month',
 ARRAY['Email Marketing', 'Klaviyo', 'Automation', 'Fashion Industry', 'Customer Segmentation'],
 '2024-02-01', 'StyleHub Fashion', false),

('HS015', 'Operations Coordinator - Logistics',
 'Coordinating supply chain and fulfillment operations for home goods brand.',
 'Operations Manager', 'South Africa', '$2,400-2,900/month',
 ARRAY['Supply Chain', 'Fulfillment', 'Vendor Coordination', 'Logistics', 'Process Optimization'],
 '2024-01-17', 'HomeComfort Goods', false),

-- Historical Data - Specialized Roles
('HS016', 'Amazon Marketing Specialist - Consumer Goods',
 'Managing Amazon marketplace presence and advertising for consumer products.',
 'Sales Operations Manager', 'Philippines', '$1,500-2,000/month',
 ARRAY['Amazon FBA', 'Amazon Advertising', 'Marketplace Management', 'PPC Optimization', 'Consumer Goods'],
 '2024-02-06', 'EverydayGoods Co', false),

('HS017', 'Community Manager - Gaming',
 'Building and managing online communities for mobile gaming company.',
 'Community Manager', 'Latin America', '$1,800-2,300/month',
 ARRAY['Community Building', 'Gaming Industry', 'Discord Management', 'Social Media', 'Crisis Management'],
 '2024-01-12', 'GameStudio Pro', false),

('HS018', 'Affiliate Marketing Manager - Health',
 'Managing affiliate partnerships and performance tracking for health supplement brand.',
 'Sales Operations Manager', 'South Africa', '$2,200-2,700/month',
 ARRAY['Affiliate Marketing', 'Partnership Management', 'Health Industry', 'Performance Tracking', 'Revenue Operations'],
 '2024-02-09', 'HealthVitality Supplements', false),

('HS019', 'CRM Manager - Financial Services',
 'Managing customer relationship systems and lifecycle marketing for fintech startup.',
 'Retention Manager', 'Philippines', '$1,600-2,100/month',
 ARRAY['CRM Management', 'Fintech', 'Lifecycle Marketing', 'Customer Data', 'Automation'],
 '2024-01-26', 'FinTech Innovations', false),

('HS020', 'Growth Marketing Analyst - Subscription',
 'Analyzing growth metrics and optimizing acquisition for subscription box service.',
 'Data Analyst', 'Latin America', '$2,000-2,600/month',
 ARRAY['Growth Analytics', 'Subscription Models', 'Cohort Analysis', 'Retention Metrics', 'Growth Hacking'],
 '2024-02-11', 'BoxDelight Subscriptions', false);