"""Question routing chain to determine RAG vs web search."""
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field

from config import LLM_MODEL
from graph.logging_config import logger


class RouteDecision(BaseModel):
    """Structured output for routing decision."""
    decision: str = Field(description="Either 'rag' for vector store or 'web_search' for web search")
    reasoning: str = Field(description="Brief explanation for the routing decision")


def create_router_chain():
    """Create question routing chain."""
    llm = ChatGoogleGenerativeAI(
        model=LLM_MODEL,
        temperature=0,
    )
    
    # Use structured output for consistent routing
    structured_llm = llm.with_structured_output(RouteDecision)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert at routing user questions to the right data source.
        
Given a question, determine if it should be answered using:
1. RAG (vector store) - for questions about documentation, APIs, code examples, technical concepts
2. Web search - for general knowledge, current events, or topics not in documentation

For offline mode, always route to RAG since web search is disabled.

Respond with your decision and reasoning."""),
        ("human", "Question: {question}")
    ])
    
    chain = prompt | structured_llm
    
    return chain


# Create the chain instance
route_question_chain = create_router_chain()


def route_question(question: str) -> dict:
    """
    Route a question to determine if RAG or web search should be used.
    
    Args:
        question: User's question
        
    Returns:
        dict with 'decision' ('rag' or 'web_search') and 'reasoning'
    """
    from config import WEB_SEARCH_ENABLED
    
    logger.info(f"Routing question: {question[:100]}...")
    
    # For offline mode, always return 'rag'
    # In future, can use chain result for online mode
    if WEB_SEARCH_ENABLED:
        try:
            result = route_question_chain.invoke({"question": question})
            decision = result.decision
            reasoning = result.reasoning
            logger.info(f"Router decision: {decision} - {reasoning}")
        except Exception as e:
            logger.error(f"Router chain error: {e}, defaulting to RAG")
            decision = "rag"
            reasoning = f"Router error, defaulting to RAG: {str(e)}"
    else:
        decision = "rag"
        reasoning = "Offline mode - using vector store only"
        logger.info(f"Router decision: {decision} (offline mode)")
    
    return {
        "decision": decision,
        "reasoning": reasoning
    }


if __name__ == "__main__":
    """Test the router chain when run directly"""
    import argparse
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from graph.test_mode_helper import set_mode, get_current_mode
    from pprint import pprint
    
    parser = argparse.ArgumentParser(description="Test Router Chain")
    parser.add_argument("--mode", choices=["offline", "online"], 
                       default=None, help="Test mode (default: current AGENT_MODE)")
    args = parser.parse_args()
    
    mode = args.mode or get_current_mode()
    
    with set_mode(mode):
        print(f"Testing Router Chain ({mode.upper()} MODE)...")
        print("="*50)
    
    test_questions = [
        "What is LangGraph?",
        "How do I create a state graph?",
        "What is the weather today?",  # Should route to web search in online mode
    ]
    
    for question in test_questions:
        print(f"\nQuestion: {question}")
        result = route_question(question)
        print(f"Decision: {result['decision']}")
        print(f"Reasoning: {result['reasoning']}")
        print("-" * 50)
    
    print("\nTest completed!")

