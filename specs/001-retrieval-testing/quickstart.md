# Quickstart: Retrieval Pipeline Testing and Validation

## Prerequisites

- Python 3.14 or higher
- Access to Qdrant vector database with embedded book content
- Valid API keys for Qdrant and Cohere (if using embeddings for validation)
- Environment variables configured in `.env` file:
  - `QDRANT_API_KEY`
  - `QDRANT_HOST`
  - `COHERE_API_KEY` (optional, for advanced validation)
  - `BOOK_SITE_URL`

## Setup

1. **Install Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   Ensure your `.env` file contains the required configuration:
   ```env
   QDRANT_API_KEY="your-qdrant-api-key"
   QDRANT_HOST="https://your-qdrant-host.com:6333"
   COHERE_API_KEY="your-cohere-api-key"  # Optional
   BOOK_SITE_URL="https://your-book-site.com"
   ```

3. **Configure Validation Settings**
   The validation system can be configured with these optional environment variables:
   ```env
   # General validation settings
   VALIDATION_ENABLED=True
   VALIDATION_TIMEOUT=30.0
   MAX_VALIDATION_RETRIES=3

   # Metadata validation settings
   METADATA_VALIDATION_ENABLED=True
   MIN_RELEVANCE_SCORE=0.5
   MAX_SEARCH_RESULTS=10
   SEARCH_TIMEOUT=15.0

   # Performance monitoring settings
   PERFORMANCE_MONITORING_ENABLED=True
   RESPONSE_TIME_THRESHOLD=5.0
   SUCCESS_RATE_THRESHOLD=0.9
   ```

4. **Verify Qdrant Connection**
   ```bash
   python -c "from qdrant_client import QdrantClient; client = QdrantClient(url='YOUR_HOST', api_key='YOUR_KEY'); print('Connected:', client.get_collections())"
   ```

## Running Validation Tests

### 1. Basic Semantic Search Test
Execute basic semantic search validation:
```bash
cd backend
python main.py test
```

This will:
- Connect to the Qdrant database
- Run sample queries to test semantic similarity
- Validate that results are relevant to the query

### 2. Metadata Validation Test
Verify that search results include correct metadata:
```bash
python main.py validation-test
```

This will:
- Test that each result includes source URL, chunk ID, and content preview
- Validate metadata accuracy against original sources
- Check for required metadata fields: URL, chunk_id, content, source, created_at

### 3. End-to-End Pipeline Test
Run comprehensive pipeline validation:
```bash
python main.py e2e-test
```

This will:
- Execute multiple test queries
- Validate relevance, metadata, and response times
- Test overall pipeline stability
- Generate detailed validation reports

### 4. API-based Validation
The validation system also provides REST API endpoints for programmatic validation:

**Start the validation server:**
```bash
cd backend
python main.py run
```

**Validate metadata for search results:**
```bash
curl -X POST http://localhost:8000/api/validation/validate \
  -H "Content-Type: application/json" \
  -d '{
    "search_results": [
      {
        "chunk_id": "chunk_1",
        "content": "Sample content for validation",
        "source_url": "https://example.com"
      }
    ]
  }'
```

**Perform search with metadata validation:**
```bash
curl -X POST http://localhost:8000/api/validation/validate-search-results \
  -H "Content-Type: application/json" \
  -d '{
    "query_text": "AI robotics fundamentals",
    "top_k": 5
  }'
```

**Extract metadata from content:**
```bash
curl -X POST http://localhost:8000/api/validation/extract-metadata \
  -H "Content-Type: application/json" \
  -d '{
    "content": "This is sample content with a URL https://example.com",
    "source_url": "https://source.com"
  }'
```

### 5. Batch and Reliability Testing
Run batch validation tests to test pipeline reliability:
```bash
python -c "
from src.services.batch_test_service import BatchTestService
from src.validation.reliability_scenarios import ReliabilityScenarios

batch_service = BatchTestService()
reliability_scenarios = ReliabilityScenarios()

# Get and execute reliability scenarios
scenarios = reliability_scenarios.get_basic_reliability_scenarios()
results = batch_service.execute_batch_tests(scenarios)
print('Batch test results:', results)
"
```

### 6. Performance Monitoring
Monitor validation performance with the performance monitoring service:
```bash
python -c "
from src.services.performance_monitor import PerformanceMonitor

monitor = PerformanceMonitor()

# Measure a specific operation
def sample_operation():
    import time
    time.sleep(0.1)  # Simulate some work
    return 'completed'

result = monitor.measure_operation('sample_operation', sample_operation)
print('Operation completed, response time:', monitor.get_response_time_stats('sample_operation'))
"
```

### 7. Generate Validation Reports
Create detailed validation reports:
```bash
python -c "
from src.services.report_service import ReportService

report_service = ReportService()

# Sample validation results
validation_results = [
    {'query_id': '1', 'passed': True, 'response_time': 0.5, 'relevance_score': 0.85},
    {'query_id': '2', 'passed': True, 'response_time': 0.7, 'relevance_score': 0.92},
    {'query_id': '3', 'passed': False, 'response_time': 1.2, 'relevance_score': 0.45}
]

# Generate summary report
summary = report_service.generate_validation_summary(validation_results)
print('Validation Summary:', summary)

# Generate detailed report
detailed = report_service.generate_detailed_report(validation_results)
print('Detailed Report Keys:', detailed.keys())
"
```

## Expected Output

When running validation tests, you should see:

1. **Connection Confirmation**: Qdrant connection established successfully
2. **Query Execution**: Test queries executed against the vector database
3. **Result Validation**: Results validated for relevance and metadata accuracy
4. **Performance Metrics**: Response times and success rates reported
5. **Summary Report**: Overall validation status and any issues detected
6. **Error Handling**: Proper handling of edge cases and error conditions
7. **Reliability Metrics**: Consistency and stability metrics for pipeline

## Validation Success Criteria

The validation system considers tests successful when:
- **Success Rate**: ≥ 90% of queries return valid results
- **Response Time**: Average response time < 5 seconds
- **Metadata Accuracy**: ≥ 95% of results include complete metadata
- **Reliability**: ≥ 95% success rate across multiple test iterations

## Troubleshooting

- **Connection Issues**: Verify QDRANT_HOST and QDRANT_API_KEY are correct
- **No Results**: Ensure the Qdrant collection contains embedded book content
- **Poor Relevance**: Check that the embedding model matches the one used for indexing
- **Missing Metadata**: Verify that the original content was indexed with proper metadata
- **Performance Issues**: Check RESPONSE_TIME_THRESHOLD configuration
- **Validation Failures**: Review error logs and validation reports

## Next Steps

After successful validation:
1. Run the full test suite: `python -m unittest discover tests/validation`
2. Generate comprehensive reports: Use the ReportService for detailed analysis
3. Optimize performance: Use PerformanceOptimizer based on validation results
4. Monitor continuously: Set up ongoing validation for production environments