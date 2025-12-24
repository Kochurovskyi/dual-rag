"""LangGraph workflow definition for Advanced RAG."""
from typing import Literal
from langgraph.graph import StateGraph, END
from langchain_core.documents import Document
import time

from graph.state import GraphState
from graph.logging_config import logger


def route_question(state: GraphState) -> GraphState:
    """
    Route question to determine if RAG or web search should be used.
    For offline mode, always use RAG (vector store).
    """
    from graph.chains.router import route_question as route_fn
    from config import WEB_SEARCH_ENABLED, AGENT_MODE, VECTOR_STORE_MODE
    
    logger.info(f"[MODE] Routing question (AGENT_MODE={AGENT_MODE}, WEB_SEARCH_ENABLED={WEB_SEARCH_ENABLED})")
    logger.info(f"[MODE] Vector store mode: {VECTOR_STORE_MODE}")
    question = state["question"]
    
    # Route question
    routing_result = route_fn(question)
    decision = routing_result["decision"]
    
    # In offline mode, force RAG even if router suggests web search
    if not WEB_SEARCH_ENABLED:
        logger.info("[MODE] Offline mode: Forcing RAG route (web search disabled)")
        logger.info("[MODE] Will use ChromaDB vector store")
        decision = "rag"
        state["web_search"] = False
    else:
        # In online mode, respect router decision
        logger.info(f"[MODE] Online mode: Router decision: {decision}")
        state["web_search"] = (decision == "web_search")
    
    state["metadata"] = state.get("metadata", {})
    state["metadata"]["routing_decision"] = decision
    state["metadata"]["routing_reasoning"] = routing_result["reasoning"]
    
    if decision == "rag":
        logger.info(f"[MODE] Route question to RAG (vector store: {'PostgreSQL' if AGENT_MODE == 'online' else 'ChromaDB'})")
    else:
        logger.info("[MODE] Route question to Tavily web search (online mode)")
    
    return state


def should_route_to_rag_or_web(state: GraphState) -> Literal["retrieve_documents", "web_search"]:
    """
    Determine if router should route to RAG or web search.
    """
    from config import AGENT_MODE, WEB_SEARCH_ENABLED
    
    decision = state.get("metadata", {}).get("routing_decision", "rag")
    
    logger.info(f"[MODE] Routing decision: {decision} (AGENT_MODE={AGENT_MODE}, WEB_SEARCH_ENABLED={WEB_SEARCH_ENABLED})")
    
    if decision == "web_search":
        logger.info("[MODE] Routing to Tavily web search (online mode)")
        return "web_search"
    else:
        logger.info(f"[MODE] Routing to RAG retrieval (vector store: {'PostgreSQL' if AGENT_MODE == 'online' else 'ChromaDB'})")
        return "retrieve_documents"


def retrieve_documents(state: GraphState) -> GraphState:
    """
    Retrieve documents from vector store using QueryEngine.
    """
    from query_engine import QueryEngine
    from config import TOP_K_RESULTS, AGENT_MODE, VECTOR_STORE_MODE
    
    logger.info(f"[MODE] Retrieving documents (AGENT_MODE={AGENT_MODE}, VECTOR_STORE_MODE={VECTOR_STORE_MODE})")
    question = state["question"]
    
    if AGENT_MODE == "online":
        logger.info("[MODE] Using PostgreSQL vector store for RAG retrieval")
    else:
        logger.info("[MODE] Using ChromaDB vector store for RAG retrieval")
    
    # Initialize QueryEngine
    engine = QueryEngine()
    logger.info(f"[MODE] QueryEngine vector store mode: {engine.vector_store_mode}")
    
    # Search for documents (use all sources, top_k from config)
    search_results = engine.search(
        query=question,
        source=None,  # Search all sources
        top_k=TOP_K_RESULTS,
        use_expansion=True,
        use_metadata_boost=True,
        use_hybrid=True,
        use_reranking=True
    )
    
    # Convert search results to LangChain Documents with deduplication
    documents = []
    scores = []
    seen_content = set()  # Track content to avoid duplicates
    duplicates_skipped = 0
    
    logger.info(f"[DEDUP] Graph Node: Processing {len(search_results)} search results")
    
    for result in search_results:
        # Create content hash for deduplication (normalize whitespace)
        content_hash = hash(result.get("content", "").strip().lower())
        
        # Skip duplicates (same content, different source/language)
        if content_hash in seen_content:
            duplicates_skipped += 1
            logger.debug(f"[DEDUP] Graph Node: Skipped duplicate (source: {result.get('source', 'unknown')})")
            continue
        
        seen_content.add(content_hash)
        
        # Create Document with content and metadata
        doc = Document(
            page_content=result["content"],
            metadata={
                "source": result["source"],
                "file_path": result["file_path"],
                "heading_path": result.get("heading_path", ""),
                "heading": result.get("heading", ""),
                "chunk_index": result.get("chunk_index", 0),
                "has_code": result.get("has_code", False),
                "code_language": result.get("code_language"),
                "score": result["score"],
                "distance": result["distance"],
                "id": result["id"],
                **result.get("metadata", {})  # Include all metadata
            }
        )
        documents.append(doc)
        scores.append(result["score"])
    
    # Replace documents array (LangGraph replaces by default, not appends)
    state["documents"] = documents
    state["document_scores"] = scores
    state["metadata"] = state.get("metadata", {})
    state["metadata"]["retrieved_count"] = len(documents)
    state["metadata"]["duplicates_skipped"] = duplicates_skipped
    state["metadata"]["total_before_dedup"] = len(search_results)
    
    logger.info(f"[DEDUP] Graph Node: Retrieved {len(documents)} unique documents from {len(search_results)} results (skipped {duplicates_skipped} duplicates)")
    logger.debug(f"[DEDUP] Graph Node: State now has {len(state.get('documents', []))} documents")
    
    return state


def grade_documents(state: GraphState) -> GraphState:
    """
    Grade documents for relevance to the question using LLM.
    """
    from graph.chains.retrieval_grader import grade_document
    
    logger.info("Checking document relevance to question")
    question = state["question"]
    documents = state.get("documents", [])
    
    # Grade each document
    graded_docs = []
    grading_scores = []
    
    for doc in documents:
        # Grade document
        grade_result = grade_document(question, doc.page_content)
        
        # If relevant (binary_score == 'yes'), keep it
        if grade_result["binary_score"].lower() == "yes":
            graded_docs.append(doc)
            # Use original similarity score
            original_score = doc.metadata.get("score", 0.5)
            grading_scores.append(original_score)
    
    state["graded_documents"] = graded_docs
    state["grading_scores"] = grading_scores
    state["metadata"] = state.get("metadata", {})
    state["metadata"]["graded_count"] = len(graded_docs)
    state["metadata"]["total_documents"] = len(documents)
    
    logger.info(f"Graded {len(documents)} documents, {len(graded_docs)} relevant")
    
    return state


def should_continue(state: GraphState) -> Literal["generate", "web_search"]:
    """
    Determine next step: generate answer or fallback to web search.
    In offline mode, always generate (web search disabled).
    In online mode, fallback to web search if no relevant documents.
    """
    from config import WEB_SEARCH_ENABLED
    
    graded_docs = state.get("graded_documents", [])
    
    logger.info("Assessing graded documents")
    
    if len(graded_docs) > 0:
        logger.info("[MODE] Decision: Generate response from RAG documents")
        return "generate"
    else:
        # Check if web search is enabled and should be used as fallback
        if WEB_SEARCH_ENABLED:
            logger.info("[MODE] Decision: No relevant documents, fallback to Tavily web search (online mode)")
            return "web_search"
        else:
            # In offline mode, generate anyway (no web search fallback)
            logger.info("[MODE] Decision: Generate response (no relevant documents, offline mode - no web search fallback)")
            return "generate"


def generate(state: GraphState) -> GraphState:
    """
    Generate answer from graded documents or graded web search results using LLM.
    """
    from graph.chains.generation import generate_answer
    from config import AGENT_MODE
    
    logger.info("Generating response")
    question = state["question"]
    graded_docs = state.get("graded_documents", [])
    graded_web_search_results = state.get("graded_web_search_results", [])
    
    # Use graded web search results if no graded documents (fallback scenario)
    if not graded_docs and graded_web_search_results:
        logger.info(f"[MODE] Generating from graded Tavily web search results ({len(graded_web_search_results)} relevant results)")
        doc_contents = [doc.page_content for doc in graded_web_search_results]
        answer = generate_answer(question, doc_contents)
        
        # Check if answer indicates documents don't contain the information
        # If so, try using ungraded web search results as fallback
        answer_lower = answer.lower()
        if any(phrase in answer_lower for phrase in ["don't contain", "doesn't contain", "do not contain", "does not contain", "not contain information", "no information"]):
            web_search_results = state.get("web_search_results", [])
            if web_search_results and len(web_search_results) > len(graded_web_search_results):
                logger.warning("[MODE] Graded web search results don't answer question, trying ungraded results as fallback")
                logger.info(f"[MODE] Using {len(web_search_results)} ungraded web search results")
                doc_contents = [doc.page_content for doc in web_search_results]
                answer = generate_answer(question, doc_contents)
                state["generation"] = answer
                state["generation_sources"] = [
                    doc.metadata.get("url", "unknown") for doc in web_search_results
                ]
                state["metadata"] = state.get("metadata", {})
                state["metadata"]["generation_source"] = "web_search_fallback"
            else:
                state["generation"] = answer
                state["generation_sources"] = [
                    doc.metadata.get("url", "unknown") for doc in graded_web_search_results
                ]
                state["metadata"] = state.get("metadata", {})
                state["metadata"]["generation_source"] = "web_search"
        else:
            state["generation"] = answer
            state["generation_sources"] = [
                doc.metadata.get("url", "unknown") for doc in graded_web_search_results
            ]
            state["metadata"] = state.get("metadata", {})
            state["metadata"]["generation_source"] = "web_search"
    elif not graded_docs:
        logger.warning("[MODE] No documents available for generation")
        
        # Check if we have ungraded web search results (all were filtered out)
        web_search_results = state.get("web_search_results", [])
        web_search_performed = state.get("metadata", {}).get("web_search_performed", False)
        
        logger.info(f"[DEBUG] Web search performed: {web_search_performed}")
        logger.info(f"[DEBUG] Web search results count: {len(web_search_results)}")
        logger.info(f"[DEBUG] Graded web search results count: {len(graded_web_search_results)}")
        
        # If web search was performed but all results filtered, use them anyway (less strict)
        if web_search_performed and web_search_results and not graded_web_search_results:
            logger.warning("[MODE] All web search results filtered as irrelevant, but using them anyway (fallback)")
            logger.info(f"[MODE] Generating from ungraded Tavily web search results ({len(web_search_results)} results)")
            doc_contents = [doc.page_content for doc in web_search_results]
            answer = generate_answer(question, doc_contents)
            state["generation"] = answer
            state["generation_sources"] = [
                doc.metadata.get("url", "unknown") for doc in web_search_results
            ]
            state["metadata"] = state.get("metadata", {})
            state["metadata"]["generation_source"] = "web_search_fallback"
            logger.info("[MODE] Used web search results despite low relevance scores")
        # In offline mode, use pure LLM fallback with limited answer
        elif AGENT_MODE == "offline":
            logger.info("[MODE] Offline mode: Using pure LLM fallback (no documents found)")
            from graph.chains.generation import generate_pure_llm_answer
            state["generation"] = generate_pure_llm_answer(question)
            state["generation_sources"] = []
            state["metadata"] = state.get("metadata", {})
            state["metadata"]["generation_source"] = "llm_guess"
        else:
            # Online mode: use pure LLM fallback if no documents at all
            logger.info("[MODE] Online mode: Using pure LLM fallback (no documents found after web search)")
            from graph.chains.generation import generate_pure_llm_answer
            state["generation"] = generate_pure_llm_answer(question)
            state["generation_sources"] = []
            state["metadata"] = state.get("metadata", {})
            state["metadata"]["generation_source"] = "llm_guess"
    else:
        # Use graded documents (RAG path)
        logger.info(f"[MODE] Generating from RAG documents ({len(graded_docs)} documents from {'PostgreSQL' if AGENT_MODE == 'online' else 'ChromaDB'})")
        doc_contents = [doc.page_content for doc in graded_docs]
        answer = generate_answer(question, doc_contents)
        state["generation"] = answer
        state["generation_sources"] = [
            doc.metadata.get("file_path", "unknown") for doc in graded_docs
        ]
        state["metadata"] = state.get("metadata", {})
        state["metadata"]["generation_source"] = "rag"
    
    state["metadata"]["generation_length"] = len(state["generation"])
    
    logger.info(f"Generated response length: {len(state['generation'])} characters")
    
    return state


def check_hallucination(state: GraphState) -> GraphState:
    """
    Check if generated answer is grounded in source documents using LLM.
    """
    from graph.chains.hallucination_grader import check_hallucination as check_fn
    
    logger.info("Checking hallucinations")
    question = state["question"]
    generation = state.get("generation", "")
    graded_docs = state.get("graded_documents", [])
    graded_web_search_results = state.get("graded_web_search_results", [])
    
    # Use graded documents or graded web search results
    source_docs = graded_docs if graded_docs else graded_web_search_results
    
    if not source_docs:
        # No documents means answer is not grounded
        state["is_grounded"] = False
        state["hallucination_score"] = 0.9
        logger.info("Generation is not grounded (no documents)")
    else:
        # Extract document contents for hallucination check
        doc_contents = [doc.page_content for doc in source_docs]
        
        # Check hallucination using LLM
        check_result = check_fn(question, generation, doc_contents)
        
        # 'yes' means grounded, 'no' means hallucinated
        state["is_grounded"] = check_result["binary_score"].lower() == "yes"
        state["hallucination_score"] = 0.1 if state["is_grounded"] else 0.9
        
        if state["is_grounded"]:
            logger.info("Generation is grounded in documents")
        else:
            logger.info("Generation contains hallucinations")
    
    state["metadata"] = state.get("metadata", {})
    state["metadata"]["hallucination_check"] = {
        "is_grounded": state["is_grounded"],
        "score": state["hallucination_score"]
    }
    
    return state


def should_retry(state: GraphState) -> Literal["retry", "end"]:
    """
    Determine if generation should be retried.
    """
    from config import MAX_RETRIES
    
    is_grounded = state.get("is_grounded", False)
    retries = state.get("retries", 0)
    
    if not is_grounded and retries < MAX_RETRIES:
        return "retry"
    else:
        return "end"


def increment_retry(state: GraphState) -> GraphState:
    """
    Increment retry counter.
    """
    retries = state.get("retries", 0) + 1
    state["retries"] = retries
    logger.info(f"Retry attempt {retries}")
    return state


# Build the graph
def create_graph():
    """Create and compile the LangGraph workflow."""
    from graph.nodes.web_search import web_search
    from graph.nodes.grade_web_search import grade_web_search_results
    
    workflow = StateGraph(GraphState)
    
    # Add nodes
    workflow.add_node("route_question", route_question)
    workflow.add_node("retrieve_documents", retrieve_documents)
    workflow.add_node("grade_documents", grade_documents)
    workflow.add_node("web_search", web_search)
    workflow.add_node("grade_web_search_results", grade_web_search_results)
    workflow.add_node("generate", generate)
    workflow.add_node("check_hallucination", check_hallucination)
    workflow.add_node("increment_retry", increment_retry)
    
    # Set entry point
    workflow.set_entry_point("route_question")
    
    # Add edges
    # Router conditionally routes to RAG or web search
    workflow.add_conditional_edges(
        "route_question",
        should_route_to_rag_or_web,
        {
            "retrieve_documents": "retrieve_documents",
            "web_search": "web_search"
        }
    )
    
    # RAG path: retrieve -> grade -> generate or web_search fallback
    workflow.add_edge("retrieve_documents", "grade_documents")
    workflow.add_conditional_edges(
        "grade_documents",
        should_continue,
        {
            "generate": "generate",
            "web_search": "web_search"  # Fallback to web search if no relevant docs
        }
    )
    
    # Web search path: web_search -> grade_web_search_results -> generate
    workflow.add_edge("web_search", "grade_web_search_results")
    workflow.add_edge("grade_web_search_results", "generate")
    
    # Generate -> check hallucination -> retry or end
    workflow.add_edge("generate", "check_hallucination")
    workflow.add_conditional_edges(
        "check_hallucination",
        should_retry,
        {
            "retry": "increment_retry",
            "end": END
        }
    )
    workflow.add_edge("increment_retry", "generate")
    
    # Compile graph
    app = workflow.compile()
    
    return app


# Create the compiled graph
app = create_graph()


# Test the graph with a sample question
if __name__ == "__main__":
    import argparse
    from graph.test_mode_helper import set_mode, get_current_mode
    
    parser = argparse.ArgumentParser(description="Test LangGraph workflow")
    parser.add_argument("--mode", choices=["offline", "online"], 
                       default=None, help="Test mode (default: current AGENT_MODE)")
    args = parser.parse_args()
    
    mode = args.mode or get_current_mode()
    
    with set_mode(mode):
        logger.info("="*50)
        logger.info(f"TESTING RAG GRAPH ({mode.upper()} MODE)")
        logger.info("="*50)
    
    # Generate PNG image of the graph
    try:
        png_content = app.get_graph(xray=True).draw_mermaid_png()
        with open("graph.png", "wb") as f: f.write(png_content)
        logger.info("PNG graph image created as ambient_graph.png")
    except Exception as e:
        logger.warning(f"Could not generate PNG graph image: {e}")
        logger.info("Note: PNG generation requires pyppeteer or playwright. Install with: pip install pyppeteer")
    
    logger.info("Graph compiled successfully!")
    
    # Test pure LLM fallback in offline mode
    logger.info("\n" + "="*50)
    logger.info("TESTING PURE LLM FALLBACK (OFFLINE MODE)")
    logger.info("="*50)
    
    if mode == "offline":
        test_question_no_docs = "What is the weather on Mars today?"
        logger.info(f"\nTest Question (no docs expected): {test_question_no_docs}")
        
        initial_state = {
            "question": test_question_no_docs,
            "web_search": False,
            "web_search_results": [],
            "graded_web_search_results": [],
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
        
        try:
            result = app.invoke(initial_state)
            generation_source = result.get("metadata", {}).get("generation_source", "unknown")
            
            logger.info(f"Generation Source: {generation_source}")
            logger.info(f"Generation preview: {result.get('generation', '')[:200]}...")
            
            if generation_source == "llm_guess":
                logger.info("✅ Pure LLM fallback working correctly")
            else:
                logger.warning(f"⚠️ Expected 'llm_guess', got '{generation_source}'")
        except Exception as e:
            logger.error(f"❌ Pure LLM fallback test failed: {e}")
    
    # Test with multiple queries (2 for each: LangChain, LangGraph, LangSmith)
    test_queries = [
        # LangChain queries
        {"query": "How to use LangChain with PostgreSQL?", "source": "langchain"},
        {"query": "What are the best practices for RAG in LangChain?", "source": "langchain"},
        {"query": "How do I build a RAG application with LangChain?", "source": "langchain"},
        {"query": "How do I create an agent with LangChain?", "source": "langchain"},
        {"query": "How do I add memory to a LangChain chain?", "source": "langchain"},
        {"query": "What's the difference between chains and agents in LangChain?", "source": "langchain"},
        {"query": "How do I use vector stores with LangChain?", "source": "langchain"},
        {"query": "How do I load documents with LangChain document loaders?", "source": "langchain"},
        {"query": "How do I implement retrieval in LangChain?", "source": "langchain"},
        {"query": "How do I add tools to a LangChain agent?", "source": "langchain"},
        {"query": "What LLM models are supported in LangChain?", "source": "langchain"},
        {"query": "How do I build a multi-agent system with LangChain?", "source": "langchain"},
        # LangGraph queries
        {"query": "What is LangGraph?", "source": "langgraph"},
        {"query": "Explain LangGraph's checkpoint system", "source": "langgraph"},
        {"query": "How do I add persistence to a LangGraph agent?", "source": "langgraph"},
        {"query": "What's the difference between StateGraph and MessageGraph?", "source": "langgraph"},
        {"query": "Show me how to implement human-in-the-loop with LangGraph", "source": "langgraph"},
        {"query": "How do I handle errors and retries in LangGraph nodes?", "source": "langgraph"},
        {"query": "What are best practices for state management in LangGraph?", "source": "langgraph"},
        {"query": "How do I stream responses from a LangGraph agent?", "source": "langgraph"},
        {"query": "How do I create a multi-agent system with LangGraph?", "source": "langgraph"},
        {"query": "How do I add tools to a LangGraph agent?", "source": "langgraph"},
        {"query": "How do I deploy a LangGraph agent to production?", "source": "langgraph"},
        {"query": "How do I use subgraphs in LangGraph?", "source": "langgraph"},
        # LangSmith queries
        {"query": "How to use LangSmith for tracing?", "source": "langsmith"},
        {"query": "What is LangSmith used for?", "source": "langsmith"},
    ]
    
    logger.info("="*50)
    logger.info(f"RUNNING SANITY TESTS WITH {len(test_queries)} QUERIES")
    logger.info("="*50)
    
    all_results = []
    
    for idx, test_case in enumerate(test_queries, 1):
        test_question = test_case["query"]
        expected_source = test_case["source"]
        
        logger.info("")
        logger.info("="*50)
        logger.info(f"TEST {idx}/{len(test_queries)}: {test_question}")
        logger.info(f"Expected Source: {expected_source}")
        logger.info("="*50)
        
        try:
            initial_state = {
                "question": test_question,
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
            
            result = app.invoke(initial_state)
            all_results.append({
                "query": test_question,
                "expected_source": expected_source,
                "result": result
            })
            
            logger.info("="*50)
            logger.info(f"TEST {idx} RESULT")
            logger.info("="*50)
            logger.info(f"Question: {result.get('question', 'N/A')}")
            logger.info(f"Generation: {result.get('generation', 'N/A')[:200]}...")
            logger.info(f"Is Grounded: {result.get('is_grounded', False)}")
            logger.info(f"Retries: {result.get('retries', 0)}")
            
            # Check metadata for retrieval info
            metadata = result.get('metadata', {})
            retrieved_count = metadata.get('retrieved_count', 'unknown')
            duplicates_skipped = metadata.get('duplicates_skipped', 0)
            
            logger.info(f"Documents Retrieved (metadata): {retrieved_count}")
            logger.info(f"Duplicates Skipped (metadata): {duplicates_skipped}")
            logger.info(f"Graded Documents: {len(result.get('graded_documents', []))}")
            
            # Deduplication Analysis
            logger.info("="*50)
            logger.info(f"TEST {idx} DEDUPLICATION ANALYSIS")
            logger.info("="*50)
            
            documents = result.get('documents', [])
            logger.info(f"Documents in state['documents']: {len(documents)}")
            
            # If documents seem duplicated, analyze what's actually in the state
            if len(documents) != retrieved_count:
                logger.warning(f"[WARNING] Mismatch: metadata says {retrieved_count} retrieved, but state has {len(documents)} documents!")
                # Check if documents are actually duplicates or if state was modified
                if len(documents) > retrieved_count:
                    # Analyze the actual documents to see if they're duplicates
                    doc_ids = [doc.metadata.get('id', 'no-id') for doc in documents]
                    unique_ids = len(set(doc_ids))
                    logger.warning(f"[WARNING] State has {len(documents)} documents with {unique_ids} unique IDs")
                    # Use the metadata count for analysis instead
                    logger.info(f"[INFO] Using metadata count ({retrieved_count}) for deduplication analysis")
                    documents = documents[:retrieved_count] if len(documents) >= retrieved_count else documents
                
                if documents:
                    # Analyze content uniqueness
                    content_hashes = {}
                    duplicate_sources = []
                    
                    for doc in documents:
                        content_normalized = doc.page_content.strip().lower()
                        content_hash = hash(content_normalized)
                        source = doc.metadata.get('source', 'unknown')
                        file_path = doc.metadata.get('file_path', 'unknown')
                        
                        if content_hash not in content_hashes:
                            content_hashes[content_hash] = {
                                'content': content_normalized[:100] + '...' if len(content_normalized) > 100 else content_normalized,
                                'sources': [source],
                                'file_paths': [file_path],
                                'count': 1
                            }
                        else:
                            content_hashes[content_hash]['sources'].append(source)
                            content_hashes[content_hash]['file_paths'].append(file_path)
                            content_hashes[content_hash]['count'] += 1
                            duplicate_sources.append({
                                'hash': content_hash,
                                'source': source,
                                'file_path': file_path
                            })
                    
                    unique_content = len(content_hashes)
                    total_docs = len(documents)
                    duplicates = total_docs - unique_content
                    
                    logger.info(f"Total Documents: {total_docs}")
                    logger.info(f"Unique Content: {unique_content}")
                    logger.info(f"Duplicates Found: {duplicates}")
                    
                    if duplicates > 0:
                        logger.warning(f"[WARNING] Found {duplicates} duplicate documents!")
                        # Show examples of duplicates
                        for hash_val, info in list(content_hashes.items())[:5]:
                            if info['count'] > 1:
                                logger.warning(f"  Duplicate content ({info['count']} copies):")
                                logger.warning(f"    Sources: {', '.join(set(info['sources']))}")
                                preview = info['content'][:80].encode('ascii', 'ignore').decode('ascii')
                                logger.warning(f"    Preview: {preview}...")
                    else:
                        logger.info("[OK] All documents are unique (no duplicates detected)")
                    
                    # Check for Python/JS duplicates specifically
                    python_js_duplicates = []
                    for hash_val, info in content_hashes.items():
                        if info['count'] > 1:
                            sources = set(info['sources'])
                            if 'langchain' in str(sources).lower() and any('python' in s.lower() or 'javascript' in s.lower() or 'js' in s.lower() for s in sources):
                                python_js_duplicates.append(info)
                    
                    if python_js_duplicates:
                        logger.warning(f"[WARNING] Found {len(python_js_duplicates)} Python/JS duplicate groups")
                        for dup in python_js_duplicates[:3]:
                            logger.warning(f"    Sources: {', '.join(set(dup['sources']))}")
                    else:
                        logger.info("[OK] No Python/JS duplicates detected")
                else:
                    logger.warning("No documents retrieved for deduplication analysis")
        
        except Exception as e:
            logger.error(f"Error during test {idx}: {e}")
            import traceback
            traceback.print_exc()
    
    # Summary of all tests
    logger.info("")
    logger.info("="*50)
    logger.info("SANITY TEST SUMMARY")
    logger.info("="*50)
    
    total_tests = len(all_results)
    successful_tests = len([r for r in all_results if r.get("result")])
    
    logger.info(f"Total Tests: {total_tests}")
    logger.info(f"Successful: {successful_tests}")
    logger.info(f"Failed: {total_tests - successful_tests}")
    
    # Check duplicates across all tests
    logger.info("")
    logger.info("="*50)
    logger.info("OVERALL DUPLICATES STATUS")
    logger.info("="*50)
    
    total_duplicates = 0
    total_documents = 0
    total_unique = 0
    
    for test_result in all_results:
        result = test_result.get("result")
        if result:
            metadata = result.get('metadata', {})
            duplicates_skipped = metadata.get('duplicates_skipped', 0)
            retrieved_count = metadata.get('retrieved_count', 0)
            documents = result.get('documents', [])
            
            if documents:
                content_hashes = set()
                for doc in documents:
                    content_hash = hash(doc.page_content.strip().lower())
                    content_hashes.add(content_hash)
                
                unique_count = len(content_hashes)
                duplicates = len(documents) - unique_count
                
                total_documents += len(documents)
                total_unique += unique_count
                total_duplicates += duplicates
                
                logger.info(f"Query: {test_result['query'][:50]}...")
                logger.info(f"  Documents: {len(documents)}, Unique: {unique_count}, Duplicates: {duplicates}")
    
    logger.info("")
    logger.info(f"TOTAL ACROSS ALL TESTS:")
    logger.info(f"  Total Documents: {total_documents}")
    logger.info(f"  Unique Documents: {total_unique}")
    logger.info(f"  Total Duplicates: {total_duplicates}")
    
    if total_duplicates == 0:
        logger.info("[OK] No duplicates detected across all tests!")
    else:
        logger.warning(f"[WARNING] Found {total_duplicates} duplicates across all tests")

