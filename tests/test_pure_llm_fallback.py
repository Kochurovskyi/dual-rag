"""Tests for pure LLM fallback functionality."""
import pytest
from unittest.mock import Mock, patch, MagicMock
from graph.chains.generation import generate_pure_llm_answer, generate_answer
from graph.graph import generate
from graph.state import GraphState


class TestPureLLMFallback:
    """Tests for pure LLM fallback when no documents are available."""
    
    @patch('graph.chains.generation.ChatGoogleGenerativeAI')
    @patch('graph.chains.generation.StrOutputParser')
    def test_generate_pure_llm_answer_basic(self, mock_parser, mock_llm_class):
        """Test basic pure LLM answer generation."""
        # Setup mocks
        mock_llm = Mock()
        mock_llm_class.return_value = mock_llm
        
        mock_output_parser = Mock()
        mock_output_parser.return_value = mock_output_parser
        mock_parser.return_value = mock_output_parser
        
        # Mock chain invoke
        mock_chain = Mock()
        mock_chain.invoke.return_value = "There is no answer in knowledge base but based on general knowledge, this is a test answer."
        mock_llm.__or__ = Mock(return_value=mock_chain)
        
        # Create a simple chain mock
        with patch('graph.chains.generation.ChatPromptTemplate') as mock_prompt:
            mock_prompt.from_messages.return_value.__or__ = Mock(return_value=mock_chain)
            
            result = generate_pure_llm_answer("What is Python?")
        
        # Verify result contains expected prefix (may have ellipsis or variations)
        assert "there is no answer in knowledge base" in result.lower() or "knowledge base" in result.lower()
        # Word limit check (allowing some flexibility)
        words = result.split()
        assert len(words) <= 110  # Allow some margin for actual LLM responses
    
    def test_generate_pure_llm_answer_word_limit(self):
        """Test that pure LLM answer is limited to ~100 words."""
        # Test with a question that might generate a longer response
        result = generate_pure_llm_answer("Explain quantum computing in detail")
        
        # Verify word limit is enforced
        words = result.split()
        # Should be limited to ~100 words (allow some margin)
        assert len(words) <= 110 or result.endswith("...")
        assert isinstance(result, str)
    
    def test_generate_pure_llm_answer_error_handling(self):
        """Test error handling in pure LLM answer generation."""
        # Mock chain invoke to raise exception
        with patch('graph.chains.generation.ChatPromptTemplate') as mock_prompt:
            mock_chain = Mock()
            mock_chain.invoke = Mock(side_effect=Exception("API Error"))
            mock_prompt.from_messages.return_value.__or__ = Mock(return_value=mock_chain)
            
            result = generate_pure_llm_answer("Test question")
        
        # Should return error fallback message (contains knowledge base reference)
        assert isinstance(result, str)
        assert len(result) > 0
        assert "knowledge base" in result.lower()


class TestGenerateNodePureLLMFallback:
    """Tests for generate node using pure LLM fallback in offline mode."""
    
    @pytest.mark.offline
    @patch('graph.chains.generation.generate_pure_llm_answer')
    @patch('config.AGENT_MODE', 'offline')
    def test_generate_node_uses_pure_llm_in_offline_mode(self, mock_pure_llm, offline_mode):
        """Test that generate node uses pure LLM fallback in offline mode when no documents."""
        mock_pure_llm.return_value = "There is no answer in knowledge base but this is a test answer."
        
        state: GraphState = {
            "question": "What is something not in the knowledge base?",
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
        
        # Verify pure LLM was called
        mock_pure_llm.assert_called_once_with(state["question"])
        
        # Verify state updates
        assert result["generation"] == mock_pure_llm.return_value
        assert result["metadata"]["generation_source"] == "llm_guess"
        assert result["generation_sources"] == []
    
    @pytest.mark.online
    @patch('config.AGENT_MODE', 'online')
    def test_generate_node_no_fallback_in_online_mode(self, online_mode):
        """Test that generate node doesn't use pure LLM fallback in online mode."""
        state: GraphState = {
            "question": "Test question",
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
        
        # In online mode, should return standard message, not pure LLM
        assert result["generation"] == "No relevant documents found to answer your question."
        assert result["metadata"]["generation_source"] == "none"
    
    @pytest.mark.offline
    @patch('graph.chains.generation.generate_answer')
    @patch('config.AGENT_MODE', 'offline')
    def test_generate_node_uses_rag_when_documents_exist(self, mock_generate, offline_mode):
        """Test that generate node uses RAG when documents exist, even in offline mode."""
        from langchain_core.documents import Document
        
        mock_generate.return_value = "Answer from RAG documents"
        
        state: GraphState = {
            "question": "What is LangGraph?",
            "web_search": False,
            "web_search_results": [],
            "graded_web_search_results": [],
            "documents": [],
            "document_scores": [],
            "graded_documents": [
                Document(page_content="LangGraph is a library", metadata={"file_path": "test.md"})
            ],
            "grading_scores": [0.9],
            "generation": "",
            "generation_sources": [],
            "is_grounded": False,
            "hallucination_score": 0.0,
            "retries": 0,
            "metadata": {}
        }
        
        result = generate(state)
        
        # Should use RAG, not pure LLM
        mock_generate.assert_called_once()
        assert result["metadata"]["generation_source"] == "rag"
        assert result["generation"] == mock_generate.return_value


class TestSourceIndicatorPureLLM:
    """Tests for source indicator showing 'Just guessing?' for pure LLM."""
    
    def test_format_source_llm_guess(self):
        """Test format_source function returns 'Just guessing?' for llm_guess."""
        from app import format_source
        
        result = format_source("llm_guess", "offline")
        assert "Just guessing" in result or "guessing" in result.lower()
    
    def test_format_source_all_sources(self):
        """Test format_source function for all source types."""
        from app import format_source
        
        assert "Web Search" in format_source("web_search", "online")
        assert "RAG" in format_source("rag", "offline")
        assert "ChromaDB" in format_source("rag", "offline")
        assert "PostgreSQL" in format_source("rag", "online")
        assert "Just guessing" in format_source("llm_guess", "offline") or "guessing" in format_source("llm_guess", "offline").lower()
        assert "Unknown" in format_source("none", "offline")

