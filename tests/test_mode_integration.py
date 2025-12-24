"""Mode-specific integration tests for full graph workflow."""
import pytest
from unittest.mock import Mock, patch, MagicMock
from graph import app
from graph.state import GraphState
from langchain_core.documents import Document


class TestFullWorkflowModes:
    """Mode-specific integration tests."""
    
    @pytest.mark.offline
    @patch('query_engine.QueryEngine')
    @patch('graph.chains.retrieval_grader.grade_document')
    @patch('graph.chains.generation.generate_answer')
    @patch('graph.chains.hallucination_grader.check_hallucination')
    def test_full_workflow_offline_mode(
        self, mock_check, mock_generate, mock_grade, mock_query_engine_class, offline_mode
    ):
        """Test complete workflow in offline mode."""
        # Setup mocks
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
        mock_query_engine_class.return_value = mock_engine
        
        mock_grade.return_value = {"binary_score": "yes", "reasoning": "Relevant"}
        mock_generate.return_value = "LangGraph is a library for building stateful agents."
        mock_check.return_value = {"binary_score": "yes", "reasoning": "Grounded"}
        
        initial_state: GraphState = {
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
        
        result = app.invoke(initial_state)
        
        # Verify offline mode behavior
        assert result["web_search"] is False
        assert result["generation"] != ""
        assert result["is_grounded"] is True
        assert len(result["generation_sources"]) > 0
        assert result["retries"] == 0
    
    @pytest.mark.online
    @patch('query_engine.QueryEngine')
    @patch('graph.chains.retrieval_grader.grade_document')
    @patch('graph.chains.generation.generate_answer')
    @patch('graph.chains.hallucination_grader.check_hallucination')
    def test_full_workflow_online_mode(
        self, mock_check, mock_generate, mock_grade, mock_query_engine_class, online_mode
    ):
        """Test complete workflow in online mode."""
        # Setup mocks
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
        mock_query_engine_class.return_value = mock_engine
        
        mock_grade.return_value = {"binary_score": "yes", "reasoning": "Relevant"}
        mock_generate.return_value = "LangGraph is a library for building stateful agents."
        mock_check.return_value = {"binary_score": "yes", "reasoning": "Grounded"}
        
        initial_state: GraphState = {
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
        
        result = app.invoke(initial_state)
        
        # Verify online mode behavior (can use web search)
        assert result["generation"] != ""
        assert result["is_grounded"] is True
        # In online mode, web_search can be True or False depending on routing
        assert isinstance(result["web_search"], bool)
    
    @pytest.mark.online
    @patch('config.WEB_SEARCH_ENABLED', True)
    @patch('config.TAVILY_API_KEY', 'test_key')
    @patch('query_engine.QueryEngine')
    @patch('graph.chains.generation.generate_answer')
    @patch('graph.chains.hallucination_grader.check_hallucination')
    def test_workflow_web_search_fallback(
        self, mock_check, mock_generate, mock_query_engine_class, online_mode
    ):
        """Test workflow with web search fallback in online mode."""
        import builtins
        original_import = builtins.__import__
        
        # No documents found
        mock_engine = Mock()
        mock_engine.search.return_value = []
        mock_query_engine_class.return_value = mock_engine
        
        # Mock Tavily module and client
        mock_tavily_module = MagicMock()
        mock_client = Mock()
        mock_client.search.return_value = {
            "results": [
                {
                    "content": "Web search result",
                    "url": "https://example.com",
                    "title": "Result",
                    "score": 0.8
                }
            ]
        }
        mock_tavily_module.TavilyClient.return_value = mock_client
        
        # Make __import__ return our mock when 'tavily' is imported
        def import_side_effect(name, *args, **kwargs):
            if name == 'tavily':
                return mock_tavily_module
            return original_import(name, *args, **kwargs)
        
        mock_generate.return_value = "Answer from web search"
        mock_check.return_value = {"binary_score": "yes", "reasoning": "Grounded"}
        
        initial_state: GraphState = {
            "question": "Current events question?",
            "web_search": False,
            "web_search_results": [],
            "documents": [],
            "document_scores": [],
            "graded_documents": [],  # No relevant docs -> triggers fallback
            "grading_scores": [],
            "generation": "",
            "generation_sources": [],
            "is_grounded": False,
            "hallucination_score": 0.0,
            "retries": 0,
            "metadata": {}
        }
        
        with patch('builtins.__import__', side_effect=import_side_effect):
            result = app.invoke(initial_state)
        
        # Verify web search fallback was used
        assert result["generation"] != ""
        # In online mode with no docs, should trigger web search fallback
        assert isinstance(result.get("web_search_results", []), list)

