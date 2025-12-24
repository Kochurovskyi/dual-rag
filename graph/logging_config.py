"""Logging configuration for LangGraph workflow."""
import logging
import sys
from config import GRAPH_LOG_LEVEL


def setup_logging():
    """Configure logging for the graph workflow."""
    # Create logger for graph module
    logger = logging.getLogger("graph")
    logger.setLevel(getattr(logging, GRAPH_LOG_LEVEL.upper(), logging.INFO))
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(getattr(logging, GRAPH_LOG_LEVEL.upper(), logging.INFO))
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(handler)
    
    # Create sub-loggers for different components
    logging.getLogger("graph.route").setLevel(logger.level)
    logging.getLogger("graph.retrieve").setLevel(logger.level)
    logging.getLogger("graph.grade_documents").setLevel(logger.level)
    logging.getLogger("graph.generate").setLevel(logger.level)
    logging.getLogger("graph.hallucination").setLevel(logger.level)
    
    return logger


# Initialize logging on import
logger = setup_logging()


if __name__ == "__main__":
    """Test logging configuration when run directly"""
    import argparse
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from graph.test_mode_helper import set_mode, get_current_mode
    
    parser = argparse.ArgumentParser(description="Test Logging Configuration")
    parser.add_argument("--mode", choices=["offline", "online"], 
                       default=None, help="Test mode (default: current AGENT_MODE)")
    args = parser.parse_args()
    
    mode = args.mode or get_current_mode()
    
    with set_mode(mode):
        print(f"Testing logging configuration ({mode.upper()} MODE)...")
        print("="*50)
    
    # Test logger setup
    print(f"Logger name: {logger.name}")
    print(f"Logger level: {logging.getLevelName(logger.level)}")
    print(f"Handlers: {len(logger.handlers)}")
    
    # Test logging at different levels
    print("\nTesting log levels:")
    print("-" * 30)
    logger.debug("This is a DEBUG message")
    logger.info("This is an INFO message")
    logger.warning("This is a WARNING message")
    logger.error("This is an ERROR message")
    
    # Test sub-loggers
    print("\nTesting sub-loggers:")
    print("-" * 30)
    sub_loggers = [
        "graph.route",
        "graph.retrieve",
        "graph.grade_documents",
        "graph.generate",
        "graph.hallucination"
    ]
    
    for sub_logger_name in sub_loggers:
        sub_logger = logging.getLogger(sub_logger_name)
        print(f"  {sub_logger_name}: level={logging.getLevelName(sub_logger.level)}")
    
    print("\nTest completed successfully!")

