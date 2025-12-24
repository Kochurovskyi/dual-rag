"""Document relevance grading chain."""
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

from config import LLM_MODEL
from graph.logging_config import logger


class GradeDocument(BaseModel):
    """Structured output for document grading."""
    binary_score: str = Field(description="Either 'yes' (relevant) or 'no' (not relevant)")
    reasoning: str = Field(description="Brief explanation for the grade")


def create_retrieval_grader_chain():
    """Create document relevance grading chain."""
    llm = ChatGoogleGenerativeAI(
        model=LLM_MODEL,
        temperature=0,
    )
    
    # Use structured output for consistent grading
    structured_llm = llm.with_structured_output(GradeDocument)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a grader assessing relevance of retrieved documents to a user question.
        
Given a question and a document, determine if the document is relevant to answering the question.

A document is relevant ONLY if:
- It directly answers the specific question asked
- It provides information that directly addresses what the user is asking for
- It contains actionable information or specific details that answer the question

A document is NOT relevant if:
- It only mentions the topic but doesn't answer the question
- It discusses related concepts but doesn't address the specific question
- It provides general information but not what was specifically asked

Be VERY strict in your grading. Only mark as 'yes' if the document actually answers the question, not just if it mentions the topic.

Respond with:
- 'yes' if the document directly answers the question
- 'no' if the document does not answer the question (even if it mentions the topic)"""),
        ("human", """Question: {question}

Document: {document}

Does this document directly answer the question? Respond with 'yes' or 'no'.""")
    ])
    
    chain = prompt | structured_llm
    
    return chain


# Create the chain instance
grade_document_chain = create_retrieval_grader_chain()


def grade_document(question: str, document: str) -> dict:
    """
    Grade a document for relevance to a question.
    
    Args:
        question: User's question
        document: Document content to grade
        
    Returns:
        dict with 'binary_score' ('yes' or 'no') and 'reasoning'
    """
    doc_preview = document[:100] + "..." if len(document) > 100 else document
    logger.debug(f"Grading document (preview: {doc_preview})")
    
    try:
        result = grade_document_chain.invoke({
            "question": question,
            "document": document
        })
        
        score = result.binary_score
        reasoning = result.reasoning
        
        logger.info(f"Document graded: {score} - {reasoning[:100]}...")
        
        return {
            "binary_score": score,
            "reasoning": reasoning
        }
    except Exception as e:
        logger.error(f"Error grading document: {e}")
        # Default to not relevant on error
        return {
            "binary_score": "no",
            "reasoning": f"Grading error: {str(e)}"
        }


if __name__ == "__main__":
    """Test the retrieval grader when run directly"""
    import argparse
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from graph.test_mode_helper import set_mode, get_current_mode
    from pprint import pprint
    
    parser = argparse.ArgumentParser(description="Test Retrieval Grader")
    parser.add_argument("--mode", choices=["offline", "online"], 
                       default=None, help="Test mode (default: current AGENT_MODE)")
    args = parser.parse_args()
    
    mode = args.mode or get_current_mode()
    
    with set_mode(mode):
        print(f"Testing Retrieval Grader ({mode.upper()} MODE)...")
        print("="*50)
    
    try:
        from query_engine import QueryEngine
        
        question = "What is LangGraph?"
        print(f"Question: {question}")
        
        # Retrieve documents
        query_engine = QueryEngine()
        search_results = query_engine.search(question)
        
        if not search_results:
            print("No documents found. Cannot test grader.")
            exit(1)
        
        print(f"Retrieved {len(search_results)} documents")
        
        # Test grading for each document
        print("\nGrading documents:")
        print("-" * 50)
        
        for i, result in enumerate(search_results[:3], 1):  # Test top 3
            doc_content = result.get("content", "")
            print(f"\nDocument {i}:")
            print(f"Content preview: {doc_content[:100]}...")
            
            grade_result = grade_document(question, doc_content)
            print(f"Relevant: {grade_result['binary_score']}")
            print(f"Reasoning: {grade_result['reasoning']}")
        
        print("\n" + "="*50)
        print("Test completed successfully!")
        
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()

