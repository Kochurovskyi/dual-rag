@echo off
REM Run tests for specific modes (Windows)

set MODE=%1
if "%MODE%"=="" set MODE=all

echo Running tests for mode: %MODE%
echo ==================================

if "%MODE%"=="offline" (
    echo Running offline mode tests...
    py -m pytest tests/ -m "offline or (not offline and not online)" -v
) else if "%MODE%"=="online" (
    echo Running online mode tests...
    py -m pytest tests/ -m "online or (not offline and not online)" -v
) else if "%MODE%"=="all" (
    echo Running all tests (both modes)...
    py -m pytest tests/ -v
) else (
    echo Usage: %0 [offline^|online^|all]
    exit /b 1
)

