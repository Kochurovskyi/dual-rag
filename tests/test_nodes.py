"""Unit tests for LangGraph node functions."""
import pytest
from unittest.mock import Mock, patch, MagicMock
from graph.graph import (
    route_question,
    retrieve_documents,
    grade_documents,
    generate,
    check_hallucination,
    should_continue,
    should_retry,
    increment_retry
)
from graph.state import GraphState
from langchain_core.documents import Document


class TestRouteQuestionNode:
    """Tests for route_question node."""
    
    @pytest.mark.offline
    def test_route_question_sets_web_search_false(self):
        """Test routing sets web_search to False in offline mode."""
        state: GraphState = {
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
        
        result = route_question(state)
        
        assert result["web_search"] is False
        assert result["metadata"]["routing_decision"] == "rag"
    
    @pytest.mark.mode
    def test_route_question_adds_metadata(self, mode):
        """Test routing adds metadata."""
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
        
        result = route_question(state)
        
        assert "routing_decision" in result["metadata"]
        assert "routing_reasoning" in result["metadata"]


class TestRetrieveDocumentsNode:
    """Tests for retrieve_documents node."""
    
    @pytest.mark.mode
    @patch('query_engine.QueryEngine')
    def test_retrieve_documents(self, mock_query_engine_class, mode):
        """Test document retrieval."""
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
        
        state: GraphState = {
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
        
        result = retrieve_documents(state)
        
        assert len(result["documents"]) > 0
        assert isinstance(result["documents"][0], Document)
        assert result["metadata"]["retrieved_count"] == 1
    
    @pytest.mark.mode
    @patch('query_engine.QueryEngine')
    def test_retrieve_documents_empty_results(self, mock_query_engine_class, mode):
        """Test retrieval with no results."""
        mock_engine = Mock()
        mock_engine.search.return_value = []
        mock_query_engine_class.return_value = mock_engine
        
        state: GraphState = {
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
        
        result = retrieve_documents(state)
        
        assert len(result["documents"]) == 0
        assert result["metadata"]["retrieved_count"] == 0


class TestGradeDocumentsNode:
    """Tests for grade_documents node."""
    
    @pytest.mark.mode
    @patch('graph.chains.retrieval_grader.grade_document')
    def test_grade_documents_filters_relevant(self, mock_grade, mode):
        """Test document grading filters relevant documents."""
        mock_grade.side_effect = [
            {"binary_score": "yes", "reasoning": "Relevant"},
            {"binary_score": "no", "reasoning": "Not relevant"}
        ]
        
        doc1 = Document(page_content="LangGraph is a library.", metadata={"score": 0.9})
        doc2 = Document(page_content="Python is a language.", metadata={"score": 0.3})
        
        state: GraphState = {
            "question": "What is LangGraph?",
            "web_search": False,
            "documents": [doc1, doc2],
            "document_scores": [0.9, 0.3],
            "graded_documents": [],
            "grading_scores": [],
            "generation": "",
            "generation_sources": [],
            "is_grounded": False,
            "hallucination_score": 0.0,
            "retries": 0,
            "metadata": {}
        }
        
        result = grade_documents(state)
        
        assert len(result["graded_documents"]) == 1
        assert result["graded_documents"][0] == doc1
        assert result["metadata"]["graded_count"] == 1


class TestGenerateNode:
    """Tests for generate node."""
    
    @pytest.mark.mode
    @patch('graph.chains.generation.generate_answer')
    def test_generate_creates_answer(self, mock_generate, mode):
        """Test answer generation."""
        mock_generate.return_value = "LangGraph is a library for building agents."
        
        doc = Document(page_content="LangGraph is a library.", metadata={"file_path": "test.md"})
        
        state: GraphState = {
            "question": "What is LangGraph?",
            "web_search": False,
            "documents": [],
            "document_scores": [],
            "graded_documents": [doc],
            "grading_scores": [0.9],
            "generation": "",
            "generation_sources": [],
            "is_grounded": False,
            "hallucination_score": 0.0,
            "retries": 0,
            "metadata": {}
        }
        
        result = generate(state)
        
        assert len(result["generation"]) > 0
        assert len(result["generation_sources"]) > 0
        assert result["metadata"]["generation_length"] > 0
    
    @pytest.mark.mode
    def test_generate_no_documents(self, mode):
        """Test generation with no documents."""
        from config import AGENT_MODE
        
        state: GraphState = {
            "question": "Test?",
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
        
        result = generate(state)
        
        # In offline mode, should use pure LLM fallback
        if AGENT_MODE == "offline":
            assert "knowledge base" in result["generation"].lower()
            assert result["metadata"]["generation_source"] == "llm_guess"
        else:
            # In online mode, should return standard message
            assert "No relevant" in result["generation"]
            assert result["metadata"]["generation_source"] == "none"


class TestCheckHallucinationNode:
    """Tests for check_hallucination node."""
    
    @pytest.mark.mode
    @patch('graph.chains.hallucination_grader.check_hallucination')
    def test_check_hallucination_grounded(self, mock_check, mode):
        """Test hallucination check for grounded answer."""
        mock_check.return_value = {"binary_score": "yes", "reasoning": "Grounded"}
        
        doc = Document(page_content="LangGraph is a library.")
        
        state: GraphState = {
            "question": "What is LangGraph?",
            "web_search": False,
            "documents": [],
            "document_scores": [],
            "graded_documents": [doc],
            "grading_scores": [0.9],
            "generation": "LangGraph is a library.",
            "generation_sources": ["test.md"],
            "is_grounded": False,
            "hallucination_score": 0.0,
            "retries": 0,
            "metadata": {}
        }
        
        result = check_hallucination(state)
        
        assert result["is_grounded"] is True
        assert result["hallucination_score"] < 0.5
    
    @pytest.mark.mode
    def test_check_hallucination_no_documents(self, mode):
        """Test hallucination check with no documents."""
        state: GraphState = {
            "question": "Test?",
            "web_search": False,
            "documents": [],
            "document_scores": [],
            "graded_documents": [],
            "grading_scores": [],
            "generation": "Some answer",
            "generation_sources": [],
            "is_grounded": False,
            "hallucination_score": 0.0,
            "retries": 0,
            "metadata": {}
        }
        
        result = check_hallucination(state)
        
        assert result["is_grounded"] is False
        assert result["hallucination_score"] > 0.5


class TestShouldContinue:
    """Tests for should_continue conditional."""
    
    @pytest.mark.mode
    def test_should_continue_with_documents(self, mode):
        """Test should_continue returns generate when documents exist."""
        doc = Document(page_content="Test")
        state: GraphState = {
            "question": "Test?",
            "web_search": False,
            "documents": [],
            "document_scores": [],
            "graded_documents": [doc],
            "grading_scores": [0.9],
            "generation": "",
            "generation_sources": [],
            "is_grounded": False,
            "hallucination_score": 0.0,
            "retries": 0,
            "metadata": {}
        }
        
        result = should_continue(state)
        
        assert result == "generate"
    
    @patch('config.WEB_SEARCH_ENABLED', False)
    @pytest.mark.mode
    def test_should_continue_no_documents(self, mode):
        """Test should_continue returns generate even with no documents (offline mode)."""
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
        
        result = should_continue(state)
        
        assert result == "generate"  # Always generate in offline mode


class TestShouldRetry:
    """Tests for should_retry conditional."""
    
    @pytest.mark.mode
    def test_should_retry_when_not_grounded(self, mode):
        """Test should_retry returns retry when not grounded."""
        state: GraphState = {
            "question": "Test?",
            "web_search": False,
            "documents": [],
            "document_scores": [],
            "graded_documents": [],
            "grading_scores": [],
            "generation": "Answer",
            "generation_sources": [],
            "is_grounded": False,
            "hallucination_score": 0.9,
            "retries": 0,
            "metadata": {}
        }
        
        result = should_retry(state)
        
        assert result == "retry"
    
    @pytest.mark.mode
    def test_should_retry_when_grounded(self, mode):
        """Test should_retry returns end when grounded."""
        state: GraphState = {
            "question": "Test?",
            "web_search": False,
            "documents": [],
            "document_scores": [],
            "graded_documents": [],
            "grading_scores": [],
            "generation": "Answer",
            "generation_sources": [],
            "is_grounded": True,
            "hallucination_score": 0.1,
            "retries": 0,
            "metadata": {}
        }
        
        result = should_retry(state)
        
        assert result == "end"
    
    @pytest.mark.mode
    def test_should_retry_max_retries(self, mode):
        """Test should_retry returns end when max retries reached."""
        state: GraphState = {
            "question": "Test?",
            "web_search": False,
            "documents": [],
            "document_scores": [],
            "graded_documents": [],
            "grading_scores": [],
            "generation": "Answer",
            "generation_sources": [],
            "is_grounded": False,
            "hallucination_score": 0.9,
            "retries": 3,  # Max retries
            "metadata": {}
        }
        
        result = should_retry(state)
        
        assert result == "end"


class TestIncrementRetry:
    """Tests for increment_retry node."""
    
    @pytest.mark.mode
    def test_increment_retry(self, mode):
        """Test retry counter increment."""
        state: GraphState = {
            "question": "Test?",
            "web_search": False,
            "documents": [],
            "document_scores": [],
            "graded_documents": [],
            "grading_scores": [],
            "generation": "Answer",
            "generation_sources": [],
            "is_grounded": False,
            "hallucination_score": 0.9,
            "retries": 0,
            "metadata": {}
        }
        
        result = increment_retry(state)
        
        assert result["retries"] == 1
    
    @pytest.mark.mode
    def test_increment_retry_multiple(self, mode):
        """Test retry counter increments multiple times."""
        state: GraphState = {
            "question": "Test?",
            "web_search": False,
            "documents": [],
            "document_scores": [],
            "graded_documents": [],
            "grading_scores": [],
            "generation": "Answer",
            "generation_sources": [],
            "is_grounded": False,
            "hallucination_score": 0.9,
            "retries": 2,
            "metadata": {}
        }
        
        result = increment_retry(state)
        
        assert result["retries"] == 3

