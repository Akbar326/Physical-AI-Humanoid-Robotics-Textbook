# Data Model: Retrieval Pipeline Testing and Validation

## Core Entities

### TestQuery
- **query_text**: String (1-500 characters) - The input query text to test
- **expected_concepts**: List[String] - Concepts that should be present in relevant results
- **category**: String - Classification of the query (e.g., "ai_robotics", "humanoid_movement", "physical_ai")
- **created_at**: DateTime - Timestamp when the test query was created

### ValidationResult
- **query_id**: String - Reference to the test query
- **retrieved_chunks**: List[RetrievedChunk] - Results returned by the search
- **relevance_score**: Float (0.0-1.0) - Overall relevance of results to query
- **metadata_accuracy**: Boolean - Whether all metadata is correct
- **response_time**: Float (seconds) - Time taken for the query to execute
- **passed**: Boolean - Whether the validation passed all criteria
- **timestamp**: DateTime - When the validation was performed

### RetrievedChunk
- **chunk_id**: String - Unique identifier for the text chunk
- **content**: String - The actual text content of the chunk
- **source_url**: String - URL where the content originated
- **relevance_score**: Float (0.0-1.0) - Similarity score to the query
- **position**: Integer - Rank position in the results
- **metadata**: Dict - Additional metadata associated with the chunk

### TestScenario
- **name**: String - Descriptive name for the test scenario
- **description**: String - Detailed explanation of what the scenario tests
- **queries**: List[TestQuery] - Queries to execute as part of this scenario
- **success_criteria**: List[ValidationCriterion] - Criteria for passing the scenario
- **category**: String - Classification of the test (e.g., "basic_search", "metadata", "edge_cases")

### ValidationCriterion
- **name**: String - Name of the validation criterion
- **description**: String - What the criterion validates
- **threshold**: Float/Boolean - Minimum acceptable value or expected result
- **metric**: String - What metric is being validated (e.g., "relevance", "metadata_accuracy", "response_time")

## Relationships

- TestScenario contains multiple TestQuery instances
- TestQuery generates one ValidationResult
- ValidationResult contains multiple RetrievedChunk instances
- RetrievedChunk belongs to a specific source document

## Validation Rules

1. **Query Length**: TestQuery.query_text must be between 1 and 500 characters
2. **Relevance Threshold**: ValidationResult.relevance_score must be >= 0.7 for passing results
3. **Metadata Completeness**: ValidationResult.metadata_accuracy must be True for valid results
4. **Response Time**: ValidationResult.response_time must be < 2 seconds for 95% of queries
5. **Result Count**: Each query must return exactly 5 results as specified in requirements
6. **Content Relevance**: RetrievedChunk.content must semantically match the query intent
7. **Source Integrity**: RetrievedChunk.source_url must point to valid, existing content
8. **Uniqueness**: Each RetrievedChunk.chunk_id must be unique within a single query result