#!/bin/bash
# Setup environment and populate all 23 candidates
# Run this script after setting your Supabase credentials

echo "🔧 Setting up environment for candidate population..."

# Check if environment variables are set
if [ -z "$SUPABASE_URL" ] || [ -z "$SUPABASE_SERVICE_KEY" ]; then
    echo "❌ Missing Supabase environment variables"
    echo ""
    echo "Please set the following environment variables:"
    echo "export SUPABASE_URL='your_supabase_project_url'"
    echo "export SUPABASE_SERVICE_KEY='your_supabase_service_key'"
    echo ""
    echo "Then run: python3 populate_all_candidates.py"
    exit 1
fi

echo "✅ Environment variables found"
echo "📊 Supabase URL: ${SUPABASE_URL}"
echo "🔑 Service Key: ${SUPABASE_SERVICE_KEY:0:20}..."

# Check if complete_candidates.json exists
if [ ! -f "complete_candidates.json" ]; then
    echo "🔍 Generating complete candidate data..."
    python3 extract_all_candidates.py
fi

echo "🚀 Populating database with all 23 candidates..."
python3 populate_all_candidates.py

echo "✅ Setup complete!"