# Data Model: Phase I - Console Todo App

**Date**: 2026-02-07
**Feature**: 001-phase1-console-app

## Entity Overview

Phase I has a single entity: **Task**. Tasks are stored in memory during the application session.

---

## Task Entity

### Definition

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `id` | int | Yes | Auto-generated | Unique sequential identifier starting from 1 |
| `title` | str | Yes | - | Task title (1-500 characters) |
| `description` | str | No | "" | Optional additional details |
| `completed` | bool | No | False | Completion status |
| `created_at` | datetime | Yes | Auto-generated | Timestamp when task was created |

### Validation Rules

| Field | Rule | Error Message |
|-------|------|---------------|
| `title` | Must not be empty | "Title is required" |
| `title` | Max 500 characters | "Title must be 500 characters or less" |
| `id` | Must be positive integer | "Invalid ID: please enter a number" |

### State Transitions

```
┌─────────┐     mark_complete()     ┌───────────┐
│ PENDING │ ──────────────────────► │ COMPLETED │
└─────────┘                         └───────────┘
     ▲                                    │
     │          mark_incomplete()         │
     └────────────────────────────────────┘
```

**States**:
- `PENDING`: Task is not yet done (completed=False)
- `COMPLETED`: Task is finished (completed=True)

**Transitions**:
- `mark_complete()`: PENDING → COMPLETED
- `mark_incomplete()`: COMPLETED → PENDING (toggle behavior per FR-004)

---

## Storage Design

### In-Memory Structure

```python
# Storage: dict[int, Task]
# Key: task.id
# Value: Task instance

tasks: dict[int, Task] = {}
next_id: int = 1  # Auto-increment counter
```

### Operations Complexity

| Operation | Time Complexity | Space Complexity |
|-----------|-----------------|------------------|
| Add task | O(1) | O(1) |
| Get task by ID | O(1) | O(1) |
| List all tasks | O(n) | O(n) |
| Update task | O(1) | O(1) |
| Delete task | O(1) | O(1) |
| Toggle complete | O(1) | O(1) |

---

## Service Interface

### TaskService

```
class TaskService:
    """Manages Task CRUD operations with in-memory storage."""
    
    Methods:
    - add_task(title: str, description: str = "") -> Task
    - get_task(task_id: int) -> Task
    - list_tasks() -> list[Task]
    - update_task(task_id: int, title: str = None, description: str = None) -> Task
    - delete_task(task_id: int) -> None
    - toggle_complete(task_id: int) -> Task
```

### Exception Types

| Exception | When Raised | User Message |
|-----------|-------------|--------------|
| `TaskNotFoundError` | Task ID doesn't exist | "Task not found: #{id}" |
| `ValidationError` | Invalid input data | Specific validation message |

---

## Example Data

### Sample Tasks

```python
Task(
    id=1,
    title="Buy groceries",
    description="Milk, eggs, bread",
    completed=False,
    created_at=datetime(2026, 2, 7, 10, 30, 0)
)

Task(
    id=2,
    title="Call mom",
    description="Wish her happy birthday",
    completed=True,
    created_at=datetime(2026, 2, 7, 10, 35, 0)
)

Task(
    id=3,
    title="Finish homework",
    description="",
    completed=False,
    created_at=datetime(2026, 2, 7, 11, 0, 0)
)
```

### Display Format

```
=== Todo List ===

#1 [ ] Buy groceries
      Milk, eggs, bread

#2 [x] Call mom
      Wish her happy birthday

#3 [ ] Finish homework

Total: 3 tasks (1 completed, 2 pending)
```

**Legend**:
- `[ ]` = Pending task
- `[x]` = Completed task

---

## Relationships

Phase I has no entity relationships (single entity). Future phases will add:
- Phase II: User → Task (one-to-many)
- Phase III: Conversation → Message (one-to-many)
