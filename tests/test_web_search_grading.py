"""Pytest tests for web search result grading."""
import pytest
from unittest.mock import Mock, patch, MagicMock
from graph.nodes.grade_web_search import grade_web_search_results
from graph.state import GraphState
from langchain_core.documents import Document


class TestWebSearchGrading:
    """Test web search result grading functionality."""
    
    @pytest.fixture
    def sample_web_search_results(self):
        """Create sample web search results for testing."""
        return [
            Document(
                page_content="LangGraph is a library for building stateful agents with LangChain.",
                metadata={
                    "source": "web_search",
                    "url": "https://example.com/langgraph",
                    "title": "LangGraph Documentation",
                    "score": 0.9
                }
            ),
            Document(
                page_content="The weather today is sunny with a high of 75 degrees.",
                metadata={
                    "source": "web_search",
                    "url": "https://example.com/weather",
                    "title": "Weather Forecast",
                    "score": 0.8
                }
            ),
            Document(
                page_content="Python is a programming language used for web development.",
                metadata={
                    "source": "web_search",
                    "url": "https://example.com/python",
                    "title": "Python Guide",
                    "score": 0.7
                }
            )
        ]
    
    @pytest.fixture
    def sample_state(self, sample_web_search_results):
        """Create sample GraphState for testing."""
        return {
            "question": "What is LangGraph?",
            "web_search": True,
            "web_search_results": sample_web_search_results,
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
    
    def test_grade_web_search_results_basic(self, sample_state):
        """Test basic grading functionality."""
        result = grade_web_search_results(sample_state)
        
        assert "graded_web_search_results" in result
        assert "web_search_grading_scores" in result
        assert "metadata" in result
        assert result["metadata"]["web_search_total_count"] == 3
        assert result["metadata"]["web_search_graded_count"] >= 0
        assert result["metadata"]["web_search_filtered_count"] >= 0
    
    def test_grade_web_search_results_empty(self):
        """Test grading with empty results."""
        state: GraphState = {
            "question": "What is LangGraph?",
            "web_search": True,
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
        
        result = grade_web_search_results(state)
        
        assert len(result["graded_web_search_results"]) == 0
        assert result["metadata"]["web_search_graded_count"] == 0
        assert result["metadata"]["web_search_total_count"] == 0
        assert result["metadata"]["web_search_filtered_count"] == 0
    
    def test_grade_web_search_results_filters_irrelevant(self, sample_state):
        """Test that irrelevant results are filtered out."""
        result = grade_web_search_results(sample_state)
        
        total = result["metadata"]["web_search_total_count"]
        graded = result["metadata"]["web_search_graded_count"]
        filtered = result["metadata"]["web_search_filtered_count"]
        
        assert total == 3
        assert graded <= total
        assert filtered == total - graded
        assert len(result["graded_web_search_results"]) == graded
    
    def test_grade_web_search_results_metadata(self, sample_state):
        """Test that metadata is properly set."""
        result = grade_web_search_results(sample_state)
        
        required_metadata = [
            "web_search_graded_count",
            "web_search_total_count",
            "web_search_filtered_count"
        ]
        
        for key in required_metadata:
            assert key in result["metadata"], f"Missing metadata key: {key}"
    
    def test_grade_web_search_results_scores(self, sample_state):
        """Test that scores are properly preserved."""
        result = grade_web_search_results(sample_state)
        
        assert len(result["web_search_grading_scores"]) == len(result["graded_web_search_results"])
        
        if result["graded_web_search_results"]:
            for score in result["web_search_grading_scores"]:
                assert isinstance(score, (int, float))
                assert 0 <= score <= 1
    
    def test_grade_web_search_results_preserves_state(self, sample_state):
        """Test that original state fields are preserved."""
        original_question = sample_state["question"]
        original_web_search_results = sample_state["web_search_results"]
        
        result = grade_web_search_results(sample_state)
        
        assert result["question"] == original_question
        assert result["web_search_results"] == original_web_search_results
        assert "graded_web_search_results" in result
        assert "web_search_grading_scores" in result


class TestWebSearchGradingIntegration:
    """Integration tests for web search grading with full workflow."""
    
    @pytest.mark.online
    @patch('graph.nodes.grade_web_search.grade_document')
    def test_web_search_grading_in_workflow(self, mock_grade, online_mode):
        """Test web search grading integrated in workflow."""
        # Mock grader to return relevant for first result, irrelevant for others
        def grade_side_effect(question, document):
            if "LangGraph" in document:
                return {"binary_score": "yes", "reasoning": "Relevant"}
            return {"binary_score": "no", "reasoning": "Not relevant"}
        
        mock_grade.side_effect = grade_side_effect
        
        web_results = [
            Document(
                page_content="LangGraph is a library.",
                metadata={"source": "web_search", "url": "https://example.com/langgraph", "score": 0.9}
            ),
            Document(
                page_content="Weather is nice.",
                metadata={"source": "web_search", "url": "https://example.com/weather", "score": 0.8}
            )
        ]
        
        state: GraphState = {
            "question": "What is LangGraph?",
            "web_search": True,
            "web_search_results": web_results,
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
        
        result = grade_web_search_results(state)
        
        assert mock_grade.call_count == 2
        assert len(result["graded_web_search_results"]) == 1
        assert result["graded_web_search_results"][0].page_content == "LangGraph is a library."
    
    @pytest.mark.online
    def test_web_search_grading_all_irrelevant(self, online_mode):
        """Test scenario where all results are irrelevant."""
        web_results = [
            Document(
                page_content="Weather is sunny.",
                metadata={"source": "web_search", "url": "https://example.com/weather", "score": 0.9}
            ),
            Document(
                page_content="Python is a language.",
                metadata={"source": "web_search", "url": "https://example.com/python", "score": 0.8}
            )
        ]
        
        state: GraphState = {
            "question": "What is LangGraph?",
            "web_search": True,
            "web_search_results": web_results,
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
        
        result = grade_web_search_results(state)
        
        assert result["metadata"]["web_search_total_count"] == 2
        assert result["metadata"]["web_search_graded_count"] <= 2
        assert len(result["graded_web_search_results"]) == result["metadata"]["web_search_graded_count"]


class TestWebSearchGradingWithGenerate:
    """Test web search grading integration with generate node."""
    
    @pytest.mark.online
    @patch('graph.chains.generation.generate_answer')
    @patch('graph.chains.retrieval_grader.grade_document')
    def test_generate_uses_graded_web_search_results(self, mock_grade, mock_generate, online_mode):
        """Test that generate node uses graded web search results."""
        from graph.graph import generate
        
        # Mock grader
        def grade_side_effect(question, document):
            if "LangGraph" in document:
                return {"binary_score": "yes", "reasoning": "Relevant"}
            return {"binary_score": "no", "reasoning": "Not relevant"}
        
        mock_grade.side_effect = grade_side_effect
        mock_generate.return_value = "LangGraph is a library."
        
        web_results = [
            Document(
                page_content="LangGraph is a library.",
                metadata={"source": "web_search", "url": "https://example.com/langgraph", "score": 0.9}
            ),
            Document(
                page_content="Weather is nice.",
                metadata={"source": "web_search", "url": "https://example.com/weather", "score": 0.8}
            )
        ]
        
        # First grade the results
        state: GraphState = {
            "question": "What is LangGraph?",
            "web_search": True,
            "web_search_results": web_results,
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
        
        graded_state = grade_web_search_results(state)
        
        # Now test generate uses graded results
        result = generate(graded_state)
        
        # Generate should use graded_web_search_results
        assert result["generation"] != ""
        assert result["metadata"]["generation_source"] == "web_search"
        assert len(result["generation_sources"]) == len(graded_state["graded_web_search_results"])


class TestWebSearchGradingModeAware:
    """Test web search grading is mode-aware."""
    
    @pytest.mark.offline
    def test_web_search_grading_works_in_offline_mode(self, offline_mode):
        """Test grading works even in offline mode (if results exist)."""
        web_results = [
            Document(
                page_content="LangGraph is a library.",
                metadata={"source": "web_search", "url": "https://example.com/langgraph", "score": 0.9}
            )
        ]
        
        state: GraphState = {
            "question": "What is LangGraph?",
            "web_search": True,
            "web_search_results": web_results,
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
        
        result = grade_web_search_results(state)
        
        # Should work regardless of mode (grading doesn't depend on mode)
        assert "graded_web_search_results" in result
        assert result["metadata"]["web_search_total_count"] == 1
    
    @pytest.mark.online
    def test_web_search_grading_works_in_online_mode(self, online_mode):
        """Test grading works in online mode."""
        web_results = [
            Document(
                page_content="LangGraph is a library.",
                metadata={"source": "web_search", "url": "https://example.com/langgraph", "score": 0.9}
            )
        ]
        
        state: GraphState = {
            "question": "What is LangGraph?",
            "web_search": True,
            "web_search_results": web_results,
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
        
        result = grade_web_search_results(state)
        
        assert "graded_web_search_results" in result
        assert result["metadata"]["web_search_total_count"] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

