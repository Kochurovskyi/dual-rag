"""Test the retrieve_documents node when run directly"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from pprint import pprint
from graph.graph import retrieve_documents
from graph.state import GraphState


if __name__ == "__main__":
    """Test the retrieve_documents function when run directly"""
    import argparse
    from graph.test_mode_helper import set_mode, get_current_mode
    
    parser = argparse.ArgumentParser(description="Test Retrieve Node")
    parser.add_argument("--mode", choices=["offline", "online"], 
                       default=None, help="Test mode (default: current AGENT_MODE)")
    args = parser.parse_args()
    
    mode = args.mode or get_current_mode()
    
    with set_mode(mode):
        try:
            print(f"Testing retrieve_documents function ({mode.upper()} MODE)...")
            print("="*50)
            
            # Test with a real question
            question = "What is LangGraph?"
            print(f"Question: {question}")
            
            # Create state
            state: GraphState = {
                "question": question,
                "web_search": False,
                "web_search_results": [],
                "documents": [],
                "document_scores": [],
                "graded_documents": [],
                "grading_scores": [],
                "generation": "",
                "generation_sources": [],
                "is_grounded": False,
                "hallucination_score": 0.0,
                "retries": 0,
                "metadata": {}
            }
            
            # Retrieve documents
            result = retrieve_documents(state)
            
            print(f"\nRetrieved {len(result['documents'])} documents")
            print(f"Document scores: {result.get('document_scores', [])[:5]}")  # Show first 5 scores
            
            if result['documents']:
                print("\nFirst document preview:")
                print("-" * 30)
                print(f"Content: {result['documents'][0].page_content[:200]}...")
                print(f"Source: {result['documents'][0].metadata.get('file_path', 'N/A')}")
                print(f"Score: {result['document_scores'][0] if result['document_scores'] else 'N/A'}")
            
            print("\nTest completed successfully!")
            
        except Exception as e:
            print(f"Test failed: {e}")
            import traceback
            traceback.print_exc()

