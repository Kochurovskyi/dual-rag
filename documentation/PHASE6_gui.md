# Phase 6: Streamlit GUI

## Overview

Complete Streamlit GUI for the Advanced RAG system with mode switching, API validation, and comprehensive document display.

## Features

### Main Application

**File**: `app.py`

**Sidebar**:
- Vector store mode switcher (Offline/Online radio buttons)
- Configuration display (current mode, vector store, web search status)
- API key validation (Google API Key, Tavily API Key)
- Example questions (7 predefined questions)

**Main Area**:
- Question input with session state management
- Run button with chat history clearing (`on_click` callback)
- Answer display with chat message format
- **Source display**: Prominently shows generation sources with `format_source()` helper
  - 🌐 Web Search
  - 📚 RAG (PostgreSQL/ChromaDB)
  - 🤔 Just guessing? (pure LLM fallback)
- Source URLs/paths expandable section
- Document viewer (expandable sections)
- Statistics expandable (documents retrieved, graded, grounding status, retries, routing decision)

### Vector Store Switching Logic

**File**: `app.py`

- Session state for agent mode (`st.session_state.agent_mode`)
- Mode toggle updates configuration automatically
- Uses `graph.test_mode_helper.set_mode()` for runtime mode switching
- API validation states reset on mode change
- Graph workflow uses correct mode via context manager

### Document Rendering

**File**: `app.py`

- `format_document()` function formats documents with metadata
- Shows source file paths
- Displays relevance scores
- Expandable sections for source documents
- Chat history with message roles (user/assistant)
- Source documents shown in expandable sections per message

### API Key Validation

- Google API Key: Validates with light LLM request
- Tavily API Key: Validates with Tavily client (online mode only)
- Visual indicators: ✅ Valid, ❌ Invalid, ⚠️ Not set
- Validation states cached in session state

## Files

- `app.py` - Complete Streamlit GUI application

## Technical Challenges & Solutions

### 1. Chat History Clearing
**Problem**: Clear history when "Run" button pressed  
**Solution**: Use `on_click` callback:
```python
def clear_chat_history():
    st.session_state.messages = []

run_button = st.button("🚀 Run", on_click=clear_chat_history)
```
- Callback executes before button state is processed
- Immediately clears session state
- Page reruns automatically
**Files**: `app.py` lines 212-214

### 2. Session State Management
**Problem**: Maintain state across reruns  
**Solution**: 
- Initialize session state keys on first run
- Use `st.session_state` for persistent data
- Reset API validation on mode change
- Preserve chat history until cleared

### 3. Mode Switching
**Problem**: Runtime mode switching without restart  
**Solution**: 
- Use `graph.test_mode_helper.set_mode()` context manager
- Patches config module at runtime
- Updates `AGENT_MODE`, `WEB_SEARCH_ENABLED`, `VECTOR_STORE_MODE`
- Resets API validation states

### 4. API Key Validation
**Problem**: Validate API keys without blocking UI  
**Solution**: 
- Light validation requests (minimal API calls)
- Cache validation results in session state
- Visual indicators (✅/❌/⚠️)
- Reset on mode change

### 5. Document Rendering
**Problem**: Display documents with metadata clearly  
**Solution**: 
- `format_document()` function for consistent formatting
- `format_source()` helper function for source display
- Expandable sections for source documents
- Chat message format for answers
- Statistics in expandable section
- Prominent source indicator after answer

### 6. Source Display Enhancement
**Problem**: Show clear indication of answer source (Web Search, RAG, or LLM Guess)  
**Solution**: 
- `format_source()` helper function formats source labels
- Prominent display after answer: **Source:** 🌐 Web Search / 📚 RAG / 🤔 Just guessing?
- Source URLs/paths in expandable section
- Matches reference implementation: https://github.com/Kochurovskyi/Advanced-RAG
**Files**: `app.py` lines 60-70, 320-335

### 7. Unicode Handling
**Problem**: Handle Unicode in Windows console  
**Solution**: 
- Safe text printing functions
- Handle encoding errors gracefully
- Clean text for display
