"""Helper utilities for mode-aware testing and sanity checks."""
import os
import sys
from contextlib import contextmanager
from unittest.mock import patch


@contextmanager
def set_mode(mode: str):
    """
    Context manager to temporarily set AGENT_MODE.
    
    Args:
        mode: "offline" or "online"
    """
    if mode not in ["offline", "online"]:
        raise ValueError(f"Mode must be 'offline' or 'online', got '{mode}'")
    
    # Store original values
    original_env = os.environ.get("AGENT_MODE")
    original_agent_mode = None
    original_web_search = None
    
    try:
        # Set environment variable
        os.environ["AGENT_MODE"] = mode
        
        # Patch config module
        import config
        original_agent_mode = config.AGENT_MODE
        original_web_search = config.WEB_SEARCH_ENABLED
        
        with patch("config.AGENT_MODE", mode):
            with patch("config.WEB_SEARCH_ENABLED", mode == "online"):
                with patch("config.VECTOR_STORE_MODE", "postgres" if mode == "online" else "chroma"):
                    yield mode
    finally:
        # Restore original values
        if original_env:
            os.environ["AGENT_MODE"] = original_env
        elif "AGENT_MODE" in os.environ:
            del os.environ["AGENT_MODE"]
        
        if original_agent_mode is not None:
            import config
            config.AGENT_MODE = original_agent_mode
            config.WEB_SEARCH_ENABLED = original_web_search


def get_current_mode() -> str:
    """Get current AGENT_MODE from config."""
    import config
    return getattr(config, "AGENT_MODE", "offline").lower()


def is_offline_mode() -> bool:
    """Check if currently in offline mode."""
    return get_current_mode() == "offline"


def is_online_mode() -> bool:
    """Check if currently in online mode."""
    return get_current_mode() == "online"

