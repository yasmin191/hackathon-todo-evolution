# Implementation Plan: Phase II - Full-Stack Web Application

**Branch**: `002-phase2-fullstack-web` | **Date**: 2026-02-07 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/002-phase2-fullstack-web/spec.md`

## Summary

Transform the Phase I console app into a modern multi-user web application. The frontend uses Next.js 16+ with App Router, the backend uses Python FastAPI with SQLModel ORM, and data is persisted in Neon Serverless PostgreSQL. Authentication is handled by Better Auth with JWT tokens shared between frontend and backend.

## Technical Context

**Frontend**:
- Framework: Next.js 16+ (App Router)
- Language: TypeScript
- Styling: Tailwind CSS
- Auth: Better Auth (client-side)

**Backend**:
- Framework: FastAPI
- Language: Python 3.13+
- ORM: SQLModel
- Auth: JWT verification (shared secret with Better Auth)

**Database**: Neon Serverless PostgreSQL

**Package Managers**:
- Frontend: npm/pnpm
- Backend: UV

**Testing**:
- Frontend: Jest + React Testing Library
- Backend: pytest

**Project Type**: Monorepo (frontend/ + backend/)

## Constitution Check

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. Spec-Driven Development | PASS | Spec created with 6 user stories, 10 FRs |
| II. No Manual Code | PASS | All code generated via `/sp.implement` |
| III. Test-First Development | PASS | Tests defined in acceptance scenarios |
| IV. Progressive Phase Evolution | PASS | Builds on Phase I, adds web + auth |
| V. AI-Native Architecture | N/A | Not applicable until Phase III |
| VI. Cloud-Native Readiness | PASS | Docker-ready, Neon serverless DB |

**Gate Status**: PASSED

## Project Structure

### Documentation

```text
specs/002-phase2-fullstack-web/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Technical decisions
├── data-model.md        # Entity definitions
├── quickstart.md        # Setup guide
├── contracts/
│   └── rest-api.md      # API specifications
├── checklists/
│   └── requirements.md  # Spec validation
└── tasks.md             # Task breakdown
```

### Source Code (Monorepo)

```text
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── login/
│   │   ├── register/
│   │   └── tasks/
│   ├── components/
│   │   ├── TaskList.tsx
│   │   ├── TaskItem.tsx
│   │   ├── TaskForm.tsx
│   │   └── AuthForm.tsx
│   ├── lib/
│   │   ├── api.ts
│   │   └── auth.ts
│   └── types/
│       └── index.ts
├── package.json
├── next.config.js
├── tailwind.config.js
└── tsconfig.json

backend/
├── src/
│   ├── __init__.py
│   ├── main.py           # FastAPI app
│   ├── config.py         # Settings
│   ├── database.py       # DB connection
│   ├── models/
│   │   ├── __init__.py
│   │   ├── task.py       # Task SQLModel
│   │   └── user.py       # User model (Better Auth)
│   ├── routers/
│   │   ├── __init__.py
│   │   └── tasks.py      # Task endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py
│   └── middleware/
│       ├── __init__.py
│       └── auth.py       # JWT verification
├── tests/
│   ├── conftest.py
│   ├── test_tasks.py
│   └── test_auth.py
├── pyproject.toml
└── alembic/              # Migrations
    └── versions/

docker-compose.yml        # Local dev environment
.env.example              # Environment template
```

## Authentication Flow

```
┌─────────────┐     ┌─────────────────────┐     ┌─────────────┐
│   Next.js   │     │    Better Auth      │     │   FastAPI   │
│  Frontend   │────▶│   (JWT Provider)    │     │   Backend   │
└─────────────┘     └─────────────────────┘     └─────────────┘
       │                      │                        │
       │  1. Login Request    │                        │
       │─────────────────────▶│                        │
       │                      │                        │
       │  2. JWT Token        │                        │
       │◀─────────────────────│                        │
       │                      │                        │
       │  3. API Request + JWT Header                  │
       │──────────────────────────────────────────────▶│
       │                      │                        │
       │                      │  4. Verify JWT         │
       │                      │  (shared secret)       │
       │                      │                        │
       │  5. Response                                  │
       │◀──────────────────────────────────────────────│
```

**Shared Secret**: `BETTER_AUTH_SECRET` environment variable used by both services.

## API Design

### Base URL
- Development: `http://localhost:8000`
- Production: `https://api.example.com`

### Authentication
All `/api/{user_id}/tasks` endpoints require:
```
Authorization: Bearer <jwt_token>
```

### Endpoints

| Method | Path | Request | Response |
|--------|------|---------|----------|
| GET | /api/{user_id}/tasks | - | Task[] |
| POST | /api/{user_id}/tasks | {title, description?} | Task |
| GET | /api/{user_id}/tasks/{id} | - | Task |
| PUT | /api/{user_id}/tasks/{id} | {title?, description?} | Task |
| DELETE | /api/{user_id}/tasks/{id} | - | 204 |
| PATCH | /api/{user_id}/tasks/{id}/complete | - | Task |

### Error Responses

| Status | Meaning |
|--------|---------|
| 400 | Validation error |
| 401 | Unauthorized (no/invalid token) |
| 404 | Task not found |
| 500 | Server error |

## Database Schema

### Tasks Table

```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
```

### Users Table (Better Auth managed)

Better Auth creates and manages the users table with sessions.

## Environment Variables

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-secret-key
```

### Backend (.env)
```
DATABASE_URL=postgresql://...@neon.tech/todo
BETTER_AUTH_SECRET=your-secret-key
CORS_ORIGINS=http://localhost:3000
```

## Complexity Tracking

| Aspect | Decision | Rationale |
|--------|----------|-----------|
| Monorepo | frontend/ + backend/ | Simpler for hackathon, single repo |
| Auth | Better Auth + JWT | Specified in requirements |
| ORM | SQLModel | Combines SQLAlchemy + Pydantic |
| Styling | Tailwind CSS | Rapid UI development |
