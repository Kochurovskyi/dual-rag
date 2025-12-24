"""Watchdog system for incremental documentation updates."""
import time
import click
import requests
from pathlib import Path
from typing import Dict, List
import json

from config import (
    SOURCES, WATCHDOG_INTERVAL, REGISTRY_FILE,
    DOWNLOAD_METADATA_FILE
)
try:
    from .download_docs import extract_md_urls, download_file, get_file_path, calculate_checksum
    from .file_registry import FileRegistry
except (ImportError, ValueError):
    from download_docs import extract_md_urls, download_file, get_file_path, calculate_checksum
    from file_registry import FileRegistry
from ingestion.indexer import DocumentationIndexer


class DocumentationWatchdog:
    """Monitors documentation sources for changes and updates incrementally."""
    
    def __init__(self):
        self.registry = FileRegistry()
        self.indexer = DocumentationIndexer()
    
    def check_index_changes(self, source: str) -> Dict[str, List[str]]:
        """Check llms.txt for new/removed URLs."""
        config = SOURCES[source]
        index_url = config['index_url']
        base_url = config['base_url']
        
        try:
            response = requests.get(index_url, timeout=30)
            response.raise_for_status()
            content = response.text
            
            current_urls = extract_md_urls(content, base_url)
            
            # Get existing URLs from registry
            existing_files = self.registry.get_all_files(source)
            existing_urls = {info['url'] for info in existing_files.values()}
            
            new_urls = current_urls - existing_urls
            removed_urls = existing_urls - current_urls
            
            return {
                'new': list(new_urls),
                'removed': list(removed_urls),
                'unchanged': list(current_urls & existing_urls)
            }
        except Exception as e:
            print(f"Error checking index for {source}: {e}")
            return {'new': [], 'removed': [], 'unchanged': []}
    
    def update_source(self, source: str, force: bool = False) -> Dict:
        """Update a single source incrementally."""
        config = SOURCES[source]
        docs_dir = config['docs_dir']
        base_url = config['base_url']
        
        print(f"\n{'='*60}")
        print(f"Checking {source.upper()} for updates...")
        print(f"{'='*60}")
        
        # Check index for URL changes
        url_changes = self.check_index_changes(source)
        
        new_files = []
        changed_files = []
        removed_files = []
        
        # Download new files
        if url_changes['new']:
            print(f"\nFound {len(url_changes['new'])} new URLs")
            for url in url_changes['new']:
                file_path = get_file_path(url, docs_dir)
                print(f"Downloading: {url}")
                metadata = download_file(url, file_path)
                if metadata:
                    relative_path = str(file_path.relative_to(docs_dir.parent))
                    checksum = calculate_checksum(file_path)
                    new_files.append((relative_path, file_path, url, checksum))
        
        # Check existing files for changes
        if docs_dir.exists():
            md_files = list(docs_dir.rglob('*.md'))
            file_status = self.registry.get_changed_files(source, md_files)
            
            for relative_path, status in file_status.items():
                file_path = docs_dir / relative_path
                if status == 'changed':
                    checksum = calculate_checksum(file_path)
                    # Get URL from registry or construct it
                    file_info = self.registry.get_file_info(source, relative_path)
                    url = file_info['url'] if file_info else f"{base_url}/{relative_path}"
                    changed_files.append((relative_path, file_path, url, checksum))
                elif status == 'new':
                    checksum = calculate_checksum(file_path)
                    url = f"{base_url}/{relative_path}"
                    new_files.append((relative_path, file_path, url, checksum))
        
        # Find deleted files
        if docs_dir.exists():
            md_files = list(docs_dir.rglob('*.md'))
            deleted_paths = self.registry.get_deleted_files(source, md_files)
            removed_files = deleted_paths
        
        # Update index
        chunks_added = 0
        chunks_removed = 0
        
        # Index new/changed files
        for relative_path, file_path, url, checksum in new_files + changed_files:
            try:
                print(f"Indexing: {relative_path}")
                
                # Delete old chunks if file changed
                if (relative_path, file_path, url, checksum) in changed_files:
                    collection = self.indexer.collections[source]
                    collection.delete(where={'file_path': relative_path})
                    chunks_removed += self.registry.get_file_info(source, relative_path).get('chunk_count', 0)
                
                # Index file
                chunk_count = self.indexer.index_file(file_path, source)
                chunks_added += chunk_count
                
                # Update registry
                self.registry.register_file(
                    source=source,
                    file_path=relative_path,
                    url=url,
                    checksum=checksum,
                    chunk_count=chunk_count
                )
            except Exception as e:
                print(f"Error indexing {relative_path}: {e}")
        
        # Remove deleted files from index
        for relative_path in removed_files:
            try:
                print(f"Removing: {relative_path}")
                collection = self.indexer.collections[source]
                file_info = self.registry.get_file_info(source, relative_path)
                if file_info:
                    chunks_removed += file_info.get('chunk_count', 0)
                collection.delete(where={'file_path': relative_path})
                self.registry.remove_file(source, relative_path)
            except Exception as e:
                print(f"Error removing {relative_path}: {e}")
        
        return {
            'source': source,
            'new_files': len(new_files),
            'changed_files': len(changed_files),
            'removed_files': len(removed_files),
            'chunks_added': chunks_added,
            'chunks_removed': chunks_removed
        }
    
    def check_all(self) -> Dict:
        """Check all sources for updates."""
        results = {}
        for source in SOURCES.keys():
            results[source] = self.update_source(source)
        return results
    
    def watch(self, interval: int = WATCHDOG_INTERVAL):
        """Continuously monitor sources for changes."""
        print(f"Starting watchdog (checking every {interval} seconds)")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Checking for updates...")
                self.check_all()
                print(f"Sleeping for {interval} seconds...")
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n\nWatchdog stopped.")


@click.command()
@click.option('--check', is_flag=True, help='Check for updates once')
@click.option('--watch', is_flag=True, help='Continuously monitor for changes')
@click.option('--interval', default=WATCHDOG_INTERVAL, help='Polling interval in seconds')
@click.option('--source', type=click.Choice(['langgraph', 'langchain', 'all']), 
              default='all', help='Source to check')
def main(check, watch, interval, source):
    """Watchdog for incremental documentation updates."""
    watchdog = DocumentationWatchdog()
    
    if watch:
        watchdog.watch(interval)
    elif check:
        if source == 'all':
            watchdog.check_all()
        else:
            watchdog.update_source(source)
    else:
        print("Use --check for one-time check or --watch for continuous monitoring")
        print("Use --help for more options")


if __name__ == "__main__":
    main()

