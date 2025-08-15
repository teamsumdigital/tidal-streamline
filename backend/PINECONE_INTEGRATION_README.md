# Pinecone Integration for Tidal Streamline

This document describes the Pinecone vector database integration for semantic matching in the Tidal Streamline backend.

## Overview

The integration provides semantic matching capabilities for market scans, allowing the system to:
- Find similar job postings based on content similarity (not just keyword matching)
- Provide enhanced job analysis using insights from historical similar scans
- Enable trend analysis and market insights based on semantic clustering
- Improve recommendation accuracy through machine learning-based similarity

## Architecture

### Components

1. **EmbeddingService** (`app/services/embedding_service.py`)
   - Handles OpenAI text embedding generation
   - Manages Pinecone index operations (create, upsert, query)
   - Provides batch processing for efficient embedding generation

2. **VectorSearchService** (`app/services/vector_search.py`)
   - Implements semantic search and similarity matching
   - Provides market trend analysis and insights
   - Manages confidence scoring and relevance calculations

3. **Enhanced JobAnalyzer** (`app/services/job_analyzer.py`)
   - Integrates semantic matching into job analysis workflow
   - Enhances analysis results with insights from similar scans
   - Stores analysis results in vector database for future matching

### Configuration

The integration is pre-configured with:
- **Pinecone API Key**: `pcsk_2asZaU_4JFVKA6KRDqh2i37Vn8bcWRx5cPhhGDhYcDmcemg3GGpG2m44TPouFMVkEzQqBe`
- **Index Name**: `tidal-streamline`
- **Embedding Model**: OpenAI `text-embedding-3-small` (1536 dimensions)
- **Similarity Metric**: Cosine similarity
- **Cloud**: AWS (Serverless)

## API Endpoints

### Enhanced Endpoints

1. **GET `/api/v1/market-scans/{scan_id}/similar`**
   - Now uses semantic matching instead of simple text similarity
   - Added `similarity_threshold` parameter (0.0-1.0)
   - Returns enhanced similarity data with match reasons and confidence scores

2. **GET `/api/v1/market-scans/analytics/trends`**
   - NEW: Provides market trend analysis based on semantic clustering
   - Parameters: `lookback_days` (1-365)

3. **GET `/api/v1/market-scans/analytics/vector-stats`**
   - NEW: Returns Pinecone index statistics and health metrics

### Enhanced Market Scan Workflow

The `/api/v1/market-scans/analyze` endpoint now:
1. Performs AI job analysis using OpenAI GPT-4
2. **NEW**: Finds semantically similar historical scans
3. **NEW**: Enhances analysis with insights from similar scans
4. Generates salary and skills recommendations
5. **NEW**: Stores the analysis in vector database for future matching
6. Returns confidence scores based on semantic similarity

## Data Flow

```
Job Posting → Embedding Generation → Semantic Search → Enhanced Analysis → Vector Storage
     ↓              ↓                     ↓                    ↓               ↓
Text Content → 1536D Vector → Similar Scans → Job Analysis → Pinecone Index
```

## Installation & Setup

### 1. Install Dependencies

```bash
# The pinecone-client is already added to requirements.txt
pip install -r requirements.txt
```

### 2. Environment Configuration

The Pinecone configuration is pre-set in `config.py`. Ensure your `.env` file has:

```env
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Pre-configured (no changes needed)
PINECONE_API_KEY=pcsk_2asZaU_4JFVKA6KRDqh2i37Vn8bcWRx5cPhhGDhYcDmcemg3GGpG2m44TPouFMVkEzQqBe
PINECONE_INDEX_NAME=tidal-streamline
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIMENSION=1536
```

### 3. Initialize Vector Database

The system automatically creates the Pinecone index on first use. No manual setup required.

### 4. Test Integration

Run the test suite to verify everything is working:

```bash
cd backend
python test_pinecone_integration.py
```

Expected output:
```
🚀 Starting Pinecone Integration Tests for Tidal Streamline
✅ Generated embedding with dimension: 1536
✅ Successfully stored test scan: test_scan_20240101_120000
✅ Found 2 similar scans with confidence: 0.84
🎉 All tests passed! Pinecone integration is working correctly.
```

## Usage Examples

### Finding Similar Scans

```python
from app.services.vector_search import vector_search_service

# Find semantically similar market scans
similar_scans, confidence = await vector_search_service.find_similar_market_scans(
    job_title="Marketing Manager",
    job_description="Looking for a marketing professional...",
    similarity_threshold=0.75,
    max_results=5
)

print(f"Found {len(similar_scans)} similar scans with confidence: {confidence}")
```

### Enhanced Job Analysis

```python
from app.services.job_analyzer import JobAnalyzer

job_analyzer = JobAnalyzer()

# Get job analysis with semantic matching
analysis, similar_scans, confidence = await job_analyzer.analyze_job_with_similar_scans(
    job_title="Data Analyst",
    job_description="We need a data analyst with Python and SQL skills...",
    hiring_challenges="Remote position"
)

print(f"Analysis enhanced by {len(similar_scans)} similar scans")
```

### Market Trends Analysis

```python
from app.services.vector_search import vector_search_service

# Get market trends based on semantic clustering
trends = await vector_search_service.get_market_trends(lookback_days=90)
print(f"Popular roles: {trends['trends']['most_common_roles']}")
```

## Performance Considerations

### Embedding Generation
- **Batch Processing**: Uses OpenAI batch API for multiple embeddings
- **Caching**: Consider implementing embedding cache for repeated content
- **Rate Limiting**: OpenAI API has rate limits (monitor usage)

### Vector Operations
- **Index Size**: Pinecone serverless scales automatically
- **Query Performance**: Sub-100ms for most similarity searches
- **Storage**: ~6KB per vector (1536 dimensions × 4 bytes)

### Optimization Tips
1. **Batch Uploads**: Upload multiple vectors simultaneously
2. **Smart Filtering**: Use metadata filtering to reduce search scope
3. **Similarity Thresholds**: Tune thresholds based on use case (0.7-0.8 recommended)
4. **Text Preprocessing**: Clean and normalize text before embedding

## Monitoring & Maintenance

### Health Checks
```bash
# Check vector database stats
curl http://localhost:8008/api/v1/market-scans/analytics/vector-stats

# Check recent trends
curl http://localhost:8008/api/v1/market-scans/analytics/trends?lookback_days=30
```

### Key Metrics to Monitor
- **Index Size**: Total number of vectors stored
- **Query Latency**: Average response time for similarity searches
- **Embedding Costs**: OpenAI API usage for text-embedding-3-small
- **Similarity Distribution**: Range and average of similarity scores

## Troubleshooting

### Common Issues

1. **"Index not found" Error**
   - Index is created automatically on first use
   - Check Pinecone API key validity
   - Verify internet connectivity

2. **"Embedding generation failed"**
   - Check OpenAI API key
   - Verify API quota/billing
   - Text may be too long (8000 char limit)

3. **Low similarity scores**
   - Adjust similarity threshold (try 0.6-0.7)
   - Check if enough data is indexed
   - Verify text quality and relevance

4. **Slow performance**
   - Use batch operations for multiple embeddings
   - Check network latency to Pinecone
   - Consider implementing local caching

### Debug Mode

Enable debug logging in your environment:

```env
LOG_LEVEL=DEBUG
```

This will show detailed logs for:
- Embedding generation processes
- Pinecone operations
- Similarity calculations
- Performance metrics

## Future Enhancements

Potential improvements to consider:

1. **Hybrid Search**: Combine semantic and keyword-based search
2. **Fine-tuned Models**: Train custom embeddings for job market domain
3. **Advanced Filtering**: More sophisticated metadata filtering
4. **Real-time Updates**: Streaming updates for live market analysis
5. **Multi-language Support**: Support for non-English job postings
6. **Clustering Analysis**: Identify job market clusters and patterns

## Support

For issues with the Pinecone integration:
1. Check the test script output: `python test_pinecone_integration.py`
2. Verify environment configuration matches this guide
3. Monitor API usage and quotas for OpenAI and Pinecone
4. Check logs for detailed error messages with `LOG_LEVEL=DEBUG`