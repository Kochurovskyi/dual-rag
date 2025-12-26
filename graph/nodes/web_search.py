"""Web search node for LangGraph workflow."""
from langchain_core.documents import Document
from graph.state import GraphState
from graph.logging_config import logger


def web_search(state: GraphState) -> GraphState:
    """
    Perform web search for the question.
    Only works in online mode (WEB_SEARCH_ENABLED=True).
    """
    # Import at function level to allow patching in tests
    from config import TAVILY_API_KEY, WEB_SEARCH_ENABLED
    
    question = state["question"]
    
    logger.info(f"[MODE] Web search node called (WEB_SEARCH_ENABLED={WEB_SEARCH_ENABLED})")
    
    if not WEB_SEARCH_ENABLED:
        logger.warning("[MODE] Web search disabled (offline mode). Skipping Tavily search.")
        logger.info("[MODE] AGENT_MODE=offline, web search not available")
        state["web_search_results"] = []
        state["metadata"] = state.get("metadata", {})
        state["metadata"]["web_search_performed"] = False
        state["metadata"]["web_search_reason"] = "Offline mode - web search disabled"
        return state
    
    logger.info(f"[MODE] Performing Tavily web search (online mode)")
    logger.info(f"[MODE] Query: '{question[:100] if len(question) > 100 else question}...'")
    
    try:
        from tavily import TavilyClient
        
        if not TAVILY_API_KEY:
            logger.error("[MODE] TAVILY_API_KEY not configured. Skipping Tavily web search.")
            state["web_search_results"] = []
            state["metadata"] = state.get("metadata", {})
            state["metadata"]["web_search_performed"] = False
            state["metadata"]["web_search_reason"] = "TAVILY_API_KEY not configured"
            return state
        
        logger.info("[MODE] Initializing Tavily client...")
        # Initialize Tavily client
        client = TavilyClient(api_key=TAVILY_API_KEY)
        
        logger.info("[MODE] Calling Tavily API...")
        
        # Enhance query for better results
        # Only add "LangGraph" or "LangChain" context if question is about general concepts
        # Don't add if question already specifies a framework or is about general topics
        enhanced_query = question
        question_lower = question.lower()
        
        # Don't enhance if question is about general topics (best practices, how to, what is, etc.)
        # or if it already mentions a specific framework
        general_topics = ["best practices", "how to", "what is", "what are", "explain", "guide"]
        is_general_topic = any(topic in question_lower for topic in general_topics)
        has_framework = "langgraph" in question_lower or "langchain" in question_lower or "langsmith" in question_lower
        
        # Only enhance if it's a specific technical question without framework context
        if not has_framework and not is_general_topic:
            enhanced_query = f"LangGraph {question}"
            logger.info(f"[DEBUG] Enhanced query: '{enhanced_query}'")
        else:
            logger.info(f"[DEBUG] Using original query (no enhancement needed): '{enhanced_query}'")
        
        # Perform web search with improved parameters
        search_results = client.search(
            query=enhanced_query,
            max_results=5,  # Increased from 3 to get more options
            search_depth="advanced",  # Changed from "basic" for better content extraction
            include_domains=[
                "langchain-ai.github.io",
                "docs.langchain.com",
                "python.langchain.com",
                "github.com/langchain-ai"
            ]  # Restrict to documentation domains
        )
        logger.info(f"[DEBUG] Tavily search params: max_results=5, search_depth=advanced, include_domains=langchain-ai.github.io,docs.langchain.com,python.langchain.com,github.com/langchain-ai")
        results_list = search_results.get("results", [])
        logger.info(f"[MODE] Tavily API returned {len(results_list)} results")
        
        # Convert search results to LangChain Documents
        web_docs = []
        for i, result in enumerate(results_list, 1):
            content = result.get("content", "")
            url = result.get("url", "")
            title = result.get("title", "")
            score = result.get("score", 0.0)
            
            logger.info(f"[DEBUG] Tavily result {i}: title='{title[:60]}...', url={url}, score={score}, content_length={len(content)}")
            
            doc = Document(
                page_content=content,
                metadata={
                    "source": "web_search",
                    "url": url,
                    "title": title,
                    "score": score
                }
            )
            web_docs.append(doc)
        
        state["web_search_results"] = web_docs
        state["metadata"] = state.get("metadata", {})
        state["metadata"]["web_search_performed"] = True
        state["metadata"]["web_search_count"] = len(web_docs)
        
        logger.info(f"[MODE] Tavily web search completed successfully: {len(web_docs)} results")
        logger.info(f"[MODE] Online mode: Using Tavily for web search")
        
    except ImportError:
        logger.error("[MODE] tavily-python not installed. Install with: pip install tavily-python")
        state["web_search_results"] = []
        state["metadata"] = state.get("metadata", {})
        state["metadata"]["web_search_performed"] = False
        state["metadata"]["web_search_reason"] = "tavily-python not installed"
    except Exception as e:
        logger.error(f"[MODE] Tavily web search failed: {e}")
        state["web_search_results"] = []
        state["metadata"] = state.get("metadata", {})
        state["metadata"]["web_search_performed"] = False
        state["metadata"]["web_search_reason"] = str(e)
    
    return state


if __name__ == "__main__":
    """Test the web_search function when run directly"""
    import argparse
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from graph.test_mode_helper import set_mode, get_current_mode
    from pprint import pprint
    from graph.state import GraphState
    
    parser = argparse.ArgumentParser(description="Test Web Search Node")
    parser.add_argument("--mode", choices=["offline", "online"], 
                       default=None, help="Test mode (default: current AGENT_MODE)")
    args = parser.parse_args()
    mode = args.mode or get_current_mode()
    with set_mode(mode):
        try:
            # Re-import config to get updated values
            import importlib
            import config
            importlib.reload(config)
            
            print(f"Testing web_search function ({mode.upper()} MODE)...")
            print("="*50)
            
            # Test with a sample question
            question = "What is the latest news about AI?"
            print(f"Question: {question}")
            print(f"WEB_SEARCH_ENABLED: {config.WEB_SEARCH_ENABLED}")
            print(f"TAVILY_API_KEY configured: {bool(config.TAVILY_API_KEY)}")
            
            # Create state
            state: GraphState = {
                "question": question,
                "web_search": True,
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
            
            # Perform web search
            result = web_search(state)
            
            print(f"\nWeb search performed: {result['metadata'].get('web_search_performed', False)}")
            print(f"Results count: {len(result['web_search_results'])}")
            print(f"Reason: {result['metadata'].get('web_search_reason', 'N/A')}")
            if result['web_search_results']:
                print("\nFirst result preview:")
                print("-" * 30)
                print(f"Title: {result['web_search_results'][0].metadata.get('title', 'N/A')}")
                print(f"URL: {result['web_search_results'][0].metadata.get('url', 'N/A')}")
                print(f"Content: {result['web_search_results'][0].page_content[:200]}...")
            
            print("\nTest completed!")
        except Exception as e:
            print(f"Test failed: {e}")
            import traceback
            traceback.print_exc()

