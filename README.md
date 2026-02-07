# Todo App - Evolution of Todo Hackathon

A progressive todo application built using **Spec-Driven Development (SDD)** with Claude Code and Spec-Kit Plus. This project evolves through 5 phases, each adding more complexity and features.

## Current Phase: Phase III - AI-Powered Chatbot

### Features

- **AI Chat Interface** - Manage tasks using natural language
- User authentication (login/register)
- Add tasks with title and optional description
- View all tasks with completion status
- Mark tasks as complete/incomplete
- Update task title and description
- Delete tasks with confirmation
- Persistent storage in PostgreSQL
- Conversation history saved to database
- Responsive web interface

## Technology Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 16+ (App Router), TypeScript, Tailwind CSS |
| Backend | Python FastAPI, SQLModel ORM |
| Database | PostgreSQL (Neon Serverless) |
| Auth | JWT tokens |
| AI | OpenAI Agents SDK, GPT-4o-mini |

## Project Structure

```
hackathon-todo/
├── frontend/           # Next.js frontend
│   ├── src/app/        # App Router pages (tasks, chat)
│   ├── src/components/ # React components
│   └── src/lib/        # Utilities
├── backend/            # FastAPI backend
│   ├── src/agents/     # AI agent and tools
│   ├── src/routers/    # API endpoints (tasks, chat)
│   └── tests/          # Pytest tests
├── src/                # Phase I console app
├── specs/              # SDD specifications
│   ├── 001-phase1-console-app/
│   ├── 002-phase2-fullstack-web/
│   └── 003-phase3-chatbot/
└── docker-compose.yml  # Local development
```

## Quick Start

### Prerequisites

- Python 3.13+
- Node.js 22+
- UV package manager
- PostgreSQL (or use Docker)
- OpenAI API key (for Phase III chat)

### Backend Setup

```bash
cd backend
cp .env.example .env
# Edit .env with your credentials:
# - DATABASE_URL (Neon PostgreSQL)
# - BETTER_AUTH_SECRET
# - OPENAI_API_KEY
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

### Task Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/{user_id}/tasks | List all tasks |
| POST | /api/{user_id}/tasks | Create a task |
| GET | /api/{user_id}/tasks/{id} | Get task details |
| PUT | /api/{user_id}/tasks/{id} | Update a task |
| DELETE | /api/{user_id}/tasks/{id} | Delete a task |
| PATCH | /api/{user_id}/tasks/{id}/complete | Toggle completion |

### Chat Endpoints (Phase III)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/chat | Send message, get AI response |
| GET | /api/conversations | List user's conversations |
| GET | /api/conversations/{id}/messages | Get conversation messages |

## Chat Commands

The AI assistant understands natural language. Try:

- "Add a task to buy groceries"
- "Show me my tasks"
- "What do I need to do?"
- "Mark task 1 as complete"
- "Delete task 2"
- "Rename task 3 to 'Call mom'"

## Testing

```bash
# Backend tests
cd backend
uv run pytest

# Frontend build check
cd frontend
npm run build
```

## Hackathon Phases

| Phase | Description | Status |
|-------|-------------|--------|
| I | In-Memory Console App | Completed |
| II | Full-Stack Web Application | Completed |
| III | AI-Powered Chatbot | In Progress |
| IV | Kubernetes Deployment | Pending |
| V | Cloud Deployment | Pending |

## Development Methodology

This project uses Spec-Driven Development (SDD):

1. `/sp.constitution` - Define project principles
2. `/sp.specify` - Create feature specification
3. `/sp.plan` - Generate implementation plan
4. `/sp.tasks` - Break down into tasks
5. `/sp.implement` - Generate code from specs
