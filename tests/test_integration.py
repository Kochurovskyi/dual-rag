"""Integration tests for full graph workflow."""
import pytest
from unittest.mock import Mock, patch, MagicMock
from graph import app
from graph.state import GraphState
from langchain_core.documents import Document


class TestFullWorkflow:
    """Integration tests for complete graph workflow."""
    
    @pytest.mark.mode
    @patch('query_engine.QueryEngine')
    @patch('graph.chains.retrieval_grader.grade_document')
    @patch('graph.chains.generation.generate_answer')
    @patch('graph.chains.hallucination_grader.check_hallucination')
    def test_full_workflow_success(self, mock_check, mock_generate, mock_grade, mock_query_engine_class, mode):
        """Test successful end-to-end workflow."""
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
        
        # Initial state
        initial_state: GraphState = {
            "question": "What is LangGraph?",
            "web_search": False,
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
        
        # Run workflow
        result = app.invoke(initial_state)
        
        # Verify results
        assert result["generation"] != ""
        assert result["is_grounded"] is True
        assert len(result["generation_sources"]) > 0
        assert result["retries"] == 0
    
    @pytest.mark.mode
    @patch('query_engine.QueryEngine')
    @patch('graph.chains.retrieval_grader.grade_document')
    @patch('graph.chains.generation.generate_answer')
    @patch('graph.chains.hallucination_grader.check_hallucination')
    def test_workflow_with_retry(self, mock_check, mock_generate, mock_grade, mock_query_engine_class, mode):
        """Test workflow with hallucination retry."""
        # Setup mocks
        mock_engine = Mock()
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
        
        mock_grade.return_value = {"binary_score": "yes", "reasoning": "Relevant"}
        # First generation hallucinated, second grounded
        mock_generate.side_effect = [
            "LangGraph was created in 2024.",  # Hallucinated
            "LangGraph is a library."  # Grounded
        ]
        mock_check.side_effect = [
            {"binary_score": "no", "reasoning": "Hallucinated"},  # First check
            {"binary_score": "yes", "reasoning": "Grounded"}  # Second check
        ]
        
        initial_state: GraphState = {
            "question": "What is LangGraph?",
            "web_search": False,
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
        
        # Run workflow
        result = app.invoke(initial_state)
        
        # Verify retry happened
        assert result["is_grounded"] is True
        assert mock_generate.call_count == 2  # Called twice due to retry
    
    @pytest.mark.mode
    @patch('query_engine.QueryEngine')
    def test_workflow_no_documents(self, mock_query_engine_class, mode):
        """Test workflow when no documents are found."""
        mock_engine = Mock()
        mock_engine.search.return_value = []
        mock_query_engine_class.return_value = mock_engine
        
        initial_state: GraphState = {
            "question": "Unknown topic?",
            "web_search": False,
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
        
        with patch('graph.chains.generation.generate_answer') as mock_generate:
            mock_generate.return_value = "No relevant documents found."
            
            result = app.invoke(initial_state)
            
            assert "No relevant" in result["generation"] or len(result["generation"]) > 0


class TestStateTransitions:
    """Tests for state transitions in workflow."""
    
    @pytest.mark.mode
    def test_state_initialization(self, mode):
        """Test initial state structure."""
        state: GraphState = {
            "question": "Test?",
            "web_search": False,
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
        
        assert state["question"] == "Test?"
        assert state["retries"] == 0
        assert isinstance(state["documents"], list)
    
    @pytest.mark.mode
    @patch('query_engine.QueryEngine')
    def test_state_after_retrieval(self, mock_query_engine_class, mode):
        """Test state after document retrieval."""
        mock_engine = Mock()
        mock_engine.search.return_value = [
            {
                "content": "Test content",
                "source": "test",
                "file_path": "test.md",
                "score": 0.8,
                "distance": 0.2,
                "id": "doc1",
                "heading": "Test",
                "heading_path": "",
                "chunk_index": 0,
                "has_code": False,
                "code_language": None,
                "metadata": {}
            }
        ]
        mock_query_engine_class.return_value = mock_engine
        
        from graph.graph import retrieve_documents
        
        state: GraphState = {
            "question": "Test?",
            "web_search": False,
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
        
        result = retrieve_documents(state)
        
        assert len(result["documents"]) > 0
        assert len(result["document_scores"]) > 0
        assert "retrieved_count" in result["metadata"]

