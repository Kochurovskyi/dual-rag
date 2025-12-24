# Phase 9: PostgreSQL Migration

## Overview

PostgreSQL vector store migration infrastructure. All ChromaDB data has been migrated to PostgreSQL with pgvector extension, enabling online mode functionality.

## Statistics

### Migration Results

**Total Documents Migrated**: 5,614
- **LangGraph**: 904 documents migrated
- **LangChain**: 4,710 documents migrated

**Migration Time**: ~10 minutes (includes re-embedding)

**PostgreSQL Table**: `langchain_document_vectors`
- Vector size: 3072 dimensions (RETRIEVAL_DOCUMENT embeddings)
- All metadata preserved
- Indexes created automatically by `langchain_postgres`

## Features

### 1. Docker Configuration

**File**: `docker-compose.yml`

- PostgreSQL service with pgvector extension (`pgvector/pgvector:pg16`)
- Environment variables from `.env` file
- Persistent volume for data storage
- Health checks configured
- Port mapping: 5432:5432

**Configuration**:
- Database: `documentation_search`
- User: `postgres!`
- Password: `postgres!`
- Table: `langchain_document_vectors`

### 2. Migration Script

**File**: `utility_scripts/migrate_to_postgres.py`

- Uses `langchain_postgres.PGEngine` and `PGVectorStore` following best practices
- Reads from ChromaDB collections (`langgraph_docs`, `langchain_docs`)
- Converts to LangChain Documents format
- Batch processing (100 documents per batch)
- Progress bars with tqdm
- Error handling and logging
- Windows event loop fix included

**Key Features**:
- Automatic table initialization (`init_vectorstore_table`)
- Vector size: 3072 (matches RETRIEVAL_DOCUMENT embeddings)
- Re-embeds documents automatically (simpler than preserving ChromaDB embeddings)
- Preserves all metadata from ChromaDB

### 3. Setup Scripts

**Files**: `utility_scripts/setup_postgres.sh`, `utility_scripts/setup_postgres.bat`

- Start PostgreSQL container
- Wait for readiness
- Simple one-command setup

## Implementation Details

### Migration Process

1. **Connect to ChromaDB**: Read all collections
2. **Connect to PostgreSQL**: Initialize `PGVectorStore`
3. **Convert Documents**: Transform ChromaDB data to LangChain Documents
4. **Batch Insert**: Add documents in batches of 100
5. **Re-embed**: PGVectorStore automatically generates embeddings

### PostgreSQL Schema

Created by `langchain_postgres`:
- Table: `langchain_document_vectors`
- Vector column: `embedding` (3072 dimensions)
- Metadata: Stored as JSONB
- Indexes: Automatic vector similarity index

### Connection String Format

```
postgresql+psycopg://{user}:{password}@{host}:{port}/{database}
```

## Files

### Core Files
- `docker-compose.yml` - PostgreSQL container configuration
- `utility_scripts/migrate_to_postgres.py` - Migration script
- `utility_scripts/setup_postgres.sh` - Linux/Mac setup script
- `utility_scripts/setup_postgres.bat` - Windows setup script
- `utility_scripts/test_postgres_connection.py` - PostgreSQL connection test
- `query_engine.py` - QueryEngine with dual vector store support

### Configuration
- `.env` - PostgreSQL credentials (user configured)

## Validation

### Migration Validation
- All 5,614 documents successfully migrated
- No errors during migration
- All metadata preserved
- PostgreSQL container running and healthy

### Data Integrity
- LangGraph: 904 documents migrated
- LangChain: 4,710 documents migrated
- Total matches ChromaDB count
- Table created successfully

## Usage

### Start PostgreSQL
```bash
docker-compose up -d postgres
```

### Run Migration
```bash
python utility_scripts/migrate_to_postgres.py
```

### Verify Migration
```bash
# Connect to PostgreSQL and check
docker exec -it documentation_postgres psql -U postgres! -d documentation_search
SELECT COUNT(*) FROM langchain_document_vectors;
```

## QueryEngine Integration

**File**: `query_engine.py`

- Conditional initialization based on `VECTOR_STORE_MODE`
- Supports both ChromaDB (offline) and PostgreSQL (online)
- Proper embedding dimension handling:
  - ChromaDB: RETRIEVAL_QUERY (768 dimensions)
  - PostgreSQL: RETRIEVAL_DOCUMENT (3072 dimensions)
- Mode-aware logging with `[MODE]` prefix
- Fully integrated into graph workflow
- Backward compatibility maintained

## Technical Details

- **Migration Tool**: `langchain_postgres.PGVectorStore`
- **Embedding Model**: Google Generative AI (`gemini-embedding-001`, RETRIEVAL_DOCUMENT)
- **Vector Dimensions**: 3072
- **Batch Size**: 100 documents
- **Connection Pooling**: Handled by `langchain_postgres`
- **Error Handling**: Comprehensive try/except with logging

## Technical Challenges & Solutions

### 1. Windows Event Loop Issue
**Problem**: `asyncio` on Windows uses `ProactorEventLoopPolicy` which conflicts with `langchain_postgres`  
**Solution**: Set event loop policy before initialization:
```python
if hasattr(asyncio, 'WindowsProactorEventLoopPolicy'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
```
**Files**: `utility_scripts/migrate_to_postgres.py` lines 37-39

### 2. Embedding Dimension Mismatch
**Problem**: ChromaDB embeddings vs PostgreSQL vector size  
**Solution**: 
- Re-embed documents using `PGVectorStore.add_documents()`
- Simpler than preserving ChromaDB embeddings
- Ensures correct vector dimensions (3072 for RETRIEVAL_DOCUMENT)
- Automatic embedding generation by `langchain_postgres`

### 3. Batch Processing
**Problem**: Efficient migration of 5,614 documents  
**Solution**: 
- Batch size: 100 documents per batch
- Progress bars with `tqdm`
- Error handling per batch (continues on failure)
- Logging for each batch

### 4. Table Initialization
**Problem**: Create vector table with correct schema  
**Solution**: 
- Use `PGEngine.init_vectorstore_table()`
- Specify vector size (3072)
- Handle "already exists" errors gracefully
- Automatic index creation

### 5. Metadata Preservation
**Problem**: Preserve all ChromaDB metadata in PostgreSQL  
**Solution**: 
- Convert ChromaDB metadata to LangChain Document metadata
- Store as JSONB in PostgreSQL
- All metadata fields preserved
- Source information included

### 6. Connection String Format
**Problem**: Correct PostgreSQL connection string format  
**Solution**: 
- Use `postgresql+psycopg://` format for `langchain_postgres`
- Include user, password, host, port, database
- Environment variables from `.env` file
