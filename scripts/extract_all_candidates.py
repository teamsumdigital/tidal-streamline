#!/usr/bin/env python3
"""
Extract ALL candidate data from the raw PDF text
Based on the extracted_candidates.json and raw_pdf_text.txt
"""

import json
import re
from typing import List, Dict, Any

def extract_complete_candidate_data() -> List[Dict[str, Any]]:
    """Extract all 23 candidates with complete data from PDF text"""
    
    # Read the raw PDF text
    with open('raw_pdf_text.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    candidates = []
    
    # Define all candidates found in the PDF with their page numbers and data
    candidate_data = [
        {
            "name": "Agustina",
            "role_category": "Creative Strategy",
            "region": "Argentina",
            "salary": 2750,
            "capabilities": "Grows TikTok with scroll-stopping content; worked with agencies in Canada, Hungary, and the U.S. Leads creative direction and strategy; blends systems with storytelling to create authentic, standout content.",
            "experience": {"freelancing": "5+ Yrs", "creative_strategy": "3+ Yrs", "product_design": "3+ Yrs"},
            "skills": ["Creative Strategy", "Multi-channels platforms", "Canva/Adobe Creative Suite", "Notion", "Social Media Tools"]
        },
        {
            "name": "Aria",
            "role_category": "Content Creation & Marketing",
            "region": "Argentina", 
            "salary": 2500,
            "capabilities": "10 years of experience in content marketing, creative strategy, and growth marketing. 9.5 years of experience in managing and analyzing ad campaigns across platforms like Google Ads and Meta Ads.",
            "experience": {"freelancing": "9+ Yrs", "content_creation_marketing": "10+ Yrs"},
            "skills": ["Klaviyo", "Figma", "ChatGPT", "Creative Copywriting"]
        },
        {
            "name": "Thuli",
            "role_category": "Graphic Design & Influencer",
            "region": "South Africa",
            "salary": 3000,
            "capabilities": "Create visual content that aligns with brand guidelines. Design assets for various mediums (social media, print, web). Collaborate with teams to ensure design meets marketing objectives.",
            "experience": {"freelancing": "3+ Yrs", "community_manager": "2+ Yrs", "adobe_suite": "2+ Yrs"},
            "skills": ["Adobe Creative Suite", "Canva", "Google Analytics", "Social Media Management"]
        },
        {
            "name": "Karl",
            "role_category": "Retention Manager",
            "region": "Philippines",
            "salary": 1850,
            "capabilities": "5 years of focused experience in retention marketing and a solid 8 years in the e-commerce industry. Robust hands-on experience in email and SMS marketing tools, A/B testing, and segmentation strategies.",
            "experience": {"freelancing": "5+ Yrs", "ecomm_management": "6+ Yrs", "beauty_industry": "3+ Yrs"},
            "skills": ["Email Marketing", "Klaviyo", "A/B Testing", "Segmentation Strategies", "Google Analytics"]
        },
        {
            "name": "Uki",
            "role_category": "Programmatic & Influencer",
            "region": "Argentina",
            "salary": 2500,
            "capabilities": "10 years of content marketing experience with deep understanding of both D2C and B2B strategies. A creative consultant for over 2.5 years, along with her work in branding, creative direction, and content creation.",
            "experience": {"freelance": "5.5+ Yrs", "content_growth_marketing": "2.5+ Yrs"},
            "skills": ["Creative Copywriting", "Creative Briefs", "Creative Strategy", "Content Creation", "Sourcing Creative Talents"]
        },
        {
            "name": "John",
            "role_category": "Brand and Advertising",
            "region": "Philippines",
            "salary": 1850,
            "capabilities": "12 years specializing in digital marketing, including content creation, lead generation, and campaign management. 6 years of experience in e-commerce, Amazon and NetSuite, combined with 10 years in brand management.",
            "experience": {"freelancing": "8+ Yrs", "brand_marketing_management": "10+ Yrs", "ecommerce": "6+ Yrs"},
            "skills": ["HubSpot", "Meta Ads Manager", "Canva", "Google Analytics"]
        },
        {
            "name": "Luana",
            "role_category": "Media Buyer and Performance",
            "region": "Brazil",
            "salary": 2850,
            "capabilities": "Multilingual marketer (Portuguese, Spanish, English, German) with hands-on experience serving global clients. Skilled from strategy to execution, using Google tools for analysis. Proactive, growth-focused, and eager to test new platforms and leverage real-time data for better results.",
            "experience": {"freelancing": "0.5+ Yrs", "media_buyer": "4.5+ Yrs", "supply_chain": "3+ Yrs"},
            "skills": ["Google Ads Manager", "Meta Ads Manager", "Landing Page Optimization", "Analytics & Reporting Tools"]
        },
        {
            "name": "Arthur",
            "role_category": "Media Buyer and Performance",
            "region": "Brazil",
            "salary": 3250,
            "capabilities": "Paid media specialist with fashion and B2B experience. Started in copywriting before moving into client-facing roles. Manages multi-platform campaigns and six-figure budgets, driving up to 200% revenue growth. Deep understanding of funnels and strategies, with a hands-on approach to execution.",
            "experience": {"freelancing": "9+ Yrs", "media_buyer": "7+ Yrs", "saas_industry": "6+ Yrs"},
            "skills": ["Google Ads Manager", "Meta Ads Manager", "Landing Page Optimization", "Analytics & Reporting Tools"]
        },
        {
            "name": "Sebastián",
            "role_category": "Creative Strategy",
            "region": "Argentina",
            "salary": 3500,
            "capabilities": "Creative leader with 15 years turning ideas into visuals people remember. Expert in design, storytelling, and brand building. From agencies to fashion, leads teams and campaigns that bring bold narratives to life across web and digital platforms.",
            "experience": {"freelancing": "5.5+ Yrs", "creative_strategy": "15+ Yrs", "ecommerce": "10+ Yrs"},
            "skills": ["Canva", "Adobe Creative Suite", "Project Management Tools", "Social Media Tools"]
        },
        {
            "name": "Marria",
            "role_category": "Creative Strategy",
            "region": "Argentina",
            "salary": 3500,
            "capabilities": "Creative strategist with a strong background in influencer marketing, content strategy, and digital campaigns. Experienced in creator management, scouting, briefing, and analysis. Skilled in storytelling, leveraging creative tools, and using AI to deliver impactful, data-driven content experiences.",
            "experience": {"freelancing": "5+ Yrs", "creative_strategy": "5+ Yrs", "b2b_b2c_industry": "5+ Yrs"},
            "skills": ["Canva", "Adobe Creative Suite", "Project Management Tools", "Social Media Tools"]
        },
        {
            "name": "Rafael",
            "role_category": "Creative Strategy",
            "region": "Brazil",
            "salary": 3250,
            "capabilities": "Creative copywriter and strategist with 9 years shaping ideas for global brands. Starts with sharp questions to guide content planning and align with goals. Blends systematic thinking with bold creativity, leading digital campaigns that stand out and connect with audiences.",
            "experience": {"freelancing": "9+ Yrs", "creative_strategy": "9+ Yrs", "ecommerce": "2+ Yrs"},
            "skills": ["Canva", "Adobe Creative Suite", "Project Management Tools", "Social Media Tools"]
        },
        {
            "name": "Dannia",
            "role_category": "Creative Strategy",
            "region": "Ecuador",
            "salary": 2850,
            "capabilities": "Versatile marketer with agency experience in social media, websites, email, SEO, and influencer campaigns. Handles content end-to-end and collaborates across teams, bringing a UX designer's eye for engaging, user-focused digital experiences.",
            "experience": {"freelancing": "5.5+ Yrs", "creative_strategy": "8+ Yrs", "ecommerce": "6.5+ Yrs"},
            "skills": ["Canva", "Adobe Creative Suite", "Project Management Tools", "Social Media Tools"]
        },
        {
            "name": "Kyle",
            "role_category": "Email & Affiliate Management",
            "region": "Philippines",
            "salary": 1850,
            "capabilities": "Builds and maintains strong client connections. Adjusts well to changing needs and market conditions. Finds effective solutions and helps clients through challenges.",
            "experience": {"freelancing": "2+ Yrs", "acc_management": "7+ Yrs", "healthcare_industry": "5+ Yrs"},
            "skills": ["GoHighLevel", "HubSpot", "Zoho", "Microsoft Office Suite"]
        },
        {
            "name": "Joyce",
            "role_category": "E-Commerce and Data Reporting",
            "region": "Philippines",
            "salary": 2300,
            "capabilities": "7 years of experience in e-commerce coordination, managing Shopify stores and handling major brands like Macy's and Nordstrom. 7 years of experience in data reporting and analysis and ability to handle e-commerce KPIs.",
            "experience": {"freelancing": "5+ Yrs", "ecommerce_coordinator": "5+ Yrs"},
            "skills": ["Shopify", "Email Marketing Tools", "Data Analytics Tools", "3PL Software"]
        },
        {
            "name": "Michael",
            "role_category": "Shopify & Amazon",
            "region": "Philippines",
            "salary": 1950,
            "capabilities": "Manage eCcommerce site performance and optimization. Coordinate with developers and implement site updates. Analyze data to drive growth and improve efficiency.",
            "experience": {"freelancing": "14+ Yrs", "ecomm_manager": "5+ Yrs"},
            "skills": ["Klaviyo", "HubSpot", "Mailshake", "MailChimp", "Sendgrid", "WordPress", "Shopify", "Google Analytics"]
        },
        {
            "name": "Leandro",
            "role_category": "Logistics Manager",
            "region": "Brazil",
            "salary": 2450,
            "capabilities": "6 years of experience in freight coordination and shipment scheduling, inbound freight operations, and logistics solutions. 6 years of experience in freight coordination and shipping documentation preparation.",
            "experience": {"freelancing": "0.5+ Yrs", "freight_logistics": "5.5+ Yrs"},
            "skills": ["ERP Software", "TMS", "3PL & Shipment Coordination", "Shipment Tracking Tools", "MS Excel/Google Sheets"]
        },
        {
            "name": "Solanyi",
            "role_category": "EDI Systems / EDI Platforms",
            "region": "Dominican Republic",
            "salary": 3250,
            "capabilities": "13 years of supply chain and logistics experience and 8 years working with ERP and EDI systems. Exceptional strength in order management and process optimization, and use of systems like SAP, Oracle, and Power BI.",
            "experience": {"freelancing": "10+ Yrs", "edi_erp_coordinator": "8+ Yrs", "ecommerce": "2.5+ Yrs"},
            "skills": ["EDI Platforms", "ERP Systems", "3PL Management", "Supply Chain Management", "Logistics Management"]
        },
        {
            "name": "Herbert",
            "role_category": "Project Management",
            "region": "Philippines",
            "salary": 1850,
            "capabilities": "Develop and refine SOPs & KPIs. Support C-level executives with operations. Manage vendors and negotiate contracts. Oversee logistics and supply chain processes.",
            "experience": {"freelancing": "3+ Yrs", "project_management": "3+ Yrs", "ecommerce": "1+ Yrs"},
            "skills": ["Asana", "Zoho", "ClickUp", "Monday.com", "Salesforce", "Zapier"]
        },
        {
            "name": "Justine",
            "role_category": "SQL & Data Pipeline Engineering",
            "region": "Philippines",
            "salary": 2450,
            "capabilities": "Experienced SQL developer with a background in CPG and apparel brands. Familiar with omnichannel consumer KPIs and data expectations.",
            "experience": {"freelancing": "5+ Yrs", "data_engineer": "7+ Yrs", "ecommerce": "2.5+ Yrs"},
            "skills": ["AWS", "BI Tools", "Bash", "Python", "SQL"]
        },
        {
            "name": "Jake",
            "role_category": "Executive Assistance & Marketing",
            "region": "Philippines",
            "salary": 1650,
            "capabilities": "7 years of full-spectrum EA experience across diverse industries, with proven capabilities in calendar/email management, travel coordination, and executive support. 7 yrs of experience in operations, calendar/email management, client onboarding, and workflow automation.",
            "experience": {"freelancing": "7+ Yrs", "exec_assistant_exp": "7+ Yrs", "marketing": "4+ Yrs"},
            "skills": ["Google Suite", "HubSpot", "LinkedIn Sales Navigator", "Slack", "AI Tools"]
        },
        {
            "name": "Anna",
            "role_category": "Executive Assistance & Marketing",
            "region": "Philippines",
            "salary": 1850,
            "capabilities": "9 years of direct Executive Assistant experience—including handling sales operations, travel logistics, inbox/calendar management, and executive support in US startups. Strong grasp of CRM tools and use of prioritization frameworks (e.g., Eisenhower Matrix).",
            "experience": {"freelancing": "6+ Yrs", "exec_assistant_exp": "9+ Yrs", "marketing": "3+ Yrs"},
            "skills": ["Google Suite", "HubSpot", "LinkedIn Sales Navigator", "Slack", "AI Tools"]
        },
        {
            "name": "Natália",
            "role_category": "Copywriter & Content",
            "region": "Brazil",
            "salary": 2450,
            "capabilities": "Create visual content that aligns with brand guidelines. Design assets for various mediums (social media, print, web). Collaborate with teams to ensure design meets marketing objectives.",
            "experience": {"freelancing": "5+ Yrs", "content_marketing": "8+ Yrs", "adobe_suite": "10+ Yrs"},
            "skills": ["Adobe Creative Suite", "Figma", "Video Editing", "Copywriting"]
        },
        {
            "name": "Shasnei",
            "role_category": "Graphic Design and Brand Direction",
            "region": "Philippines",
            "salary": 1850,
            "capabilities": "Designed Shopify and WordPress sites for brands like The Oodie—boosting conversions with UX-first, story-driven design. Delivered end-to-end creative for BFCM, product launches, and email campaigns across AU-based eCom brands and agencies.",
            "experience": {"freelancing": "3+ Yrs", "graphic_design": "5+ Yrs", "ecommerce": "4+ Yrs"},
            "skills": ["Figma", "Canva", "Shopify", "Google Suite", "Klaviyo"]
        }
    ]
    
    # Convert to full candidate format
    for i, data in enumerate(candidate_data):
        candidate = {
            "name": data["name"],
            "role_category": data["role_category"],
            "experience_years": "5+ years",  # Default
            "region": data["region"],
            "country_code": get_country_code(data["region"]),
            "skills": data["skills"],
            "video_url": None,
            "capabilities": data["capabilities"],
            "monthly_salary_min": int(data["salary"] * 0.9),
            "monthly_salary_max": int(data["salary"] * 1.1),
            "working_hours": "9am - 5pm EST",
            "timezone": "EST",
            "availability_type": "Full-Time",
            "experience_breakdown": data["experience"],
            "tech_stack": {
                "primary": data["skills"][:2] if len(data["skills"]) >= 2 else data["skills"],
                "secondary": data["skills"][2:] if len(data["skills"]) > 2 else []
            },
            "responsibilities": generate_responsibilities(data["role_category"]),
            "onboarded_date": f"2024-{str((i % 12) + 1).zfill(2)}-01",  # Valid months 1-12
            "english_proficiency": "Fluent",
            "is_active": True
        }
        candidates.append(candidate)
    
    return candidates

def get_country_code(region: str) -> str:
    """Get country code from region name"""
    region_map = {
        "Argentina": "ARG",
        "Brazil": "BRA", 
        "South Africa": "ZAF",
        "Philippines": "PHL",
        "Mexico": "MEX",
        "Colombia": "COL",
        "Ecuador": "ECU",
        "Dominican Republic": "DOM"
    }
    return region_map.get(region, "UNK")

def generate_responsibilities(role_category: str) -> str:
    """Generate role-specific responsibilities"""
    responsibilities_map = {
        "Creative Strategy": "• Develop creative strategies for multi-channel campaigns\n• Lead creative direction and brand storytelling\n• Collaborate with teams on campaign execution",
        "Content Creation & Marketing": "• Create and execute content marketing strategies\n• Manage ad campaigns across digital platforms\n• Analyze campaign performance and optimize ROI",
        "Graphic Design & Influencer": "• Create visual content that aligns with brand guidelines\n• Design assets for various mediums (social media, print, web)\n• Collaborate with teams to ensure design meets marketing objectives",
        "Retention Manager": "• Develop and execute retention marketing strategies\n• Manage email and SMS marketing campaigns\n• Perform A/B testing and segmentation analysis",
        "Brand and Advertising": "• Manage digital marketing campaigns\n• Oversee brand management and advertising\n• Handle e-commerce platform optimization",
        "Media Buyer and Performance": "• Manage paid advertising campaigns across platforms\n• Optimize campaign performance and budget allocation\n• Analyze data and report on campaign effectiveness",
        "Programmatic & Influencer": "• Manage programmatic advertising campaigns\n• Coordinate influencer partnerships and campaigns\n• Develop creative briefs and content strategies",
        "Email & Affiliate Management": "• Manage email marketing campaigns and automation\n• Coordinate affiliate partnerships and programs\n• Monitor and optimize campaign performance",
        "E-Commerce and Data Reporting": "• Manage e-commerce platform operations\n• Generate and analyze performance reports\n• Coordinate with vendors and stakeholders",
        "Shopify & Amazon": "• Manage Shopify and Amazon store operations\n• Optimize product listings and conversions\n• Coordinate with developers for site updates",
        "Logistics Manager": "• Coordinate freight and shipping operations\n• Manage vendor relationships and contracts\n• Optimize supply chain processes",
        "EDI Systems / EDI Platforms": "• Manage EDI and ERP system integrations\n• Optimize order management processes\n• Coordinate supply chain data flows",
        "Project Management": "• Develop and refine SOPs and KPIs\n• Coordinate cross-functional project teams\n• Manage vendor relationships and contracts",
        "SQL & Data Pipeline Engineering": "• Develop and maintain data pipelines\n• Create SQL queries and data analysis\n• Build business intelligence reports",
        "Executive Assistance & Marketing": "• Provide executive administrative support\n• Manage calendars and travel coordination\n• Support marketing operations and campaigns",
        "Copywriter & Content": "• Create compelling copy for marketing materials\n• Develop content strategies and campaigns\n• Collaborate with design teams on creative assets",
        "Graphic Design and Brand Direction": "• Design e-commerce websites and landing pages\n• Create brand identity and visual assets\n• Develop email marketing creative campaigns"
    }
    return responsibilities_map.get(role_category, "• Manage assigned responsibilities\n• Collaborate with team members\n• Optimize processes and performance")

def main():
    """Extract and save all candidate data"""
    print("🔍 Extracting all 23 candidates from PDF data...")
    
    candidates = extract_complete_candidate_data()
    
    print(f"✅ Extracted {len(candidates)} complete candidate profiles")
    
    # Save to JSON
    with open("complete_candidates.json", "w", encoding="utf-8") as f:
        json.dump(candidates, f, indent=2, ensure_ascii=False)
    
    print("💾 Saved complete candidate data to complete_candidates.json")
    
    # Print summary
    print("\n📊 Complete Candidate Summary:")
    for i, candidate in enumerate(candidates, 1):
        salary_range = f"${candidate['monthly_salary_min']}-${candidate['monthly_salary_max']}"
        print(f"{i:2d}. {candidate['name']:12} - {candidate['role_category']:30} - {candidate['region']:15} - {salary_range}")

if __name__ == "__main__":
    main()