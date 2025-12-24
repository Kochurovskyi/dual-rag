"""Markdown chunking utilities for splitting documents by headings."""
import re
from typing import List, Dict, Optional
from pathlib import Path


class MarkdownChunker:
    """Chunks markdown files by heading boundaries."""
    
    def __init__(self, max_chunk_size: int = 1000, min_chunk_size: int = 50, chunk_overlap: int = 0):
        self.max_chunk_size = max_chunk_size
        self.min_chunk_size = min_chunk_size
        self.chunk_overlap = chunk_overlap
    
    def _estimate_tokens(self, text: str) -> int:
        """Rough token estimation (1 token ≈ 4 characters)."""
        return len(text) // 4
    
    def _extract_code_blocks(self, text: str) -> List[Dict]:
        """Extract code blocks with their positions."""
        code_blocks = []
        pattern = r'```(\w+)?\n(.*?)```'
        
        for match in re.finditer(pattern, text, re.DOTALL):
            language = match.group(1) or ''
            code_content = match.group(2)
            code_blocks.append({
                'start': match.start(),
                'end': match.end(),
                'language': language,
                'content': code_content,
                'full_match': match.group(0)
            })
        
        return code_blocks
    
    def _split_by_headings(self, content: str) -> List[Dict]:
        """Split markdown content by headings (H1-H3)."""
        lines = content.split('\n')
        chunks = []
        current_chunk = []
        current_heading = None
        heading_stack = []
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Check for heading (H1-H3)
            heading_match = re.match(r'^(#{1,3})\s+(.+)$', line)
            if heading_match:
                level = len(heading_match.group(1))
                heading_text = heading_match.group(2).strip()
                
                # Finalize current chunk if exists
                if current_chunk:
                    chunk_text = '\n'.join(current_chunk)
                    if chunk_text.strip() and self._estimate_tokens(chunk_text) >= self.min_chunk_size:
                        chunks.append({
                            'content': chunk_text,
                            'heading_path': ' > '.join([h[0] for h in heading_stack]) if heading_stack else '',
                            'heading': current_heading,
                            'level': heading_stack[-1][1] if heading_stack else 0
                        })
                
                # Update heading stack
                while heading_stack and heading_stack[-1][1] >= level:
                    heading_stack.pop()
                
                heading_stack.append((heading_text, level))
                current_heading = heading_text
                current_chunk = [line]
            else:
                current_chunk.append(line)
            
            i += 1
        
        # Add final chunk
        if current_chunk:
            chunk_text = '\n'.join(current_chunk)
            if chunk_text.strip() and self._estimate_tokens(chunk_text) >= self.min_chunk_size:
                chunks.append({
                    'content': chunk_text,
                    'heading_path': ' > '.join([h[0] for h in heading_stack]) if heading_stack else '',
                    'heading': current_heading,
                    'level': heading_stack[-1][1] if heading_stack else 0
                })
        
        return chunks
    
    def _split_long_chunk(self, chunk: Dict) -> List[Dict]:
        """Split a chunk that exceeds max_chunk_size by paragraphs."""
        content = chunk['content']
        tokens = self._estimate_tokens(content)
        
        if tokens <= self.max_chunk_size:
            return [chunk]
        
        # Phase 2.4: For comparison sections, preserve more context
        # Detect if this is a comparison chunk (check heading and content)
        heading = chunk.get('heading', '')
        content_lower = content.lower()
        heading_lower = heading.lower() if heading else ''
        is_comparison = any(kw in content_lower or kw in heading_lower for kw in ['difference', 'vs', 'compare', 'versus', 'contrast', 'alternative'])
        
        # Use larger overlap for comparison chunks
        overlap_tokens = self.chunk_overlap * 2 if is_comparison else self.chunk_overlap
        
        # Split by double newlines (paragraphs)
        paragraphs = re.split(r'\n\n+', content)
        sub_chunks = []
        current_sub_chunk = []
        current_tokens = 0
        
        for para in paragraphs:
            para_tokens = self._estimate_tokens(para)
            
            if current_tokens + para_tokens > self.max_chunk_size and current_sub_chunk:
                # Finalize current sub-chunk
                chunk_text = '\n\n'.join(current_sub_chunk)
                sub_chunks.append({
                    'content': chunk_text,
                    'heading_path': chunk['heading_path'],
                    'heading': chunk['heading'],
                    'level': chunk['level']
                })
                
                # Add overlap: take last N tokens from current chunk
                if overlap_tokens > 0:
                    overlap_text = self._get_overlap_text(chunk_text, overlap_tokens)
                    current_sub_chunk = [overlap_text, para] if overlap_text else [para]
                    current_tokens = self._estimate_tokens(overlap_text) + para_tokens if overlap_text else para_tokens
                else:
                    current_sub_chunk = [para]
                    current_tokens = para_tokens
            else:
                current_sub_chunk.append(para)
                current_tokens += para_tokens
        
        # Add final sub-chunk
        if current_sub_chunk:
            sub_chunks.append({
                'content': '\n\n'.join(current_sub_chunk),
                'heading_path': chunk['heading_path'],
                'heading': chunk['heading'],
                'level': chunk['level']
            })
        
        return sub_chunks
    
    def _get_overlap_text(self, text: str, overlap_tokens: int) -> str:
        """Extract last N tokens from text for overlap."""
        if overlap_tokens <= 0:
            return ""
        
        # Estimate characters for overlap tokens
        overlap_chars = overlap_tokens * 4  # rough estimate
        if len(text) <= overlap_chars:
            return text
        
        # Get last N characters and find a sentence boundary
        overlap_text = text[-overlap_chars:]
        # Try to start at a sentence boundary
        for sep in ['\n\n', '. ', '.\n', '! ', '?\n']:
            idx = overlap_text.find(sep)
            if idx > 0:
                return overlap_text[idx + len(sep):]
        
        return overlap_text
    
    def _detect_code_in_chunk(self, content: str) -> tuple[bool, Optional[str]]:
        """Detect if chunk contains code blocks and return language."""
        code_blocks = self._extract_code_blocks(content)
        if not code_blocks:
            return False, None
        
        # Return the first code language found
        languages = [cb['language'] for cb in code_blocks if cb['language']]
        return True, languages[0] if languages else None
    
    def _detect_topics(self, content: str, heading: str) -> List[str]:
        """
        Detect topics in chunk content (Phase 2.1).
        
        Returns list of topic strings: error-handling, best-practices, comparison, etc.
        """
        topics = []
        content_lower = content.lower()
        heading_lower = heading.lower() if heading else ""
        combined = f"{content_lower} {heading_lower}"
        
        # Error handling
        if any(kw in combined for kw in ['error', 'exception', 'retry', 'fail', 'handle', 'catch', 'fault', 'troubleshoot']):
            topics.append('error-handling')
        
        # Best practices
        if any(kw in combined for kw in ['best practice', 'recommendation', 'guideline', 'should', 'tip', 'advice', 'pattern', 'do\'s', 'don\'ts']):
            topics.append('best-practices')
        
        # Comparison
        if any(kw in combined for kw in ['difference', 'vs', 'compare', 'versus', 'contrast', 'versus', 'alternative']):
            topics.append('comparison')
        
        # Graph types
        if any(kw in combined for kw in ['stategraph', 'messagegraph', 'graph type', 'graph api', 'graph class']):
            topics.append('graph-types')
        
        # Implementation guides
        if any(kw in combined for kw in ['how to', 'tutorial', 'example', 'guide', 'step', 'implement', 'create']):
            topics.append('tutorial')
        
        # Persistence/memory
        if any(kw in combined for kw in ['persistence', 'memory', 'checkpoint', 'state', 'thread', 'save', 'load', 'restore']):
            topics.append('persistence')
        
        # Human-in-the-loop
        if any(kw in combined for kw in ['human', 'interrupt', 'approval', 'review', 'loop', 'human-in-the-loop', 'interactive']):
            topics.append('human-in-the-loop')
        
        # Streaming
        if any(kw in combined for kw in ['stream', 'streaming', 'async', 'realtime', 'yield', 'generator']):
            topics.append('streaming')
        
        # Multi-agent
        if any(kw in combined for kw in ['multi-agent', 'multi_agent', 'multiagent', 'orchestrate', 'coordinate', 'supervisor']):
            topics.append('multi-agent')
        
        # Tools
        if any(kw in combined for kw in ['tool', 'tools', 'function', 'callable', 'function calling']):
            topics.append('tools')
        
        # Deployment
        if any(kw in combined for kw in ['deploy', 'deployment', 'production', 'serve', 'hosting', 'cloud', 'docker', 'kubernetes']):
            topics.append('deployment')
        
        # Subgraphs
        if any(kw in combined for kw in ['subgraph', 'subgraphs', 'modular', 'compose', 'nested']):
            topics.append('subgraphs')
        
        # RAG
        if any(kw in combined for kw in ['rag', 'retrieval', 'augmented', 'generation', 'retrieval-augmented']):
            topics.append('rag')
        
        # Agents
        if any(kw in combined for kw in ['agent', 'agents', 'autonomous']):
            topics.append('agents')
        
        # Vector stores
        if any(kw in combined for kw in ['vector', 'embedding', 'similarity', 'store', 'vectorstore']):
            topics.append('vectorstores')
        
        # Document loaders
        if any(kw in combined for kw in ['loader', 'loaders', 'document', 'ingest', 'ingestion', 'parse']):
            topics.append('document-loaders')
        
        # Memory
        if any(kw in combined for kw in ['memory', 'conversation', 'history', 'chat', 'context']):
            topics.append('memory')
        
        # Models
        if any(kw in combined for kw in ['model', 'models', 'llm', 'provider', 'openai', 'anthropic']):
            topics.append('models')
        
        return topics
    
    def _extract_keywords(self, content: str, max_keywords: int = 15) -> List[str]:
        """
        Extract important keywords from chunk content (Phase 2.2).
        
        Returns list of keyword strings.
        """
        keywords = []
        
        # Extract code-related terms (class names, function names)
        # Pattern: Capitalized words, def function_name, class ClassName
        code_pattern = r'\b([A-Z][a-zA-Z]{2,}|def\s+(\w+)|class\s+(\w+))\b'
        matches = re.findall(code_pattern, content)
        for match in matches:
            keyword = match[0] if match[0] else (match[1] if match[1] else match[2])
            if keyword and len(keyword) > 2 and keyword not in ['The', 'This', 'That', 'You', 'For', 'With', 'From']:
                keywords.append(keyword)
        
        # Extract quoted terms (often important concepts)
        quoted_pattern = r'"([^"]{3,})"'
        keywords.extend(re.findall(quoted_pattern, content))
        
        # Extract markdown code blocks language
        code_block_pattern = r'```(\w+)'
        keywords.extend(re.findall(code_block_pattern, content))
        
        # Extract technical terms (StateGraph, MessageGraph, etc.)
        tech_pattern = r'\b([A-Z][a-z]+[A-Z][a-zA-Z]+)\b'  # CamelCase
        keywords.extend(re.findall(tech_pattern, content))
        
        # Remove duplicates, common words, and limit
        stop_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'its', 'may', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'let', 'put', 'say', 'she', 'too', 'use', 'this', 'that', 'with', 'from', 'have', 'been', 'will', 'when', 'what', 'where', 'which', 'there', 'their', 'them', 'then', 'than', 'these', 'those'}
        unique_keywords = [kw.lower() for kw in set(keywords) if kw.lower() not in stop_words and len(kw) > 2]
        return unique_keywords[:max_keywords]
    
    def _detect_content_type(self, content: str, heading: str) -> str:
        """
        Detect content type of chunk (Phase 2.3).
        
        Returns: 'code-example', 'tutorial', 'reference', 'concept', or 'general'
        """
        content_lower = content.lower()
        
        # Code-heavy chunks
        if content.count('```') >= 2:
            return 'code-example'
        
        # Tutorial chunks
        if any(kw in content_lower for kw in ['step', 'tutorial', 'example', 'how to', 'guide', 'walkthrough']):
            return 'tutorial'
        
        # Reference chunks
        if any(kw in content_lower for kw in ['api', 'reference', 'class', 'function', 'method', 'parameter', 'attribute', 'property']):
            return 'reference'
        
        # Concept chunks
        if any(kw in content_lower for kw in ['concept', 'overview', 'introduction', 'what is', 'understanding', 'explanation']):
            return 'concept'
        
        return 'general'
    
    def chunk_file(self, file_path: Path, source: str) -> List[Dict]:
        """Chunk a markdown file and return chunks with metadata."""
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return []
        
        # Split by headings
        chunks = self._split_by_headings(content)
        
        # Split long chunks
        final_chunks = []
        for chunk in chunks:
            if self._estimate_tokens(chunk['content']) > self.max_chunk_size:
                final_chunks.extend(self._split_long_chunk(chunk))
            else:
                final_chunks.append(chunk)
        
        # Add metadata to each chunk
        # Calculate relative path from docs directory
        from config import SOURCES
        docs_dir = SOURCES[source]['docs_dir']
        try:
            relative_path = str(file_path.relative_to(docs_dir.parent))
        except ValueError:
            # Fallback: find docs in path
            parts = file_path.parts
            if 'docs' in parts:
                docs_idx = parts.index('docs')
                relative_path = '/'.join(parts[docs_idx:])
            else:
                relative_path = str(file_path)
        
        result = []
        for i, chunk in enumerate(final_chunks):
            has_code, code_language = self._detect_code_in_chunk(chunk['content'])
            
            # Phase 2: Detect topics, extract keywords, detect content type
            topics = self._detect_topics(chunk['content'], chunk.get('heading', ''))
            keywords = self._extract_keywords(chunk['content'])
            content_type = self._detect_content_type(chunk['content'], chunk.get('heading', ''))
            
            result.append({
                'content': chunk['content'],
                'metadata': {
                    'source': source,
                    'file_path': relative_path,
                    'heading_path': chunk['heading_path'],
                    'heading': chunk['heading'],
                    'chunk_index': i,
                    'has_code': has_code,
                    'code_language': code_language,
                    'token_count': self._estimate_tokens(chunk['content']),
                    # Phase 2 metadata
                    'topics': topics,  # List[str]
                    'keywords': keywords,  # List[str]
                    'content_type': content_type  # str
                }
            })
        
        return result

