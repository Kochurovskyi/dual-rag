"""Streamlit GUI for Advanced RAG with LangGraph workflow."""
import streamlit as st
import os
from typing import Optional, Tuple
from graph import app as graph_app
from graph.state import GraphState
from graph.test_mode_helper import set_mode
from config import (
    AGENT_MODE, GOOGLE_API_KEY, TAVILY_API_KEY,
    WEB_SEARCH_ENABLED, VECTOR_STORE_MODE, LLM_MODEL
)

# Page configuration
st.set_page_config(
    page_title="Advanced RAG Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent_mode" not in st.session_state:
    st.session_state.agent_mode = AGENT_MODE
if "google_api_validated" not in st.session_state:
    st.session_state.google_api_validated = False
if "tavily_api_validated" not in st.session_state:
    st.session_state.tavily_api_validated = False


def validate_google_api_key(api_key: str) -> Tuple[bool, str]:
    """Validate Google API key with a light request."""
    if not api_key or api_key.strip() == "":
        return False, "API key not provided"
    
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        # Light validation: create a simple model instance
        from config import LLM_MODEL
        llm = ChatGoogleGenerativeAI(
            model=LLM_MODEL,
            google_api_key=api_key,
            temperature=0.1
        )
        
        # Make a minimal request
        response = llm.invoke("Hi")
        
        if response and response.content:
            return True, "Valid"
        else:
            return False, "Invalid response"
    except Exception as e:
        return False, f"Validation failed: {str(e)}"


def validate_tavily_api_key(api_key: str) -> Tuple[bool, str]:
    """Validate Tavily API key with a light request."""
    if not api_key or api_key.strip() == "":
        return False, "API key not provided"
    
    try:
        from tavily import TavilyClient
        
        # Light validation: create client and make minimal request
        client = TavilyClient(api_key=api_key)
        
        # Make a simple search request
        result = client.search(query="test", max_results=1)
        
        if result and isinstance(result, dict):
            return True, "Valid"
        else:
            return False, "Invalid response"
    except Exception as e:
        return False, f"Validation failed: {str(e)}"


def create_initial_state(question: str) -> GraphState:
    """Create initial graph state from question."""
    return {
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


def format_document(doc, index: int) -> str:
    """Format document for display."""
    metadata = doc.metadata
    content = doc.page_content[:500] + "..." if len(doc.page_content) > 500 else doc.page_content
    
    return f"""
**Document {index + 1}**
- **Source**: `{metadata.get('file_path', 'Unknown')}`
- **Score**: {metadata.get('score', 0.0):.3f}
- **Content**: {content}
"""


def format_source(generation_source: str, agent_mode: str) -> str:
    """
    Format the source of data used for generation.
    Similar to reference implementation: https://github.com/Kochurovskyi/Advanced-RAG/blob/main/app.py
    """
    if generation_source == "web_search":
        return "🌐 Web Search"
    elif generation_source == "rag":
        vector_store = "PostgreSQL" if agent_mode == "online" else "ChromaDB"
        return f"📚 RAG ({vector_store})"
    elif generation_source == "llm_guess":
        return "🤔 Just guessing?"
    else:
        return "❓ Unknown"


# Sidebar
with st.sidebar:
    st.title("⚙️ Configuration", )
    # Agent Mode Toggle
    agent_mode = st.radio(
        "Select mode:",
        ["offline", "online"],
        index=0 if st.session_state.agent_mode == "offline" else 1,
        help="Offline: ChromaDB only. Online: PostgreSQL + Web Search"
    )
    
    if agent_mode != st.session_state.agent_mode:
        st.session_state.agent_mode = agent_mode
        # Reset validation states when mode changes
        st.session_state.google_api_validated = False
        st.session_state.tavily_api_validated = False
        # Log mode change
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"[MODE] GUI mode changed: {agent_mode.upper()}")
        logger.info(f"[MODE] Vector store: {'PostgreSQL' if agent_mode == 'online' else 'ChromaDB'}")
        logger.info(f"[MODE] Web search: {'Enabled (Tavily)' if agent_mode == 'online' else 'Disabled'}")
        st.rerun()

    st.write(f"**Current Mode**: {agent_mode.upper()}")
    st.write(f"**Vector Store**: {'ChromaDB' if agent_mode == 'offline' else 'PostgreSQL'}")
    st.write(f"**Web Search**: {'Disabled' if agent_mode == 'offline' else 'Enabled'}")
   
    # API Key Validation
    st.subheader("🔑 API Keys")
    
    # Google API Key
    google_key = os.getenv("GOOGLE_API_KEY", "")
    if google_key:
        if not st.session_state.google_api_validated:
            with st.spinner("Validating Google API key..."):
                try:
                    is_valid, message = validate_google_api_key(google_key)
                    st.session_state.google_api_validated = is_valid
                    st.session_state.google_api_message = message
                except Exception as e:
                    st.session_state.google_api_validated = False
                    st.session_state.google_api_message = f"Error: {str(e)}"
        
        if st.session_state.google_api_validated:
            st.success("✅ Google API Key: Valid")
        else:
            st.error(f"❌ Google API Key: {st.session_state.get('google_api_message', 'Invalid')}")
    else:
        st.warning("⚠️ Google API Key: Not set")
    
    # Tavily API Key (only show in online mode)
    if agent_mode == "online":
        tavily_key = os.getenv("TAVILY_API_KEY", "")
        if tavily_key:
            if not st.session_state.tavily_api_validated:
                with st.spinner("Validating Tavily API key..."):
                    try:
                        is_valid, message = validate_tavily_api_key(tavily_key)
                        st.session_state.tavily_api_validated = is_valid
                        st.session_state.tavily_api_message = message
                    except Exception as e:
                        st.session_state.tavily_api_validated = False
                        st.session_state.tavily_api_message = f"Error: {str(e)}"
            
            if st.session_state.tavily_api_validated:
                st.success("✅ Tavily API Key: Valid")
            else:
                st.error(f"❌ Tavily API Key: {st.session_state.get('tavily_api_message', 'Invalid')}")
        else:
            st.warning("⚠️ Tavily API Key: Not set (required for web search)")
        
    # Example Questions
    st.subheader("💡 Example Questions")
    example_questions = [
        "What is LangGraph?",
        "How do I add persistence to a LangGraph agent?",
        "What's the difference between StateGraph and MessageGraph?",
        "What are the latest updates to LangGraph in October 2025?",
        "How to handle errors in LangChain?",
        "What's the general price for pizza in NY?",
        "Explain LangGraph's checkpoint system",
        "What are the best practices for RAG?"
    ]
    
    for i, example in enumerate(example_questions):
        if st.button(f"📌 {example}", key=f"example_{i}", use_container_width=True):
            st.session_state.question_input = example


# Main area
st.title("🤖 Advanced RAG Assistant")
st.markdown("Ask questions about LangGraph and LangChain documentation, or general questions (online mode).")

# Initialize question_input in session state if not exists
if "question_input" not in st.session_state:
    st.session_state.question_input = ""

# Question input (no value parameter - uses session state via key only)
question = st.text_input(
    "Enter your question:",
    key="question_input",
    placeholder="e.g., What is LangGraph?"
)

# Function to clear chat history
def clear_chat_history():
    st.session_state.messages = []

# Run button with on_click callback to clear history
run_button = st.button("🚀 Run", type="primary", use_container_width=True, on_click=clear_chat_history)

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "documents" in message and message["documents"]:
            with st.expander("📄 View Sources"):
                for i, doc in enumerate(message["documents"]):
                    st.markdown(format_document(doc, i))

# Process question
if run_button and question:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": question})
    
    with st.chat_message("user"):
        st.markdown(question)
    
    # Validate API keys before running
    google_key = os.getenv("GOOGLE_API_KEY", "")
    if not google_key:
        st.error("❌ Google API Key is required. Please set GOOGLE_API_KEY in your .env file.")
        st.stop()
    
    # Validate Google API key if not already validated
    if not st.session_state.google_api_validated:
        with st.spinner("Validating Google API key..."):
            is_valid, message = validate_google_api_key(google_key)
            st.session_state.google_api_validated = is_valid
            if not is_valid:
                st.error(f"❌ Google API Key validation failed: {message}")
                st.stop()
    
    # Validate Tavily API key for online mode
    if agent_mode == "online":
        tavily_key = os.getenv("TAVILY_API_KEY", "")
        if not tavily_key:
            st.warning("⚠️ Tavily API Key not set. Web search will be disabled.")
        elif not st.session_state.tavily_api_validated:
            with st.spinner("Validating Tavily API key..."):
                is_valid, message = validate_tavily_api_key(tavily_key)
                st.session_state.tavily_api_validated = is_valid
                if not is_valid:
                    st.warning(f"⚠️ Tavily API Key validation failed: {message}. Web search will be disabled.")
    
    # Run graph workflow
    with st.chat_message("assistant"):
        with st.spinner("Processing your question..."):
            try:
                # Set agent mode
                with set_mode(agent_mode):
                    # Create initial state
                    initial_state = create_initial_state(question)
                    
                    # Invoke graph
                    result = graph_app.invoke(initial_state)
                    
                    # Display answer
                    answer = result.get("generation", "No answer generated.")
                    st.markdown(answer)
                    
                    # Display metadata
                    metadata = result.get("metadata", {})
                    
                    # Source indicator (prominently displayed like reference implementation)
                    # Reference: https://github.com/Kochurovskyi/Advanced-RAG/blob/main/app.py
                    generation_source = metadata.get("generation_source", "unknown")
                    source_label = format_source(generation_source, agent_mode)
                    st.write(f"**Source:** {source_label}")
                    
                    # Source information (detailed)
                    sources = result.get("generation_sources", [])
                    if sources:
                        with st.expander("🔗 View Source URLs/Paths"):
                            for i, source in enumerate(sources[:10], 1):  # Show top 10 sources
                                st.write(f"{i}. {source}")
                    
                    # Statistics
                    with st.expander("📊 Statistics"):
                        st.write(f"**Documents Retrieved**: {len(result.get('documents', []))}")
                        st.write(f"**Graded Documents**: {len(result.get('graded_documents', []))}")
                        st.write(f"**Is Grounded**: {'✅ Yes' if result.get('is_grounded', False) else '❌ No'}")
                        st.write(f"**Retries**: {result.get('retries', 0)}")
                        st.write(f"**Generation Source**: {metadata.get('generation_source', 'unknown')}")
                        
                        if metadata.get('routing_decision'):
                            st.write(f"**Routing Decision**: {metadata.get('routing_decision')}")
                            st.write(f"**Routing Reasoning**: {metadata.get('routing_reasoning', 'N/A')}")
                    
                    # Documents viewer
                    graded_docs = result.get("graded_documents", [])
                    if graded_docs:
                        with st.expander(f"📄 View {len(graded_docs)} Source Documents"):
                            for i, doc in enumerate(graded_docs):
                                st.markdown(format_document(doc, i))
                    
                    # Add assistant message
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "documents": graded_docs,
                        "metadata": metadata
                    })
                    
            except Exception as e:
                st.error(f"❌ Error processing question: {str(e)}")
                import traceback
                with st.expander("Error Details"):
                    st.code(traceback.format_exc())

