# Quickstart: Phase I - Console Todo App

**Date**: 2026-02-07
**Feature**: 001-phase1-console-app

## Prerequisites

- Python 3.13 or higher
- UV package manager
- Git

## Setup

### 1. Clone and Navigate

```bash
git clone <repository-url>
cd hackathon-todo
git checkout 001-phase1-console-app
```

### 2. Create Virtual Environment with UV

```bash
# Install UV if not already installed
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv venv
uv pip install -e .
```

### 3. Verify Installation

```bash
# Activate virtual environment
# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

# Check Python version
python --version  # Should show Python 3.13+
```

## Running the Application

### Start the Todo App

```bash
python -m src.main
```

### Expected Output

```
╔══════════════════════════════════╗
║         TODO APP - Phase I       ║
║    Welcome! Your tasks await.    ║
╚══════════════════════════════════╝

╔══════════════════════════════════╗
║         TODO APP - Phase I       ║
╠══════════════════════════════════╣
║  1. Add Task                     ║
║  2. View All Tasks               ║
║  3. Mark Task Complete/Incomplete║
║  4. Update Task                  ║
║  5. Delete Task                  ║
║  6. Exit                         ║
╚══════════════════════════════════╝

Enter your choice (1-6): 
```

## Running Tests

### Run All Tests

```bash
pytest
```

### Run with Coverage

```bash
pytest --cov=src --cov-report=term-missing
```

### Run Specific Test Categories

```bash
# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# Specific test file
pytest tests/unit/test_task_service.py
```

### Expected Test Output

```
======================== test session starts ========================
collected X items

tests/unit/test_task.py ....                                   [ 40%]
tests/unit/test_task_service.py ........                       [ 80%]
tests/integration/test_cli_workflow.py ..                      [100%]

========================= X passed in 0.XXs =========================
```

## Development Workflow

### 1. Make Changes
Edit files in `src/` directory.

### 2. Run Tests
```bash
pytest
```

### 3. Run Application
```bash
python -m src.main
```

### 4. Commit Changes
```bash
git add .
git commit -m "feat: description of change"
```

## Project Structure

```
hackathon-todo/
├── src/
│   ├── __init__.py
│   ├── main.py              # Entry point
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py          # Task dataclass
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py  # CRUD operations
│   └── cli/
│       ├── __init__.py
│       ├── menu.py          # Menu handling
│       └── formatters.py    # Output formatting
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Fixtures
│   ├── unit/
│   └── integration/
├── specs/
│   └── 001-phase1-console-app/
├── pyproject.toml
└── README.md
```

## Troubleshooting

### Python Version Issues

```bash
# Check Python version
python --version

# If not 3.13+, install with UV
uv python install 3.13
uv python pin 3.13
```

### UV Not Found

```bash
# Reinstall UV
# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Add to PATH if needed
```

### Tests Failing

```bash
# Run with verbose output
pytest -v

# Run single failing test
pytest tests/unit/test_task.py::test_create_task -v
```

## Next Steps

After completing Phase I:
1. Run `/sp.tasks` to generate task breakdown
2. Run `/sp.implement` to generate code from specs
3. Verify all tests pass
4. Submit for Phase I evaluation

## Quick Reference

| Command | Description |
|---------|-------------|
| `python -m src.main` | Run the todo app |
| `pytest` | Run all tests |
| `pytest --cov=src` | Run tests with coverage |
| `uv pip install -e .` | Install in development mode |
