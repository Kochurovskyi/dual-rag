"""Answer generation chain for RAG."""
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from config import LLM_MODEL
from graph.logging_config import logger


def create_generation_chain():
    """Create answer generation chain."""
    # Higher temperature for more creative answers
    llm = ChatGoogleGenerativeAI(model=LLM_MODEL, temperature=0.7)
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert assistant helping users understand technical documentation.
        
        Use the provided context documents to answer the user's question. 
        - Provide a clear, concise answer based on the documents
        - If the documents contain relevant information, extract and present it clearly
        - Include relevant code examples or explanations from the documents
        - Cite which document(s) you used for your answer
        - If the documents don't directly answer the question but contain related information, explain what they DO contain and how it relates
        IMPORTANT: If the documents don't contain enough information to answer the question, be helpful:
        - Explain what information the documents DO contain
        - Suggest what additional information would be needed
        - Don't just say "the documents don't contain information" - be constructive
        Format your response clearly and be helpful."""),
                ("human", """Context Documents:{context}
        Question: {question}
        Answer the question based on the context documents above. If the documents don't directly answer the question, explain what they do contain and how it relates to the question.""")
            ])
    
    chain = prompt | llm | StrOutputParser()
    return chain


# Create the chain instance
generate_answer_chain = create_generation_chain()


def generate_pure_llm_answer(question: str) -> str:
    """
    Generate a pure LLM answer without documents (fallback for offline mode).
    Limited to ~100 words, summarized response.
    
    Args:
        question: User's question
        
    Returns:
        Generated answer string (limited to ~100 words)
    """
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    from config import LLM_MODEL
    
    logger.info(f"Generating pure LLM answer (question: {question[:100]}...)")
    
    llm = ChatGoogleGenerativeAI(
        model=LLM_MODEL,
        temperature=0.7,
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful assistant. Provide a brief, summarized answer in approximately 100 words or less.
        
        Start your answer with: "There is no answer in knowledge base but..."
        Then provide a concise, helpful response based on your general knowledge.
        Keep it brief and to the point."""),
                ("human", "Question: {question}\n\nProvide a brief answer (approximately 100 words).")
            ])
    
    chain = prompt | llm | StrOutputParser()
    
    try:
        answer = chain.invoke({"question": question})
        
        # Limit to approximately 100 words
        words = answer.split()
        if len(words) > 100:
            answer = " ".join(words[:100]) + "..."
        
        logger.info(f"Generated pure LLM answer (length: {len(answer)} characters, words: {len(answer.split())})")
        return answer
    except Exception as e:
        logger.error(f"Error generating pure LLM answer: {e}")
        return "There is no answer in knowledge base but I'm unable to generate a response at this time."


def generate_answer(question: str, documents: list) -> str:
    """
    Generate an answer from documents.
    
    Args:
        question: User's question
        documents: List of document contents
        
    Returns:
        Generated answer string
    """
    logger.info(f"Generating answer (question: {question[:100]}..., documents: {len(documents)})")
    
    if not documents:
        logger.warning("No documents provided for generation")
        return "No relevant documents found to answer your question."
    
    # Format documents for prompt
    context = "\n\n---\n\n".join([
        f"Document {i+1}:\n{doc}" for i, doc in enumerate(documents)
    ])
    
    try:
        answer = generate_answer_chain.invoke({
            "question": question,
            "context": context
        })
        
        logger.info(f"Generated answer (length: {len(answer)} characters)")
        logger.debug(f"Answer preview: {answer[:200]}...")
        
        return answer
    except Exception as e:
        logger.error(f"Error generating answer: {e}")
        return f"Error generating answer: {str(e)}"


if __name__ == "__main__":
    """Test the generation chain when run directly"""
    import argparse
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from graph.test_mode_helper import set_mode, get_current_mode
    from pprint import pprint
    parser = argparse.ArgumentParser(description="Test Generation Chain")
    parser.add_argument("--mode", choices=["offline", "online"], 
                       default=None, help="Test mode (default: current AGENT_MODE)")
    parser.add_argument("--test-pure-llm", action="store_true",
                       help="Test pure LLM fallback (no documents)")
    args = parser.parse_args()
    mode = args.mode or get_current_mode()
    with set_mode(mode):
        try:
            if args.test_pure_llm:
                print(f"Testing pure LLM fallback ({mode.upper()} MODE)...")
                print("="*50)
                
                question = "What is something completely unrelated to documentation?"
                print(f"Question: {question}")
                print("\nGenerating pure LLM answer (no documents)...")
                
                answer = generate_pure_llm_answer(question)
                
                print("\nGenerated Answer:")
                print("-" * 50)
                print(answer)
                print("-" * 50)
                print(f"Answer length: {len(answer)} characters")
                print(f"Word count: {len(answer.split())} words")
                
                # Verify it starts with expected prefix
                if "There is no answer in knowledge base but" in answer:
                    print("\n[OK] Answer starts with expected prefix")
                else:
                    print("\n[WARNING] Answer doesn't start with expected prefix")
                
                # Verify word limit
                if len(answer.split()) <= 100 or answer.endswith("..."):
                    print("[OK] Answer respects word limit")
                else:
                    print(f"[WARNING] Answer exceeds word limit: {len(answer.split())} words")
                
            else:
                from query_engine import QueryEngine
                
                print(f"Testing generation chain ({mode.upper()} MODE)...")
                print("="*50)
                
                # Initialize query engine
                query_engine = QueryEngine()
                
                # Test with a real question
                question = "What is LangGraph?"
                print(f"Question: {question}")
                
                # Retrieve documents
                search_results = query_engine.search(question)
                print(f"Retrieved {len(search_results)} documents")
                
                # Extract document contents
                docs = [result.get("content", "") for result in search_results[:3]]  # Use top 3
                
                if not docs:
                    print("No documents found. Cannot test generation.")
                    print("\n💡 Tip: Use --test-pure-llm to test pure LLM fallback")
                    exit(1)
                
                # Generate answer
                print("\nGenerating answer...")
                answer = generate_answer(question, docs)
                
                print("\nGenerated Answer:")
                print("-" * 50)
                print(answer)
                print("-" * 50)
                print(f"Answer length: {len(answer)} characters")
            
            print("\nTest completed successfully!")
            
        except Exception as e:
            print(f"Test failed: {e}")
            import traceback
            traceback.print_exc()

