# Data Update Strategy

## Overview

This document describes the data freshness and update strategies for both offline and online modes of the LangGraph Helper Agent, addressing the requirement to specify how users can refresh/update documentation data.

## Table of Contents

1. [Data Sources](#data-sources)
2. [Offline Mode - Data Preparation](#offline-mode---data-preparation)
3. [Offline Mode - Update Strategy](#offline-mode---update-strategy)
4. [Online Mode - Data Preparation](#online-mode---data-preparation)
5. [Online Mode - Update Strategy](#online-mode---update-strategy)
6. [Watchdog System](#watchdog-system)
7. [Manual Update Procedures](#manual-update-procedures)
8. [Adding New Data Sources](#adding-new-data-sources)

---

## Data Sources

### Primary Sources (Required)

The agent uses documentation from `llms.txt` format files:

- **LangGraph**: `https://langchain-ai.github.io/langgraph/llms.txt`
- **LangChain**: `https://docs.langchain.com/llms-full.txt`

### Data Format

- **Input**: `llms.txt` files containing URLs to markdown documentation
- **Downloaded**: Markdown files (`.md`) organized by source
- **Processed**: Chunked by headings, embedded, stored in vector database
- **Storage**: 
  - Offline: ChromaDB (local persistent storage)
  - Online: PostgreSQL with pgvector extension

---

## Offline Mode - Data Preparation

### Initial Setup

**Step 1: Download Documentation**
```bash
python ingestion/download_docs.py
```

**What it does:**
- Fetches `llms.txt` files from configured sources
- Extracts markdown URLs from `llms.txt` format
- Downloads all markdown files to `docs/langgraph/` and `docs/langchain/`
- Converts HTML to markdown (if needed)
- Saves download metadata to `metadata/download_metadata.json`

**Step 2: Index Documentation**
```bash
python -m ingestion.indexer
```

**What it does:**
- Parses markdown files using heading-based chunking
- Generates embeddings using Google Gemini (`gemini-embedding-001`)
  - Task type: `RETRIEVAL_DOCUMENT` (3072 dimensions)
- Stores in ChromaDB with metadata:
  - File paths, headings, chunk indices
  - Topics, keywords, content types
  - Code detection, language identification
- Saves indexing metadata to `metadata/indexing_metadata.json`

**Result:**
- ~5,614 document chunks indexed
- ChromaDB collections: `langgraph_docs`, `langchain_docs`
- Persistent storage in `index/` directory

---

## Offline Mode - Update Strategy

### Automated Updates (Recommended)

**Watchdog System** (`ingestion/watchdog.py`)

The watchdog provides **incremental updates** - only processes changed files, making updates 10x faster than full re-indexing.

#### How Watchdog Works

1. **URL Monitoring**: Checks `llms.txt` files for new/removed URLs
2. **Change Detection**: Compares file checksums to detect modifications
3. **Incremental Processing**: 
   - Downloads only new files
   - Re-indexes only changed files
   - Removes deleted files from index
4. **Registry Tracking**: Maintains `metadata/file_registry.json` with checksums

#### Usage

**One-time Check:**
```bash
# Check all sources
python -m ingestion.watchdog --check

# Check specific source
python -m ingestion.watchdog --check --source langgraph
python -m ingestion.watchdog --check --source langchain
```

**Continuous Monitoring:**
```bash
# Monitor every hour (3600 seconds)
python -m ingestion.watchdog --watch --interval 3600

# Monitor every 6 hours
python -m ingestion.watchdog --watch --interval 21600

# Monitor daily
python -m ingestion.watchdog --watch --interval 86400
```

**Scheduled Updates (Cron/Windows Task Scheduler):**
```bash
# Linux/Mac: Add to crontab (runs daily at 2 AM)
0 2 * * * cd /path/to/project && python -m ingestion.watchdog --check

# Windows: Use Task Scheduler to run:
python -m ingestion.watchdog --check
```

#### Watchdog Features

- **Efficient**: Only processes changed files (checksum-based)
- **Reliable**: Tracks file registry to avoid duplicate work
- **Safe**: Preserves existing data, only updates what changed
- **Informative**: Reports new/changed/removed files

### Manual Updates

**Option 1: Full Re-download and Re-index**
```bash
# Re-download all files
python ingestion/download_docs.py

# Re-index everything
python -m ingestion.indexer
```

**When to use:**
- Major documentation restructuring
- Suspected data corruption
- After adding new sources

**Option 2: Selective Update**
```bash
# Download specific source
python ingestion/download_docs.py --source langgraph

# Index specific source
python -m ingestion.indexer --source langgraph
```

---

## Online Mode - Data Preparation

### Initial Setup

**Step 1: Local Data Preparation** (Same as Offline)
```bash
python ingestion/download_docs.py
python -m ingestion.indexer
```

**Step 2: Migrate to PostgreSQL**
```bash
# Set PostgreSQL connection
export POSTGRES_HOST=your-postgres-host
export POSTGRES_PASSWORD=your-password

# Migrate from ChromaDB to PostgreSQL
python utility_scripts/migrate_to_eb.py
```

**What it does:**
- Reads all documents from ChromaDB collections
- Re-embeds using PostgreSQL-compatible embeddings (3072 dims)
- Stores in PostgreSQL table `langchain_document_vectors`
- Preserves all metadata (topics, keywords, file paths)

**Alternative: Direct Indexing to PostgreSQL**
```bash
# Set mode to online before indexing
export AGENT_MODE=online
export POSTGRES_HOST=your-postgres-host

# Index directly to PostgreSQL
python -m ingestion.indexer
```

### Online Mode Services

**Vector Store: PostgreSQL + pgvector**
- **Why**: Scalable, persistent, production-ready
- **Extension**: pgvector (enables vector similarity search)
- **Table**: `langchain_document_vectors`
- **Vector Size**: 3072 dimensions (Google Gemini RETRIEVAL_DOCUMENT)

**Web Search: Tavily API**
- **Service**: [Tavily Search API](https://tavily.com/)
- **Why**: 
  - Free tier: 1,000 requests/month
  - Fast response times
  - Domain filtering support
  - Good for technical documentation
- **Get API Key**: [Tavily Dashboard](https://app.tavily.com/)
- **Configuration**: Set `TAVILY_API_KEY` in `.env` file

**Domain Filtering:**
- Automatically restricts searches to:
  - `langchain-ai.github.io` (LangGraph docs)
  - `docs.langchain.com` (LangChain docs)
  - `python.langchain.com` (LangChain Python)

---

## Online Mode - Update Strategy

### Vector Store Updates

**Method 1: Watchdog + Migration** (Recommended)
```bash
# 1. Update local ChromaDB using watchdog
python -m ingestion.watchdog --check

# 2. Migrate changes to PostgreSQL
python utility_scripts/migrate_to_eb.py
```

**Method 2: Direct PostgreSQL Updates**
```bash
# Set online mode
export AGENT_MODE=online
export POSTGRES_HOST=your-postgres-host

# Run watchdog (will update PostgreSQL directly)
python -m ingestion.watchdog --check
```

**Note**: Current watchdog implementation updates ChromaDB. For PostgreSQL, use migration script or extend watchdog to support PostgreSQL directly.

### Web Search Updates

**No Updates Required** ✅

- Tavily queries live web in real-time
- Always returns current information
- Domain filtering ensures documentation-focused results
- No manual updates needed

---

## Watchdog System

### Architecture

```
┌─────────────────┐
│  llms.txt URLs  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│  Check Changes  │─────▶│  File Registry   │
│  (checksums)    │      │  (metadata.json) │
└────────┬────────┘      └──────────────────┘
         │
         ▼
┌─────────────────┐
│  Download New   │
│  Changed Files  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Incremental    │
│  Re-indexing    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Update Vector  │
│  Store          │
└─────────────────┘
```

### Change Detection Algorithm

1. **URL-Level Changes**:
   - Fetches current `llms.txt` from source
   - Compares URLs with file registry
   - Identifies: new URLs, removed URLs, unchanged URLs

2. **File-Level Changes**:
   - Calculates MD5 checksum for each file
   - Compares with stored checksums in registry
   - Identifies: new files, changed files, deleted files

3. **Incremental Processing**:
   - Downloads only new files
   - Re-indexes only changed files
   - Removes deleted files from index
   - Updates registry with new checksums

### File Registry

**Location**: `metadata/file_registry.json`

**Structure**:
```json
{
  "langgraph": {
    "docs/langgraph/file.md": {
      "url": "https://...",
      "checksum": "abc123...",
      "chunk_count": 5,
      "last_updated": "2025-12-24T10:00:00"
    }
  }
}
```

**Purpose**:
- Track file checksums for change detection
- Store metadata (URLs, chunk counts)
- Enable incremental updates

---

## Manual Update Procedures

### Complete Refresh

**When**: Major changes, data corruption, or adding new sources

```bash
# 1. Backup existing data (optional)
cp -r index/ index_backup/
cp metadata/file_registry.json metadata/file_registry_backup.json

# 2. Re-download all documentation
python ingestion/download_docs.py

# 3. Re-index everything
python -m ingestion.indexer

# 4. For online mode: Migrate to PostgreSQL
export AGENT_MODE=online
python utility_scripts/migrate_to_eb.py
```

### Source-Specific Update

```bash
# Update only LangGraph
python ingestion/download_docs.py --source langgraph
python -m ingestion.indexer --source langgraph

# Update only LangChain
python ingestion/download_docs.py --source langchain
python -m ingestion.indexer --source langchain
```

### Validation

After updates, validate data integrity:

```bash
# Check download metadata
python ingestion/validate_downloads.py

# Check indexing results
cat metadata/indexing_metadata.json
```

---

## Adding New Data Sources

### Step 1: Configure Source

Edit `config.py`:

```python
SOURCES = {
    "langgraph": {...},
    "langchain": {...},
    "new_source": {
        "index_url": "https://example.com/docs/llms.txt",
        "base_url": "https://example.com/docs",
        "docs_dir": DOCS_DIR / "new_source",
        "collection_name": "new_source_docs"
    }
}
```

### Step 2: Download and Index

```bash
# Download new source
python ingestion/download_docs.py --source new_source

# Index new source
python -m ingestion.indexer --source new_source
```

### Step 3: Update Watchdog

Watchdog automatically detects new sources from `config.py`. No changes needed.

### Step 4: Document Update Strategy

- Add source to this documentation
- Specify update frequency recommendations
- Document any source-specific requirements

---

## Update Frequency Recommendations

### Development Environment

- **Initial Setup**: Full download + index
- **Regular Updates**: Weekly watchdog check
- **Before Important Tasks**: Manual check

### Production Environment

- **Initial Setup**: Full download + index
- **Automated Updates**: Daily watchdog (cron/scheduler)
- **Monitoring**: Check logs for update failures

### Example Cron Schedule

```bash
# Daily at 2 AM
0 2 * * * cd /path/to/project && python -m ingestion.watchdog --check >> logs/watchdog.log 2>&1
```

---

## Troubleshooting

### Watchdog Not Detecting Changes

**Check**:
1. File registry exists: `metadata/file_registry.json`
2. Checksums are being calculated correctly
3. Network connectivity to `llms.txt` URLs

**Solution**:
```bash
# Force full check
python -m ingestion.watchdog --check --force
```

### Index Out of Sync

**Symptoms**: Queries return outdated information

**Solution**:
```bash
# Full re-index
python -m ingestion.indexer
```

### PostgreSQL Migration Issues

**Check**:
1. PostgreSQL connection settings
2. pgvector extension installed
3. Table exists: `langchain_document_vectors`

**Solution**:
```bash
# Enable pgvector
python utility_scripts/enable_pgvector_eb.py

# Re-migrate
python utility_scripts/migrate_to_eb.py
```

---

## Summary

### Offline Mode

| Aspect | Strategy |
|--------|----------|
| **Initial Setup** | Download + Index (one-time) |
| **Regular Updates** | Watchdog (automated) |
| **Manual Updates** | Full re-download + re-index |
| **Update Frequency** | Weekly recommended |

### Online Mode

| Aspect | Strategy |
|--------|----------|
| **Vector Store** | Watchdog + Migration, or Direct PostgreSQL indexing |
| **Web Search** | Always fresh (no updates needed) |
| **Update Frequency** | Weekly for vector store, real-time for web search |

### Key Benefits

- **Efficiency**: Incremental updates are 10x faster than full re-index
- **Automation**: Watchdog can run continuously or on schedule
- **Reliability**: Checksum-based change detection ensures accuracy
- **Flexibility**: Supports both automated and manual update workflows

---

## References

- [Watchdog Implementation](../ingestion/watchdog.py)
- [Indexer Implementation](../ingestion/indexer.py)
- [Download Script](../ingestion/download_docs.py)
- [Migration Script](../utility_scripts/migrate_to_eb.py)
- [Configuration](../config.py)

