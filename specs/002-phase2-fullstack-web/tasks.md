# Tasks: Phase II - Full-Stack Web Application

**Feature Branch**: `002-phase2-fullstack-web`
**Created**: 2026-02-07
**Spec**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

---

## Phase Overview

Transform Phase I console app into a multi-user web application with:
- Next.js 16+ frontend with App Router
- FastAPI backend with SQLModel ORM
- Neon PostgreSQL database
- Better Auth for authentication

**Total Tasks**: 72 | **Estimated Complexity**: High

---

## Epic 1: Project Infrastructure Setup

### Task 1.1: Initialize Monorepo Structure
**Priority**: P0 | **Type**: Setup | **Depends on**: None

Create the monorepo directory structure with frontend and backend workspaces.

**Acceptance Criteria**:
- [ ] Create `frontend/` directory for Next.js app
- [ ] Create `backend/` directory for FastAPI app
- [ ] Create root `docker-compose.yml` placeholder
- [ ] Create root `.env.example` with all required variables
- [ ] Update root `.gitignore` for both workspaces

**Test Cases**:
```
TC-1.1.1: Directory structure matches plan.md specification
TC-1.1.2: .env.example contains DATABASE_URL, BETTER_AUTH_SECRET, CORS_ORIGINS
```

---

### Task 1.2: Initialize Backend Python Project
**Priority**: P0 | **Type**: Setup | **Depends on**: 1.1

Set up the FastAPI backend with UV package manager.

**Acceptance Criteria**:
- [ ] Create `backend/pyproject.toml` with FastAPI, SQLModel, uvicorn dependencies
- [ ] Create `backend/src/__init__.py`
- [ ] Create `backend/src/main.py` with minimal FastAPI app
- [ ] Create `backend/tests/conftest.py`
- [ ] Verify `uv sync` succeeds

**Test Cases**:
```
TC-1.2.1: `uv run uvicorn src.main:app` starts server on port 8000
TC-1.2.2: GET /health returns {"status": "ok"}
```

---

### Task 1.3: Initialize Frontend Next.js Project
**Priority**: P0 | **Type**: Setup | **Depends on**: 1.1

Set up the Next.js 16+ frontend with App Router and Tailwind CSS.

**Acceptance Criteria**:
- [ ] Initialize Next.js with `npx create-next-app@latest frontend --typescript --tailwind --app --src-dir`
- [ ] Configure `next.config.js` for API proxy (optional)
- [ ] Create `frontend/.env.local.example`
- [ ] Verify `npm run dev` starts on port 3000

**Test Cases**:
```
TC-1.3.1: `npm run dev` starts without errors
TC-1.3.2: Homepage renders at localhost:3000
```

---

### Task 1.4: Create Backend Configuration Module
**Priority**: P0 | **Type**: Implementation | **Depends on**: 1.2

Create centralized configuration with environment variable management.

**Acceptance Criteria**:
- [ ] Create `backend/src/config.py` with pydantic-settings
- [ ] Define DATABASE_URL, BETTER_AUTH_SECRET, CORS_ORIGINS settings
- [ ] Validate required environment variables at startup
- [ ] Create `backend/.env.example`

**Test Cases**:
```
TC-1.4.1: App fails to start if DATABASE_URL is missing
TC-1.4.2: Settings loaded correctly from environment
```

---

### Task 1.5: Set Up Database Connection
**Priority**: P0 | **Type**: Implementation | **Depends on**: 1.4

Configure SQLModel database connection to Neon PostgreSQL.

**Acceptance Criteria**:
- [ ] Create `backend/src/database.py` with engine and session management
- [ ] Implement `get_session()` dependency for FastAPI
- [ ] Add connection pooling configuration for serverless
- [ ] Test connection to Neon database

**Test Cases**:
```
TC-1.5.1: Database connection succeeds with valid DATABASE_URL
TC-1.5.2: Connection fails gracefully with invalid URL
TC-1.5.3: Session is properly closed after request
```

---

### Task 1.6: Create Docker Compose for Local Development
**Priority**: P1 | **Type**: Setup | **Depends on**: 1.2, 1.3

Create docker-compose.yml for local development environment.

**Acceptance Criteria**:
- [ ] Create `docker-compose.yml` with frontend and backend services
- [ ] Add local PostgreSQL service for development
- [ ] Configure volume mounts for hot reload
- [ ] Document usage in README

**Test Cases**:
```
TC-1.6.1: `docker-compose up` starts all services
TC-1.6.2: Frontend accessible at localhost:3000
TC-1.6.3: Backend accessible at localhost:8000
```

---

## Epic 2: Database Models and Migrations

### Task 2.1: Create Task SQLModel
**Priority**: P0 | **Type**: Implementation | **Depends on**: 1.5

Define the Task entity using SQLModel.

**Acceptance Criteria**:
- [ ] Create `backend/src/models/__init__.py`
- [ ] Create `backend/src/models/task.py` with Task model
- [ ] Include all fields: id, user_id, title, description, completed, created_at, updated_at
- [ ] Add field validations (title max 500 chars, required)
- [ ] Add user_id index

**Test Cases**:
```
TC-2.1.1: Task model validates title is required
TC-2.1.2: Task model validates title max length 500
TC-2.1.3: Task model defaults completed to False
TC-2.1.4: Task model auto-generates created_at
```

---

### Task 2.2: Create Request/Response Schemas
**Priority**: P0 | **Type**: Implementation | **Depends on**: 2.1

Create Pydantic models for API request and response payloads.

**Acceptance Criteria**:
- [ ] Create TaskCreate schema (title required, description optional)
- [ ] Create TaskUpdate schema (title optional, description optional)
- [ ] Create TaskResponse schema (all fields)
- [ ] Add validation messages

**Test Cases**:
```
TC-2.2.1: TaskCreate rejects empty title
TC-2.2.2: TaskCreate accepts title without description
TC-2.2.3: TaskUpdate allows partial updates
TC-2.2.4: TaskResponse includes all Task fields
```

---

### Task 2.3: Set Up Alembic Migrations
**Priority**: P0 | **Type**: Setup | **Depends on**: 2.1

Configure Alembic for database migrations.

**Acceptance Criteria**:
- [ ] Initialize Alembic in backend directory
- [ ] Configure alembic.ini for Neon PostgreSQL
- [ ] Create initial migration for tasks table
- [ ] Add updated_at trigger migration

**Test Cases**:
```
TC-2.3.1: `alembic upgrade head` creates tasks table
TC-2.3.2: `alembic downgrade -1` drops tasks table
TC-2.3.3: updated_at trigger updates on row modification
```

---

### Task 2.4: Create Database Test Fixtures
**Priority**: P1 | **Type**: Test | **Depends on**: 2.1, 2.3

Create pytest fixtures for database testing.

**Acceptance Criteria**:
- [ ] Create test database configuration
- [ ] Create fixture for test database session
- [ ] Create fixture for sample tasks
- [ ] Ensure test isolation (rollback after each test)

**Test Cases**:
```
TC-2.4.1: Test database is isolated from production
TC-2.4.2: Each test starts with clean database
TC-2.4.3: Sample tasks fixture creates valid data
```

---

## Epic 3: Authentication System

### Task 3.1: Set Up Better Auth in Frontend
**Priority**: P0 | **Type**: Implementation | **Depends on**: 1.3

Configure Better Auth for user authentication in Next.js.

**Acceptance Criteria**:
- [ ] Install Better Auth: `npm install better-auth`
- [ ] Create `frontend/src/lib/auth.ts` with Better Auth client
- [ ] Configure BETTER_AUTH_SECRET environment variable
- [ ] Set up auth API route handler

**Test Cases**:
```
TC-3.1.1: Better Auth initializes without errors
TC-3.1.2: Auth configuration loads from environment
```

---

### Task 3.2: Create Registration Page
**Priority**: P0 | **Type**: Implementation | **Depends on**: 3.1

Build the user registration page with form validation.

**Acceptance Criteria**:
- [ ] Create `frontend/src/app/register/page.tsx`
- [ ] Create AuthForm component for email/password input
- [ ] Implement client-side validation (email format, password length)
- [ ] Handle registration API call
- [ ] Redirect to tasks page on success
- [ ] Display error messages on failure

**Test Cases**:
```
TC-3.2.1: Registration form renders with email and password fields
TC-3.2.2: Submit with invalid email shows validation error
TC-3.2.3: Submit with short password shows validation error
TC-3.2.4: Successful registration redirects to /tasks
TC-3.2.5: Duplicate email shows appropriate error
```

---

### Task 3.3: Create Login Page
**Priority**: P0 | **Type**: Implementation | **Depends on**: 3.1

Build the user login page.

**Acceptance Criteria**:
- [ ] Create `frontend/src/app/login/page.tsx`
- [ ] Reuse AuthForm component with login mode
- [ ] Handle login API call
- [ ] Store JWT token in session
- [ ] Redirect to tasks page on success
- [ ] Display error for invalid credentials

**Test Cases**:
```
TC-3.3.1: Login form renders with email and password fields
TC-3.3.2: Invalid credentials show error message
TC-3.3.3: Successful login redirects to /tasks
TC-3.3.4: JWT token stored after login
```

---

### Task 3.4: Implement Logout Functionality
**Priority**: P1 | **Type**: Implementation | **Depends on**: 3.3

Add logout capability to clear session and redirect.

**Acceptance Criteria**:
- [ ] Create logout button component
- [ ] Clear JWT token on logout
- [ ] Redirect to login page
- [ ] Invalidate server-side session

**Test Cases**:
```
TC-3.4.1: Clicking logout clears session
TC-3.4.2: After logout, accessing /tasks redirects to /login
```

---

### Task 3.5: Create Auth Middleware for Frontend
**Priority**: P0 | **Type**: Implementation | **Depends on**: 3.3

Protect routes that require authentication.

**Acceptance Criteria**:
- [ ] Create middleware.ts for route protection
- [ ] Redirect unauthenticated users from /tasks to /login
- [ ] Redirect authenticated users from /login to /tasks
- [ ] Pass user info to protected pages

**Test Cases**:
```
TC-3.5.1: Unauthenticated user on /tasks redirected to /login
TC-3.5.2: Authenticated user on /login redirected to /tasks
TC-3.5.3: User info available in protected pages
```

---

### Task 3.6: Create JWT Verification Middleware for Backend
**Priority**: P0 | **Type**: Implementation | **Depends on**: 1.4

Implement JWT token verification in FastAPI.

**Acceptance Criteria**:
- [ ] Create `backend/src/middleware/__init__.py`
- [ ] Create `backend/src/middleware/auth.py`
- [ ] Implement JWT decode and verification using BETTER_AUTH_SECRET
- [ ] Create `get_current_user` dependency
- [ ] Return 401 for invalid/expired tokens
- [ ] Verify user_id in path matches token

**Test Cases**:
```
TC-3.6.1: Request without token returns 401
TC-3.6.2: Request with invalid token returns 401
TC-3.6.3: Request with expired token returns 401
TC-3.6.4: Request with valid token extracts user_id
TC-3.6.5: Request to /api/{user_a}/tasks with user_b token returns 404
```

---

### Task 3.7: Create Auth Integration Tests
**Priority**: P1 | **Type**: Test | **Depends on**: 3.2, 3.3, 3.6

End-to-end tests for authentication flow.

**Acceptance Criteria**:
- [ ] Test complete registration flow
- [ ] Test login with valid credentials
- [ ] Test login with invalid credentials
- [ ] Test protected route access
- [ ] Test logout flow

**Test Cases**:
```
TC-3.7.1: User can register and immediately access tasks
TC-3.7.2: User can logout and must login again
TC-3.7.3: User cannot access tasks without login
```

---

## Epic 4: Task API Endpoints

### Task 4.1: Create Task Service Layer
**Priority**: P0 | **Type**: Implementation | **Depends on**: 2.1

Implement business logic for task operations.

**Acceptance Criteria**:
- [ ] Create `backend/src/services/__init__.py`
- [ ] Create `backend/src/services/task_service.py`
- [ ] Implement create_task(user_id, data) -> Task
- [ ] Implement get_tasks(user_id) -> List[Task]
- [ ] Implement get_task(user_id, task_id) -> Task | None
- [ ] Implement update_task(user_id, task_id, data) -> Task | None
- [ ] Implement delete_task(user_id, task_id) -> bool
- [ ] Implement toggle_complete(user_id, task_id) -> Task | None

**Test Cases**:
```
TC-4.1.1: create_task returns Task with generated ID
TC-4.1.2: get_tasks returns only tasks for given user_id
TC-4.1.3: get_task returns None for non-existent ID
TC-4.1.4: get_task returns None for other user's task
TC-4.1.5: update_task updates only provided fields
TC-4.1.6: delete_task returns False for non-existent task
TC-4.1.7: toggle_complete flips completed status
```

---

### Task 4.2: Create Task Router
**Priority**: P0 | **Type**: Implementation | **Depends on**: 4.1, 3.6

Implement REST API endpoints for tasks.

**Acceptance Criteria**:
- [ ] Create `backend/src/routers/__init__.py`
- [ ] Create `backend/src/routers/tasks.py`
- [ ] Implement GET /api/{user_id}/tasks
- [ ] Implement POST /api/{user_id}/tasks
- [ ] Implement GET /api/{user_id}/tasks/{task_id}
- [ ] Implement PUT /api/{user_id}/tasks/{task_id}
- [ ] Implement DELETE /api/{user_id}/tasks/{task_id}
- [ ] Implement PATCH /api/{user_id}/tasks/{task_id}/complete
- [ ] Apply auth middleware to all endpoints

**Test Cases**:
```
TC-4.2.1: GET /api/{user_id}/tasks returns 200 with task list
TC-4.2.2: POST /api/{user_id}/tasks returns 201 with created task
TC-4.2.3: GET /api/{user_id}/tasks/{id} returns 200 with task
TC-4.2.4: GET /api/{user_id}/tasks/{id} returns 404 for non-existent
TC-4.2.5: PUT /api/{user_id}/tasks/{id} returns 200 with updated task
TC-4.2.6: DELETE /api/{user_id}/tasks/{id} returns 204
TC-4.2.7: PATCH /api/{user_id}/tasks/{id}/complete returns 200
```

---

### Task 4.3: Register Router in Main App
**Priority**: P0 | **Type**: Implementation | **Depends on**: 4.2

Wire up the task router to the FastAPI application.

**Acceptance Criteria**:
- [ ] Import tasks router in main.py
- [ ] Include router with prefix
- [ ] Configure CORS for frontend origin
- [ ] Add exception handlers for common errors

**Test Cases**:
```
TC-4.3.1: Task endpoints accessible at /api/{user_id}/tasks
TC-4.3.2: CORS headers present for frontend origin
TC-4.3.3: Validation errors return 400 with details
```

---

### Task 4.4: Create API Error Handlers
**Priority**: P1 | **Type**: Implementation | **Depends on**: 4.3

Implement consistent error response format.

**Acceptance Criteria**:
- [ ] Create custom exception classes
- [ ] Create exception handlers for ValidationError, NotFoundError
- [ ] Return consistent JSON error format: {error: string, detail?: any}
- [ ] Log errors appropriately

**Test Cases**:
```
TC-4.4.1: Validation error returns {error: "Validation failed", detail: [...]}
TC-4.4.2: Not found error returns {error: "Task not found"}
TC-4.4.3: Server error returns {error: "Internal server error"}
```

---

### Task 4.5: Create API Integration Tests
**Priority**: P0 | **Type**: Test | **Depends on**: 4.2, 2.4

Comprehensive tests for all API endpoints.

**Acceptance Criteria**:
- [ ] Create `backend/tests/test_tasks_api.py`
- [ ] Test all CRUD operations
- [ ] Test authentication requirements
- [ ] Test validation errors
- [ ] Test user isolation

**Test Cases**:
```
TC-4.5.1: Unauthorized requests return 401
TC-4.5.2: User A cannot access User B's tasks
TC-4.5.3: Empty title returns 400
TC-4.5.4: Task CRUD cycle works end-to-end
```

---

## Epic 5: Frontend Task UI Components

### Task 5.1: Create TypeScript Types
**Priority**: P0 | **Type**: Implementation | **Depends on**: 1.3

Define shared TypeScript types for the frontend.

**Acceptance Criteria**:
- [ ] Create `frontend/src/types/index.ts`
- [ ] Define Task interface matching API response
- [ ] Define TaskCreate, TaskUpdate types
- [ ] Define User type for auth context

**Test Cases**:
```
TC-5.1.1: Types compile without errors
TC-5.1.2: Types match API response structure
```

---

### Task 5.2: Create API Client Module
**Priority**: P0 | **Type**: Implementation | **Depends on**: 5.1, 3.5

Implement API client for backend communication.

**Acceptance Criteria**:
- [ ] Create `frontend/src/lib/api.ts`
- [ ] Implement getTasks(userId) function
- [ ] Implement createTask(userId, data) function
- [ ] Implement updateTask(userId, taskId, data) function
- [ ] Implement deleteTask(userId, taskId) function
- [ ] Implement toggleComplete(userId, taskId) function
- [ ] Include JWT token in Authorization header
- [ ] Handle API errors consistently

**Test Cases**:
```
TC-5.2.1: API calls include Authorization header
TC-5.2.2: 401 response triggers redirect to login
TC-5.2.3: Network errors are caught and reported
```

---

### Task 5.3: Create TaskItem Component
**Priority**: P0 | **Type**: Implementation | **Depends on**: 5.1

Build the individual task display component.

**Acceptance Criteria**:
- [ ] Create `frontend/src/components/TaskItem.tsx`
- [ ] Display task title with completion checkbox
- [ ] Show description if present (expandable)
- [ ] Include Edit and Delete buttons
- [ ] Style completed tasks differently
- [ ] Responsive design for mobile

**Test Cases**:
```
TC-5.3.1: TaskItem renders title and checkbox
TC-5.3.2: Completed task shows strikethrough
TC-5.3.3: Edit button triggers edit mode
TC-5.3.4: Delete button shows confirmation
```

---

### Task 5.4: Create TaskList Component
**Priority**: P0 | **Type**: Implementation | **Depends on**: 5.3

Build the task list container component.

**Acceptance Criteria**:
- [ ] Create `frontend/src/components/TaskList.tsx`
- [ ] Render list of TaskItem components
- [ ] Show empty state message when no tasks
- [ ] Handle loading state
- [ ] Handle error state

**Test Cases**:
```
TC-5.4.1: TaskList renders all tasks
TC-5.4.2: Empty list shows "No tasks yet" message
TC-5.4.3: Loading state shows spinner
TC-5.4.4: Error state shows retry option
```

---

### Task 5.5: Create TaskForm Component
**Priority**: P0 | **Type**: Implementation | **Depends on**: 5.1

Build the task creation/edit form component.

**Acceptance Criteria**:
- [ ] Create `frontend/src/components/TaskForm.tsx`
- [ ] Support create and edit modes
- [ ] Include title input (required)
- [ ] Include description textarea (optional)
- [ ] Client-side validation
- [ ] Submit and Cancel buttons
- [ ] Loading state during submission

**Test Cases**:
```
TC-5.5.1: Form shows validation error for empty title
TC-5.5.2: Form submits with valid data
TC-5.5.3: Edit mode pre-fills existing values
TC-5.5.4: Cancel clears form and closes
```

---

### Task 5.6: Create Tasks Page
**Priority**: P0 | **Type**: Implementation | **Depends on**: 5.2, 5.4, 5.5

Build the main tasks management page.

**Acceptance Criteria**:
- [ ] Create `frontend/src/app/tasks/page.tsx`
- [ ] Fetch and display user's tasks
- [ ] Include "Add Task" button
- [ ] Handle task creation
- [ ] Handle task updates
- [ ] Handle task deletion
- [ ] Handle completion toggle
- [ ] Show user email and logout button

**Test Cases**:
```
TC-5.6.1: Page loads and displays tasks
TC-5.6.2: Add Task opens form modal
TC-5.6.3: Completing task updates UI immediately
TC-5.6.4: Deleting task removes from list
TC-5.6.5: Edit task updates in list
```

---

### Task 5.7: Create Layout Component
**Priority**: P1 | **Type**: Implementation | **Depends on**: 3.4

Build the app layout with navigation.

**Acceptance Criteria**:
- [ ] Update `frontend/src/app/layout.tsx`
- [ ] Add header with app title
- [ ] Show user info when authenticated
- [ ] Include logout button
- [ ] Responsive navigation

**Test Cases**:
```
TC-5.7.1: Layout shows app title
TC-5.7.2: Authenticated user sees their email
TC-5.7.3: Logout button visible when authenticated
```

---

### Task 5.8: Style with Tailwind CSS
**Priority**: P1 | **Type**: Implementation | **Depends on**: 5.3, 5.4, 5.5, 5.6

Apply consistent styling across all components.

**Acceptance Criteria**:
- [ ] Define color scheme in tailwind.config.js
- [ ] Style form inputs consistently
- [ ] Style buttons (primary, secondary, danger)
- [ ] Responsive breakpoints for mobile/tablet/desktop
- [ ] Accessible focus states

**Test Cases**:
```
TC-5.8.1: App is usable on mobile (320px width)
TC-5.8.2: Form elements have visible focus states
TC-5.8.3: Colors have sufficient contrast
```

---

### Task 5.9: Create Frontend Unit Tests
**Priority**: P1 | **Type**: Test | **Depends on**: 5.3, 5.4, 5.5

Unit tests for React components.

**Acceptance Criteria**:
- [ ] Set up Jest and React Testing Library
- [ ] Test TaskItem renders correctly
- [ ] Test TaskList handles empty state
- [ ] Test TaskForm validation
- [ ] Test API client mocking

**Test Cases**:
```
TC-5.9.1: TaskItem snapshot matches
TC-5.9.2: TaskList shows empty message when no tasks
TC-5.9.3: TaskForm shows error for empty title
```

---

## Epic 6: Home and Landing Page

### Task 6.1: Create Home Page
**Priority**: P2 | **Type**: Implementation | **Depends on**: 3.5

Build the landing page for the application.

**Acceptance Criteria**:
- [ ] Update `frontend/src/app/page.tsx`
- [ ] Show app description
- [ ] Include Login and Register links/buttons
- [ ] Redirect authenticated users to /tasks

**Test Cases**:
```
TC-6.1.1: Home page renders for unauthenticated users
TC-6.1.2: Authenticated users redirected to /tasks
TC-6.1.3: Login and Register links work
```

---

## Epic 7: Error Handling and Edge Cases

### Task 7.1: Handle Token Expiration
**Priority**: P1 | **Type**: Implementation | **Depends on**: 5.2, 3.6

Gracefully handle expired JWT tokens.

**Acceptance Criteria**:
- [ ] Detect 401 responses in API client
- [ ] Clear local session on token expiry
- [ ] Redirect to login with message
- [ ] Show "Session expired" notification

**Test Cases**:
```
TC-7.1.1: Expired token triggers logout
TC-7.1.2: User sees session expired message
TC-7.1.3: User can login again after expiry
```

---

### Task 7.2: Handle Network Errors
**Priority**: P1 | **Type**: Implementation | **Depends on**: 5.2

Handle offline and network failure scenarios.

**Acceptance Criteria**:
- [ ] Catch network errors in API client
- [ ] Show user-friendly error message
- [ ] Provide retry option
- [ ] Don't lose unsaved form data

**Test Cases**:
```
TC-7.2.1: Network error shows friendly message
TC-7.2.2: Retry button attempts request again
TC-7.2.3: Form data preserved after error
```

---

### Task 7.3: Handle Concurrent Edits
**Priority**: P2 | **Type**: Implementation | **Depends on**: 4.1

Handle race conditions with updated_at checks.

**Acceptance Criteria**:
- [ ] Include updated_at in update requests
- [ ] Compare timestamps on server
- [ ] Return conflict error if stale
- [ ] Show user conflict notification

**Test Cases**:
```
TC-7.3.1: Stale update returns 409 Conflict
TC-7.3.2: User sees conflict message
TC-7.3.3: User can refresh and retry
```

---

## Epic 8: Documentation and Deployment

### Task 8.1: Create Backend README
**Priority**: P1 | **Type**: Documentation | **Depends on**: 4.3

Document backend setup and API.

**Acceptance Criteria**:
- [ ] Create `backend/README.md`
- [ ] Document environment variables
- [ ] Document local development setup
- [ ] Document API endpoints
- [ ] Include example requests

**Test Cases**:
```
TC-8.1.1: README contains all required environment variables
TC-8.1.2: Setup instructions work on clean machine
```

---

### Task 8.2: Create Frontend README
**Priority**: P1 | **Type**: Documentation | **Depends on**: 5.6

Document frontend setup.

**Acceptance Criteria**:
- [ ] Create `frontend/README.md`
- [ ] Document environment variables
- [ ] Document local development setup
- [ ] Document build and deployment

**Test Cases**:
```
TC-8.2.1: README contains all required environment variables
TC-8.2.2: Setup instructions work on clean machine
```

---

### Task 8.3: Create Quickstart Guide
**Priority**: P1 | **Type**: Documentation | **Depends on**: 8.1, 8.2

Create unified setup guide.

**Acceptance Criteria**:
- [ ] Create `specs/002-phase2-fullstack-web/quickstart.md`
- [ ] Document prerequisites
- [ ] Step-by-step local setup
- [ ] Common troubleshooting

**Test Cases**:
```
TC-8.3.1: New developer can set up in 15 minutes
```

---

### Task 8.4: Create Backend Dockerfile
**Priority**: P1 | **Type**: DevOps | **Depends on**: 4.3

Containerize the FastAPI backend.

**Acceptance Criteria**:
- [ ] Create `backend/Dockerfile`
- [ ] Multi-stage build for smaller image
- [ ] Run as non-root user
- [ ] Health check endpoint

**Test Cases**:
```
TC-8.4.1: Docker build succeeds
TC-8.4.2: Container starts and passes health check
TC-8.4.3: Container runs as non-root
```

---

### Task 8.5: Create Frontend Dockerfile
**Priority**: P1 | **Type**: DevOps | **Depends on**: 5.6

Containerize the Next.js frontend.

**Acceptance Criteria**:
- [ ] Create `frontend/Dockerfile`
- [ ] Multi-stage build for production
- [ ] Optimize for Vercel deployment
- [ ] Environment variable support

**Test Cases**:
```
TC-8.5.1: Docker build succeeds
TC-8.5.2: Container serves frontend correctly
```

---

### Task 8.6: Configure Vercel Deployment
**Priority**: P2 | **Type**: DevOps | **Depends on**: 5.6

Set up frontend deployment on Vercel.

**Acceptance Criteria**:
- [ ] Create `frontend/vercel.json` if needed
- [ ] Configure environment variables in Vercel
- [ ] Set up production build

**Test Cases**:
```
TC-8.6.1: Vercel deployment succeeds
TC-8.6.2: Production app works correctly
```

---

### Task 8.7: Configure Backend Deployment
**Priority**: P2 | **Type**: DevOps | **Depends on**: 8.4

Set up backend deployment (Railway, Render, or similar).

**Acceptance Criteria**:
- [ ] Document deployment platform choice
- [ ] Configure environment variables
- [ ] Set up health monitoring

**Test Cases**:
```
TC-8.7.1: Backend deployment succeeds
TC-8.7.2: API accessible from frontend
```

---

## Epic 9: End-to-End Testing

### Task 9.1: Set Up E2E Testing Framework
**Priority**: P1 | **Type**: Test | **Depends on**: 5.6

Configure Playwright or Cypress for E2E tests.

**Acceptance Criteria**:
- [ ] Install and configure test framework
- [ ] Create test utilities and helpers
- [ ] Set up test database seeding

**Test Cases**:
```
TC-9.1.1: E2E test framework runs without errors
TC-9.1.2: Tests can interact with both frontend and backend
```

---

### Task 9.2: Create User Flow E2E Tests
**Priority**: P1 | **Type**: Test | **Depends on**: 9.1

Comprehensive end-to-end tests.

**Acceptance Criteria**:
- [ ] Test registration flow
- [ ] Test login/logout flow
- [ ] Test complete task CRUD cycle
- [ ] Test user isolation

**Test Cases**:
```
TC-9.2.1: New user can register, add task, complete it, delete it
TC-9.2.2: User A's tasks not visible to User B
TC-9.2.3: Logout prevents further access
```

---

## Task Dependency Graph

```
1.1 ──┬── 1.2 ── 1.4 ── 1.5 ── 2.1 ── 2.2 ── 4.1 ── 4.2 ── 4.3
      │                              │                      │
      └── 1.3 ── 3.1 ──┬── 3.2      2.3 ── 2.4             4.4
                       │    │                               │
                       ├── 3.3 ── 3.4 ── 3.5               4.5
                       │                  │
                       └── 3.6 ──────────┘
                             │
                             └── 3.7

5.1 ── 5.2 ── 5.3 ── 5.4 ──┬── 5.6 ── 5.7 ── 5.8 ── 5.9
                           │
                           5.5 ─┘

5.6 ── 6.1
5.2 ── 7.1
5.2 ── 7.2
4.1 ── 7.3

4.3 ── 8.1 ──┬── 8.3
5.6 ── 8.2 ──┘
4.3 ── 8.4 ── 8.7
5.6 ── 8.5 ── 8.6

5.6 ── 9.1 ── 9.2
```

---

## Implementation Order

### Wave 1: Infrastructure (Tasks 1.1-1.5)
Parallel work possible on frontend (1.3) and backend (1.2, 1.4, 1.5) after 1.1.

### Wave 2: Database (Tasks 2.1-2.4)
Sequential, depends on Wave 1 backend completion.

### Wave 3: Auth (Tasks 3.1-3.7)
Frontend auth (3.1-3.5) and backend auth (3.6) can be parallel after Wave 1.

### Wave 4: API (Tasks 4.1-4.5)
Sequential, depends on Wave 2 and 3.6.

### Wave 5: UI (Tasks 5.1-5.9)
Can start after 3.5, parallel with Wave 4.

### Wave 6: Polish (Tasks 6.1, 7.1-7.3)
After main features complete.

### Wave 7: Docs & Deploy (Tasks 8.1-8.7)
After core functionality complete.

### Wave 8: E2E (Tasks 9.1-9.2)
Final validation.

---

## Summary

| Epic | Tasks | Priority Mix |
|------|-------|--------------|
| 1. Infrastructure | 6 | P0: 5, P1: 1 |
| 2. Database | 4 | P0: 3, P1: 1 |
| 3. Auth | 7 | P0: 5, P1: 2 |
| 4. API | 5 | P0: 4, P1: 1 |
| 5. Frontend UI | 9 | P0: 6, P1: 3 |
| 6. Landing | 1 | P2: 1 |
| 7. Error Handling | 3 | P1: 2, P2: 1 |
| 8. Docs & Deploy | 7 | P1: 5, P2: 2 |
| 9. E2E Testing | 2 | P1: 2 |
| **Total** | **44** | P0: 23, P1: 16, P2: 5 |
