#!/usr/bin/env python3
"""
Add missing roles to the database
"""

import asyncio
import sys
import os
from datetime import datetime
import uuid

# Add backend directory to path
sys.path.append('/Users/joeymuller/Documents/coding-projects/active-projects/tidal-streamline/backend')

from app.core.database import db

async def add_missing_roles():
    """Add the 4 missing roles to the database"""
    print("🔄 Adding missing roles to database...")
    
    # Test database connection
    try:
        connection_test = await db.test_connection()
        if not connection_test:
            print("❌ Database connection failed")
            return
        print("✅ Database connection: Success")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return
    
    # Define the missing roles
    missing_roles = [
        {
            'id': str(uuid.uuid4()),
            'core_role': 'Demand Planner',
            'common_titles': [
                'Inventory Planner',
                'Supply Planner', 
                'Merchandise Planner',
                'Sales & Operations Planning (S&OP) Analyst',
                'Forecasting Analyst',
                'Planning & Inventory Analyst'
            ],
            'description': 'Plans and forecasts product demand, manages inventory levels and supply planning',
            'category': 'Operations',
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        },
        {
            'id': str(uuid.uuid4()),
            'core_role': 'Product Development Manager',
            'common_titles': [
                'Sourcing Manager',
                'Product Lifecycle Manager',
                'Production Manager',
                'Product Operations Manager'
            ],
            'description': 'Manages product development lifecycle from concept to market launch',
            'category': 'Product',
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        },
        {
            'id': str(uuid.uuid4()),
            'core_role': 'Customer Experience Manager',
            'common_titles': [
                'CX Lead',
                'Customer Success Manager',
                'Customer Experience Specialist',
                'CX Operations Manager'
            ],
            'description': 'Manages customer experience strategy and satisfaction initiatives',
            'category': 'Customer Success',
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        },
        {
            'id': str(uuid.uuid4()),
            'core_role': 'Admin & EA',
            'common_titles': [
                'Administrative Assistant',
                'Executive Assistant',
                'Virtual Assistant',
                'Chief of Staff',
                'Operations Manager'
            ],
            'description': 'Provides administrative and executive support, manages operations and coordination',
            'category': 'Administrative',
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
    ]
    
    # Insert each role
    success_count = 0
    error_count = 0
    
    for role in missing_roles:
        try:
            # Check if role already exists
            existing = await check_role_exists(role['core_role'])
            
            if existing:
                print(f"⚠️  Role already exists: {role['core_role']}")
                continue
            
            # Insert new role
            result = await insert_role(role)
            if result:
                print(f"✅ Added role: {role['core_role']}")
                print(f"   ID: {role['id']}")
                print(f"   Category: {role['category']}")
                print(f"   Common titles: {len(role['common_titles'])} variations")
                success_count += 1
            else:
                print(f"❌ Failed to add role: {role['core_role']}")
                error_count += 1
                
        except Exception as e:
            print(f"❌ Error adding {role['core_role']}: {str(e)}")
            error_count += 1
    
    print(f"\n🎉 Role Addition Complete!")
    print(f"✅ Successfully added: {success_count} roles")
    if error_count > 0:
        print(f"❌ Errors encountered: {error_count} roles")
    
    # Verify total roles in database
    try:
        all_roles = await get_all_roles()
        print(f"\n📊 Total roles in database: {len(all_roles)}")
        print("📋 Complete role list:")
        for i, role in enumerate(all_roles, 1):
            print(f"   {i:2d}. {role.get('core_role', 'Unknown')} ({role.get('category', 'No category')})")
    except Exception as e:
        print(f"❌ Failed to retrieve role summary: {e}")

async def check_role_exists(core_role: str) -> bool:
    """Check if a role already exists in the database"""
    try:
        result = db.client.table('roles').select('id').eq('core_role', core_role).execute()
        return len(result.data) > 0
    except Exception as e:
        print(f"Error checking role existence: {e}")
        return False

async def insert_role(role_data: dict) -> bool:
    """Insert a role into the database"""
    try:
        result = db.client.table('roles').insert(role_data).execute()
        return len(result.data) > 0
    except Exception as e:
        print(f"Error inserting role: {e}")
        return False

async def get_all_roles():
    """Get all roles from database"""
    try:
        result = db.client.table('roles').select('*').order('core_role').execute()
        return result.data
    except Exception as e:
        print(f"Error getting roles: {e}")
        return []

if __name__ == "__main__":
    asyncio.run(add_missing_roles())