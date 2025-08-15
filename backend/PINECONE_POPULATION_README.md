# Pinecone Historical Data Population Guide

This guide explains how to populate your Pinecone vector index with existing historical market scan data from the Tidal Streamline database.

## Overview

The system consists of three main scripts:

1. **`scripts/setup_pinecone_index.py`** - Creates and manages the Pinecone index
2. **`populate_pinecone_historical.py`** - Populates the index with historical data
3. **`manage_pinecone_data.py`** - Utility for checking status and running tests

## Prerequisites

1. **Environment Variables**: Ensure your `.env` file contains:
   ```env
   SUPABASE_URL=your_supabase_url
   SUPABASE_SERVICE_KEY=your_service_key
   OPENAI_API_KEY=your_openai_key
   PINECONE_API_KEY=your_pinecone_key
   PINECONE_INDEX_NAME=tidal-streamline
   ```

2. **Dependencies**: Install required packages:
   ```bash
   pip install supabase openai pinecone-client loguru
   ```

## Step-by-Step Setup

### Step 1: Check Current Status

First, check the current state of your system:

```bash
python manage_pinecone_data.py status
```

This will show:
- Database statistics (total scans, completed scans, etc.)
- Pinecone index status
- Sync status between database and Pinecone
- Recommendations for next steps

### Step 2: Create Pinecone Index (if needed)

If the index doesn't exist, create it:

```bash
# Create new index
python scripts/setup_pinecone_index.py --create

# Or force recreate if it exists
python scripts/setup_pinecone_index.py --force-recreate
```

Other index management commands:
```bash
# Get index information
python scripts/setup_pinecone_index.py --info

# Verify index is working
python scripts/setup_pinecone_index.py --verify

# Delete index (DANGEROUS!)
python scripts/setup_pinecone_index.py --delete
```

### Step 3: Run System Test

Verify everything is working before population:

```bash
python manage_pinecone_data.py test
```

This tests:
- Database connection
- Pinecone connection
- Embedding generation

### Step 4: Populate Historical Data

Now populate the index with historical data:

```bash
# Standard population
python populate_pinecone_historical.py

# Dry run to see what would happen (recommended first)
python populate_pinecone_historical.py --dry-run

# With custom batch size
python populate_pinecone_historical.py --batch-size 100

# Resume from a specific scan ID (if previous run failed)
python populate_pinecone_historical.py --resume-from SCAN_ID_HERE

# With verification after completion
python populate_pinecone_historical.py --verify
```

## Population Script Features

### Batch Processing
- Processes scans in batches (default: 50 per batch)
- Prevents memory issues with large datasets
- Includes progress tracking and rate limiting

### Error Handling & Recovery
- Validates data before processing
- Skips invalid or incomplete scans
- Tracks failed scan IDs for debugging
- Supports resuming from specific scan IDs
- Comprehensive logging to file and console

### Data Validation
- Ensures required fields exist (id, job_title, job_description)
- Validates minimum content length
- Handles malformed JSON in job_analysis
- Gracefully skips problematic records

### Progress Tracking
The script provides detailed progress information:
```
Processing batch 1/50 (50 scans)
Progress: 50/2,500 (2.0%) - Successful: 48, Failed: 1, Skipped: 1
```

### Final Statistics
After completion, you'll see comprehensive statistics:
```
📊 FINAL RESULTS
==========================================
Total Scans Found: 2,500
Scans Processed: 2,500
Successfully Uploaded: 2,450
Failed: 25
Skipped: 25
Processing Time: 0:15:30
Processing Rate: 2.63 scans/second
Success Rate: 98.0%
```

## Verification

### Automatic Verification
Use the `--verify` flag to automatically check a sample of uploaded vectors:

```bash
python populate_pinecone_historical.py --verify
```

### Manual Verification
Check the results manually:

```bash
# Get current status
python manage_pinecone_data.py status

# Get index statistics
python scripts/setup_pinecone_index.py --info
```

## Troubleshooting

### Common Issues

1. **"Index does not exist"**
   ```bash
   python scripts/setup_pinecone_index.py --create
   ```

2. **"Database connection failed"**
   - Check SUPABASE_URL and SUPABASE_SERVICE_KEY in .env
   - Verify Supabase project is active

3. **"Pinecone connection failed"**
   - Check PINECONE_API_KEY in .env
   - Verify Pinecone account has available quota

4. **"OpenAI API rate limit exceeded"**
   - The script includes rate limiting, but you may need to reduce batch size:
   ```bash
   python populate_pinecone_historical.py --batch-size 25
   ```

5. **"Out of memory"**
   - Reduce batch size:
   ```bash
   python populate_pinecone_historical.py --batch-size 20
   ```

### Resume from Failures

If the script fails partway through, you can resume from the last successful scan:

1. Find the last successfully processed scan ID from the logs
2. Resume from that point:
   ```bash
   python populate_pinecone_historical.py --resume-from LAST_SUCCESSFUL_SCAN_ID
   ```

### Logs

All operations are logged to:
- Console output with timestamps
- `logs/populate_pinecone_historical.log` (detailed)
- `logs/pinecone_setup.log` (index operations)

## Advanced Usage

### Custom Configuration

You can modify the embedding and indexing behavior by editing the configuration in:
- `app/core/config.py` - General settings
- `app/services/embedding_service.py` - Embedding parameters

### Filtering Data

To populate only specific types of scans, modify the query in `get_all_market_scans()` method:

```python
# Example: Only completed scans from last year
query = (
    self.db.client
    .table('market_scans')
    .select('*')
    .eq('status', 'completed')
    .gte('created_at', '2023-01-01')
    .order('created_at', desc=False)
)
```

### Monitoring Progress

For long-running operations, you can monitor progress by:

1. **Watching the log file:**
   ```bash
   tail -f logs/populate_pinecone_historical.log
   ```

2. **Checking Pinecone index stats:**
   ```bash
   # In another terminal
   python scripts/setup_pinecone_index.py --info
   ```

## Performance Expectations

Based on typical API limits:

- **OpenAI Embeddings**: ~500-1000 requests/minute
- **Pinecone Upserts**: ~100-200 vectors/second
- **Expected Rate**: 1-3 scans/second with batch_size=50

For 10,000 scans: ~1-3 hours
For 100,000 scans: ~10-30 hours

## Best Practices

1. **Always run a dry-run first** to estimate time and catch issues
2. **Use appropriate batch sizes** - start with 50, adjust based on performance
3. **Monitor API quotas** - especially OpenAI usage
4. **Keep logs** for debugging and auditing
5. **Run verification** to ensure data integrity
6. **Schedule during off-peak hours** for large datasets

## Data Structure

Each vector in Pinecone contains:

**Vector Data:**
- 1536-dimensional embedding from OpenAI text-embedding-3-small
- Generated from: "Job Title: [title]\n\nJob Description: [description]"

**Metadata:**
- `scan_id` - Database record ID
- `job_title` - Job posting title  
- `company_domain` - Client company
- `client_name` - Client name
- `role_category` - Standardized role category
- `experience_level` - Required experience
- `complexity_score` - Job complexity (1-10)
- `must_have_skills` - JSON array of required skills
- `recommended_regions` - JSON array of suitable regions
- `created_at` - Original scan timestamp
- Plus additional metadata from job analysis

This enables similarity search, filtering, and analytics on the vector data.