"""Graph state definition for LangGraph workflow."""
from typing import TypedDict, List, Dict, Optional
from langchain_core.documents import Document


class GraphState(TypedDict):
    """State passed between graph nodes."""
    
    # Input
    question: str  # User's question
    
    # Routing
    web_search: bool  # Whether to use web search (False for offline mode)
    web_search_results: List[Document]  # Web search results (if used)
    
    # Web search grading
    graded_web_search_results: List[Document]  # Web search results that passed grading
    web_search_grading_scores: List[float]  # Grading scores for web search results
    
    # Document retrieval
    documents: List[Document]  # Retrieved documents from vector store (replaced, not appended)
    document_scores: List[float]  # Relevance scores for documents
    
    # Document grading
    graded_documents: List[Document]  # Documents that passed grading (replaced, not appended)
    grading_scores: List[float]  # Grading scores for each document
    
    # Generation
    generation: str  # Generated answer
    generation_sources: List[str]  # Source file paths used in generation
    
    # Hallucination detection
    is_grounded: bool  # Whether generation is grounded in documents
    hallucination_score: float  # Hallucination detection score (0-1)
    
    # Retry mechanism
    retries: int  # Number of retry attempts
    
    # Metadata
    metadata: Dict  # Additional metadata for debugging/logging


if __name__ == "__main__":
    """Test GraphState structure and validation"""
    import argparse
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from graph.test_mode_helper import set_mode, get_current_mode
    
    parser = argparse.ArgumentParser(description="Test GraphState")
    parser.add_argument("--mode", choices=["offline", "online"], 
                       default=None, help="Test mode (default: current AGENT_MODE)")
    args = parser.parse_args()
    
    mode = args.mode or get_current_mode()
    
    with set_mode(mode):
        print(f"Testing GraphState structure ({mode.upper()} MODE)...")
        print("="*50)
    
    # Test creating a valid state
    test_state: GraphState = {
        "question": "What is LangGraph?",
        "web_search": False,
        "web_search_results": [],
        "documents": [],
        "document_scores": [],
        "graded_documents": [],
        "grading_scores": [],
        "graded_web_search_results": [],
        "web_search_grading_scores": [],
        "generation": "",
        "generation_sources": [],
        "is_grounded": False,
        "hallucination_score": 0.0,
        "retries": 0,
        "metadata": {}
    }
    
    print("[OK] GraphState created successfully")
    print(f"  Question: {test_state['question']}")
    print(f"  Web search: {test_state['web_search']}")
    print(f"  Retries: {test_state['retries']}")
    print(f"  Documents: {len(test_state['documents'])}")
    print(f"  Graded documents: {len(test_state['graded_documents'])}")
    
    # Test required fields
    required_fields = [
        "question", "web_search", "web_search_results", "documents",
        "document_scores", "graded_documents", "grading_scores",
        "graded_web_search_results", "web_search_grading_scores",
        "generation", "generation_sources", "is_grounded",
        "hallucination_score", "retries", "metadata"
    ]
    
    print("\n[OK] Validating required fields:")
    for field in required_fields:
        if field in test_state:
            print(f"  [OK] {field}: {type(test_state[field]).__name__}")
        else:
            print(f"  [FAIL] Missing: {field}")
    
    print("\nTest completed successfully!")

