"""Query engine for semantic search over indexed documentation."""
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
from pathlib import Path
import os
import logging
import asyncio

logger = logging.getLogger(__name__)

from config import (
    EMBEDDING_MODEL, USE_GOOGLE_EMBEDDINGS, CHROMA_PERSIST_DIR, SOURCES,
    TOP_K_RESULTS, MIN_SCORE, VECTOR_STORE_MODE,
    POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_VECTOR_TABLE
)
from query_expander import expand_query, extract_entities
from reranker import Reranker

# Import embedding model based on configuration
if USE_GOOGLE_EMBEDDINGS:
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    # API key is already loaded by config.py via load_dotenv()
else:
    from sentence_transformers import SentenceTransformer


class QueryEngine:
    """Semantic search engine for documentation."""
    
    def __init__(self):
        # Initialize embedding model
        if USE_GOOGLE_EMBEDDINGS:
            self.embedding_model = GoogleGenerativeAIEmbeddings(
                model=EMBEDDING_MODEL,
                task_type="RETRIEVAL_QUERY"  # Use QUERY task type for queries (768 dimensions)
            )
            print(f"[QueryEngine] Using Google embedding model: {EMBEDDING_MODEL} (RETRIEVAL_QUERY, 768 dimensions)")
        else:
            self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)
            print(f"[QueryEngine] Using sentence-transformers model: {EMBEDDING_MODEL}")
        
        # Initialize vector store based on VECTOR_STORE_MODE
        self.vector_store_mode = VECTOR_STORE_MODE
        self.postgres_vector_store = None
        self.client = None
        self.collections = {}
        
        if self.vector_store_mode == "postgres":
            # Initialize PostgreSQL vector store
            logger.info(f"[MODE] QueryEngine initialized with PostgreSQL vector store (AGENT_MODE=online)")
            logger.info(f"[MODE] PostgreSQL connection: {POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")
            logger.info(f"[MODE] PostgreSQL table: {POSTGRES_VECTOR_TABLE}")
            print(f"[QueryEngine] Using PostgreSQL vector store (mode: {VECTOR_STORE_MODE})")
            self._init_postgres()
        else:
            # Initialize ChromaDB client
            logger.info(f"[MODE] QueryEngine initialized with ChromaDB vector store (AGENT_MODE=offline)")
            logger.info(f"[MODE] ChromaDB path: {CHROMA_PERSIST_DIR}")
            print(f"[QueryEngine] Using ChromaDB vector store (mode: {VECTOR_STORE_MODE})")
            self._init_chroma()
        
        # Initialize reranker (Phase 3.4)
        self.reranker = Reranker(enabled=True)
    
    def _init_postgres(self):
        """Initialize PostgreSQL vector store."""
        try:
            from langchain_postgres import PGEngine, PGVectorStore
            
            # Fix Windows event loop issue
            if hasattr(asyncio, 'WindowsProactorEventLoopPolicy'):
                asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            
            # Build connection string
            connection_string = f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
            
            # Initialize PGEngine
            engine = PGEngine.from_connection_string(url=connection_string)
            
            # Initialize table if it doesn't exist (vector size: 3072 for RETRIEVAL_DOCUMENT embeddings)
            VECTOR_SIZE = 3072
            try:
                engine.init_vectorstore_table(table_name=POSTGRES_VECTOR_TABLE, vector_size=VECTOR_SIZE)
                logger.info(f"[MODE] PostgreSQL table '{POSTGRES_VECTOR_TABLE}' initialized (vector_size={VECTOR_SIZE})")
            except Exception as e:
                if "already exists" in str(e).lower():
                    logger.info(f"[MODE] PostgreSQL table '{POSTGRES_VECTOR_TABLE}' already exists, continuing...")
                else:
                    raise
            
            # Initialize embeddings (RETRIEVAL_DOCUMENT to match stored embeddings)
            # Note: PostgreSQL stores RETRIEVAL_DOCUMENT (3072 dims), so we must use the same for queries
            # This differs from ChromaDB which uses RETRIEVAL_QUERY (768 dims) for queries
            query_embeddings = GoogleGenerativeAIEmbeddings(
                model=EMBEDDING_MODEL,
                task_type="RETRIEVAL_DOCUMENT"
            )
            
            # Create vector store
            self.postgres_vector_store = PGVectorStore.create_sync(
                engine=engine,
                table_name=POSTGRES_VECTOR_TABLE,
                embedding_service=query_embeddings
            )
            
            logger.info(f"[MODE] PostgreSQL vector store initialized successfully (table: {POSTGRES_VECTOR_TABLE})")
            logger.info(f"[MODE] Using RETRIEVAL_DOCUMENT embeddings (3072 dimensions) for PostgreSQL queries")
        except Exception as e:
            logger.error(f"[MODE] Failed to initialize PostgreSQL vector store: {e}")
            raise
    
    def _init_chroma(self):
        """Initialize ChromaDB client and collections."""
        self.client = chromadb.PersistentClient(
            path=str(CHROMA_PERSIST_DIR),
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get collections
        for source_name, config in SOURCES.items():
            collection_name = config['collection_name']
            try:
                self.collections[source_name] = self.client.get_collection(
                    name=collection_name
                )
            except Exception:
                print(f"Warning: Collection {collection_name} not found. Run indexer first.")
                self.collections[source_name] = None
    
    def search(
        self,
        query: str,
        source: Optional[str] = None,
        top_k: int = TOP_K_RESULTS,
        min_score: float = MIN_SCORE,
        use_expansion: bool = True,
        use_metadata_boost: bool = True,
        use_hybrid: bool = True,
        use_reranking: bool = True
    ) -> List[Dict]:
        """
        Search documentation and return results with Phase 3 improvements.
        
        Args:
            query: Search query
            source: Optional source filter
            top_k: Number of results to return
            min_score: Minimum similarity score
            use_expansion: Use query expansion (Phase 3.1)
            use_metadata_boost: Use metadata boosting (Phase 3.3)
        """
        # Route to PostgreSQL or ChromaDB based on vector store mode
        if self.vector_store_mode == "postgres":
            return self._search_postgres(
                query, source, top_k, min_score, use_expansion,
                use_metadata_boost, use_hybrid, use_reranking
            )
        else:
            return self._search_chroma(
                query, source, top_k, min_score, use_expansion,
                use_metadata_boost, use_hybrid, use_reranking
            )
    
    def _search_postgres(
        self,
        query: str,
        source: Optional[str],
        top_k: int,
        min_score: float,
        use_expansion: bool,
        use_metadata_boost: bool,
        use_hybrid: bool,
        use_reranking: bool
    ) -> List[Dict]:
        """Search PostgreSQL vector store."""
        logger.info(f"[MODE] Searching PostgreSQL vector store (online mode)")
        logger.info(f"[MODE] Query: '{query[:100]}...' (top_k={top_k}, source={source})")
        
        # Phase 3.1: Query expansion
        if use_expansion:
            expanded_queries = expand_query(query)
            logger.info(f"[DEDUP] Query expansion: {len(expanded_queries)} queries generated")
        else:
            expanded_queries = [query]
        
        all_results = []
        
        # Search with all expanded queries
        for exp_query in expanded_queries:
            try:
                logger.debug(f"[MODE] PostgreSQL search: '{exp_query[:50]}...'")
                # Use similarity_search_with_score to get scores
                docs_with_scores = self.postgres_vector_store.similarity_search_with_score(
                    query=exp_query,
                    k=top_k * 3  # Get more results for deduplication and filtering
                )
                logger.info(f"[MODE] PostgreSQL returned {len(docs_with_scores)} raw results (requested k={top_k * 3})")
                
                # Convert to ChromaDB-like format
                filtered_count = 0
                for doc, score in docs_with_scores:
                    # Convert distance to similarity (lower distance = higher similarity)
                    similarity = 1.0 - min(score, 1.0)  # Ensure similarity is between 0 and 1
                    
                    if similarity < min_score:
                        filtered_count += 1
                        logger.debug(f"[MODE] Filtered result: similarity={similarity:.4f} < min_score={min_score}, distance={score:.4f}")
                        continue
                    
                    # Extract metadata
                    metadata = doc.metadata.copy()
                    
                    # Filter by source if specified
                    if source and metadata.get('source') != source:
                        continue
                    
                    # Generate ID from metadata if not present (PostgreSQL doesn't store ID in metadata)
                    doc_id = metadata.get('id', '')
                    if not doc_id:
                        # Generate ID same way as ChromaDB: source:file_path:chunk_index
                        doc_source = metadata.get('source', 'unknown')
                        doc_file_path = metadata.get('file_path', '')
                        doc_chunk_index = metadata.get('chunk_index', 0)
                        doc_id = f"{doc_source}:{doc_file_path}:{doc_chunk_index}"
                    
                    result = {
                        'source': metadata.get('source', 'unknown'),
                        'file_path': metadata.get('file_path', ''),
                        'heading_path': metadata.get('heading_path', ''),
                        'heading': metadata.get('heading', ''),
                        'chunk_index': metadata.get('chunk_index', 0),
                        'has_code': metadata.get('has_code', False),
                        'code_language': metadata.get('code_language'),
                        'content': doc.page_content,
                        'score': similarity,
                        'distance': score,
                        'id': doc_id,
                        'metadata': metadata
                    }
                    all_results.append(result)
                    logger.debug(f"[MODE] Added result: source={result['source']}, similarity={similarity:.4f}, distance={score:.4f}")
                
                if filtered_count > 0:
                    logger.info(f"[MODE] Filtered {filtered_count} results below min_score={min_score}")
                added_count = len(docs_with_scores) - filtered_count
                logger.info(f"[MODE] Added {added_count} results from this query")
            except Exception as e:
                logger.error(f"Error querying PostgreSQL: {e}")
                import traceback
                logger.error(traceback.format_exc())
                continue
        
        # Deduplicate by ID and content (same as ChromaDB)
        seen_ids = set()
        seen_content = set()
        unique_results = []
        duplicates_removed = 0
        for result in all_results:
            content_normalized = result.get('content', '').strip().lower()
            content_hash = hash(content_normalized)
            
            if result['id'] not in seen_ids and content_hash not in seen_content:
                seen_ids.add(result['id'])
                seen_content.add(content_hash)
                unique_results.append(result)
            else:
                duplicates_removed += 1
        
        if duplicates_removed > 0:
            logger.info(f"[DEDUP] Initial: Removed {duplicates_removed} duplicates from {len(all_results)} results, kept {len(unique_results)} unique")
        
        logger.info(f"[MODE] PostgreSQL search completed: {len(unique_results)} unique results")
        
        # Phase 3.2: Hybrid Search (keyword search not available for PostgreSQL, skip)
        # Note: PostgreSQL doesn't support keyword search easily, so we skip hybrid for now
        if use_hybrid:
            logger.info("[MODE] Hybrid search skipped for PostgreSQL (keyword search not implemented)")
        
        # Phase 3.3: Metadata boosting
        if use_metadata_boost:
            unique_results = self._boost_by_metadata(query, unique_results)
        
        # Phase 3.4: Cross-encoder reranking
        if use_reranking and self.reranker.enabled:
            unique_results = self.reranker.rerank(query, unique_results, top_k=top_k * 2)
        
        # Sort by score and return top_k
        unique_results.sort(key=lambda x: x['score'], reverse=True)
        return unique_results[:top_k]
    
    def _search_chroma(
        self,
        query: str,
        source: Optional[str],
        top_k: int,
        min_score: float,
        use_expansion: bool,
        use_metadata_boost: bool,
        use_hybrid: bool,
        use_reranking: bool
    ) -> List[Dict]:
        """Search ChromaDB vector store (original implementation)."""
        logger.info(f"[MODE] Searching ChromaDB vector store (offline mode)")
        logger.info(f"[MODE] Query: '{query[:100]}...' (top_k={top_k}, source={source})")
        
        # Phase 3.1: Query expansion
        if use_expansion:
            expanded_queries = expand_query(query)
            logger.info(f"[DEDUP] Query expansion: {len(expanded_queries)} queries generated")
        else:
            expanded_queries = [query]
        
        all_results = []
        
        # Search in specified source or all sources
        sources_to_search = [source] if source else list(SOURCES.keys())
        logger.info(f"[DEDUP] Searching in {len(sources_to_search)} sources: {sources_to_search}")
        
        for source_name in sources_to_search:
            collection = self.collections.get(source_name)
            if collection is None:
                continue
            
            # Build where clause for metadata filtering
            where_clause = {}
            if source:
                where_clause['source'] = source
            
            # Phase 3.1: Search with all expanded queries
            for idx, exp_query in enumerate(expanded_queries):
                # Generate query embedding
                if USE_GOOGLE_EMBEDDINGS:
                    query_embedding = self.embedding_model.embed_query(exp_query)
                else:
                    query_embedding = self.embedding_model.encode(
                        exp_query,
                        normalize_embeddings=True
                    ).tolist()
                
                # Query ChromaDB (get more results for deduplication)
                n_results_per_query = top_k * 2 if len(expanded_queries) > 1 else top_k
                try:
                    results = collection.query(
                        query_embeddings=[query_embedding],
                        n_results=n_results_per_query,
                        where=where_clause if where_clause else None,
                        include=['documents', 'metadatas', 'distances']
                    )
                    
                    results_count = len(results['ids'][0]) if results['ids'] else 0
                    logger.debug(f"[DEDUP] Query {idx+1}/{len(expanded_queries)} ('{exp_query[:50]}...'): {results_count} results from {source_name}")
                    
                    # Process results
                    if results['ids'] and len(results['ids'][0]) > 0:
                        for i in range(len(results['ids'][0])):
                            distance = results['distances'][0][i]
                            # Convert distance to similarity score
                            score = 1 - distance if distance <= 1 else 0
                            
                            if score >= min_score:
                                result = {
                                    'source': source_name,
                                    'file_path': results['metadatas'][0][i]['file_path'],
                                    'heading_path': results['metadatas'][0][i].get('heading_path', ''),
                                    'heading': results['metadatas'][0][i].get('heading', ''),
                                    'chunk_index': results['metadatas'][0][i].get('chunk_index', 0),
                                    'has_code': results['metadatas'][0][i].get('has_code', False),
                                    'code_language': results['metadatas'][0][i].get('code_language'),
                                    'content': results['documents'][0][i],
                                    'score': score,
                                    'distance': distance,
                                    'id': results['ids'][0][i],
                                    'metadata': results['metadatas'][0][i]  # Full metadata for boosting
                                }
                                all_results.append(result)
                except Exception as e:
                    logger.error(f"Error querying {source_name}: {e}")
                    continue
        
        # Deduplicate by ID and content (handle Python/JS duplicates)
        seen_ids = set()
        seen_content = set()  # Track content hashes to avoid duplicates
        unique_results = []
        duplicates_removed = 0
        for result in all_results:
            # Create content hash for deduplication (normalize whitespace)
            content_normalized = result.get('content', '').strip().lower()
            content_hash = hash(content_normalized)
            
            # Skip if we've seen this ID or this exact content
            if result['id'] not in seen_ids and content_hash not in seen_content:
                seen_ids.add(result['id'])
                seen_content.add(content_hash)
                unique_results.append(result)
            else:
                duplicates_removed += 1
        
        if duplicates_removed > 0:
            logger.info(f"[DEDUP] Initial: Removed {duplicates_removed} duplicates from {len(all_results)} results, kept {len(unique_results)} unique")
        else:
            logger.info(f"[DEDUP] Initial: {len(all_results)} results, all unique")
        
        # Phase 3.2: Hybrid Search - combine semantic + keyword search
        if use_hybrid:
            keyword_results = self._keyword_search(query, sources_to_search, top_k * 2)
            logger.info(f"[DEDUP] Hybrid: Semantic={len(unique_results)}, Keyword={len(keyword_results)}")
            # Merge semantic and keyword results
            before_merge = len(unique_results)
            unique_results = self._merge_hybrid_results(unique_results, keyword_results)
            after_merge = len(unique_results)
            logger.info(f"[DEDUP] Merge: {before_merge} semantic + {len(keyword_results)} keyword → {after_merge} merged")
            # Re-deduplicate after merge (content-based)
            before_dedup = len(unique_results)
            unique_results = self._deduplicate_by_content(unique_results)
            after_dedup = len(unique_results)
            if before_dedup > after_dedup:
                logger.info(f"[DEDUP] Post-merge: Removed {before_dedup - after_dedup} duplicates, kept {after_dedup} unique")
        
        # Phase 3.3: Metadata boosting
        if use_metadata_boost:
            unique_results = self._boost_by_metadata(query, unique_results)
        
        # Sort by boosted score (descending)
        unique_results.sort(key=lambda x: x['score'], reverse=True)
        
        # Phase 3.4: Cross-encoder reranking (rerank top 2x results for better ordering)
        if use_reranking and len(unique_results) > top_k:
            # Rerank top 2x results, then return top_k
            top_results_to_rerank = unique_results[:top_k * 2]
            reranked = self.reranker.rerank(query, top_results_to_rerank, top_k)
            # Ensure we return exactly top_k (safety check)
            return reranked[:top_k] if len(reranked) > top_k else reranked
        else:
            # Return top-k results (ensure we don't return more than top_k)
            return unique_results[:top_k]
    
    def _keyword_search(self, query: str, sources: List[str], top_k: int) -> List[Dict]:
        """
        Keyword search using extracted keywords and metadata (Phase 3.2).
        
        Searches for exact keyword matches in document content and metadata.
        """
        from query_expander import extract_entities
        
        # Extract keywords from query
        query_keywords = extract_entities(query)
        # Also extract lowercase keywords from query
        query_lower = query.lower()
        query_terms = [term for term in query_lower.split() if len(term) > 3]  # Filter short words
        all_keywords = list(set(query_keywords + query_terms))
        
        if not all_keywords:
            return []
        
        keyword_results = []
        
        for source_name in sources:
            collection = self.collections.get(source_name)
            if collection is None:
                continue
            
            # Get all documents (or sample for efficiency)
            # For large collections, we might want to sample, but for now get all
            try:
                all_docs = collection.get(include=['documents', 'metadatas'])
            except Exception as e:
                print(f"Error getting documents from {source_name}: {e}")
                continue
            
            if not all_docs.get('ids') or not all_docs['ids']:
                continue
            
            scored = []
            for i, (doc_id, doc, metadata) in enumerate(zip(
                all_docs['ids'],
                all_docs['documents'],
                all_docs['metadatas']
            )):
                score = 0.0
                doc_lower = doc.lower()
                metadata_keywords = metadata.get('keywords', '').lower() if metadata.get('keywords') else ''
                heading = metadata.get('heading', '').lower() if metadata.get('heading') else ''
                
                # Count keyword matches
                for keyword in all_keywords:
                    keyword_lower = keyword.lower()
                    # Match in document content
                    if keyword_lower in doc_lower:
                        score += 1.0
                    # Boost for metadata keyword match
                    if keyword_lower in metadata_keywords:
                        score += 2.0
                    # Boost for heading match
                    if keyword_lower in heading:
                        score += 1.5
                
                if score > 0:
                    # Convert score to distance (lower = better, for consistency)
                    # Use inverse relationship: higher score = lower distance
                    distance = 1.0 / (1.0 + score)
                    similarity = 1 - distance
                    
                    scored.append({
                        'id': doc_id,
                        'source': source_name,
                        'file_path': metadata.get('file_path', ''),
                        'heading_path': metadata.get('heading_path', ''),
                        'heading': metadata.get('heading', ''),
                        'chunk_index': metadata.get('chunk_index', 0),
                        'has_code': metadata.get('has_code', False),
                        'code_language': metadata.get('code_language'),
                        'content': doc,
                        'score': similarity,
                        'distance': distance,
                        'metadata': metadata,
                        'keyword_score': score  # Store original keyword score
                    })
            
            # Sort by score (distance) - lower distance = better
            scored.sort(key=lambda x: x['distance'])
            keyword_results.extend(scored[:top_k])
        
        return keyword_results
    
    def _merge_hybrid_results(self, semantic_results: List[Dict], keyword_results: List[Dict]) -> List[Dict]:
        """
        Merge semantic and keyword search results (Phase 3.2).
        
        Combines results from both methods, giving preference to results that appear in both.
        Deduplicates by both ID and content hash to handle Python/JS duplicates.
        """
        # Create maps: by ID and by content hash
        result_map_by_id = {}
        result_map_by_content = {}  # Track by content to deduplicate Python/JS duplicates
        seen_content = set()
        
        # Add semantic results
        for result in semantic_results:
            result_id = result['id']
            content_hash = hash(result.get('content', '').strip().lower())
            
            result['semantic_score'] = result['score']
            result['keyword_score'] = 0.0
            
            # Store by ID
            result_map_by_id[result_id] = result
            
            # Store by content hash (keep first occurrence, prefer higher score)
            if content_hash not in seen_content:
                seen_content.add(content_hash)
                result_map_by_content[content_hash] = result
            else:
                # If we've seen this content, keep the one with higher score
                existing = result_map_by_content[content_hash]
                if result['score'] > existing.get('semantic_score', existing.get('score', 0)):
                    result_map_by_content[content_hash] = result
        
        # Merge keyword results
        for result in keyword_results:
            result_id = result['id']
            content_hash = hash(result.get('content', '').strip().lower())
            
            # Check if we have this content already (Python/JS duplicate)
            if content_hash in seen_content:
                # Boost existing result instead of adding duplicate
                existing = result_map_by_content[content_hash]
                if result_id in result_map_by_id:
                    # Same ID - boost it
                    combined_score = (existing.get('semantic_score', existing['score']) * 0.7) + (result['score'] * 0.3)
                    existing['score'] = min(1.0, combined_score)
                    existing['distance'] = 1.0 - existing['score']
                    existing['keyword_score'] = result.get('keyword_score', 0.0)
                    existing['in_both'] = True
                # If different ID but same content, skip (already have it)
                continue
            
            # New content - check if same ID exists
            if result_id in result_map_by_id:
                # Result appears in both - boost it
                existing = result_map_by_id[result_id]
                combined_score = (existing.get('semantic_score', existing['score']) * 0.7) + (result['score'] * 0.3)
                existing['score'] = min(1.0, combined_score)
                existing['distance'] = 1.0 - existing['score']
                existing['keyword_score'] = result.get('keyword_score', 0.0)
                existing['in_both'] = True
            else:
                # New result from keyword search only
                result['semantic_score'] = 0.0
                result['keyword_score'] = result.get('keyword_score', 0.0)
                result['in_both'] = False
                result['score'] = result['score'] * 0.6
                result['distance'] = 1.0 - result['score']
                result_map_by_id[result_id] = result
                seen_content.add(content_hash)
                result_map_by_content[content_hash] = result
        
        # Return unique results (deduplicated by content)
        return list(result_map_by_content.values())
    
    def _deduplicate_by_content(self, results: List[Dict]) -> List[Dict]:
        """
        Deduplicate results by content hash (handles Python/JS duplicates).
        Keeps the result with the highest score for each unique content.
        """
        content_map = {}
        duplicates_found = []
        for result in results:
            content_normalized = result.get('content', '').strip().lower()
            content_hash = hash(content_normalized)
            
            if content_hash not in content_map:
                content_map[content_hash] = result
            else:
                # Keep the one with higher score
                existing = content_map[content_hash]
                existing_score = existing.get('score', 0)
                new_score = result.get('score', 0)
                if new_score > existing_score:
                    duplicates_found.append({
                        'removed': existing.get('source', 'unknown'),
                        'kept': result.get('source', 'unknown'),
                        'score_diff': new_score - existing_score
                    })
                    content_map[content_hash] = result
                else:
                    duplicates_found.append({
                        'removed': result.get('source', 'unknown'),
                        'kept': existing.get('source', 'unknown'),
                        'score_diff': existing_score - new_score
                    })
        
        if duplicates_found:
            logger.debug(f"[DEDUP] Content dedup: Found {len(duplicates_found)} duplicate content blocks")
            for dup in duplicates_found[:3]:  # Log first 3
                logger.debug(f"  Removed {dup['removed']}, kept {dup['kept']} (score diff: {dup['score_diff']:.3f})")
        
        return list(content_map.values())
    
    def _boost_by_metadata(self, query: str, results: List[Dict]) -> List[Dict]:
        """
        Boost results based on metadata matches (Phase 3.3).
        
        Boosts results that have:
        - Matching topics
        - Matching keywords
        - Matching headings
        """
        # Extract query topics and keywords (simple detection)
        query_lower = query.lower()
        query_topics = []
        if 'error' in query_lower or 'retry' in query_lower:
            query_topics.append('error-handling')
        if 'best practice' in query_lower:
            query_topics.append('best-practices')
        if 'difference' in query_lower or ' vs ' in query_lower or 'compare' in query_lower:
            query_topics.append('comparison')
        if 'persistence' in query_lower or 'memory' in query_lower:
            query_topics.append('persistence')
        
        query_keywords = set(extract_entities(query))
        query_terms = set(query_lower.split())
        
        boosted = []
        for result in results:
            score = result['score']
            distance = result.get('distance', 1.0 - score)
            metadata = result.get('metadata', {})
            
            # Boost if topic matches
            result_topics = metadata.get('topics', '')
            if result_topics:
                result_topics_list = [t.strip() for t in result_topics.split(',') if t.strip()]
                topic_overlap = len(set(query_topics) & set(result_topics_list))
                if topic_overlap > 0:
                    # Significant boost for topic match (lower distance = better)
                    distance *= (1.0 - topic_overlap * 0.15)
            
            # Boost if keywords match
            result_keywords = metadata.get('keywords', '')
            if result_keywords:
                result_keywords_list = [k.strip().lower() for k in result_keywords.split(',') if k.strip()]
                keyword_overlap = len(query_keywords & set(result_keywords_list))
                if keyword_overlap > 0:
                    distance *= (1.0 - keyword_overlap * 0.1)
            
            # Boost if heading matches query terms
            heading = metadata.get('heading', '').lower()
            if heading:
                heading_terms = set(heading.split())
                heading_overlap = len(query_terms & heading_terms)
                if heading_overlap > 0:
                    distance *= (1.0 - heading_overlap * 0.05)
            
            # Update score from boosted distance
            result['score'] = 1 - distance if distance <= 1 else 0
            result['distance'] = distance
            boosted.append(result)
        
        return boosted
    
    def format_result(self, result: Dict) -> str:
        """Format a single search result for display."""
        lines = []
        
        # Header
        lines.append("=" * 80)
        lines.append(f"Source: {result['source']}")
        lines.append(f"File: {result['file_path']}")
        if result['heading_path']:
            lines.append(f"Section: {result['heading_path']}")
        lines.append(f"Score: {result['score']:.4f}")
        lines.append("-" * 80)
        
        # Content
        lines.append(result['content'])
        lines.append("=" * 80)
        lines.append("")
        
        return "\n".join(lines)
    
    def format_results(self, results: List[Dict]) -> str:
        """Format all search results for display."""
        if not results:
            return "No results found."
        
        lines = [f"Found {len(results)} result(s):\n"]
        
        for i, result in enumerate(results, 1):
            lines.append(f"Result {i}:")
            lines.append(self.format_result(result))
        
        return "\n".join(lines)

