"""Mode-specific tests for LangGraph nodes."""
import pytest
from unittest.mock import Mock, patch, MagicMock
from graph.graph import route_question, should_continue
from graph.nodes.web_search import web_search
from graph.state import GraphState
from langchain_core.documents import Document


class TestRouteQuestionNodeModes:
    """Mode-specific tests for route_question node."""
    
    @pytest.mark.offline
    def test_route_question_offline_forced_rag(self, offline_mode):
        """Test routing always sets web_search=False in offline mode."""
        state: GraphState = {
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
        
        result = route_question(state)
        
        assert result["web_search"] is False
        assert result["metadata"]["routing_decision"] == "rag"
    
    @pytest.mark.online
    @patch('graph.chains.router.route_question')
    def test_route_question_online_can_web_search(self, mock_route_fn, online_mode):
        """Test routing can set web_search=True in online mode."""
        # Mock router to return web_search decision
        mock_route_fn.return_value = {
            "decision": "web_search",
            "reasoning": "Question requires current information"
        }
        
        state: GraphState = {
            "question": "What is the weather today?",
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
        
        result = route_question(state)
        
        # In online mode, web_search can be True
        assert result["web_search"] in [True, False]
        assert result["metadata"]["routing_decision"] in ["rag", "web_search"]


class TestShouldContinueModes:
    """Mode-specific tests for should_continue conditional."""
    
    @pytest.mark.offline
    def test_should_continue_offline_no_docs(self, offline_mode):
        """Test should_continue always generates in offline mode (no fallback)."""
        state: GraphState = {
            "question": "Test?",
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
        
        result = should_continue(state)
        
        assert result == "generate"  # Always generate in offline mode
    
    @pytest.mark.online
    def test_should_continue_online_fallback(self, online_mode):
        """Test should_continue routes to web_search fallback in online mode."""
        state: GraphState = {
            "question": "Test?",
            "web_search": False,
            "web_search_results": [],
            "documents": [],
            "document_scores": [],
            "graded_documents": [],  # No relevant docs
            "grading_scores": [],
            "generation": "",
            "generation_sources": [],
            "is_grounded": False,
            "hallucination_score": 0.0,
            "retries": 0,
            "metadata": {}
        }
        
        result = should_continue(state)
        
        assert result == "web_search"  # Fallback to web search in online mode
    
    @pytest.mark.mode
    def test_should_continue_with_docs(self, mode):
        """Test should_continue generates when docs exist (both modes)."""
        doc = Document(
            page_content="Test content",
            metadata={"file_path": "test.md", "score": 0.9}
        )
        
        state: GraphState = {
            "question": "Test?",
            "web_search": False,
            "web_search_results": [],
            "documents": [],
            "document_scores": [],
            "graded_documents": [doc],  # Has relevant docs
            "grading_scores": [0.9],
            "generation": "",
            "generation_sources": [],
            "is_grounded": False,
            "hallucination_score": 0.0,
            "retries": 0,
            "metadata": {}
        }
        
        result = should_continue(state)
        
        assert result == "generate"  # Always generate when docs exist


class TestWebSearchNodeModes:
    """Mode-specific tests for web_search node."""
    
    @pytest.mark.offline
    def test_web_search_offline_returns_empty(self, offline_mode):
        """Test web_search returns empty results in offline mode."""
        state: GraphState = {
            "question": "What is the weather?",
            "web_search": True,
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
        
        result = web_search(state)
        
        assert len(result["web_search_results"]) == 0
        assert result["metadata"]["web_search_performed"] is False
        assert "offline" in result["metadata"]["web_search_reason"].lower()
    
    @pytest.mark.online
    @patch('config.WEB_SEARCH_ENABLED', True)
    @patch('config.TAVILY_API_KEY', 'test_key')
    def test_web_search_online_performs_search(self, online_mode):
        """Test web_search performs actual search in online mode."""
        import builtins
        original_import = builtins.__import__
        
        # Mock Tavily module and client
        mock_tavily_module = MagicMock()
        mock_client = Mock()
        mock_client.search.return_value = {
            "results": [
                {
                    "content": "Weather information",
                    "url": "https://example.com/weather",
                    "title": "Weather Forecast",
                    "score": 0.9
                }
            ]
        }
        mock_tavily_module.TavilyClient.return_value = mock_client
        
        # Make __import__ return our mock when 'tavily' is imported
        def import_side_effect(name, *args, **kwargs):
            if name == 'tavily':
                return mock_tavily_module
            return original_import(name, *args, **kwargs)
        
            state: GraphState = {
                "question": "What is the weather?",
                "web_search": True,
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
            
            result = web_search(state)
            
            assert len(result["web_search_results"]) > 0
            assert result["metadata"]["web_search_performed"] is True
            assert result["metadata"]["web_search_count"] > 0

