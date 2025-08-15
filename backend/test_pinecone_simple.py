#!/usr/bin/env python3
"""
Simple Pinecone connection test for Tidal Streamline
"""

import os
from pinecone import Pinecone, ServerlessSpec

def test_pinecone_connection():
    """Test basic Pinecone connection"""
    print("🧪 Testing Pinecone Connection...")
    
    # Initialize Pinecone
    api_key = "pcsk_2asZaU_4JFVKA6KRDqh2i37Vn8bcWRx5cPhhGDhYcDmcemg3GGpG2m44TPouFMVkEzQqBe"
    index_name = "tidal-streamline"
    
    try:
        pc = Pinecone(api_key=api_key)
        print("✅ Pinecone client initialized successfully")
        
        # Check if index exists
        existing_indexes = pc.list_indexes()
        index_names = [index.name for index in existing_indexes]
        print(f"📋 Existing indexes: {index_names}")
        
        if index_name not in index_names:
            print(f"🔧 Creating index: {index_name}")
            pc.create_index(
                name=index_name,
                dimension=1536,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1")
            )
            print("✅ Index created successfully")
        else:
            print(f"✅ Index '{index_name}' already exists")
            
        # Get index stats
        index = pc.Index(index_name)
        stats = index.describe_index_stats()
        print(f"📊 Index stats: {stats}")
        
        print("\n🎉 Pinecone connection test successful!")
        return True
        
    except Exception as e:
        print(f"❌ Pinecone connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_pinecone_connection()