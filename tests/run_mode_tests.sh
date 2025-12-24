#!/bin/bash
# Run tests for specific modes

MODE=${1:-"all"}

echo "Running tests for mode: $MODE"
echo "=================================="

if [ "$MODE" = "offline" ]; then
    echo "Running offline mode tests..."
    pytest tests/ -m "offline or (not offline and not online)" -v
elif [ "$MODE" = "online" ]; then
    echo "Running online mode tests..."
    pytest tests/ -m "online or (not offline and not online)" -v
elif [ "$MODE" = "all" ]; then
    echo "Running all tests (both modes)..."
    pytest tests/ -v
else
    echo "Usage: $0 [offline|online|all]"
    exit 1
fi

