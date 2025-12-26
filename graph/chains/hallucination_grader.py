"""Hallucination detection chain."""
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

from config import LLM_MODEL
from graph.logging_config import logger


class GradeHallucination(BaseModel):
    """Structured output for hallucination detection."""
    binary_score: str = Field(description="Either 'yes' (grounded) or 'no' (hallucinated)")
    reasoning: str = Field(description="Brief explanation for the grade")


def create_hallucination_grader_chain():
    """Create hallucination detection chain."""
    llm = ChatGoogleGenerativeAI(
        model=LLM_MODEL,
        temperature=0,
    )
    
    # Use structured output for consistent detection
    structured_llm = llm.with_structured_output(GradeHallucination)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a grader assessing whether an answer is grounded in the provided documents.
            Given a question, an answer, and source documents, determine if the answer is grounded in the documents.
            An answer is grounded if it can be supported by information in the source documents.
            Respond with:
            - 'yes' if the answer is grounded in the documents
            - 'no' if the answer contains information not found in the documents (hallucinated)
            Be strict in your assessment. Only mark as grounded if the answer can be directly supported by the documents."""),
                    ("human", """Question: {question}
            Answer: {answer}
            Source Documents:
            {documents}
            Is the answer grounded in the source documents? Respond with 'yes' or 'no'.""")
                ])
    
    chain = prompt | structured_llm
    return chain


# Create the chain instance
check_hallucination_chain = create_hallucination_grader_chain()


def check_hallucination(question: str, answer: str, documents: list) -> dict:
    """
    Check if an answer is grounded in source documents.
    Args:
        question: User's question
        answer: Generated answer
        documents: List of source document contents
    Returns:
        dict with 'binary_score' ('yes' or 'no') and 'reasoning'
    """
    logger.info(f"Checking hallucination for answer (length: {len(answer)} chars, docs: {len(documents)})")
    
    if not documents:
        logger.warning("No documents provided for hallucination check")
        return {
            "binary_score": "no",
            "reasoning": "No documents provided for grounding check"
        }
    # Format documents for prompt
    docs_text = "\n\n---\n\n".join([
        f"Document {i+1}:\n{doc}" for i, doc in enumerate(documents)
    ])
    try:
        result = check_hallucination_chain.invoke({
            "question": question,
            "answer": answer,
            "documents": docs_text
        })
        score = result.binary_score
        reasoning = result.reasoning
        is_grounded = score.lower() == "yes"
        logger.info(f"Hallucination check: {'Grounded' if is_grounded else 'Hallucinated'} - {reasoning[:100]}...")
        return {
            "binary_score": score,
            "reasoning": reasoning
        }
    except Exception as e:
        logger.error(f"Error checking hallucination: {e}")
        # Default to hallucinated on error (safer)
        return {
            "binary_score": "no",
            "reasoning": f"Hallucination check error: {str(e)}"
        }


def main(mode=None):
    """Test the hallucination grader with sample queries"""
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from graph.test_mode_helper import set_mode as set_mode_helper, get_current_mode
    
    test_mode = mode or get_current_mode()
    
    with set_mode_helper(test_mode):
        print(f"Testing Hallucination Grader ({test_mode.upper()} MODE)...")
        print("="*50)
    
    try:
        from query_engine import QueryEngine
        from graph.chains.generation import generate_answer
        
        # Test with relevant query and generation
        question = "What is LangGraph?"
        print(f"Question: {question}")
        
        # Retrieve documents
        query_engine = QueryEngine()
        search_results = query_engine.search(question)
        docs_content = [result.get("content", "") for result in search_results[:3]]
        
        if len(docs_content) < 1:
            print(f"No documents found for query: {question}")
            return
        
        print(f"Retrieved {len(docs_content)} documents")
        
        # Generate a response using the generation chain
        generation = generate_answer(question, docs_content)
        print(f"\nGenerated response: {generation[:100]}...")
        
        # Test hallucination grader
        result = check_hallucination(question, generation, docs_content)
        print(f"\nGrounded in facts: {result['binary_score']}")
        print(f"Reasoning: {result['reasoning']}")
        print(f"Test passed: {result['binary_score'] == 'yes'}")
        
        # Test with hallucinated content
        print("\n" + "="*50)
        print("Testing with hallucinated content...")
        print("="*50)
        hallucinated_generation = "LangGraph is a Python library used for cooking recipes and food preparation."
        result2 = check_hallucination(question, hallucinated_generation, docs_content)
        print(f"Hallucinated response: {hallucinated_generation}")
        print(f"Grounded in facts: {result2['binary_score']}")
        print(f"Reasoning: {result2['reasoning']}")
        print(f"Test passed: {result2['binary_score'] == 'no'}")
        
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Test Hallucination Grader")
    parser.add_argument("--mode", choices=["offline", "online"], 
                       default=None, help="Test mode (default: current AGENT_MODE)")
    args = parser.parse_args()
    main(mode=args.mode)

