# Research: Phase II - Full-Stack Web Application

**Date**: 2026-02-07
**Feature**: 002-phase2-fullstack-web

## Research Summary

Phase II transforms the console app into a full-stack web application with authentication and persistent storage.

---

## Decision 1: Monorepo Structure

**Decision**: Use monorepo with `frontend/` and `backend/` directories.

**Rationale**:
- Single repository for hackathon simplicity
- Claude Code can navigate and edit both in single context
- Shared configuration (.env, docker-compose)
- Easier to manage for spec-driven development

**Alternatives Rejected**:
| Alternative | Why Rejected |
|-------------|--------------|
| Separate repos | More complex, harder for Claude Code context |
| Turborepo/Nx | Overkill for two projects |

---

## Decision 2: Frontend Framework

**Decision**: Next.js 16+ with App Router

**Rationale**:
- Required by hackathon specifications
- App Router is the modern React pattern
- Built-in API routes (though we use separate backend)
- Server components for performance
- Easy Vercel deployment

---

## Decision 3: Backend Framework

**Decision**: FastAPI with SQLModel

**Rationale**:
- Required by hackathon specifications
- Async by default, high performance
- Automatic OpenAPI documentation
- SQLModel combines SQLAlchemy + Pydantic
- Excellent typing support

---

## Decision 4: Authentication

**Decision**: Better Auth with JWT tokens

**Rationale**:
- Required by hackathon specifications
- Better Auth handles user registration, login, sessions
- JWT tokens can be verified by FastAPI
- Shared secret (BETTER_AUTH_SECRET) between services
- No need to build custom auth

**JWT Verification Flow**:
1. User logs in via Better Auth (frontend)
2. Better Auth issues JWT token
3. Frontend includes token in API requests
4. FastAPI middleware verifies token using shared secret
5. Backend extracts user_id from token

---

## Decision 5: Database

**Decision**: Neon Serverless PostgreSQL

**Rationale**:
- Required by hackathon specifications
- Serverless, scales to zero
- PostgreSQL compatibility
- Free tier available
- Connection pooling included

**Schema Decisions**:
- `tasks` table with `user_id` foreign key
- Index on `user_id` for efficient filtering
- `updated_at` timestamp for conflict detection

---

## Decision 6: API Design

**Decision**: RESTful API with user_id in path

**Rationale**:
- Clear resource hierarchy: `/api/{user_id}/tasks`
- JWT validation ensures user can only access own tasks
- Standard HTTP methods (GET, POST, PUT, DELETE, PATCH)
- Consistent with hackathon API specification

**Security**:
- JWT middleware validates token on every request
- Middleware extracts user_id and compares with path
- Return 404 (not 403) to prevent user enumeration

---

## Decision 7: Frontend State Management

**Decision**: React Query for server state, React Context for auth

**Rationale**:
- React Query handles caching, refetching, optimistic updates
- Auth context provides user state throughout app
- No need for Redux/Zustand for this scope

---

## Decision 8: Styling

**Decision**: Tailwind CSS

**Rationale**:
- Rapid development with utility classes
- Responsive by default
- Works well with Next.js
- No CSS-in-JS runtime overhead

---

## Decision 9: Testing Strategy

**Decision**: pytest for backend, Jest for frontend

**Rationale**:
- pytest: Standard Python testing, works with FastAPI TestClient
- Jest: Standard React testing with React Testing Library
- Both support mocking for isolated unit tests

---

## Decision 10: Development Environment

**Decision**: Docker Compose for local development

**Rationale**:
- Consistent environment across machines
- Easy to run frontend + backend + database
- Matches production-like setup

**Services**:
- `frontend`: Next.js on port 3000
- `backend`: FastAPI on port 8000
- Database: Neon (external, no local container needed)

---

## Open Questions Resolved

| Question | Resolution |
|----------|------------|
| How to share auth between frontend/backend? | JWT with BETTER_AUTH_SECRET |
| Where to store user data? | Better Auth manages users table |
| How to handle CORS? | FastAPI CORS middleware |
| How to deploy? | Vercel (frontend), separate (backend) |
