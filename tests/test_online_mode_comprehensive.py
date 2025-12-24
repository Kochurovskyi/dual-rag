"""Comprehensive online mode tests for PostgreSQL and Tavily integration."""
import pytest
from unittest.mock import Mock, patch, MagicMock
from graph import app
from graph.state import GraphState
from graph.nodes.web_search import web_search
from graph.graph import retrieve_documents, route_question, should_continue
from langchain_core.documents import Document
from query_engine import QueryEngine


class TestOnlineModePostgreSQL:
    """Test PostgreSQL vector store integration in online mode."""
    
    @pytest.mark.online
    @patch('config.VECTOR_STORE_MODE', 'postgres')
    def test_query_engine_uses_postgres_in_online_mode(self, online_mode):
        """Test QueryEngine initializes PostgreSQL in online mode."""
        # Reload config and QueryEngine module to pick up patched config
        import importlib
        import config
        import query_engine
        importlib.reload(config)
        importlib.reload(query_engine)
        
        # Mock the actual initialization to avoid real DB connection
        with patch.object(query_engine.QueryEngine, '_init_postgres') as mock_postgres:
            with patch.object(query_engine.QueryEngine, '_init_chroma') as mock_chroma:
                engine = query_engine.QueryEngine()
                
                # Verify PostgreSQL was initialized, not ChromaDB
                mock_postgres.assert_called_once()
                mock_chroma.assert_not_called()
                assert engine.vector_store_mode == "postgres"
    
    @pytest.mark.online
    @patch('config.VECTOR_STORE_MODE', 'postgres')
    def test_query_engine_routes_to_postgres_search(self, online_mode):
        """Test QueryEngine routes to PostgreSQL search in online mode."""
        import importlib
        import config
        import query_engine
        importlib.reload(config)
        importlib.reload(query_engine)
        
        # Mock the postgres vector store
        mock_vector_store = Mock()
        mock_doc = Mock()
        mock_doc.page_content = "Test content"
        mock_doc.metadata = {
            "source": "langgraph",
            "file_path": "test.md",
            "id": "doc1"
        }
        mock_vector_store.similarity_search_with_score.return_value = [
            (mock_doc, 0.9)  # (Document, score)
        ]
        
        with patch.object(query_engine.QueryEngine, '_init_postgres'):
            engine = query_engine.QueryEngine()
            engine.vector_store_mode = "postgres"
            engine.postgres_vector_store = mock_vector_store
            
            with patch.object(engine, '_search_postgres') as mock_postgres_search:
                mock_postgres_search.return_value = [
                    {
                        "content": "Test content",
                        "source": "langgraph",
                        "file_path": "test.md",
                        "score": 0.9,
                        "distance": 0.1,
                        "id": "doc1",
                        "metadata": {}
                    }
                ]
                
                results = engine.search("test query")
                
                mock_postgres_search.assert_called_once()
                assert len(results) > 0


class TestOnlineModeTavily:
    """Test Tavily web search integration in online mode."""
    
    @pytest.mark.online
    @patch('config.TAVILY_API_KEY', 'test_key')
    def test_web_search_online_mode_enabled(self, online_mode):
        """Test web search is enabled in online mode."""
        import importlib
        import config
        importlib.reload(config)
        
        assert config.WEB_SEARCH_ENABLED is True
        assert config.AGENT_MODE == "online"
    
    @pytest.mark.online
    @patch('config.TAVILY_API_KEY', 'test_key')
    @patch('config.WEB_SEARCH_ENABLED', True)
    def test_web_search_calls_tavily_api(self, online_mode):
        """Test web search calls Tavily API in online mode."""
        import sys
        
        # Mock Tavily client
        mock_tavily_module = MagicMock()
        mock_client = Mock()
        mock_client.search.return_value = {
            "results": [
                {
                    "content": "Web search result content",
                    "url": "https://example.com",
                    "title": "Test Result",
                    "score": 0.8
                }
            ]
        }
        mock_tavily_module.TavilyClient.return_value = mock_client
        
        state: GraphState = {
            "question": "What is the weather today?",
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
        
        # Patch tavily module before importing web_search
        with patch.dict('sys.modules', {'tavily': mock_tavily_module}):
            # Reload web_search module to pick up mocked tavily
            import importlib
            import graph.nodes.web_search
            importlib.reload(graph.nodes.web_search)
            
            # Patch config values (patch config module since imports are inside function)
            with patch('config.WEB_SEARCH_ENABLED', True):
                with patch('config.TAVILY_API_KEY', 'test_key'):
                    result = graph.nodes.web_search.web_search(state)
        
        assert result["metadata"]["web_search_performed"] is True
        assert len(result["web_search_results"]) > 0
        assert result["web_search_results"][0].metadata["source"] == "web_search"
    
    @pytest.mark.online
    @patch('config.TAVILY_API_KEY', '')
    @patch('config.WEB_SEARCH_ENABLED', True)
    def test_web_search_no_api_key_handles_gracefully(self, online_mode):
        """Test web search handles missing API key gracefully."""
        import sys
        import importlib
        
        # Mock tavily module to avoid ImportError
        mock_tavily_module = MagicMock()
        
        state: GraphState = {
            "question": "Test question",
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
        
        with patch.dict('sys.modules', {'tavily': mock_tavily_module}):
            # Reload web_search module to pick up mocked tavily
            import graph.nodes.web_search
            importlib.reload(graph.nodes.web_search)
            
            with patch('config.WEB_SEARCH_ENABLED', True):
                with patch('config.TAVILY_API_KEY', ''):
                    result = graph.nodes.web_search.web_search(state)
        
        assert result["metadata"]["web_search_performed"] is False
        assert "TAVILY_API_KEY" in result["metadata"]["web_search_reason"] or "not configured" in result["metadata"]["web_search_reason"].lower()


class TestOnlineModeRouting:
    """Test routing behavior in online mode."""
    
    @pytest.mark.online
    @patch('graph.chains.router.route_question')
    def test_router_can_route_to_web_search(self, mock_route_fn, online_mode):
        """Test router can route to web search in online mode."""
        # Mock route_question to return web_search decision
        mock_route_fn.return_value = {"decision": "web_search", "reasoning": "Current events question"}
        
        result = route_question({
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
        })
        
        assert result["web_search"] is True
        assert result["metadata"]["routing_decision"] == "web_search"
    
    @pytest.mark.online
    @patch('graph.chains.router.route_question')
    def test_router_can_route_to_rag(self, mock_route_fn, online_mode):
        """Test router can route to RAG in online mode."""
        # Mock route_question to return rag decision
        mock_route_fn.return_value = {"decision": "rag", "reasoning": "Technical question"}
        
        result = route_question({
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
        })
        
        assert result["web_search"] is False
        assert result["metadata"]["routing_decision"] == "rag"


class TestOnlineModeFallback:
    """Test fallback to web search in online mode."""
    
    @pytest.mark.online
    def test_fallback_to_web_search_when_no_docs(self, online_mode):
        """Test fallback to web search when no relevant documents."""
        state: GraphState = {
            "question": "Current events question?",
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
        
        assert result == "web_search"  # Should fallback to web search
    
    @pytest.mark.online
    def test_no_fallback_when_docs_exist(self, online_mode):
        """Test no fallback when relevant documents exist."""
        from langchain_core.documents import Document
        
        state: GraphState = {
            "question": "Test question",
            "web_search": False,
            "web_search_results": [],
            "documents": [],
            "document_scores": [],
            "graded_documents": [Document(page_content="Relevant content")],
            "grading_scores": [],
            "generation": "",
            "generation_sources": [],
            "is_grounded": False,
            "hallucination_score": 0.0,
            "retries": 0,
            "metadata": {}
        }
        
        result = should_continue(state)
        
        assert result == "generate"  # Should generate from docs


class TestOnlineModeFullWorkflow:
    """Test complete workflow in online mode."""
    
    @pytest.mark.online
    @patch('query_engine.QueryEngine')
    @patch('graph.chains.retrieval_grader.grade_document')
    @patch('graph.chains.generation.generate_answer')
    @patch('graph.chains.hallucination_grader.check_hallucination')
    @patch('graph.chains.router.route_question')
    def test_full_workflow_rag_path_online(
        self, mock_route_fn, mock_check, mock_generate, mock_grade, mock_query_engine_class, online_mode
    ):
        """Test full workflow RAG path in online mode (PostgreSQL)."""
        # Setup mocks
        mock_engine = Mock()
        mock_engine.vector_store_mode = "postgres"
        mock_engine.search.return_value = [
            {
                "content": "LangGraph is a library.",
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
        
        mock_route_fn.return_value = {"decision": "rag", "reasoning": "Technical"}
        mock_grade.return_value = {"binary_score": "yes", "reasoning": "Relevant"}
        mock_generate.return_value = "LangGraph is a library."
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
        
        # Verify online mode behavior
        assert result["generation"] != ""
        assert result["is_grounded"] is True
        assert mock_engine.vector_store_mode == "postgres"
        assert result["metadata"].get("routing_decision") == "rag"
    
    @pytest.mark.online
    @patch('query_engine.QueryEngine')
    @patch('graph.chains.generation.generate_answer')
    @patch('graph.chains.hallucination_grader.check_hallucination')
    @patch('graph.chains.retrieval_grader.grade_document')
    @patch('graph.chains.router.route_question')
    def test_full_workflow_web_search_path_online(
        self, mock_route_fn, mock_grade, mock_check, mock_generate, mock_query_engine_class, online_mode
    ):
        """Test full workflow web search path in online mode."""
        import sys
        import importlib
        
        # Mock Tavily
        mock_tavily_module = MagicMock()
        mock_client = Mock()
        mock_client.search.return_value = {
            "results": [
                {
                    "content": "Web search answer",
                    "url": "https://example.com",
                    "title": "Result",
                    "score": 0.8
                }
            ]
        }
        mock_tavily_module.TavilyClient.return_value = mock_client
        
        mock_route_fn.return_value = {"decision": "web_search", "reasoning": "Current events"}
        # Mock grading to return relevant results (for web search grading)
        mock_grade.return_value = {"binary_score": "yes", "reasoning": "Relevant"}
        mock_generate.return_value = "Answer from web search"
        mock_check.return_value = {"binary_score": "yes", "reasoning": "Grounded"}
        
        initial_state: GraphState = {
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
        
        with patch.dict('sys.modules', {'tavily': mock_tavily_module}):
            # Reload web_search module to pick up mocked tavily
            import graph.nodes.web_search
            importlib.reload(graph.nodes.web_search)
            
            with patch('config.WEB_SEARCH_ENABLED', True):
                with patch('config.TAVILY_API_KEY', 'test_key'):
                    result = app.invoke(initial_state)
        
        # Verify web search path was used
        assert result["generation"] != ""
        assert result["metadata"].get("routing_decision") == "web_search"
        assert result["metadata"].get("generation_source") == "web_search"


class TestOnlineModeVectorStore:
    """Test vector store mode switching."""
    
    @pytest.mark.online
    def test_vector_store_mode_is_postgres(self, online_mode):
        """Test VECTOR_STORE_MODE is postgres in online mode."""
        import importlib
        import config
        importlib.reload(config)
        
        assert config.VECTOR_STORE_MODE == "postgres"
        assert config.AGENT_MODE == "online"
    
    @pytest.mark.offline
    def test_vector_store_mode_is_chroma(self, offline_mode):
        """Test VECTOR_STORE_MODE is chroma in offline mode."""
        import importlib
        import config
        importlib.reload(config)
        
        assert config.VECTOR_STORE_MODE == "chroma"
        assert config.AGENT_MODE == "offline"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

