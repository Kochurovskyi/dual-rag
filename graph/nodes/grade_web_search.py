"""Grade web search results for relevancy to the question."""
from langchain_core.documents import Document
from graph.state import GraphState
from graph.logging_config import logger
from graph.chains.retrieval_grader import grade_document


def grade_web_search_results(state: GraphState) -> GraphState:
    """
    Grade web search results for relevance to the question using LLM.
    Filters out irrelevant results before generation.
    """
    logger.info("[MODE] Checking web search results relevance to question")
    question = state["question"]
    web_search_results = state.get("web_search_results", [])
    
    if not web_search_results:
        logger.warning("[MODE] No web search results to grade")
        state["graded_web_search_results"] = []
        state["web_search_grading_scores"] = []
        state["metadata"] = state.get("metadata", {})
        state["metadata"]["web_search_graded_count"] = 0
        state["metadata"]["web_search_total_count"] = 0
        state["metadata"]["web_search_filtered_count"] = 0
        return state
    
    logger.info(f"[MODE] Grading {len(web_search_results)} web search results")
    
    # Grade each web search result
    graded_results = []
    grading_scores = []
    
    for i, doc in enumerate(web_search_results):
        title = doc.metadata.get('title', 'Unknown')[:50]
        url = doc.metadata.get('url', 'Unknown')
        logger.info(f"[MODE] Grading web search result {i+1}/{len(web_search_results)}: {title}...")
        logger.debug(f"[DEBUG] URL: {url}")
        logger.debug(f"[DEBUG] Content preview: {doc.page_content[:200]}...")
        
        # Grade document for relevance
        grade_result = grade_document(question, doc.page_content)
        
        logger.info(f"[DEBUG] Grade result for result {i+1}: binary_score={grade_result['binary_score']}, reasoning={grade_result.get('reasoning', '')[:150]}...")
        
        # If relevant (binary_score == 'yes'), keep it
        if grade_result["binary_score"].lower() == "yes":
            graded_results.append(doc)
            # Use Tavily score if available, otherwise use grading result
            tavily_score = doc.metadata.get("score", 0.5)
            grading_scores.append(tavily_score)
            logger.info(f"[MODE] Web search result {i+1} is RELEVANT: {grade_result.get('reasoning', '')[:100]}...")
        else:
            logger.info(f"[MODE] Web search result {i+1} is NOT RELEVANT: {grade_result.get('reasoning', '')[:100]}...")
    
    state["graded_web_search_results"] = graded_results
    state["web_search_grading_scores"] = grading_scores
    state["metadata"] = state.get("metadata", {})
    state["metadata"]["web_search_graded_count"] = len(graded_results)
    state["metadata"]["web_search_total_count"] = len(web_search_results)
    state["metadata"]["web_search_filtered_count"] = len(web_search_results) - len(graded_results)
    
    logger.info(f"[MODE] Graded {len(web_search_results)} web search results, {len(graded_results)} relevant (filtered {len(web_search_results) - len(graded_results)} irrelevant)")
    
    if len(graded_results) == 0:
        logger.warning("[MODE] No relevant web search results found after grading")
    
    return state


if __name__ == "__main__":
    """Test the grade_web_search_results function when run directly"""
    import argparse
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from graph.test_mode_helper import set_mode, get_current_mode
    from pprint import pprint
    from graph.state import GraphState
    
    parser = argparse.ArgumentParser(description="Test Web Search Grading Node")
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
            
            print(f"Testing grade_web_search_results function ({mode.upper()} MODE)...")
            print("="*50)
            
            # Create test web search results
            test_results = [
                Document(
                    page_content="LangGraph is a library for building stateful agents with LangChain.",
                    metadata={
                        "source": "web_search",
                        "url": "https://example.com/langgraph",
                        "title": "LangGraph Documentation",
                        "score": 0.9
                    }
                ),
                Document(
                    page_content="The weather today is sunny with a high of 75 degrees.",
                    metadata={
                        "source": "web_search",
                        "url": "https://example.com/weather",
                        "title": "Weather Forecast",
                        "score": 0.8
                    }
                ),
                Document(
                    page_content="Python is a programming language used for web development.",
                    metadata={
                        "source": "web_search",
                        "url": "https://example.com/python",
                        "title": "Python Guide",
                        "score": 0.7
                    }
                )
            ]
            
            question = "What is LangGraph?"
            print(f"Question: {question}")
            print(f"Web search results: {len(test_results)}")
            
            # Create state
            state: GraphState = {
                "question": question,
                "web_search": True,
                "web_search_results": test_results,
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
            
            # Grade web search results
            result = grade_web_search_results(state)
            
            print(f"\nGrading Results:")
            print(f"  Total results: {result['metadata']['web_search_total_count']}")
            print(f"  Relevant: {result['metadata']['web_search_graded_count']}")
            print(f"  Filtered: {result['metadata']['web_search_filtered_count']}")
            
            if result['graded_web_search_results']:
                print("\nRelevant Results:")
                for i, doc in enumerate(result['graded_web_search_results'], 1):
                    print(f"  {i}. {doc.metadata.get('title', 'Unknown')}")
                    print(f"     URL: {doc.metadata.get('url', 'Unknown')}")
                    print(f"     Score: {result['web_search_grading_scores'][i-1]:.2f}")
            else:
                print("\nNo relevant results found.")
            
            print("\nTest completed!")
            
        except Exception as e:
            print(f"Test failed: {e}")
            import traceback
            traceback.print_exc()

