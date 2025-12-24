"""CLI interface for LangGraph Helper Agent."""
import os
import click
from graph import app as graph_app
from graph.state import GraphState
from graph.test_mode_helper import set_mode
from config import AGENT_MODE


@click.command()
@click.argument('query', required=False)
@click.option('--mode', '-m', type=click.Choice(['offline', 'online']), 
              default=None, help='Agent mode: offline (local docs) or online (web search). '
                                 'If not specified, uses AGENT_MODE from .env or config.')
@click.option('--verbose', '-v', is_flag=True, help='Show verbose output including metadata')
@click.option('--interactive', '-i', is_flag=True, help='Interactive mode')
def main(query, mode, verbose, interactive):
    """Query documentation using LangGraph workflow."""
    
    # Determine mode
    if mode:
        selected_mode = mode
        # Override environment variable
        os.environ["AGENT_MODE"] = selected_mode
    else:
        # Use environment variable or config default
        selected_mode = os.environ.get("AGENT_MODE", AGENT_MODE).lower()
        if selected_mode not in ["offline", "online"]:
            selected_mode = "offline"  # Default fallback
    
    # Reload config to pick up mode changes
    import importlib
    import config
    importlib.reload(config)
    
    def process_question(question: str):
        """Process a single question through the graph."""
        with set_mode(selected_mode):
            try:
                if verbose:
                    print(f"Mode: {selected_mode.upper()}")
                    print(f"Question: {question}")
                    print("=" * 80)
                    print()
                
                # Create initial state
                initial_state: GraphState = {
                    "question": question,
                    "web_search": False,
                    "web_search_results": [],
                    "graded_web_search_results": [],
                    "web_search_grading_scores": [],
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
                
                # Invoke graph
                result = graph_app.invoke(initial_state)
                
                # Display result
                print("Answer:")
                print("-" * 80)
                print(result["generation"])
                print("-" * 80)
                print()
                
                # Show sources if available
                if result.get("generation_sources"):
                    print("Sources:")
                    for i, source in enumerate(result["generation_sources"], 1):
                        print(f"  {i}. {source}")
                    print()
                
                # Show metadata if verbose
                if verbose:
                    metadata = result.get("metadata", {})
                    print("Metadata:")
                    print(f"  Generation source: {metadata.get('generation_source', 'unknown')}")
                    print(f"  Generation length: {metadata.get('generation_length', 0)} characters")
                    
                    if "retrieved_count" in metadata:
                        print(f"  Documents retrieved: {metadata['retrieved_count']}")
                    if "graded_count" in metadata:
                        print(f"  Documents graded: {metadata['graded_count']}")
                    if "web_search_performed" in metadata:
                        print(f"  Web search performed: {metadata['web_search_performed']}")
                    if "web_search_count" in metadata:
                        print(f"  Web search results: {metadata['web_search_count']}")
                    
                    print(f"  Is grounded: {result.get('is_grounded', False)}")
                    print(f"  Retries: {result.get('retries', 0)}")
                    print()
                
                # Show status
                if result.get("is_grounded"):
                    print("[OK] Answer is grounded in source documents")
                else:
                    print("[WARNING] Answer may contain hallucinations (not fully grounded)")
                print()
                
            except KeyboardInterrupt:
                print("\n\nInterrupted by user.")
                raise
            except Exception as e:
                print(f"Error: {e}")
                if verbose:
                    import traceback
                    traceback.print_exc()
                raise
    
    if interactive:
        print(f"Entering interactive mode (Mode: {selected_mode.upper()}).")
        print("Type 'quit' or 'exit' to exit.")
        print("=" * 80)
        print()
        
        while True:
            try:
                user_query = input("Query: ").strip()
                
                if user_query.lower() in ['quit', 'exit', 'q']:
                    break
                
                if not user_query:
                    continue
                
                process_question(user_query)
                
            except KeyboardInterrupt:
                print("\n\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")
                if verbose:
                    import traceback
                    traceback.print_exc()
    else:
        if not query:
            print("Error: Query is required in non-interactive mode.")
            print("Usage: python cli.py [--mode offline|online] 'your query' or use --interactive")
            return
        
        process_question(query)


if __name__ == "__main__":
    main()

