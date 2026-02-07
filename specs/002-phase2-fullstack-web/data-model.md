# Data Model: Phase II - Full-Stack Web Application

**Date**: 2026-02-07
**Feature**: 002-phase2-fullstack-web

## Entity Overview

Phase II has two main entities: **User** (managed by Better Auth) and **Task** (application-managed).

---

## User Entity (Better Auth Managed)

Better Auth creates and manages the users table automatically.

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique identifier (UUID) |
| `email` | string | Yes | User email (unique) |
| `name` | string | No | Display name |
| `emailVerified` | boolean | No | Email verification status |
| `image` | string | No | Profile image URL |
| `createdAt` | datetime | Yes | Registration timestamp |
| `updatedAt` | datetime | Yes | Last update timestamp |

### Notes
- Better Auth handles password hashing internally
- Sessions table managed by Better Auth
- No direct manipulation of users table by our code

---

## Task Entity

### Definition (SQLModel)

```python
class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, foreign_key="user.id")
    title: str = Field(max_length=500)
    description: str | None = Field(default=None)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `id` | int | Yes | Auto | Primary key |
| `user_id` | string | Yes | - | Owner's user ID |
| `title` | string | Yes | - | Task title (1-500 chars) |
| `description` | string | No | null | Optional details |
| `completed` | boolean | No | false | Completion status |
| `created_at` | datetime | Yes | Auto | Creation timestamp |
| `updated_at` | datetime | Yes | Auto | Last update timestamp |

### Validation Rules

| Field | Rule | Error Message |
|-------|------|---------------|
| `title` | Must not be empty | "Title is required" |
| `title` | Max 500 characters | "Title must be 500 characters or less" |
| `user_id` | Must match authenticated user | 404 response |

### Indexes

```sql
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_user_completed ON tasks(user_id, completed);
```

---

## Relationships

```
┌─────────────────┐         ┌─────────────────┐
│      User       │         │      Task       │
│─────────────────│         │─────────────────│
│ id (PK)         │◄───────┤│ user_id (FK)    │
│ email           │    1:N  │ id (PK)         │
│ name            │         │ title           │
│ ...             │         │ description     │
└─────────────────┘         │ completed       │
                            │ created_at      │
                            │ updated_at      │
                            └─────────────────┘
```

- One User has Many Tasks (1:N)
- Tasks are soft-isolated by user_id
- Deleting user should cascade delete tasks

---

## API Request/Response Models

### TaskCreate (Request)

```python
class TaskCreate(SQLModel):
    title: str = Field(min_length=1, max_length=500)
    description: str | None = None
```

### TaskUpdate (Request)

```python
class TaskUpdate(SQLModel):
    title: str | None = Field(default=None, min_length=1, max_length=500)
    description: str | None = None
```

### TaskResponse (Response)

```python
class TaskResponse(SQLModel):
    id: int
    user_id: str
    title: str
    description: str | None
    completed: bool
    created_at: datetime
    updated_at: datetime
```

---

## Database Schema (SQL)

```sql
-- Users table (managed by Better Auth)
-- See Better Auth documentation for exact schema

-- Tasks table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_user_completed ON tasks(user_id, completed);

-- Updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_tasks_updated_at
    BEFORE UPDATE ON tasks
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

---

## Example Data

### Sample Tasks

```json
[
  {
    "id": 1,
    "user_id": "usr_abc123",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2026-02-07T10:00:00Z",
    "updated_at": "2026-02-07T10:00:00Z"
  },
  {
    "id": 2,
    "user_id": "usr_abc123",
    "title": "Call mom",
    "description": null,
    "completed": true,
    "created_at": "2026-02-07T10:05:00Z",
    "updated_at": "2026-02-07T11:30:00Z"
  }
]
```

---

## Migration Strategy

Since Phase I used in-memory storage, there's no migration needed. Phase II starts fresh with PostgreSQL.

For future phases:
- Use Alembic for schema migrations
- Version control all migration scripts
- Test migrations on staging before production
