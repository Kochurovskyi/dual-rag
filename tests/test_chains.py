"""Unit tests for LangChain chains."""
import pytest
from unittest.mock import Mock, patch
from graph.chains.router import route_question, RouteDecision
from graph.chains.retrieval_grader import grade_document, GradeDocument
from graph.chains.hallucination_grader import check_hallucination, GradeHallucination
from graph.chains.generation import generate_answer


class TestRouterChain:
    """Tests for question routing chain."""
    
    @pytest.mark.offline
    def test_route_question_offline_mode(self, offline_mode):
        """Test routing in offline mode always returns RAG."""
        result = route_question("What is LangGraph?")
        
        assert result["decision"] == "rag"
        assert "offline" in result["reasoning"].lower()
    
    @pytest.mark.mode
    def test_route_question_returns_dict(self, mode):
        """Test router returns proper dict structure."""
        result = route_question("Test question")
        
        assert isinstance(result, dict)
        assert "decision" in result
        assert "reasoning" in result
        assert result["decision"] in ["rag", "web_search"]


class TestRetrievalGraderChain:
    """Tests for document relevance grading chain."""
    
    @pytest.mark.mode
    @patch('graph.chains.retrieval_grader.grade_document_chain')
    def test_grade_document_relevant(self, mock_chain, mode):
        """Test grading relevant document."""
        mock_result = Mock()
        mock_result.binary_score = "yes"
        mock_result.reasoning = "Document is relevant"
        mock_chain.invoke.return_value = mock_result
        
        result = grade_document(
            question="What is LangGraph?",
            document="LangGraph is a library for building stateful agents."
        )
        
        assert result["binary_score"] == "yes"
        assert "reasoning" in result
    
    @patch('graph.chains.retrieval_grader.grade_document_chain')
    @pytest.mark.mode
    def test_grade_document_not_relevant(self, mock_chain, mode):
        """Test grading irrelevant document."""
        mock_result = Mock()
        mock_result.binary_score = "no"
        mock_result.reasoning = "Document is not relevant"
        mock_chain.invoke.return_value = mock_result
        
        result = grade_document(
            question="What is LangGraph?",
            document="Python is a programming language."
        )
        
        assert result["binary_score"] == "no"
    
    @pytest.mark.mode
    def test_grade_document_returns_dict(self, mode):
        """Test grader returns proper dict structure."""
        with patch('graph.chains.retrieval_grader.grade_document_chain') as mock_chain:
            mock_result = Mock()
            mock_result.binary_score = "yes"
            mock_result.reasoning = "Test"
            mock_chain.invoke.return_value = mock_result
            
            result = grade_document("Q", "D")
            
            assert isinstance(result, dict)
            assert "binary_score" in result
            assert "reasoning" in result


class TestHallucinationGraderChain:
    """Tests for hallucination detection chain."""
    
    @pytest.mark.mode
    @patch('graph.chains.hallucination_grader.check_hallucination_chain')
    def test_check_hallucination_grounded(self, mock_chain, mode):
        """Test detecting grounded answer."""
        mock_result = Mock()
        mock_result.binary_score = "yes"
        mock_result.reasoning = "Answer is grounded"
        mock_chain.invoke.return_value = mock_result
        
        result = check_hallucination(
            question="What is LangGraph?",
            answer="LangGraph is a library for building agents.",
            documents=["LangGraph is a library for building stateful agents."]
        )
        
        assert result["binary_score"] == "yes"
    
    @patch('graph.chains.hallucination_grader.check_hallucination_chain')
    @pytest.mark.mode
    def test_check_hallucination_hallucinated(self, mock_chain, mode):
        """Test detecting hallucinated answer."""
        mock_result = Mock()
        mock_result.binary_score = "no"
        mock_result.reasoning = "Answer contains information not in documents"
        mock_chain.invoke.return_value = mock_result
        
        result = check_hallucination(
            question="What is LangGraph?",
            answer="LangGraph is a Python library created in 2024.",
            documents=["LangGraph is a library."]
        )
        
        assert result["binary_score"] == "no"
    
    @pytest.mark.mode
    def test_check_hallucination_formats_documents(self, mode):
        """Test document formatting for hallucination check."""
        with patch('graph.chains.hallucination_grader.check_hallucination_chain') as mock_chain:
            mock_result = Mock()
            mock_result.binary_score = "yes"
            mock_result.reasoning = "Test"
            mock_chain.invoke.return_value = mock_result
            
            check_hallucination("Q", "A", ["Doc1", "Doc2"])
            
            # Verify documents were formatted
            call_args = mock_chain.invoke.call_args[0][0]
            assert "documents" in call_args
            assert "Doc1" in call_args["documents"]
            assert "Doc2" in call_args["documents"]


class TestGenerationChain:
    """Tests for answer generation chain."""
    
    @pytest.mark.mode
    @patch('graph.chains.generation.generate_answer_chain')
    def test_generate_answer(self, mock_chain, mode):
        """Test answer generation."""
        mock_chain.invoke.return_value = "LangGraph is a library for building agents."
        
        result = generate_answer(
            question="What is LangGraph?",
            documents=["LangGraph is a library for building stateful agents."]
        )
        
        assert isinstance(result, str)
        assert len(result) > 0
    
    @pytest.mark.mode
    def test_generate_answer_formats_context(self, mode):
        """Test context formatting for generation."""
        with patch('graph.chains.generation.generate_answer_chain') as mock_chain:
            mock_chain.invoke.return_value = "Answer"
            
            generate_answer("Q", ["Doc1", "Doc2"])
            
            # Verify context was formatted
            call_args = mock_chain.invoke.call_args[0][0]
            assert "context" in call_args
            assert "Doc1" in call_args["context"]
            assert "Doc2" in call_args["context"]
    
    @patch('graph.chains.generation.generate_answer_chain')
    @pytest.mark.mode
    def test_generate_answer_empty_documents(self, mock_chain, mode):
        """Test generation with empty documents."""
        mock_chain.invoke.return_value = "No relevant documents found."
        
        result = generate_answer(question="Test?", documents=[])
        
        assert isinstance(result, str)

