"""Configuration settings for the documentation search system."""
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directories
BASE_DIR = Path(".")
DOCS_DIR = BASE_DIR / "docs"
INDEX_DIR = BASE_DIR / "index"
METADATA_DIR = BASE_DIR / "metadata"

# Embedding model configuration
USE_GOOGLE_EMBEDDINGS = True  # Use Google gemini-embedding-001
EMBEDDING_MODEL = "models/gemini-embedding-001"  # Google embedding model
# Fallback (if not using Google)

# Chunking configuration (optimized for technical documentation)
MAX_CHUNK_SIZE = 800  # tokens (optimal range: 500-800)
MIN_CHUNK_SIZE = 100  # tokens (filter very small chunks)
CHUNK_OVERLAP = 160   # tokens (20% overlap for context preservation)

# Query configuration
TOP_K_RESULTS = 5     # Default number of results to return
MIN_SCORE = 0.0        # Minimum similarity score threshold

# Documentation sources
SOURCES = {
    "langgraph": {
        "index_url": "https://langchain-ai.github.io/langgraph/llms.txt",
        "base_url": "https://langchain-ai.github.io/langgraph",
        "docs_dir": DOCS_DIR / "langgraph",
        "collection_name": "langgraph_docs"
    },
    "langchain": {
        "index_url": "https://docs.langchain.com/llms-full.txt",
        "base_url": "https://docs.langchain.com",
        "docs_dir": DOCS_DIR / "langchain",
        "collection_name": "langchain_docs"
    }
}

# Watchdog configuration
WATCHDOG_INTERVAL = 3600  # Default polling interval in seconds (1 hour)
REGISTRY_FILE = METADATA_DIR / "file_registry.json"
DOWNLOAD_METADATA_FILE = METADATA_DIR / "download_metadata.json"

# ChromaDB configuration
CHROMA_PERSIST_DIR = INDEX_DIR

# Agent Mode Configuration
# If AGENT_MODE=online: Uses PostgreSQL vector store + web search enabled
# If AGENT_MODE=offline: Uses ChromaDB vector store + web search disabled
AGENT_MODE = os.getenv("AGENT_MODE", "offline").lower()

# PostgreSQL Vector Store Configuration (used when AGENT_MODE=online)
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
POSTGRES_DB = os.getenv("POSTGRES_DB", "documentation_search")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
POSTGRES_VECTOR_TABLE = os.getenv("POSTGRES_VECTOR_TABLE", "document_vectors")

# Vector Store Mode (derived from AGENT_MODE setting)
# Automatically set based on AGENT_MODE flag
VECTOR_STORE_MODE = "postgres" if AGENT_MODE == "online" else "chroma"

# Web Search Configuration (derived from AGENT_MODE setting)
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
# Automatically enabled when AGENT_MODE=online, disabled when AGENT_MODE=offline
WEB_SEARCH_ENABLED = AGENT_MODE == "online"

# LLM Configuration for Graph Chains
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")  # Google API key for LLM
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-2.5-flash-lite")  # Model for generation, grading, routing
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "5"))  # Maximum retry attempts for generation

# Graph Configuration
GRAPH_LOG_LEVEL = os.getenv("GRAPH_LOG_LEVEL", "INFO")  # Logging level for graph execution

# LangSmith Configuration
# Disable LangSmith tracing to avoid payload size errors (large document content)
# Set to "false" or unset to disable tracing
LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING", "false").lower() == "true"
if not LANGSMITH_TRACING:
    # Explicitly disable LangSmith tracing
    os.environ["LANGSMITH_TRACING"] = "false"

