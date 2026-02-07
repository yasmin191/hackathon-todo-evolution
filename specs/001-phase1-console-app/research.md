# Research: Phase I - Console Todo App

**Date**: 2026-02-07
**Feature**: 001-phase1-console-app

## Research Summary

Phase I has minimal technical unknowns due to its simplicity. All decisions are straightforward applications of Python best practices for CLI applications.

---

## Decision 1: Python Project Structure

**Context**: How to organize a Python CLI application for maintainability and testability.

**Decision**: Use a layered architecture with models/, services/, and cli/ packages.

**Rationale**:
- Clean separation of concerns enables unit testing of each layer
- Models layer contains data structures (Task dataclass)
- Services layer contains business logic (CRUD operations)
- CLI layer handles user interaction (menu, input, output)
- This structure scales naturally to Phase II (web app)

**Alternatives Considered**:
| Alternative | Why Rejected |
|-------------|--------------|
| Single file | Not scalable, harder to test individual components |
| Flat structure | Less organized, harder to navigate as project grows |
| Domain-driven | Over-engineered for Phase I scope |

---

## Decision 2: Task ID Generation

**Context**: How to assign unique IDs to tasks (FR-002).

**Decision**: Use auto-incrementing integer starting from 1, stored as class variable in TaskService.

**Rationale**:
- Simple implementation using class-level counter
- Sequential IDs are user-friendly for CLI interaction
- No external dependencies required
- Counter resets when app restarts (acceptable for in-memory storage)

**Alternatives Considered**:
| Alternative | Why Rejected |
|-------------|--------------|
| UUID | Less user-friendly for CLI input (users must type long strings) |
| Timestamp-based | More complex, no benefit for single-user in-memory app |
| Database sequence | Requires external dependency, overkill for Phase I |

---

## Decision 3: In-Memory Storage Implementation

**Context**: How to store tasks in memory (FR-008).

**Decision**: Use Python dict with task ID as key, Task dataclass as value.

**Rationale**:
- O(1) lookup by ID for get, update, delete operations
- Simple iteration for list all operation
- Native Python, no dependencies
- Preserves insertion order (Python 3.7+)

**Alternatives Considered**:
| Alternative | Why Rejected |
|-------------|--------------|
| List | O(n) lookup by ID, less efficient for updates/deletes |
| SQLite in-memory | External dependency, overkill for Phase I |
| Redis | External service, not appropriate for console app |

---

## Decision 4: CLI Menu Implementation

**Context**: How to implement the command-line menu (FR-009).

**Decision**: Simple while loop with numbered menu options and input() for user interaction.

**Rationale**:
- No external dependencies (Click, Typer, argparse not needed)
- Straightforward implementation matching spec requirements
- Easy to test with mocked input/output
- Menu-based interaction matches SC-003 (3 or fewer steps)

**Alternatives Considered**:
| Alternative | Why Rejected |
|-------------|--------------|
| Typer/Click | External dependency, more complex than needed |
| argparse | Command-line args not suitable for interactive menu |
| curses/rich | Over-engineered for basic text menu |

---

## Decision 5: Testing Framework

**Context**: How to implement test-first development (Constitution Principle III).

**Decision**: Use pytest with fixtures for TaskService setup.

**Rationale**:
- Industry standard for Python testing
- Fixtures enable clean test setup/teardown
- Parametrized tests for edge cases
- Easy mocking of stdin/stdout for CLI tests

**Alternatives Considered**:
| Alternative | Why Rejected |
|-------------|--------------|
| unittest | More verbose, less Pythonic |
| nose2 | Less popular, fewer features |
| No framework | Cannot verify acceptance criteria automatically |

---

## Decision 6: Error Handling Strategy

**Context**: How to handle errors and provide clear messages (FR-007).

**Decision**: Custom exception classes with user-friendly messages, caught at CLI layer.

**Rationale**:
- Service layer raises specific exceptions (TaskNotFoundError, ValidationError)
- CLI layer catches and displays user-friendly messages
- Separates error logic from presentation
- Enables consistent error format across all operations

**Exceptions Defined**:
- `TaskNotFoundError`: Raised when task ID doesn't exist
- `ValidationError`: Raised for invalid input (empty title, invalid ID format)

---

## Decision 7: Data Model Implementation

**Context**: How to implement the Task entity.

**Decision**: Use Python dataclass with default values and factory for created_at.

**Rationale**:
- Dataclass provides automatic __init__, __repr__, __eq__
- Type hints for better code clarity
- Default values match spec (completed=False)
- field(default_factory=datetime.now) for created_at timestamp

**Task Fields**:
```python
@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
```

---

## Open Questions Resolved

| Question | Resolution |
|----------|------------|
| Package manager? | UV as specified in constitution |
| Python version? | 3.13+ as specified in constitution |
| External CLI library? | None - standard library only |
| Persistence? | None - in-memory only for Phase I |
| Multi-user? | No - single user as per spec assumptions |

---

## Phase 1 Readiness

All technical decisions are finalized. Ready to proceed to:
- `data-model.md`: Task entity definition
- `contracts/cli-interface.md`: CLI command specification
- `quickstart.md`: Developer setup guide
