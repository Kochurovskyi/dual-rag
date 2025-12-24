# Phase 3: LangGraph State Management

## Overview

The LangGraph workflow uses type-safe state definitions and a complete graph structure with all nodes and conditional routing.

## Graph State Definition

**File**: `graph/state.py`

TypedDict `GraphState` with all required fields:

- `question: str` - User question
- `web_search: bool` - Routing flag
- `web_search_results: List[Document]` - Web search results
- `graded_web_search_results: List[Document]` - Graded web search results
- `web_search_grading_scores: List[float]` - Web search grading scores
- `documents: List[Document]` - Retrieved documents (replaced, not appended)
- `document_scores: List[float]` - Relevance scores
- `graded_documents: List[Document]` - Filtered relevant docs (replaced, not appended)
- `grading_scores: List[float]` - Grading scores
- `generation: str` - Generated answer
- `generation_sources: List[str]` - Source citations
- `is_grounded: bool` - Hallucination check result
- `hallucination_score: float` - Hallucination score
- `retries: int` - Retry counter
- `metadata: Dict` - Execution metadata (includes `generation_source`: "rag", "web_search", or "llm_guess")

Type annotations for all fields. Full type safety with TypedDict. Documents are replaced (not accumulated) in each node.

## Graph Structure

**File**: `graph/graph.py`

Initialized `StateGraph(GraphState)` with LangGraph.

All 8 nodes implemented:
- `route_question` - Intelligent routing (RAG vs web search)
- `retrieve_documents` - Document retrieval from vector store
- `grade_documents` - Document relevance grading
- `web_search` - Web search fallback
- `grade_web_search_results` - Web search result grading
- `generate` - Answer generation (includes pure LLM fallback for offline mode)
- `check_hallucination` - Hallucination detection
- `increment_retry` - Retry mechanism

Conditional edges:
- Route decision: RAG path or web search path
- Grade decision: Generate or web search fallback
- Retry decision: Retry or end

Comprehensive logging integrated in all nodes. Mode-aware behavior (offline/online).

## Files

- `graph/state.py` - State TypedDict definition
- `graph/graph.py` - Main graph structure with all nodes

## Technical Challenges & Solutions

### 1. State Management with TypedDict
**Problem**: Manage state transitions across nodes  
**Solution**: 
- Documents are replaced (not accumulated) in each node
- Each node returns updated state dictionary
- LangGraph merges state updates automatically
- Enables multi-stage document filtering (retrieve → grade → generate)

### 2. Conditional Routing Logic
**Problem**: Complex routing decisions based on mode and state  
**Solution**: 
- Separate conditional functions (`should_continue`, `should_retry`)
- Mode-aware routing (offline mode always RAG path)
- State-based decisions (web_search flag, retry count)

### 3. Type Safety
**Problem**: Ensure type safety across graph execution  
**Solution**: 
- TypedDict with all required fields
- Type annotations for all state fields
- State fields are replaced (not accumulated) in each node
- Type checking in IDE and runtime

### 4. Logging Integration
**Problem**: Track execution flow across multiple nodes  
**Solution**: 
- Structured logging in each node
- Log routing decisions, document counts, scores
- Configurable log level via environment variable
- Separate loggers for different components
