-- Mock Market Scan Batch from Tidal Client
-- 5 Real-world market scans for testing the complete workflow

-- Batch 1: E-commerce Brand Marketing Manager
INSERT INTO market_scans (
    client_name, client_email, company_domain, job_title, job_description, hiring_challenges,
    status, created_at, processing_time_seconds
) VALUES (
    'Sarah Chen', 'sarah@luxefitness.com', 'luxefitness.com', 
    'Brand Marketing Manager - E-commerce Focus',
    'We are seeking a dynamic Brand Marketing Manager to lead our e-commerce marketing initiatives for our premium fitness apparel brand. This role requires managing creative campaigns across digital channels, coordinating with influencers, and driving brand awareness in the competitive fitness market. Key responsibilities include: campaign strategy development, creative project management, influencer partnership coordination, email marketing automation, social media content planning, and performance tracking. Must have experience with Shopify, Google Analytics, and creative tools like Adobe Creative Suite. Strong project management skills essential as you will coordinate between creative teams, external agencies, and internal stakeholders.',
    'Finding someone with both creative vision and strong project management skills who can work across multiple time zones with our remote team.',
    'completed', NOW() - INTERVAL '2 days', 45.2
);

-- Batch 2: Customer Success & Retention Specialist  
INSERT INTO market_scans (
    client_name, client_email, company_domain, job_title, job_description, hiring_challenges,
    status, created_at, processing_time_seconds
) VALUES (
    'Marcus Rodriguez', 'marcus@petparadise.co', 'petparadise.co',
    'Customer Success & Retention Manager', 
    'Join our growing pet products company as a Customer Success & Retention Manager. You will own the entire customer lifecycle from onboarding to long-term retention. This includes managing our email marketing campaigns, analyzing customer behavior data, implementing retention strategies, and working closely with our customer support team. Technical requirements: Advanced Excel/Google Sheets, experience with email marketing platforms (Klaviyo preferred), basic SQL knowledge for data analysis, and familiarity with customer support tools like Zendesk. You will also coordinate with our warehouse team for order fulfillment issues and work with our marketing team on customer feedback integration.',
    'Need someone who can balance analytical thinking with empathetic customer communication. Previous candidates either had great technical skills but poor communication, or excellent people skills but struggled with data analysis.',
    'completed', NOW() - INTERVAL '1 day', 38.7
);

-- Batch 3: Shopify Operations Manager
INSERT INTO market_scans (
    client_name, client_email, company_domain, job_title, job_description, hiring_challenges,
    status, created_at, processing_time_seconds
) VALUES (
    'Jennifer Park', 'jen@urbanhome.design', 'urbanhome.design',
    'Shopify Operations Manager',
    'We need an experienced Shopify Operations Manager to oversee our home decor e-commerce operations. This role manages day-to-day Shopify store operations, inventory management, order processing optimization, app integrations, and coordination with our 3PL fulfillment partner. Must have deep Shopify admin experience, understanding of inventory management systems, and ability to troubleshoot technical issues. You will also manage our product catalog updates, coordinate with our design team on new product launches, and analyze sales data to optimize product positioning. Experience with Shopify apps like Klaviyo, ReCharge, and inventory management systems required.',
    'Looking for someone with 3+ years of hands-on Shopify experience who can also handle vendor communication and has worked with international shipping logistics.',
    'completed', NOW() - INTERVAL '6 hours', 52.1
);

-- Batch 4: Performance Marketing Data Analyst
INSERT INTO market_scans (
    client_name, client_email, company_domain, job_title, job_description, hiring_challenges,
    status, created_at, processing_time_seconds
) VALUES (
    'David Kim', 'david@techgadgets.store', 'techgadgets.store',
    'Performance Marketing Data Analyst',
    'Seeking a Performance Marketing Data Analyst to join our fast-growing tech accessories brand. You will be responsible for analyzing marketing campaign performance across Facebook Ads, Google Ads, TikTok, and Amazon advertising. Key responsibilities include: building automated reporting dashboards, analyzing customer acquisition costs and lifetime value, A/B testing campaign creatives, tracking attribution across multiple touchpoints, and providing actionable insights to optimize ad spend. Technical requirements: Advanced Excel, SQL for database queries, experience with Google Analytics 4, Facebook Ads Manager, Google Ads, and preferably some Python for data analysis. You will work closely with our paid media team and report directly to the CMO.',
    'Finding someone with strong analytical skills who can also communicate insights clearly to non-technical team members. Need someone comfortable with large datasets and familiar with e-commerce attribution challenges.',
    'completed', NOW() - INTERVAL '3 hours', 41.8
);

-- Batch 5: Content Creator & Social Media Manager
INSERT INTO market_scans (
    client_name, client_email, company_domain, job_title, job_description, hiring_challenges,
    status, created_at, processing_time_seconds
) VALUES (
    'Amanda Foster', 'amanda@greenbeauty.co', 'greenbeauty.co',
    'Content Creator & Social Media Manager',
    'We are looking for a creative Content Creator & Social Media Manager for our sustainable beauty brand. This role involves creating engaging content for Instagram, TikTok, and Pinterest, managing our social media calendar, coordinating with micro-influencers, and developing user-generated content campaigns. You will also write product descriptions, email newsletter content, and blog posts about sustainable beauty practices. Required skills: content creation and editing (photos/videos), social media strategy, basic graphic design, copywriting, and community management. Experience with content creation tools, scheduling platforms, and understanding of beauty industry trends essential.',
    'Need someone who truly understands sustainable beauty and can create authentic content that resonates with our environmentally conscious audience. Previous candidates either lacked industry knowledge or had great creativity but poor strategic thinking.',
    'completed', NOW() - INTERVAL '1 hour', 36.9
);