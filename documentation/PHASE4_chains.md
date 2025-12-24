# Phase 4: LangChain Chains

## Overview

All LangChain chains required for the Advanced RAG workflow: routing, document grading, hallucination detection, and answer generation.

## Chains

### 1. Question Router Chain

**File**: `graph/chains/router.py`

- LLM chain using `ChatGoogleGenerativeAI`
- Structured output with `RouteDecision` Pydantic model
- Routes questions to RAG or web search
- Offline mode: Always routes to RAG
- Online mode: LLM decides based on question type
- Returns routing decision with reasoning
- Error handling with fallback to RAG

### 2. Document Grader Chain

**File**: `graph/chains/retrieval_grader.py`

- LLM chain to evaluate document relevance
- Structured output with `GradeDocument` Pydantic model
- Binary classification: "yes" (relevant) or "no" (not relevant)
- Provides reasoning for grading decision
- Integrated into `grade_documents` node
- Filters documents based on relevance scores

### 3. Hallucination Grader Chain

**File**: `graph/chains/hallucination_grader.py`

- LLM chain to detect hallucinations
- Structured output with `GradeHallucination` Pydantic model
- Compares generation against source documents
- Returns grounded/hallucinated decision
- Provides reasoning for hallucination check
- Integrated into `check_hallucination` node
- Triggers retry mechanism if hallucinated

### 4. Generation Chain

**File**: `graph/chains/generation.py`

- RAG chain for answer generation
- Uses `ChatGoogleGenerativeAI` with model `gemini-2.5-flash` and temperature 0.7
- Formats context from retrieved documents
- Includes source citations in generation
- Handles empty document cases gracefully
- Integrated into `generate` node

**Pure LLM Fallback**: `generate_pure_llm_answer()` function for offline mode when no documents found
- Limited to ~100 words
- Starts with "There is no answer in knowledge base but..." prefix
- Uses same LLM model with temperature 0.7

## Files

- `graph/chains/router.py` - Question routing chain
- `graph/chains/retrieval_grader.py` - Document grading chain
- `graph/chains/hallucination_grader.py` - Hallucination detection chain
- `graph/chains/generation.py` - Answer generation chain
- `graph/chains/__init__.py` - Chain exports

## Technical Challenges & Solutions

### 1. Structured Output with Pydantic
**Problem**: Ensure consistent LLM output format  
**Solution**: 
- Pydantic models for all chain outputs (`RouteDecision`, `GradeDocument`, `GradeHallucination`)
- `with_structured_output()` for type-safe responses
- Fallback handling for malformed responses

### 2. Mode-Aware Routing
**Problem**: Router should always return "rag" in offline mode  
**Solution**: 
- Check `AGENT_MODE` before calling LLM
- Return hardcoded "rag" decision in offline mode
- Skip LLM call to save API costs

### 3. Binary Classification for Grading
**Problem**: LLM needs to return yes/no decisions consistently  
**Solution**: 
- Structured output with explicit "yes"/"no" values
- Clear prompt instructions
- Error handling with fallback to "yes" (include document)

### 4. Hallucination Detection
**Problem**: Compare generation against source documents  
**Solution**: 
- Pass both generation and source documents to LLM
- Structured output: "grounded" or "hallucinated"
- Reasoning included for debugging

### 5. Context Formatting
**Problem**: Format retrieved documents for generation  
**Solution**: 
- Concatenate document content with separators
- Include source citations
- Handle empty document cases gracefully
