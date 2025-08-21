#!/usr/bin/env python3
"""
Extract candidate data from Regional Talent Comparison Master PDF
Uses PyMuPDF (fitz) to extract text and structure candidate profiles
"""

import PyPDF2
import json
import re
from typing import List, Dict, Any

def extract_pdf_text(pdf_path: str) -> str:
    """Extract all text from PDF"""
    try:
        full_text = ""
        
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page_num, page in enumerate(pdf_reader.pages):
                text = page.extract_text()
                full_text += f"\n--- PAGE {page_num + 1} ---\n{text}\n"
        
        return full_text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

def parse_candidate_profiles(text: str) -> List[Dict[str, Any]]:
    """Parse candidate profiles from extracted PDF text"""
    candidates = []
    
    # Split by pages first, then look for "Meet" sections
    pages = text.split('--- PAGE')
    
    for page in pages:
        if 'Meet' in page:
            # Extract name after "Meet"
            name_match = re.search(r'Meet\s+([A-Za-z]+)', page, re.IGNORECASE)
            if name_match:
                name = name_match.group(1).strip()
                candidate = parse_single_candidate(name, page)
                if candidate and candidate['name']:
                    candidates.append(candidate)
    
    return candidates

def parse_single_candidate(name: str, content: str) -> Dict[str, Any]:
    """Parse a single candidate's information"""
    candidate = {
        "name": name,
        "role_category": "",
        "experience_years": "",
        "region": "",
        "country_code": "",
        "skills": [],
        "capabilities": "",
        "monthly_salary_min": None,
        "monthly_salary_max": None,
        "working_hours": "",
        "timezone": "",
        "availability_type": "Full-Time",
        "experience_breakdown": {},
        "tech_stack": {"primary": [], "secondary": []},
        "responsibilities": "",
        "onboarded_date": None,
        "english_proficiency": "Fluent",
        "is_active": True
    }
    
    # Clean up spaced text by removing extra spaces between characters
    clean_content = re.sub(r'(\w)\s+(\w)', r'\1\2', content)
    clean_content = re.sub(r'\s+', ' ', clean_content)
    
    # Extract role category (appears at top)
    role_patterns = [
        r'(CONTENTCREATION&MARKETING|CONTENT CREATION & MARKETING)',
        r'(CREATIVESTRATEGY|CREATIVE STRATEGY)', 
        r'(GRAPHICDESIGN&INFLUENCER|GRAPHIC DESIGN & INFLUENCER)',
        r'(RETENTIONMANAGER|RETENTION MANAGER)',
        r'(MARKETINGSTRATEGY|MARKETING STRATEGY)',
        r'(DIGITALMARKETING|DIGITAL MARKETING)',
        r'(E-COMMERCE|ECOMMERCE)',
        r'(DATAANALYSIS|DATA ANALYSIS)',
        r'(SOCIALMEDIA|SOCIAL MEDIA)',
        r'(PROJECTMANAGEMENT|PROJECT MANAGEMENT)',
        r'(COPYWRITING)',
        r'(SALES)',
        r'(CUSTOMERSUCCESS|CUSTOMER SUCCESS)',
        r'(OPERATIONS)',
        r'(DESIGN)',
        r'(DEVELOPMENT)',
        r'(FINANCE)',
        r'(HR&RECRUITING|HR & RECRUITING)'
    ]
    
    for pattern in role_patterns:
        match = re.search(pattern, clean_content, re.IGNORECASE)
        if match:
            role = match.group(1).replace('&', ' & ').replace('RETENTION', 'Retention ').replace('MANAGER', 'Manager')
            candidate["role_category"] = role.title()
            break
    
    # Extract region - look for common country names
    if 'Argentina' in content:
        candidate["region"] = "Argentina"
        candidate["country_code"] = "ARG"
    elif 'Brazil' in content:
        candidate["region"] = "Brazil"
        candidate["country_code"] = "BRA"
    elif 'SouthAfrica' in clean_content or 'South Africa' in content:
        candidate["region"] = "South Africa"
        candidate["country_code"] = "ZAF"
    elif 'Philippines' in content:
        candidate["region"] = "Philippines"
        candidate["country_code"] = "PHL"
    elif 'Mexico' in content:
        candidate["region"] = "Mexico"
        candidate["country_code"] = "MEX"
    elif 'Colombia' in content:
        candidate["region"] = "Colombia"
        candidate["country_code"] = "COL"
    
    # Extract working hours - look for time pattern
    time_patterns = [
        r'(\d+am-\d+pmEST|\d+ a m - \d+ p m E S T)',
        r'(\d+am-\d+pmPST|\d+ a m - \d+ p m P S T)'
    ]
    
    for pattern in time_patterns:
        match = re.search(pattern, clean_content, re.IGNORECASE)
        if match:
            time_str = match.group(1).replace(' ', '')
            if 'EST' in time_str.upper():
                candidate["working_hours"] = "9am - 5pm EST"
                candidate["timezone"] = "EST"
            elif 'PST' in time_str.upper():
                candidate["working_hours"] = "9am - 5pm PST"
                candidate["timezone"] = "PST"
            break
    
    # Extract monthly salary
    salary_patterns = [
        r'\$(\d{1,3}(?:,\d{3})*)/month',
        r'\$(\d{1,3}(?:,\d{3})*) / month',
        r'\$ (\d{1,3} , \d{3}) / m o n t h'
    ]
    
    for pattern in salary_patterns:
        match = re.search(pattern, content)
        if match:
            salary_str = match.group(1).replace(' ', '').replace(',', '')
            try:
                salary = int(salary_str)
                candidate["monthly_salary_min"] = int(salary * 0.9)
                candidate["monthly_salary_max"] = int(salary * 1.1)
                break
            except ValueError:
                continue
    
    # Extract experience breakdown - look for years + category patterns
    exp_patterns = [
        r'(\d+\+?)\s*Yrs?\s+(Freelancing|FreeLancing)',
        r'(\d+\+?)\s*Yrs?\s+(ContentCreation|Content Creation)',
        r'(\d+\+?)\s*Yrs?\s+(CreativeStrategy|Creative Strategy)',
        r'(\d+\+?)\s*Yrs?\s+(ProductDesign|Product Design)',
        r'(\d+\+?)\s*Yrs?\s+(CommunityManager|Community Manager)',
        r'(\d+\+?)\s*Yrs?\s+(AdobeSuite|Adobe Suite)',
        r'(\d+\+?)\s*Yrs?\s+(eComm|E-Commerce)',
        r'(\d+\+?)\s*Yrs?\s+(BeautyIndustry|Beauty Industry)'
    ]
    
    for pattern in exp_patterns:
        matches = re.findall(pattern, clean_content, re.IGNORECASE)
        for years, category in matches:
            clean_cat = category.lower().replace(' ', '_')
            candidate["experience_breakdown"][clean_cat] = f"{years}+ Yrs"
    
    # Extract capabilities - look for descriptive text
    capability_patterns = [
        r'(Grows?.*?content)',
        r'(\d+ years? of experience.*?)',
        r'(Leads? creative.*?)',
        r'(Creates? visual content.*?)',
        r'(Robust hands-on experience.*?)'
    ]
    
    capabilities = []
    for pattern in capability_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
        capabilities.extend(matches)
    
    if capabilities:
        candidate["capabilities"] = '. '.join(capabilities[:2])  # Take first 2 capabilities
    
    # Extract tech stack - look for tool names
    tech_tools = []
    tools_pattern = r'(Klaviyo|Figma|ChatGPT|CreativeCopywriting|Creative Copywriting|AdobeCreativeSuite|Adobe Creative Suite|Canva|GoogleAnalytics|Google Analytics|SocialMediaManagement|Social Media Management|EmailMarketing|Email Marketing|ABTesting|A/B Testing|SegmentationStrategies|Segmentation Strategies|Notion|SocialMediaTools|Social Media Tools)'
    
    matches = re.findall(tools_pattern, clean_content, re.IGNORECASE)
    for match in matches:
        clean_tool = match.replace('&', ' & ').title()
        if clean_tool not in tech_tools:
            tech_tools.append(clean_tool)
    
    candidate["skills"] = tech_tools
    if len(tech_tools) >= 2:
        candidate["tech_stack"]["primary"] = tech_tools[:2]
        candidate["tech_stack"]["secondary"] = tech_tools[2:] if len(tech_tools) > 2 else []
    else:
        candidate["tech_stack"]["primary"] = tech_tools
    
    return candidate

def main():
    """Extract and process candidate data from PDF"""
    pdf_path = "/Users/joeymuller/Downloads/Regional Talent Comparison Master -- only candidates.pdf"
    
    print("🔍 Extracting text from PDF...")
    full_text = extract_pdf_text(pdf_path)
    
    if not full_text:
        print("❌ Failed to extract PDF text")
        return
    
    print(f"✅ Extracted {len(full_text)} characters from PDF")
    
    # Save raw text for debugging
    with open("raw_pdf_text.txt", "w", encoding="utf-8") as f:
        f.write(full_text)
    print("💾 Saved raw text to raw_pdf_text.txt")
    
    print("🔍 Parsing candidate profiles...")
    candidates = parse_candidate_profiles(full_text)
    
    print(f"✅ Found {len(candidates)} candidate profiles")
    
    # Save structured data
    with open("extracted_candidates.json", "w", encoding="utf-8") as f:
        json.dump(candidates, f, indent=2, ensure_ascii=False)
    
    print("💾 Saved candidate data to extracted_candidates.json")
    
    # Print summary
    print("\n📊 Candidate Summary:")
    for i, candidate in enumerate(candidates, 1):
        print(f"{i}. {candidate['name']} - {candidate['role_category']} - {candidate['region']}")

if __name__ == "__main__":
    main()