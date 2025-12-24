#!/usr/bin/env python3
"""Validate downloaded documentation files for Phase 1a and 1b."""
import requests
from pathlib import Path
import json
from collections import defaultdict
try:
    from .download_docs import extract_md_urls, get_file_path, validate_markdown_content
except (ImportError, ValueError):
    from download_docs import extract_md_urls, get_file_path, validate_markdown_content
import hashlib

def calculate_checksum(file_path: Path) -> str:
    """Calculate SHA256 checksum of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    return sha256.hexdigest()

def validate_file(file_path: Path, expected_url: str = None) -> dict:
    """Validate a single downloaded file."""
    result = {
        'file': str(file_path),
        'exists': False,
        'size': 0,
        'is_redirect': False,
        'is_empty': False,
        'validation_passed': False,
        'validation_error': None,
        'checksum': None,
        'issues': []
    }
    
    if not file_path.exists():
        result['issues'].append('File does not exist')
        return result
    
    result['exists'] = True
    result['size'] = file_path.stat().st_size
    result['checksum'] = calculate_checksum(file_path)
    
    # Check for redirect (298 bytes is typical GitHub login redirect)
    if result['size'] == 298:
        result['is_redirect'] = True
        result['issues'].append('Likely GitHub redirect (298 bytes)')
        # Check content
        content = file_path.read_bytes()[:200]
        if b'Sign in to GitHub' in content or b'github.com/login' in content:
            result['issues'].append('Contains GitHub login page')
    
    # Check if empty
    if result['size'] < 100:
        result['is_empty'] = True
        result['issues'].append(f'File too small ({result["size"]} bytes)')
    
    # Validate markdown content
    if result['size'] > 0:
        try:
            content = file_path.read_text('utf-8', errors='ignore')
            
            # For HTML-converted files (LangGraph), check if it starts with source comment
            # This is expected and valid
            is_html_converted = content.strip().startswith('<!-- Source:')
            
            if is_html_converted:
                # For HTML-converted files, check if there's actual content after the comment
                # Remove the comment and check if there's substantial content
                lines = content.split('\n')
                content_start = 0
                for i, line in enumerate(lines):
                    if line.strip() and not line.strip().startswith('<!--'):
                        content_start = i
                        break
                
                # Check if there's substantial content (at least 20 lines or 500 chars)
                # Error pages and short docs are valid, just shorter
                remaining_content = '\n'.join(lines[content_start:])
                if len(remaining_content) > 500 or len(lines[content_start:]) > 20:
                    result['validation_passed'] = True
                    result['is_html_converted'] = True
                else:
                    result['validation_passed'] = False
                    result['validation_error'] = 'HTML-converted file but insufficient content'
                    result['issues'].append('HTML-converted but too little content')
            else:
                # For regular markdown files, use standard validation
                is_valid, error = validate_markdown_content(content, expected_url or str(file_path))
                result['validation_passed'] = is_valid
                if not is_valid:
                    result['validation_error'] = error
                    result['issues'].append(f'Validation failed: {error}')
        except Exception as e:
            result['issues'].append(f'Error reading file: {str(e)}')
    
    return result

def validate_phase_1a():
    """Validate Phase 1a: LangChain downloads."""
    print("="*70)
    print("Validating Phase 1a: LangChain Downloads")
    print("="*70)
    
    # Get expected URLs from index
    print("\nFetching LangChain index...")
    index_url = 'https://docs.langchain.com/llms-full.txt'
    base_url = 'https://docs.langchain.com'
    
    try:
        response = requests.get(index_url, timeout=30)
        response.raise_for_status()
        expected_urls = extract_md_urls(response.text, base_url)
        print(f"Found {len(expected_urls)} URLs in index")
    except Exception as e:
        print(f"Error fetching index: {e}")
        return
    
    # Get downloaded files
    docs_dir = Path("docs/langchain")
    downloaded_files = list(docs_dir.rglob("*.md")) if docs_dir.exists() else []
    print(f"Found {len(downloaded_files)} downloaded files")
    
    # Create mapping of URLs to file paths
    url_to_file = {}
    for url in expected_urls:
        file_path = get_file_path(url, docs_dir)
        url_to_file[url] = file_path
    
    # Validate each expected file
    print("\nValidating files...")
    results = []
    issues_by_type = defaultdict(list)
    
    for url, file_path in url_to_file.items():
        result = validate_file(file_path, url)
        result['expected_url'] = url
        results.append(result)
        
        if result['issues']:
            for issue in result['issues']:
                issues_by_type[issue].append(str(file_path))
    
    # Summary
    total = len(results)
    exists = sum(1 for r in results if r['exists'])
    valid = sum(1 for r in results if r['exists'] and r['validation_passed'] and not r['is_redirect'])
    redirects = sum(1 for r in results if r['is_redirect'])
    empty = sum(1 for r in results if r['is_empty'])
    validation_failed = sum(1 for r in results if r['exists'] and not r['validation_passed'])
    
    print("\n" + "="*70)
    print("Phase 1a Validation Summary")
    print("="*70)
    print(f"Total URLs in index: {total}")
    print(f"Files downloaded: {exists} ({exists/total*100:.1f}%)")
    print(f"Valid files: {valid} ({valid/total*100:.1f}%)")
    print(f"Redirects (298 bytes): {redirects}")
    print(f"Empty files (<100 bytes): {empty}")
    print(f"Validation failed: {validation_failed}")
    print(f"Missing files: {total - exists}")
    
    if issues_by_type:
        print("\n" + "="*70)
        print("Issues Found")
        print("="*70)
        for issue_type, files in issues_by_type.items():
            print(f"\n{issue_type}: {len(files)} files")
            if len(files) <= 10:
                for f in files:
                    print(f"  - {f}")
            else:
                for f in files[:5]:
                    print(f"  - {f}")
                print(f"  ... and {len(files) - 5} more")
    
    return {
        'total': total,
        'downloaded': exists,
        'valid': valid,
        'redirects': redirects,
        'empty': empty,
        'validation_failed': validation_failed,
        'missing': total - exists
    }

def validate_phase_1b():
    """Validate Phase 1b: LangGraph downloads."""
    print("\n" + "="*70)
    print("Validating Phase 1b: LangGraph Downloads")
    print("="*70)
    
    # Get expected URLs from index
    print("\nFetching LangGraph index...")
    index_url = 'https://langchain-ai.github.io/langgraph/llms.txt'
    base_url = 'https://langchain-ai.github.io/langgraph'
    
    try:
        response = requests.get(index_url, timeout=30)
        response.raise_for_status()
        expected_urls = extract_md_urls(response.text, base_url, include_html=True)
        print(f"Found {len(expected_urls)} URLs in index")
    except Exception as e:
        print(f"Error fetching index: {e}")
        return
    
    # Get downloaded files
    docs_dir = Path("docs/langgraph")
    downloaded_files = list(docs_dir.rglob("*.md")) if docs_dir.exists() else []
    print(f"Found {len(downloaded_files)} downloaded files")
    
    # Create mapping of URLs to file paths
    url_to_file = {}
    for url in expected_urls:
        file_path = get_file_path(url, docs_dir)
        url_to_file[url] = file_path
    
    # Validate each expected file
    print("\nValidating files...")
    results = []
    issues_by_type = defaultdict(list)
    
    for url, file_path in url_to_file.items():
        result = validate_file(file_path, url)
        result['expected_url'] = url
        results.append(result)
        
        if result['issues']:
            for issue in result['issues']:
                issues_by_type[issue].append(str(file_path))
    
    # Summary
    total = len(results)
    exists = sum(1 for r in results if r['exists'])
    valid = sum(1 for r in results if r['exists'] and r['validation_passed'] and not r['is_redirect'])
    redirects = sum(1 for r in results if r['is_redirect'])
    empty = sum(1 for r in results if r['is_empty'])
    validation_failed = sum(1 for r in results if r['exists'] and not r['validation_passed'])
    
    print("\n" + "="*70)
    print("Phase 1b Validation Summary")
    print("="*70)
    print(f"Total URLs in index: {total}")
    print(f"Files downloaded: {exists} ({exists/total*100:.1f}%)")
    print(f"Valid files: {valid} ({valid/total*100:.1f}%)")
    print(f"Redirects (298 bytes): {redirects}")
    print(f"Empty files (<100 bytes): {empty}")
    print(f"Validation failed: {validation_failed}")
    print(f"Missing files: {total - exists}")
    
    if issues_by_type:
        print("\n" + "="*70)
        print("Issues Found")
        print("="*70)
        for issue_type, files in issues_by_type.items():
            print(f"\n{issue_type}: {len(files)} files")
            if len(files) <= 10:
                for f in files:
                    print(f"  - {f}")
            else:
                for f in files[:5]:
                    print(f"  - {f}")
                print(f"  ... and {len(files) - 5} more")
    
    return {
        'total': total,
        'downloaded': exists,
        'valid': valid,
        'redirects': redirects,
        'empty': empty,
        'validation_failed': validation_failed,
        'missing': total - exists
    }

def validate_urls():
    """Validate that URLs are accessible and match downloaded content."""
    print("\n" + "="*70)
    print("Validating URL Accessibility")
    print("="*70)
    
    # Check metadata file
    metadata_file = Path("metadata/download_metadata.json")
    if not metadata_file.exists():
        print("No metadata file found. Skipping URL validation.")
        return
    
    with open(metadata_file, 'r') as f:
        metadata = json.load(f)
    
    print(f"\nFound metadata for {len(metadata.get('sources', {}))} sources")
    
    total_urls = 0
    accessible = 0
    inaccessible = 0
    
    for source_name, source_data in metadata.get('sources', {}).items():
        files = source_data.get('files', {})
        print(f"\n{source_name}: {len(files)} files")
        
        # Sample check (first 10 URLs)
        sample_files = list(files.items())[:10]
        for file_path, file_meta in sample_files:
            url = file_meta.get('actual_url') or file_meta.get('url')
            if url:
                total_urls += 1
                try:
                    response = requests.head(url, timeout=10, allow_redirects=True)
                    if response.status_code == 200:
                        accessible += 1
                    else:
                        inaccessible += 1
                        print(f"  [FAIL] {url}: HTTP {response.status_code}")
                except Exception as e:
                    inaccessible += 1
                    print(f"  [FAIL] {url}: {str(e)[:50]}")
    
    print(f"\nURL Accessibility: {accessible}/{total_urls} accessible")

def main():
    """Run all validations."""
    print("="*70)
    print("Complete Download Validation")
    print("="*70)
    
    phase1a_results = validate_phase_1a()
    phase1b_results = validate_phase_1b()
    validate_urls()
    
    # Overall summary
    print("\n" + "="*70)
    print("Overall Summary")
    print("="*70)
    
    if phase1a_results:
        print(f"\nPhase 1a (LangChain):")
        print(f"  Downloaded: {phase1a_results['downloaded']}/{phase1a_results['total']}")
        print(f"  Valid: {phase1a_results['valid']}/{phase1a_results['total']} ({phase1a_results['valid']/phase1a_results['total']*100:.1f}%)")
        print(f"  Issues: {phase1a_results['redirects']} redirects, {phase1a_results['empty']} empty, {phase1a_results['validation_failed']} validation failed")
    
    if phase1b_results:
        print(f"\nPhase 1b (LangGraph):")
        print(f"  Downloaded: {phase1b_results['downloaded']}/{phase1b_results['total']}")
        print(f"  Valid: {phase1b_results['valid']}/{phase1b_results['total']} ({phase1b_results['valid']/phase1b_results['total']*100:.1f}%)")
        print(f"  Issues: {phase1b_results['redirects']} redirects, {phase1b_results['empty']} empty, {phase1b_results['validation_failed']} validation failed")
    
    if phase1a_results and phase1b_results:
        total_files = phase1a_results['total'] + phase1b_results['total']
        total_valid = phase1a_results['valid'] + phase1b_results['valid']
        print(f"\nTotal: {total_valid}/{total_files} valid files ({total_valid/total_files*100:.1f}%)")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    main()
