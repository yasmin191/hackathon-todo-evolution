# Todo App - Evolution of Todo Hackathon

A progressive todo application built using **Spec-Driven Development (SDD)** with Claude Code and Spec-Kit Plus. This project evolves through 5 phases, each adding more complexity and features.

## Current Phase: Phase II - Full-Stack Web Application

### Features

- User authentication (login/register)
- Add tasks with title and optional description
- View all tasks with completion status
- Mark tasks as complete/incomplete
- Update task title and description
- Delete tasks with confirmation
- Persistent storage in PostgreSQL
- Responsive web interface

## Technology Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 16+ (App Router), TypeScript, Tailwind CSS |
| Backend | Python FastAPI, SQLModel ORM |
| Database | PostgreSQL (Neon Serverless) |
| Auth | JWT tokens |

## Project Structure

```
hackathon-todo/
├── frontend/           # Next.js frontend
│   ├── src/app/        # App Router pages
│   ├── src/components/ # React components
│   └── src/lib/        # Utilities
├── backend/            # FastAPI backend
│   ├── src/            # Application code
│   └── tests/          # Pytest tests
├── src/                # Phase I console app
├── specs/              # SDD specifications
│   ├── 001-phase1-console-app/
│   └── 002-phase2-fullstack-web/
└── docker-compose.yml  # Local development
```

## Quick Start

### Prerequisites

- Python 3.13+
- Node.js 22+
- UV package manager
- PostgreSQL (or use Docker)

### Backend Setup

```bash
cd backend
cp .env.example .env
# Edit .env with your database credentials
uv sync --all-extras
uv run uvicorn src.main:app --reload
```

### Frontend Setup

```bash
cd frontend
cp .env.local.example .env.local
npm install
npm run dev
```

### Using Docker

```bash
docker-compose up
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | Health check |
| GET | /api/{user_id}/tasks | List all tasks |
| POST | /api/{user_id}/tasks | Create a task |
| GET | /api/{user_id}/tasks/{id} | Get task details |
| PUT | /api/{user_id}/tasks/{id} | Update a task |
| DELETE | /api/{user_id}/tasks/{id} | Delete a task |
| PATCH | /api/{user_id}/tasks/{id}/complete | Toggle completion |

## Testing

```bash
# Backend tests
cd backend
uv run pytest

# Frontend build check
cd frontend
npm run build
```

## Phase I: Console App (Completed)

The original console application is still available:

```bash
uv sync
python -m src.main
```

## Hackathon Phases

| Phase | Description | Status |
|-------|-------------|--------|
| I | In-Memory Console App | Completed |
| II | Full-Stack Web Application | In Progress |
| III | AI-Powered Chatbot | Pending |
| IV | Kubernetes Deployment | Pending |
| V | Cloud Deployment | Pending |

## Development Methodology

This project uses Spec-Driven Development (SDD):

1. `/sp.constitution` - Define project principles
2. `/sp.specify` - Create feature specification
3. `/sp.plan` - Generate implementation plan
4. `/sp.tasks` - Break down into tasks
5. `/sp.implement` - Generate code from specs
