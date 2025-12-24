# Phase 5: Graph Nodes Implementation

## Overview

All graph nodes for the Advanced RAG workflow, integrated into the main graph structure with conditional routing and comprehensive logging.

## Nodes

### 1. Route Question Node

- Calls router chain
- Updates state with routing decision
- Sets `web_search=False` for offline mode
- Adds metadata for debugging (routing_decision, routing_reasoning)
- Conditional routing to RAG or web search

### 2. Retrieve Documents Node

- Uses QueryEngine directly (ChromaDB or PostgreSQL)
- Retrieves documents with improvements:
  - Query expansion
  - Hybrid search (semantic + keyword)
  - Metadata boosting
  - Cross-encoder reranking
- Converts results to LangChain Documents
- Returns top-k documents with scores
- Updates state with documents and scores

### 3. Grade Documents Node

- Calls retrieval grader chain for each document
- Filters to relevant documents only (binary_score == "yes")
- Updates state with graded documents
- Tracks grading scores
- Conditional routing: generate or web search fallback

### 4. Web Search Node

**File**: `graph/nodes/web_search.py`

- Implemented with Tavily API integration
- Disabled gracefully in offline mode (returns empty results)
- Enabled in online mode when `WEB_SEARCH_ENABLED=True`
- Converts web search results to LangChain Documents
- Includes error handling and logging

### 5. Grade Web Search Results Node

**File**: `graph/nodes/grade_web_search.py`

- Grades web search results for relevance using LLM
- Uses same retrieval grader chain as RAG documents
- Filters irrelevant results before generation
- Preserves Tavily scores for relevant results
- Includes comprehensive logging
- Updates state with `graded_web_search_results` and `web_search_grading_scores`

### 6. Generate Node

- Calls generation chain
- Uses graded documents as context (RAG path) OR graded web search results (fallback)
- Generates answer with citations
- Updates state with generation and sources
- Handles empty document cases
- **Pure LLM Fallback**: In offline mode, when no documents found, uses `generate_pure_llm_answer()`
  - Sets `generation_source` to `"llm_guess"`
  - Only used in offline mode (online mode falls back to web search)
  - Limited to ~100 words with specific prefix

### 7. Check Hallucination Node

- Calls hallucination grader chain
- Validates generation against source documents (graded documents or graded web search results)
- Updates retry count if hallucinated
- Returns decision: retry or end
- Conditional routing based on grounding status
- Uses `graded_web_search_results` for web search path
- Respects `MAX_RETRIES` limit (default: 5)

### 8. Increment Retry Node

- Increments retry counter
- Logs retry attempt
- Loops back to generate node
- Respects MAX_RETRIES limit

## Files

- `graph/graph.py` - All nodes integrated (including grade_web_search_results and pure LLM fallback)
- `graph/nodes/web_search.py` - Web search node implementation
- `graph/nodes/grade_web_search.py` - Web search result grading node
- `utility_scripts/test_retrieve_node.py` - Retrieve node test script

## Technical Challenges & Solutions

### 1. Document Deduplication
**Problem**: Python/JS versions of same docs create duplicates  
**Solution**: Content-based deduplication in `retrieve_documents` node:
- Hash normalized content (`hash(content.strip().lower())`)
- Track seen content hashes
- Skip duplicates, keep first occurrence
- Logs duplicate counts for debugging
**Files**: `graph/graph.py` lines 82-100

### 2. QueryEngine Integration
**Problem**: Convert QueryEngine results to LangChain Documents  
**Solution**: 
- Extract content and metadata from search results
- Create `Document` objects with proper metadata
- Preserve scores and source information
- Handle missing fields gracefully

### 3. Web Search Graceful Degradation
**Problem**: Web search should fail gracefully in offline mode  
**Solution**: 
- Check `WEB_SEARCH_ENABLED` before API call
- Return empty results list if disabled
- Log mode status
- No errors thrown in offline mode

### 4. Retry Mechanism
**Problem**: Prevent infinite retry loops  
**Solution**: 
- Track retry count in state
- Check against `MAX_RETRIES` limit
- Increment retry counter before retry
- End graph if max retries exceeded

### 5. State Updates
**Problem**: Update state correctly across nodes  
**Solution**: 
- Return state dictionaries from nodes
- LangGraph merges updates automatically
- State fields are replaced (not accumulated) in each node
- Preserve existing state fields

## Web Search Relevancy Validation

**Implementation**: `graph/nodes/grade_web_search.py`

- Validates web search results for relevance before generation
- Uses same retrieval grader chain as RAG documents
- Filters irrelevant web content
- Improves answer quality
- Consistent validation approach for both RAG and web search

**Workflow Update**:
```
web_search → grade_web_search_results → generate
```

**State Fields**:
- `graded_web_search_results: List[Document]`
- `web_search_grading_scores: List[float]`
- `metadata.web_search_graded_count: int`
- `metadata.web_search_filtered_count: int`
