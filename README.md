# Todo App - Evolution of Todo Hackathon

A progressive todo application built using **Spec-Driven Development (SDD)** with Claude Code and Spec-Kit Plus. This project evolves through 5 phases, each adding more complexity and features.

## Current Phase: Phase V - Advanced Cloud Deployment

### Features

**Core Features**
- User authentication (login/register)
- Add, update, delete tasks
- Mark tasks as complete/incomplete
- Persistent storage in PostgreSQL

**Phase III: AI Chat Interface**
- Manage tasks using natural language
- Conversation history saved to database

**Phase IV: Kubernetes Deployment**
- Docker multi-stage builds
- Kubernetes manifests and Helm charts
- Minikube deployment scripts

**Phase V: Advanced Features**
- Task priorities (low, medium, high, urgent)
- Tags for task organization
- Due dates and reminders
- Recurring tasks (daily, weekly, monthly)
- Search and filter capabilities
- Dapr integration (pub/sub, state, bindings)
- CI/CD with GitHub Actions
- Cloud deployment (Azure AKS)

## Technology Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 16+ (App Router), TypeScript, Tailwind CSS |
| Backend | Python FastAPI, SQLModel ORM |
| Database | PostgreSQL (Neon Serverless) |
| Auth | JWT tokens |
| AI | OpenAI Agents SDK, GPT-4o-mini |
| Containers | Docker, Kubernetes, Helm |
| Distributed | Dapr (pub/sub, state, bindings) |
| Event Streaming | Apache Kafka (Strimzi) |
| CI/CD | GitHub Actions |
| Cloud | Azure AKS / GKE / Oracle OKE |

## Project Structure

```
hackathon-todo/
├── frontend/           # Next.js frontend
│   ├── src/app/        # App Router pages (tasks, chat)
│   ├── src/components/ # React components
│   └── src/lib/        # Utilities
├── backend/            # FastAPI backend
│   ├── src/agents/     # AI agent and tools
│   ├── src/routers/    # API endpoints (tasks, chat, tags)
│   ├── src/services/   # Business logic
│   └── tests/          # Pytest tests
├── docker/             # Dockerfiles
├── helm/               # Helm charts
├── k8s/                # Kubernetes manifests
│   ├── base/           # Base manifests
│   ├── dapr/           # Dapr-enabled manifests
│   └── cloud/          # Cloud-specific configs
├── dapr/               # Dapr components
├── scripts/            # Deployment scripts
├── .github/workflows/  # CI/CD pipelines
├── src/                # Phase I console app
└── specs/              # SDD specifications
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
- "Add a high priority task to review the report"
- "Add task to call mom tomorrow"
- "Add a daily task to take vitamins"
- "Show me my tasks"
- "Find tasks about meeting"
- "Show my urgent tasks"
- "What's overdue?"
- "Mark task 1 as complete"
- "Tag task 5 as personal"

## Testing

```bash
# Backend tests
cd backend
uv run pytest

# Frontend build check
cd frontend
npm run build
```

## Deployment

### Local (Minikube)

```bash
# Basic Kubernetes deployment
./scripts/deploy-minikube.sh

# With Dapr integration
./scripts/deploy-dapr.sh
```

### Cloud (Azure AKS)

See [k8s/cloud/aks/README.md](k8s/cloud/aks/README.md) for detailed instructions.

## Hackathon Phases

| Phase | Description | Status |
|-------|-------------|--------|
| I | In-Memory Console App | Completed |
| II | Full-Stack Web Application | Completed |
| III | AI-Powered Chatbot | Completed |
| IV | Kubernetes Deployment | Completed |
| V | Cloud Deployment | Completed |

## Development Methodology

This project uses Spec-Driven Development (SDD):

1. `/sp.constitution` - Define project principles
2. `/sp.specify` - Create feature specification
3. `/sp.plan` - Generate implementation plan
4. `/sp.tasks` - Break down into tasks
5. `/sp.implement` - Generate code from specs
