"""Cross-encoder reranking for better result ordering."""
from typing import List, Dict, Optional
import warnings

# Suppress warnings for optional dependency
try:
    from sentence_transformers import CrossEncoder
    HAS_CROSS_ENCODER = True
except ImportError:
    HAS_CROSS_ENCODER = False
    warnings.warn("sentence-transformers not available. Reranking will be disabled. Install with: pip install sentence-transformers")


class Reranker:
    """
    Cross-encoder reranker for improving result ordering (Phase 3.4).
    
    Uses a cross-encoder model to better understand query-document relevance
    than bi-encoder (embedding) models alone.
    """
    
    def __init__(self, model_name: str = 'cross-encoder/ms-marco-MiniLM-L-6-v2', enabled: bool = True):
        """
        Initialize reranker with cross-encoder model.
        
        Args:
            model_name: Name of the cross-encoder model to use
            enabled: Whether reranking is enabled (can disable if model not available)
        """
        self.enabled = enabled and HAS_CROSS_ENCODER
        if self.enabled:
            try:
                self.model = CrossEncoder(model_name)
                print(f"Reranker initialized with model: {model_name}")
            except Exception as e:
                print(f"Warning: Failed to initialize reranker: {e}")
                self.enabled = False
        else:
            self.model = None
            if not HAS_CROSS_ENCODER:
                print("Warning: sentence-transformers not available. Reranking disabled.")
    
    def rerank(self, query: str, results: List[Dict], top_k: int = 10) -> List[Dict]:
        """
        Rerank results using cross-encoder.
        
        Args:
            query: Search query
            results: List of result dictionaries with 'content' field
            top_k: Number of top results to return
            
        Returns:
            Reranked list of results
        """
        if not self.enabled or not results:
            return results[:top_k]
        
        if len(results) <= top_k:
            # No need to rerank if we have fewer results than top_k
            return results[:top_k]  # Ensure we return at most top_k
        
        try:
            # Prepare pairs for scoring: (query, document_content)
            pairs = [(query, result.get('content', '')) for result in results]
            
            # Score pairs (returns similarity scores, higher = better)
            scores = self.model.predict(pairs)
            
            # Sort by score (higher = better)
            reranked = sorted(
                zip(results, scores),
                key=lambda x: x[1],
                reverse=True
            )
            
            # Update results with reranking scores
            reranked_results = []
            for result, rerank_score in reranked[:top_k]:
                # Update score with reranking score (normalize to 0-1 range)
                # Cross-encoder scores can vary, so we normalize
                if rerank_score > 0:
                    # Normalize: assume scores are typically in range -5 to 5
                    normalized_score = min(1.0, max(0.0, (rerank_score + 5) / 10))
                else:
                    normalized_score = result.get('score', 0.0)
                
                # Combine original score (0.7 weight) with rerank score (0.3 weight)
                original_score = result.get('score', 0.0)
                combined_score = (original_score * 0.7) + (normalized_score * 0.3)
                
                result['score'] = combined_score
                result['distance'] = 1.0 - combined_score
                result['rerank_score'] = float(rerank_score)
                reranked_results.append(result)
            
            return reranked_results
            
        except Exception as e:
            print(f"Error during reranking: {e}")
            # Fallback: return original results
            return results[:top_k]

