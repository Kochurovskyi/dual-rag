"""Pytest configuration and shared fixtures."""
import pytest
import os
from unittest.mock import Mock, MagicMock, patch
from graph.state import GraphState


@pytest.fixture
def sample_state():
    """Create a sample GraphState for testing."""
    return {
        "question": "What is LangGraph?",
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


@pytest.fixture
def offline_mode(monkeypatch):
    """Fixture to set offline mode for tests."""
    monkeypatch.setenv("AGENT_MODE", "offline")
    with patch("config.AGENT_MODE", "offline"):
        with patch("config.WEB_SEARCH_ENABLED", False):
            with patch("config.VECTOR_STORE_MODE", "chroma"):
                yield


@pytest.fixture
def online_mode(monkeypatch):
    """Fixture to set online mode for tests."""
    monkeypatch.setenv("AGENT_MODE", "online")
    with patch("config.AGENT_MODE", "online"):
        with patch("config.WEB_SEARCH_ENABLED", True):
            with patch("config.VECTOR_STORE_MODE", "postgres"):
                yield


@pytest.fixture(params=["offline", "online"])
def mode(request, monkeypatch):
    """Parametrized fixture for testing both modes."""
    mode_value = request.param
    monkeypatch.setenv("AGENT_MODE", mode_value)
    
    if mode_value == "offline":
        with patch("config.AGENT_MODE", "offline"):
            with patch("config.WEB_SEARCH_ENABLED", False):
                with patch("config.VECTOR_STORE_MODE", "chroma"):
                    yield mode_value
    else:
        with patch("config.AGENT_MODE", "online"):
            with patch("config.WEB_SEARCH_ENABLED", True):
                with patch("config.VECTOR_STORE_MODE", "postgres"):
                    yield mode_value


@pytest.fixture
def mock_query_engine():
    """Mock QueryEngine for testing."""
    mock_engine = Mock()
    mock_engine.search.return_value = [
        {
            "content": "LangGraph is a library for building stateful agents.",
            "source": "langgraph",
            "file_path": "test.md",
            "score": 0.9,
            "distance": 0.1,
            "id": "doc1",
            "heading": "Introduction",
            "heading_path": "",
            "chunk_index": 0,
            "has_code": False,
            "code_language": None,
            "metadata": {}
        }
    ]
    return mock_engine


@pytest.fixture
def sample_document():
    """Create a sample LangChain Document for testing."""
    from langchain_core.documents import Document
    
    return Document(
        page_content="LangGraph is a library for building stateful agents.",
        metadata={
            "source": "langgraph",
            "file_path": "test.md",
            "score": 0.9,
            "heading": "Introduction"
        }
    )

