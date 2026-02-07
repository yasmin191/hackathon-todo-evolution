# Todo App - Phase I

In-Memory Python Console Todo Application built with Spec-Driven Development.

## Features

- Add tasks with title and optional description
- View all tasks with completion status
- Mark tasks as complete/incomplete
- Update task title and description
- Delete tasks with confirmation

## Requirements

- Python 3.13+
- UV package manager

## Installation

```bash
# Create virtual environment
uv venv

# Activate virtual environment
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

# Install dependencies
uv pip install -e ".[dev]"
```

## Usage

```bash
python -m src.main
```

## Testing

```bash
pytest
```

## Project Structure

```
src/
├── main.py              # Entry point
├── models/task.py       # Task dataclass
├── services/task_service.py  # CRUD operations
├── cli/menu.py          # Menu handling
├── cli/formatters.py    # Output formatting
└── exceptions.py        # Custom exceptions

tests/
├── unit/               # Unit tests
└── integration/        # Integration tests
```

## Hackathon Phase I Deliverables

This is Phase I of the 5-Phase Evolution of Todo hackathon project, implementing Basic Level features using Spec-Driven Development with Claude Code and Spec-Kit Plus.
