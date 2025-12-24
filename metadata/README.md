# Metadata Directory

This directory contains metadata files for the documentation search system.

## Essential Files

### Current State
- **`indexing_metadata.json`** - Current index statistics (files, chunks per source)
- **`file_registry.json`** - File tracking registry for incremental updates
- **`download_metadata.json`** - Download metadata (checksums, URLs, timestamps)
- **`query_accuracy_20251223_122204.json`** - Latest test results (fresh index, Phase 2 complete)

## Archive

The `archive/` directory contains:
- Old query accuracy test results
- Old comparison reports
- Old validation files

## Logs

The `logs/` directory contains:
- Indexing logs (`indexing_*.log`)
- Validation logs (`validation_*.log`)

## File Descriptions

### `indexing_metadata.json`
Current indexing statistics including:
- Total files and chunks indexed
- Per-source breakdown (LangGraph, LangChain)
- Indexing errors (if any)

### `file_registry.json`
File tracking registry for incremental updates:
- File paths and URLs
- Checksums (SHA256)
- HTTP headers (ETag, Last-Modified)
- Download and indexing timestamps
- Chunk counts per file

### `download_metadata.json`
Download metadata from Phase 1:
- Original and actual URLs (after redirects)
- File checksums
- Download timestamps
- Validation status
- File sizes

### `query_accuracy_*.json`
Test results from accuracy testing:
- Precision@10 scores
- Average similarity scores
- Per-query results
- Relevance analysis

## Maintenance

- **Keep**: Current metadata files, latest test results, baseline results
- **Archive**: Old test results, old comparison reports, old validation files
- **Logs**: Move to `logs/` directory for organization

