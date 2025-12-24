"""Indexing system for parsing markdown files and storing embeddings in ChromaDB."""
import chromadb
from chromadb.config import Settings
from pathlib import Path
from typing import List, Dict
import json
import os
import logging
from datetime import datetime

from config import (
    EMBEDDING_MODEL, USE_GOOGLE_EMBEDDINGS, CHROMA_PERSIST_DIR, SOURCES,
    DOCS_DIR, METADATA_DIR, DOWNLOAD_METADATA_FILE,
    MAX_CHUNK_SIZE, MIN_CHUNK_SIZE, CHUNK_OVERLAP
)
from ingestion.chunker import MarkdownChunker
from ingestion.file_registry import FileRegistry
from ingestion.download_docs import calculate_checksum

# Import embedding model based on configuration
if USE_GOOGLE_EMBEDDINGS:
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    # Load API key from .env
    with open('.env', 'r') as f:
        for line in f:
            if 'GOOGLE_API_KEY' in line and not line.strip().startswith('#'):
                api_key = line.split('=', 1)[1].strip().strip('"').strip("'")
                os.environ['GOOGLE_API_KEY'] = api_key
                break
else:
    from sentence_transformers import SentenceTransformer


class DocumentationIndexer:
    """Indexes documentation files into ChromaDB."""
    
    def __init__(self, log_file: str = None):
        # Setup logging
        log_file = log_file or (METADATA_DIR / f"indexing_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Initializing indexer, log file: {log_file}")
        
        if USE_GOOGLE_EMBEDDINGS:
            self.logger.info(f"Using Google embeddings: {EMBEDDING_MODEL} (RETRIEVAL_DOCUMENT)")
            self.embedding_model = GoogleGenerativeAIEmbeddings(
                model=EMBEDDING_MODEL,
                task_type="RETRIEVAL_DOCUMENT"  # 3072 dimensions for documents
            )
        else:
            self.logger.info(f"Using sentence-transformers: {EMBEDDING_MODEL}")
            self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)
        
        self.chunker = MarkdownChunker(
            max_chunk_size=MAX_CHUNK_SIZE,
            min_chunk_size=MIN_CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )
        self.registry = FileRegistry()
        self.logger.info(f"Chunking config: max={MAX_CHUNK_SIZE}, min={MIN_CHUNK_SIZE}, overlap={CHUNK_OVERLAP}")
        
        # Initialize ChromaDB with persistent storage
        self.client = chromadb.PersistentClient(
            path=str(CHROMA_PERSIST_DIR),
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Create collections for each source
        self.collections = {}
        for source_name, config in SOURCES.items():
            collection_name = config['collection_name']
            self.collections[source_name] = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"source": source_name}
            )
    
    def index_file(self, file_path: Path, source: str) -> int:
        """Index a single markdown file. Returns number of chunks indexed."""
        try:
            chunks = self.chunker.chunk_file(file_path, source)
        except Exception as e:
            self.logger.error(f"Error chunking {file_path}: {e}", exc_info=True)
            raise
        
        if not chunks:
            self.logger.warning(f"No chunks generated for {file_path}")
            return 0
        
        # Prepare data for ChromaDB
        documents = []
        metadatas = []
        ids = []
        
        # Batch embeddings for efficiency
        chunk_texts = [chunk['content'] for chunk in chunks]
        
        if USE_GOOGLE_EMBEDDINGS:
            # Use embed_documents for batch (3072 dims)
            embeddings_list = self.embedding_model.embed_documents(chunk_texts)
        else:
            embeddings_list = self.embedding_model.encode(
                chunk_texts,
                normalize_embeddings=True
            ).tolist()
        
        # Prepare data for ChromaDB
        for i, chunk in enumerate(chunks):
            # Create unique ID
            chunk_id = f"{source}:{chunk['metadata']['file_path']}:{chunk['metadata']['chunk_index']}"
            
            # Clean metadata: ChromaDB requires strings, not None, and normalized paths
            # ChromaDB metadata types: str, int, float, bool (no None, no tuples, no lists)
            metadata = chunk['metadata'].copy()
            for key, value in metadata.items():
                if value is None:
                    metadata[key] = ""
                elif isinstance(value, (tuple, list)):
                    # Phase 2: For topics/keywords, join with comma; others use ' > '
                    if key in ['topics', 'keywords']:
                        metadata[key] = ', '.join(str(v) for v in value) if value else ""
                    else:
                        metadata[key] = ' > '.join(str(v) for v in value) if value else ""
                elif key == 'file_path':
                    # Normalize path separators for ChromaDB
                    metadata[key] = str(value).replace('\\', '/')
                elif not isinstance(value, (str, int, float, bool)):
                    # Convert any other type to string
                    metadata[key] = str(value)
            
            documents.append(chunk['content'])
            metadatas.append(metadata)
            ids.append(chunk_id)
        
        # Add to ChromaDB collection
        collection = self.collections[source]
        try:
            collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids,
                embeddings=embeddings_list
            )
            self.logger.debug(f"Added {len(documents)} chunks to {source} collection")
        except Exception as e:
            self.logger.error(f"Error adding to ChromaDB: {e}", exc_info=True)
            # Log first problematic metadata for debugging
            if metadatas:
                self.logger.error(f"Sample metadata: {metadatas[0]}")
            raise
        
        # Update registry
        relative_path = chunks[0]['metadata']['file_path'] if chunks else ''
        if relative_path:
            # Get URL from download metadata or construct it
            try:
                with open(DOWNLOAD_METADATA_FILE, 'r') as f:
                    download_meta = json.load(f)
                    url = download_meta.get(source, {}).get('files', {}).get(relative_path, {}).get('url', '')
            except:
                url = f"{SOURCES[source]['base_url']}/{relative_path}"
            
            checksum = calculate_checksum(file_path)
            self.registry.register_file(
                source=source,
                file_path=relative_path,
                url=url,
                checksum=checksum,
                chunk_count=len(chunks)
            )
        
        return len(chunks)
    
    def index_source(self, source: str) -> Dict:
        """Index all files for a given source."""
        config = SOURCES[source]
        docs_dir = config['docs_dir']
        
        if not docs_dir.exists():
            print(f"Docs directory not found: {docs_dir}")
            return {'files_indexed': 0, 'chunks_indexed': 0, 'errors': []}
        
        # Find all markdown files
        md_files = list(docs_dir.rglob('*.md'))
        total_files = len(md_files)
        
        # Full indexing (Phase 2: removed 20% limit for production)
        # limit = max(1, int(total_files * 0.20))
        # md_files = md_files[:limit]
        
        self.logger.info(f"Found {total_files} total files, indexing all {len(md_files)} files from {source}")
        print(f"\nIndexing {len(md_files)} files from {source}...")
        
        # Progress monitoring
        try:
            from tqdm import tqdm
            has_tqdm = True
        except ImportError:
            has_tqdm = False
        
        files_indexed = 0
        chunks_indexed = 0
        errors = []
        
        file_iter = tqdm(md_files, desc=f"Indexing {source}") if has_tqdm else md_files
        
        for file_path in file_iter:
            try:
                if has_tqdm:
                    file_iter.set_postfix(file=file_path.name[:30])
                else:
                    print(f"[{files_indexed+1}/{len(md_files)}] Indexing {file_path.name}...")
                
                chunk_count = self.index_file(file_path, source)
                chunks_indexed += chunk_count
                files_indexed += 1
                
                if has_tqdm:
                    file_iter.set_postfix(chunks=chunks_indexed, files=files_indexed)
            except Exception as e:
                error_msg = f"Error indexing {file_path}: {e}"
                self.logger.error(error_msg, exc_info=True)
                if has_tqdm:
                    file_iter.set_postfix(error="ERROR")
                else:
                    print(f"  ERROR: {error_msg}")
                errors.append(error_msg)
        
        return {
            'source': source,
            'files_indexed': files_indexed,
            'chunks_indexed': chunks_indexed,
            'errors': errors
        }
    
    def index_all(self) -> Dict:
        """Index all sources."""
        print("=" * 60)
        print("Indexing Documentation")
        print("=" * 60)
        
        results = {}
        total_files = 0
        total_chunks = 0
        
        for source_name in SOURCES.keys():
            result = self.index_source(source_name)
            results[source_name] = result
            total_files += result['files_indexed']
            total_chunks += result['chunks_indexed']
        
        # Save indexing metadata
        metadata_file = METADATA_DIR / 'indexing_metadata.json'
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump({
                'total_files_indexed': total_files,
                'total_chunks_indexed': total_chunks,
                'sources': results
            }, f, indent=2, ensure_ascii=False)
        
        print("\n" + "=" * 60)
        print(f"Indexing completed!")
        print(f"Total files indexed: {total_files}")
        print(f"Total chunks indexed: {total_chunks}")
        print(f"Metadata saved to: {metadata_file}")
        print("=" * 60)
        
        return results


def main():
    indexer = DocumentationIndexer()
    indexer.index_all()


if __name__ == "__main__":
    main()

