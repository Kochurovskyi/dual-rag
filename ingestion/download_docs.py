#!/usr/bin/env python3
"""Download all markdown files from LangGraph and LangChain llms.txt index files."""
import re
import json
import hashlib
import requests
import time
from pathlib import Path
from urllib.parse import urlparse
from typing import Set, Dict, Optional
from datetime import datetime

try:
    from .html_cleaner import LangGraphHTMLCleaner
    HAS_HTML_CLEANER = True
except (ImportError, ValueError):
    try:
        from html_cleaner import LangGraphHTMLCleaner
        HAS_HTML_CLEANER = True
    except ImportError:
        HAS_HTML_CLEANER = False
        print("Warning: html_cleaner module not found. HTML pages will be skipped.")

try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False
    # Fallback progress function
    def tqdm(iterable, **kwargs):
        return iterable

def convert_github_url_to_docs_url(github_url: str) -> str:
    """Convert GitHub edit URL to docs URL."""
    # Pattern: https://github.com/langchain-ai/docs/edit/main/src/langsmith/add-auth-server.mdx
    # Convert to: https://docs.langchain.com/langsmith/add-auth-server.md
    
    if '/edit/main/src/' in github_url:
        # Extract path after /src/
        path_part = github_url.split('/edit/main/src/')[1]
        # Remove .mdx or .md extension
        path_part = path_part.replace('.mdx', '').replace('.md', '')
        # Convert to docs URL
        docs_url = f"https://docs.langchain.com/{path_part}.md"
        return docs_url
    return None


def detect_file_content_type(file_path: Path, url: str) -> str:
    """
    Detect content type from file path and URL (Phase 1.1).
    
    Returns: 'tutorial', 'reference', 'api', 'concept', 'how-to', 'guide', or 'general'
    """
    path_str = str(file_path).lower()
    url_lower = url.lower()
    combined = f"{path_str} {url_lower}"
    
    # Tutorial indicators
    if any(kw in combined for kw in ['tutorial', 'tutorials', 'learn', 'getting-started', 'quickstart', 'quick-start']):
        return 'tutorial'
    
    # Reference/API indicators
    if any(kw in combined for kw in ['api', 'reference', 'api-reference', 'api_reference']):
        return 'reference'
    
    # How-to guides
    if any(kw in combined for kw in ['how-to', 'howto', 'how_to', 'guide', 'guides', 'how-tos']):
        return 'how-to'
    
    # Concept/overview
    if any(kw in combined for kw in ['concept', 'concepts', 'overview', 'introduction', 'intro', 'what-is']):
        return 'concept'
    
    # Examples
    if any(kw in combined for kw in ['example', 'examples', 'sample', 'samples']):
        return 'example'
    
    # Deployment/production
    if any(kw in combined for kw in ['deploy', 'deployment', 'production', 'serve', 'hosting']):
        return 'deployment'
    
    # Integration
    if any(kw in combined for kw in ['integration', 'integrations', 'integrate']):
        return 'integration'
    
    return 'general'


def detect_file_topics(file_path: Path, url: str) -> list[str]:
    """
    Detect topic hints from file path and URL (Phase 1.2).
    
    Returns: List of topic strings
    """
    topics = []
    path_str = str(file_path).lower()
    url_lower = url.lower()
    combined = f"{path_str} {url_lower}"
    
    # Error handling
    if any(kw in combined for kw in ['error', 'exception', 'retry', 'fail', 'handle', 'catch', 'fault']):
        topics.append('error-handling')
    
    # Best practices
    if any(kw in combined for kw in ['best-practice', 'best_practice', 'recommendation', 'guideline', 'pattern', 'tip']):
        topics.append('best-practices')
    
    # Persistence/memory
    if any(kw in combined for kw in ['persist', 'persistence', 'memory', 'checkpoint', 'state', 'thread', 'storage']):
        topics.append('persistence')
    
    # Human-in-the-loop
    if any(kw in combined for kw in ['human', 'interrupt', 'approval', 'review', 'loop', 'human-in-the-loop']):
        topics.append('human-in-the-loop')
    
    # Streaming
    if any(kw in combined for kw in ['stream', 'streaming', 'async', 'realtime']):
        topics.append('streaming')
    
    # Multi-agent
    if any(kw in combined for kw in ['multi-agent', 'multi_agent', 'multiagent', 'orchestrate', 'coordinate']):
        topics.append('multi-agent')
    
    # Tools
    if any(kw in combined for kw in ['tool', 'tools', 'function', 'callable']):
        topics.append('tools')
    
    # Deployment
    if any(kw in combined for kw in ['deploy', 'deployment', 'production', 'serve', 'hosting', 'cloud']):
        topics.append('deployment')
    
    # Subgraphs
    if any(kw in combined for kw in ['subgraph', 'subgraphs', 'modular', 'compose']):
        topics.append('subgraphs')
    
    # Graph types
    if any(kw in combined for kw in ['stategraph', 'messagegraph', 'graph-type', 'graph_api']):
        topics.append('graph-types')
    
    # Comparison
    if any(kw in combined for kw in ['difference', 'vs', 'compare', 'versus', 'contrast']):
        topics.append('comparison')
    
    # RAG
    if any(kw in combined for kw in ['rag', 'retrieval', 'augmented', 'generation']):
        topics.append('rag')
    
    # Agents
    if any(kw in combined for kw in ['agent', 'agents']):
        topics.append('agents')
    
    # Vector stores
    if any(kw in combined for kw in ['vector', 'embedding', 'similarity', 'store']):
        topics.append('vectorstores')
    
    # Document loaders
    if any(kw in combined for kw in ['loader', 'loaders', 'document', 'ingest', 'ingestion']):
        topics.append('document-loaders')
    
    # Memory
    if any(kw in combined for kw in ['memory', 'conversation', 'history', 'chat']):
        topics.append('memory')
    
    # Models
    if any(kw in combined for kw in ['model', 'models', 'llm', 'provider']):
        topics.append('models')
    
    return topics

def extract_md_urls(content: str, base_url: str = None, include_html: bool = False) -> Set[str]:
    """
    Extract all markdown URLs from llms.txt content.
    
    Args:
        content: Content of llms.txt file
        base_url: Base URL for normalization
        include_html: If True, also extract HTML page URLs (for LangGraph)
    
    Returns:
        Set of URLs to download
    """
    urls = set()
    
    # Pattern 1: Markdown links: [text](url.md)
    pattern1 = r'https://[^\s)]+\.md'
    found_urls = re.findall(pattern1, content)
    # Convert GitHub edit URLs to docs URLs, filter out others
    for url in found_urls:
        if 'github.com' in url and '/edit/' in url:
            # Convert GitHub edit URL to docs URL
            docs_url = convert_github_url_to_docs_url(url)
            if docs_url:
                urls.add(docs_url)
        elif 'github.com' not in url:
            # Regular docs URL
            urls.add(url)
    
    # Pattern 2: Source: lines in llms-full.txt format
    # Source: https://docs.langchain.com/path/to/page
    pattern2 = r'Source:\s+(https://[^\s]+)'
    source_urls = re.findall(pattern2, content)
    for url in source_urls:
        # Skip GitHub URLs
        if 'github.com' in url:
            continue
        # Add .md if not already present
        if not url.endswith('.md'):
            urls.add(url + '.md')
        else:
            urls.add(url)
    
    # Pattern 3: URLs in markdown links (LangGraph format)
    # LangGraph llms.txt contains HTML page URLs that need to be converted
    pattern3 = r'\[([^\]]+)\]\((https://[^\)]+)\)'
    md_links = re.findall(pattern3, content)
    for text, url in md_links:
        # Convert GitHub edit URLs to docs URLs
        if 'github.com' in url and '/edit/' in url:
            docs_url = convert_github_url_to_docs_url(url)
            if docs_url:
                urls.add(docs_url)
            continue
        if url.endswith('.md'):
            urls.add(url)
        elif include_html and 'langchain-ai.github.io/langgraph' in url:
            # Include HTML pages from LangGraph - we'll convert them to markdown
            urls.add(url)
    
    return urls

def calculate_checksum(file_path: Path) -> str:
    """Calculate SHA256 checksum of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    return sha256.hexdigest()

def validate_markdown_content(content: str, url: str) -> tuple[bool, str]:
    """
    Validate markdown content for common issues.
    
    Returns:
        (is_valid, error_message)
    """
    content = content.strip()
    
    # Check if content is empty
    if not content:
        return False, "Content is empty"
    
    # Check minimum length (should have substantial content)
    if len(content) < 50:
        return False, f"Content too short ({len(content)} chars)"
    
    # Check for redirect pages
    if 'Redirecting...' in content or 'redirect' in content.lower()[:200]:
        return False, "Contains redirect text"
    
    # Check for HTML error pages
    if content.startswith('<!DOCTYPE') or content.startswith('<html'):
        return False, "Content is HTML, not markdown"
    
    # Check for valid markdown structure (should start with heading, code block, or list)
    first_line = content.split('\n')[0].strip()
    valid_starters = ['#', '```', '*', '-', '1.', '>', '[', '`']
    if not any(first_line.startswith(s) for s in valid_starters):
        # Allow if it's a code block continuation or has markdown-like content
        if '`' not in content[:100] and '[' not in content[:100]:
            return False, f"Doesn't appear to be valid markdown (starts with: {first_line[:50]})"
    
    # Check for common error indicators
    error_indicators = [
        '404', 'not found', 'page not found', 'error', 'forbidden',
        'access denied', 'unauthorized'
    ]
    content_lower = content.lower()
    for indicator in error_indicators:
        if indicator in content_lower[:500]:
            return False, f"Contains error indicator: {indicator}"
    
    # Check for reasonable content distribution (not just whitespace)
    non_whitespace_ratio = len(''.join(content.split())) / len(content) if content else 0
    if non_whitespace_ratio < 0.3:
        return False, f"Too much whitespace (ratio: {non_whitespace_ratio:.2f})"
    
    return True, ""

def _extract_redirect_target(html_content: str) -> Optional[str]:
    """Extract redirect target URL from HTML (meta refresh or canonical)."""
    from bs4 import BeautifulSoup
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Check for canonical link
    canonical = soup.find('link', rel='canonical')
    if canonical and canonical.get('href'):
        return canonical['href']
    
    # Check for meta refresh
    meta_refresh = soup.find('meta', attrs={'http-equiv': 'refresh'})
    if meta_refresh and meta_refresh.get('content'):
        content = meta_refresh['content']
        # Format: "0; url=https://..."
        if 'url=' in content:
            return content.split('url=')[1]
    
    # Check for JavaScript redirect
    scripts = soup.find_all('script')
    for script in scripts:
        if script.string and 'location.href' in script.string:
            # Extract URL from location.href="..."
            import re
            match = re.search(r'location\.href\s*=\s*["\']([^"\']+)["\']', script.string)
            if match:
                return match.group(1)
    
    return None

def download_file(url: str, output_path: Path, progress_bar=None, try_variants=True, is_html: bool = False) -> Optional[Dict]:
    """
    Download a file from URL and save to output_path. Returns metadata dict.
    
    Args:
        url: URL to download
        output_path: Path to save the file
        progress_bar: Optional progress bar
        try_variants: Whether to try URL variants
        is_html: Whether this is an HTML page that needs conversion
    """
    start_time = time.time()
    
    # Try URL variants if first attempt fails
    urls_to_try = [url]
    if try_variants and not url.endswith('.md') and not is_html:
        urls_to_try.extend([
            url + '.md',
            url.rstrip('/') + '/index.md' if url.endswith('/') else url + '/index.md'
        ])
    
    validation_passed = True  # Initialize validation flag
    
    for try_url in urls_to_try:
        try:
            # Follow redirects automatically
            if progress_bar:
                progress_bar.set_postfix({'status': 'fetching...'})
            response = requests.get(try_url, timeout=30, allow_redirects=True)
            response.raise_for_status()
            
            content_type = response.headers.get('Content-Type', '')
            content = response.text
            is_html_response = 'text/html' in content_type
            
            if progress_bar:
                progress_bar.set_postfix({'status': 'downloaded'})
            
            # Handle HTML pages (LangGraph documentation)
            if is_html_response or is_html:
                if not HAS_HTML_CLEANER:
                    if progress_bar:
                        progress_bar.set_postfix({'error': 'HTML cleaner not available'})
                    return None
                
                # Check if this is a redirect page (JavaScript/meta redirect)
                redirect_target = _extract_redirect_target(content)
                if redirect_target:
                    # Follow the redirect
                    try:
                        redirect_response = requests.get(redirect_target, timeout=30, allow_redirects=True)
                        redirect_response.raise_for_status()
                        content = redirect_response.text
                        try_url = redirect_target  # Update URL for metadata
                    except Exception as e:
                        if progress_bar:
                            progress_bar.set_postfix({'error': f'Redirect failed: {str(e)[:30]}'})
                        return None
                
                # Convert HTML to markdown
                try:
                    cleaner = LangGraphHTMLCleaner()
                    markdown_content = cleaner.html_to_markdown(content, url=try_url)
                    content = markdown_content
                    # Ensure output path has .md extension
                    if not output_path.suffix == '.md':
                        output_path = output_path.with_suffix('.md')
                except Exception as e:
                    if progress_bar:
                        progress_bar.set_postfix({'error': f'HTML conversion failed: {str(e)[:30]}'})
                    return None
            elif not url.endswith('.md') and 'text/markdown' not in content_type:
                # Skip non-markdown, non-HTML content
                continue
            
            # Validate content before saving (for LangChain markdown files)
            if not is_html_response and not is_html:
                # For markdown files, validate content
                if progress_bar:
                    progress_bar.set_postfix({'status': 'validating...'})
                is_valid, validation_error = validate_markdown_content(content, try_url)
                if not is_valid:
                    if progress_bar:
                        progress_bar.set_postfix({'error': f'Validation failed: {validation_error[:30]}'})
                    if try_url == urls_to_try[-1]:  # Last attempt
                        return None
                    continue
                if progress_bar:
                    progress_bar.set_postfix({'status': 'validated'})
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            # Write in binary mode to preserve original line endings from server
            if is_html_response or is_html:
                # HTML converted to markdown - write as UTF-8
                output_path.write_bytes(content.encode('utf-8'))
                file_size = len(content.encode('utf-8'))
            else:
                # Raw markdown - preserve original bytes
                output_path.write_bytes(response.content)
                file_size = len(response.content)
            
            download_time = time.time() - start_time
            
            # Get file metadata
            checksum = calculate_checksum(output_path)
            last_modified = response.headers.get('Last-Modified')
            etag = response.headers.get('ETag')
            
            # Phase 1: File-level content type and topic detection
            content_type = detect_file_content_type(output_path, try_url)
            topics = detect_file_topics(output_path, try_url)
            
            # Update progress bar with final status
            if progress_bar:
                speed = file_size / download_time if download_time > 0 else 0
                status_text = 'validated ✓' if validation_passed else 'validation failed'
                progress_bar.set_postfix({
                    'size': f"{file_size/1024:.1f}KB",
                    'speed': f"{speed/1024:.1f}KB/s",
                    'status': status_text
                })
                progress_bar.update(1)  # Explicitly update progress
            
            return {
                'checksum': checksum,
                'last_modified': last_modified,
                'etag': etag,
                'size': file_size,
                'download_time': download_time,
                'downloaded_at': datetime.utcnow().isoformat() + 'Z',
                'actual_url': try_url,  # Store the URL that worked
                'converted_from_html': is_html_response or is_html,
                'validation_passed': validation_passed,
                # Phase 1 metadata
                'content_type': content_type,
                'topics': topics
            }
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                continue  # Try next variant
            raise
        except Exception as e:
            if try_url == urls_to_try[-1]:  # Last attempt
                if progress_bar:
                    progress_bar.set_postfix({'error': str(e)[:30]})
                return None
            continue
    
    # All attempts failed
    if progress_bar:
        progress_bar.set_postfix({'error': '404 Not Found'})
    return None

def get_file_path(url: str, base_dir: Path, is_html: bool = False) -> Path:
    """
    Convert URL to local file path preserving directory structure.
    
    Args:
        url: URL to convert
        base_dir: Base directory for output
        is_html: Whether this is an HTML URL (will be converted to .md)
    """
    parsed = urlparse(url)
    # Remove leading / and ensure .md extension
    path = parsed.path.lstrip('/')
    
    # Remove trailing slash
    if path.endswith('/'):
        path = path.rstrip('/') + '/index'
    
    # Ensure .md extension
    if not path.endswith('.md'):
        path = path + '.md'
    
    return base_dir / path

def download_from_index(index_url: str, output_dir: Path, source_name: str, base_url: str = None) -> Dict:
    """Download all markdown files from an index URL. Returns metadata dict."""
    print(f"\nFetching index from {index_url}...")
    try:
        response = requests.get(index_url, timeout=30)
        response.raise_for_status()
        content = response.text
    except Exception as e:
        print(f"Error fetching index {index_url}: {e}")
        return {}
    
    # For LangGraph, include HTML pages
    include_html = 'langgraph' in source_name.lower()
    urls = extract_md_urls(content, base_url, include_html=include_html)
    print(f"Found {len(urls)} URLs ({'including HTML pages' if include_html else 'markdown only'})")
    
    metadata = {
        'source': source_name,
        'index_url': index_url,
        'base_url': base_url,
        'files': {}
    }
    
    downloaded = 0
    failed = 0
    total_size = 0
    html_converted = 0
    
    # Create progress bar
    sorted_urls = sorted(urls)
    
    # Test limit removed - downloading all files
    # test_limit = 20
    # if len(sorted_urls) > test_limit:
    #     sorted_urls = sorted_urls[:test_limit]
    #     print(f"\n[TEST MODE] Limiting to first {test_limit} URLs for testing")
    
    progress_bar = tqdm(
        sorted_urls,
        desc=f"Downloading {source_name}",
        unit="file",
        ncols=120,
        disable=not HAS_TQDM,
        bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}] {postfix}'
    )
    
    for url in progress_bar:
        # Determine if this is an HTML URL
        is_html = include_html and 'langchain-ai.github.io/langgraph' in url and not url.endswith('.md')
        file_path = get_file_path(url, output_dir, is_html=is_html)
        
        # Update progress bar description with current file
        if HAS_TQDM:
            file_name = file_path.name[:30] + "..." if len(file_path.name) > 30 else file_path.name
            progress_bar.set_description(f"{source_name}: {file_name}")
            progress_bar.set_postfix({'status': 'starting...'})
        
        file_metadata = download_file(url, file_path, progress_bar, is_html=is_html)
        if file_metadata:
            relative_path = str(file_path.relative_to(output_dir.parent))
            metadata['files'][relative_path] = {
                'url': url,
                'file_path': relative_path,
                **file_metadata
            }
            downloaded += 1
            total_size += file_metadata.get('size', 0)
            if file_metadata.get('converted_from_html'):
                html_converted += 1
        else:
            failed += 1
    
    if HAS_TQDM:
        progress_bar.close()
    
    # Print summary
    print(f"\nCompleted: {downloaded} downloaded, {failed} failed")
    if html_converted > 0:
        print(f"  HTML pages converted to markdown: {html_converted}")
    if total_size > 0:
        print(f"  Total size: {total_size / 1024 / 1024:.2f} MB")
    return metadata

def main():
    base_dir = Path(".")
    docs_dir = base_dir / "docs"
    metadata_dir = base_dir / "metadata"
    metadata_dir.mkdir(exist_ok=True)
    
    # Source configurations
    sources = {
        'langgraph': {
            'index_url': 'https://langchain-ai.github.io/langgraph/llms.txt',
            'base_url': 'https://langchain-ai.github.io/langgraph',
            'docs_dir': docs_dir / 'langgraph'
        },
        'langchain': {
            'index_url': 'https://docs.langchain.com/llms-full.txt',
            'base_url': 'https://docs.langchain.com',
            'docs_dir': docs_dir / 'langchain'
        }
    }
    
    print("=" * 60)
    print("Downloading Documentation")
    print("=" * 60)
    
    all_metadata = {}
    
    for source_name, config in sources.items():
        print(f"\n[{source_name.upper()}] Processing {config['index_url']}...")
        metadata = download_from_index(
            config['index_url'],
            config['docs_dir'],
            source_name,
            config['base_url']
        )
        all_metadata[source_name] = metadata
    
    # Save metadata to JSON file
    metadata_file = metadata_dir / 'download_metadata.json'
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(all_metadata, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 60)
    print("All downloads completed!")
    print(f"Metadata saved to: {metadata_file}")
    print("=" * 60)

if __name__ == "__main__":
    main()
