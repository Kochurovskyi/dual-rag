# Mode Testing Summary

## Test Extension Complete

### Files Created

1. **`tests/conftest.py`** (Extended)
   - `offline_mode` fixture: Sets offline mode for tests
   - `online_mode` fixture: Sets online mode for tests
   - `mode` fixture: Parametrized fixture for both modes

2. **`pytest.ini`** (Extended)
   - Added markers: `offline`, `online`, `mode`

3. **`tests/test_mode_chains.py`** (New)
   - Mode-specific router chain tests
   - Tests offline forced RAG behavior
   - Tests online web_search capability

4. **`tests/test_mode_nodes.py`** (New)
   - Mode-specific node tests
   - Route question node (offline/online)
   - Should continue conditional (offline/online)
   - Web search node (offline/online)

5. **`tests/test_mode_integration.py`** (New)
   - Full workflow offline mode test
   - Full workflow online mode test
   - Web search fallback test

6. **`graph/test_mode_helper.py`** (New)
   - `set_mode()` context manager for sanity checks
   - `get_current_mode()` helper
   - `is_offline_mode()` / `is_online_mode()` helpers

7. **`tests/run_mode_tests.sh`** / **`tests/run_mode_tests.bat`** (New)
   - Scripts to run tests for specific modes

8. **`tests/TEST_EXTENSION_PLAN.md`** (New)
   - Detailed extension plan and documentation

## Test Structure

### Existing Tests (32 tests)
- `test_chains.py`: 11 tests (mostly mode-agnostic)
- `test_nodes.py`: 16 tests (1 explicit offline test)
- `test_integration.py`: 5 tests (all offline implicit)

### New Mode-Specific Tests (~15 tests)
- `test_mode_chains.py`: ~3 tests
- `test_mode_nodes.py`: ~7 tests
- `test_mode_integration.py`: ~5 tests

### Total: ~47 tests
- Offline mode: ~24 tests
- Online mode: ~23 tests
- Mode-agnostic: ~20 tests (run in both modes)

## Running Tests

### All Tests
```bash
pytest tests/ -v
```

### Offline Mode Only
```bash
pytest tests/ -m offline -v
# Or use script:
bash tests/run_mode_tests.sh offline
# Windows:
tests\run_mode_tests.bat offline
```

### Online Mode Only
```bash
pytest tests/ -m online -v
# Or use script:
bash tests/run_mode_tests.sh online
# Windows:
tests\run_mode_tests.bat online
```

### Mode-Agnostic Tests
```bash
pytest tests/ -m "not offline and not online" -v
```

## Sanity Check Extensions (Pending)

To extend sanity checks for mode testing, update each sanity check script:

```python
if __name__ == "__main__":
    import argparse
    from graph.test_mode_helper import set_mode
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["offline", "online"], 
                       default=None, help="Test mode")
    args = parser.parse_args()
    
    mode = args.mode or get_current_mode()
    
    with set_mode(mode):
        # Run sanity check
        print(f"Testing in {mode} mode...")
        # ... existing sanity check code ...
```

## Key Test Scenarios

### Offline Mode
- ✅ Router always returns "rag"
- ✅ `web_search` always False
- ✅ No web search fallback
- ✅ Web search node returns empty results
- ✅ Uses ChromaDB vector store

### Online Mode
- ✅ Router can return "rag" or "web_search"
- ✅ `web_search` can be True or False
- ✅ Web search fallback enabled
- ✅ Web search node performs actual search (mocked)
- ✅ Uses PostgreSQL vector store (future)

## Next Steps

1. **Extend Sanity Checks**: Add `--mode` parameter to all sanity check scripts
2. **Run Tests**: Execute test suite for both modes
3. **Verify Coverage**: Ensure all critical paths tested in both modes
4. **Document Results**: Create test results report for both modes

