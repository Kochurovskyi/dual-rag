"""File tracking utilities for change detection."""
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

from config import REGISTRY_FILE, SOURCES


class FileRegistry:
    """Manages file registry for tracking documentation files."""
    
    def __init__(self):
        self.registry_file = REGISTRY_FILE
        self.registry_file.parent.mkdir(parents=True, exist_ok=True)
        self.registry = self._load_registry()
    
    def _load_registry(self) -> Dict:
        """Load registry from file."""
        if self.registry_file.exists():
            try:
                with open(self.registry_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading registry: {e}")
                return {}
        return {}
    
    def _save_registry(self):
        """Save registry to file."""
        with open(self.registry_file, 'w', encoding='utf-8') as f:
            json.dump(self.registry, f, indent=2, ensure_ascii=False)
    
    def calculate_checksum(self, file_path: Path) -> str:
        """Calculate SHA256 checksum of a file."""
        sha256 = hashlib.sha256()
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except Exception as e:
            print(f"Error calculating checksum for {file_path}: {e}")
            return ""
    
    def register_file(
        self,
        source: str,
        file_path: str,
        url: str,
        checksum: str,
        chunk_count: int = 0,
        last_modified: Optional[str] = None,
        etag: Optional[str] = None
    ):
        """Register a file in the registry."""
        if source not in self.registry:
            self.registry[source] = {}
        
        self.registry[source][file_path] = {
            'file_path': file_path,
            'url': url,
            'checksum': checksum,
            'last_modified': last_modified,
            'etag': etag,
            'last_indexed': datetime.utcnow().isoformat() + 'Z',
            'chunk_count': chunk_count
        }
        self._save_registry()
    
    def get_file_info(self, source: str, file_path: str) -> Optional[Dict]:
        """Get file information from registry."""
        return self.registry.get(source, {}).get(file_path)
    
    def get_all_files(self, source: str) -> Dict[str, Dict]:
        """Get all files for a source."""
        return self.registry.get(source, {})
    
    def file_changed(self, source: str, file_path: str, current_checksum: str) -> bool:
        """Check if file has changed based on checksum."""
        file_info = self.get_file_info(source, file_path)
        if not file_info:
            return True  # New file
        
        return file_info.get('checksum') != current_checksum
    
    def update_chunk_count(self, source: str, file_path: str, chunk_count: int):
        """Update chunk count for a file."""
        if source in self.registry and file_path in self.registry[source]:
            self.registry[source][file_path]['chunk_count'] = chunk_count
            self.registry[source][file_path]['last_indexed'] = datetime.utcnow().isoformat() + 'Z'
            self._save_registry()
    
    def remove_file(self, source: str, file_path: str):
        """Remove a file from registry."""
        if source in self.registry and file_path in self.registry[source]:
            del self.registry[source][file_path]
            self._save_registry()
    
    def get_changed_files(self, source: str, file_paths: List[Path]) -> Dict[str, str]:
        """Compare current files with registry and return changed/new files.
        
        Returns dict mapping file_path -> 'new' | 'changed' | 'unchanged'
        """
        result = {}
        source_registry = self.get_all_files(source)
        
        for file_path in file_paths:
            relative_path = str(file_path.relative_to(SOURCES[source]['docs_dir']))
            current_checksum = self.calculate_checksum(file_path)
            
            if not current_checksum:
                continue
            
            file_info = source_registry.get(relative_path)
            
            if not file_info:
                result[relative_path] = 'new'
            elif file_info.get('checksum') != current_checksum:
                result[relative_path] = 'changed'
            else:
                result[relative_path] = 'unchanged'
        
        return result
    
    def get_deleted_files(self, source: str, current_file_paths: List[Path]) -> List[str]:
        """Find files that exist in registry but not in current files."""
        source_registry = self.get_all_files(source)
        current_relative_paths = {
            str(fp.relative_to(SOURCES[source]['docs_dir']))
            for fp in current_file_paths
        }
        
        deleted = []
        for file_path in source_registry.keys():
            if file_path not in current_relative_paths:
                deleted.append(file_path)
        
        return deleted

