# Phase 2: Indexing System

## Overview

The indexing system parses markdown files, chunks them by headings, enriches with metadata, and indexes them into ChromaDB with embeddings. The system supports both ChromaDB (offline) and PostgreSQL (online) vector stores.

## Statistics

### Indexing Results

**Total Files Indexed**: 732
- **LangGraph**: 137 files → 904 chunks
- **LangChain**: 595 files → 4,710 chunks

**Total Chunks Indexed**: 5,614

### Index Coverage

- **LangGraph**: 100% (137/137 files)
- **LangChain**: 100% (595/595 files)
- **Overall**: 100% coverage of downloaded documentation

## Features

### 1. Markdown Parsing & Chunking

- **Heading-based chunking**: Splits by H1-H3 headings to preserve logical structure
- **Code block preservation**: Keeps code blocks as single units (never splits)
- **Smart splitting**: Handles long sections (>1000 tokens) by splitting on paragraphs
- **Context preservation**: Maintains heading hierarchy and document structure

### 2. Metadata Enrichment

#### Topic Detection
- Detects 17 topic types:
  - `error-handling`, `best-practices`, `comparison`, `graph-types`
  - `tutorial`, `persistence`, `human-in-the-loop`, `streaming`
  - `multi-agent`, `tools`, `deployment`, `subgraphs`
  - `rag`, `agents`, `vectorstores`, `document-loaders`, `memory`, `models`
- Applied to both chunk content and file paths
- Stored as comma-separated strings in ChromaDB metadata

#### Keyword Extraction
- Extracts technical terms (class names, function names, CamelCase terms)
- Identifies quoted terms (important concepts)
- Captures code block languages
- Extracts from headings and content
- Limited to 15 most important keywords per chunk
- Stored as comma-separated strings in ChromaDB metadata

#### Content Type Detection
- Classifies chunks into types:
  - `code-example`: Code-heavy chunks (2+ code blocks)
  - `tutorial`: Step-by-step guides
  - `reference`: API references, class/function docs
  - `concept`: Overviews, introductions
  - `deployment`: Production deployment guides
  - `integration`: Integration guides
  - `general`: Other content
- Applied at both chunk and file levels

#### Enhanced Context Preservation
- Double overlap (320 tokens) for comparison chunks
- Preserves context when splitting long sections
- Maintains heading hierarchy in metadata

### 3. Embedding Generation

- **Model**: Google Generative AI (`gemini-embedding-001`)
- **Batch processing**: Efficient batch embedding generation
- **Normalization**: Embeddings normalized for cosine similarity
- **Storage**: Stored in ChromaDB with persistent local storage
- **Dimensions**: 
  - ChromaDB queries: RETRIEVAL_QUERY (768 dimensions)
  - PostgreSQL storage: RETRIEVAL_DOCUMENT (3072 dimensions)

### 4. Vector Storage

#### ChromaDB (Offline Mode)
- **Persistent storage**: Index persists across sessions in `index/` directory
- **Separate collections**: One collection per source (langgraph_docs, langchain_docs)
- **Rich metadata**: All metadata stored and queryable

#### PostgreSQL (Online Mode)
- **Table**: `langchain_document_vectors`
- **Vector dimensions**: 3072 (RETRIEVAL_DOCUMENT embeddings)
- **Metadata**: Stored as JSONB
- **Indexes**: Automatic vector similarity index

### 5. Metadata Fields

- `source`: "langgraph" or "langchain"
- `file_path`: Relative path to MD file
- `heading_path`: Full heading hierarchy
- `chunk_index`: Index within document
- `has_code`: Boolean indicating code presence
- `code_language`: Language of code blocks
- `topics`: Comma-separated topic tags
- `keywords`: Comma-separated keywords
- `content_type`: Chunk type
- `file_content_type`: File-level content type
- `file_topics`: File-level topics

## Test Results

### Fresh Index Test Results

**Test Set**: 20 queries (10 LangGraph + 10 LangChain)

| Metric | LangGraph | LangChain |
|--------|-----------|-----------|
| **Precision@10** | **10.5%** | **14.0%** |
| **Avg Similarity** | **0.6031** | **0.6242** |

### Comparison with Baseline

| Metric | Baseline | Current | Improvement |
|--------|----------|---------|-------------|
| **LangGraph Precision** | 4.0% | 10.5% | **+162.5%** |
| **LangGraph Similarity** | 0.488 | 0.6031 | **+23.6%** |
| **LangChain Precision** | 1.0% | 14.0% | **+1,300%** |
| **LangChain Similarity** | 0.484 | 0.6242 | **+29.0%** |

## Implementation Details

### Chunking Algorithm

1. Parse markdown into structured format
2. Traverse content maintaining heading stack
3. When encountering heading (H1-H3):
   - Finalize current chunk if exists
   - Start new chunk with heading context
4. For code blocks: keep as single unit, don't split
5. For long sections (>1000 tokens): split by paragraphs while preserving heading context
6. Apply metadata enhancements:
   - Detect topics from content and heading
   - Extract keywords from content
   - Detect content type
   - Apply enhanced overlap for comparison chunks

### Metadata Processing

- **List handling**: Convert lists (topics, keywords) to comma-separated strings for ChromaDB
- **Path normalization**: Normalize file paths for cross-platform compatibility
- **Type conversion**: Ensure all metadata values are ChromaDB-compatible types (str, int, float, bool)
- **Validation**: Validate metadata before storage

### Embedding Pipeline

1. Load embedding model (Google Generative AI)
2. Process files in batches
3. Generate embeddings for each chunk
4. Store embeddings with metadata in ChromaDB or PostgreSQL
5. Update indexing metadata with statistics

## Files

### Core Files
- `utility_scripts/indexer.py`: Main indexing logic with metadata integration
- `chunker.py`: Enhanced chunking with topic detection, keyword extraction, content type detection
- `config.py`: Configuration for chunking, embeddings, and storage

### Metadata Files
- `metadata/indexing_metadata.json`: Indexing statistics and metadata
- `metadata/query_accuracy_*.json`: Test results

## Validation

### Index Integrity
- All files from Phase 1 successfully indexed
- All chunks have required metadata
- No indexing errors
- ChromaDB collections created and populated
- PostgreSQL table created and populated (5,614 documents)

### Metadata Quality
- Topics detected for 90%+ of chunks
- Keywords extracted for all chunks
- Content types assigned correctly
- File-level metadata preserved

## Usage

```bash
# Index all documentation
python utility_scripts/indexer.py

# Validate indexing
python utility_scripts/validate_indexing.py

# Run accuracy tests
python utility_scripts/test_query_accuracy.py
```

## Technical Details

- **Chunking**: Heading-based with smart paragraph splitting
- **Embedding Model**: Google Generative AI (`gemini-embedding-001`)
- **Vector Storage**: ChromaDB (offline) or PostgreSQL (online)
- **Metadata**: Rich metadata for filtering and boosting
- **Batch Processing**: Efficient batch embedding generation
- **Error Handling**: Graceful handling of parsing and embedding errors

## PostgreSQL Integration

### QueryEngine Dual Vector Store Support

**File**: `query_engine.py`

**Implementation**:
- Conditional initialization based on `VECTOR_STORE_MODE`
- Support both ChromaDB and PostgreSQL backends
- Maintain same public API for backward compatibility
- Use `PGVectorStore` when `VECTOR_STORE_MODE=postgres`
- Use ChromaDB when `VECTOR_STORE_MODE=chroma`
- Proper embedding dimension handling:
  - ChromaDB: RETRIEVAL_QUERY (768 dimensions)
  - PostgreSQL: RETRIEVAL_DOCUMENT (3072 dimensions)
- Mode-aware logging with `[MODE]` prefix
- Fully integrated into graph workflow

## Technical Challenges & Solutions

### 1. Chunker Tuple Bug Fix
**Problem**: `TypeError: sequence item 0: expected str instance, tuple found`  
**Root Cause**: `heading_stack` contains tuples `(heading_text, level)`, but was being joined directly  
**Solution**: Extract heading text from tuples before joining:
```python
' > '.join([h[0] for h in heading_stack])  # Extract h[0] (heading text)
```
**Files**: `chunker.py` lines 61, 84

### 2. Metadata Type Cleaning
**Problem**: ChromaDB doesn't accept None, tuples, or lists in metadata  
**Solution**: Enhanced metadata cleaning in `indexer.py`:
- None → empty string `""`
- Tuples/Lists → joined string (comma-separated for topics/keywords, ` > ` for others)
- Path normalization: Windows backslashes → forward slashes
- Type conversion: All values converted to ChromaDB-compatible types (str, int, float, bool)
**Files**: `utility_scripts/indexer.py` lines 95-135

### 3. Heading Path Construction
**Problem**: Need to preserve heading hierarchy in metadata  
**Solution**: Maintain `heading_stack` as list of tuples `(heading_text, level)`:
- Stack-based approach: Pop higher-level headings when encountering lower-level ones
- Convert to string path: `' > '.join([h[0] for h in heading_stack])`
- Preserves document structure for better context

### 4. Code Block Preservation
**Problem**: Code blocks should never be split across chunks  
**Solution**: 
- Detect code blocks (triple backticks)
- Keep entire code block as single unit
- Never split within code blocks
- Preserve code language in metadata

### 5. Token Estimation
**Problem**: Need accurate token counts for chunking  
**Solution**: 
- Uses `tiktoken` for GPT-style token counting
- Falls back to character-based estimation if tiktoken fails
- Validates chunk sizes before adding to collection

### 6. Batch Embedding Processing
**Problem**: Efficient embedding generation for large document sets  
**Solution**:
- Batch processing: Groups chunks into batches
- Uses `embed_documents()` for batch API calls
- Progress tracking with `tqdm`
- Error handling per batch (continues on failure)

### 7. Metadata Enrichment Pipeline
**Problem**: Extract topics, keywords, and content types efficiently  
**Solution**:
- Topic detection: Pattern matching on content and file paths
- Keyword extraction: Regex-based (CamelCase, quoted terms, code languages)
- Content type detection: Heuristic-based (code blocks, structure analysis)
- Applied at both chunk and file levels

### 8. Path Normalization
**Problem**: Windows backslashes cause issues in ChromaDB metadata  
**Solution**: 
- Normalize all file paths: `str(value).replace('\\', '/')`
- Ensures cross-platform compatibility
- Consistent path format in metadata
**Files**: `utility_scripts/indexer.py` line 132
