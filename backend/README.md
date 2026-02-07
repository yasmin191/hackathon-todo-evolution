# Todo Backend - Phase II

FastAPI backend for the Todo application with PostgreSQL persistence and JWT authentication.

## Technology Stack

- **Framework**: FastAPI
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: JWT (shared secret with Better Auth)
- **Package Manager**: UV

## Setup

1. Copy environment file:
   ```bash
   cp .env.example .env
   ```

2. Configure environment variables in `.env`:
   - `DATABASE_URL`: Neon PostgreSQL connection string
   - `BETTER_AUTH_SECRET`: Shared secret with frontend (min 32 chars)
   - `CORS_ORIGINS`: Allowed frontend origins

3. Install dependencies:
   ```bash
   uv sync --all-extras
   ```

4. Run the server:
   ```bash
   uv run uvicorn src.main:app --reload
   ```

## API Endpoints

All task endpoints require JWT authentication via `Authorization: Bearer <token>` header.

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
uv run pytest
```

## Project Structure

```
backend/
├── src/
│   ├── main.py           # FastAPI app
│   ├── config.py         # Settings
│   ├── database.py       # DB connection
│   ├── models/           # SQLModel entities
│   ├── routers/          # API endpoints
│   ├── services/         # Business logic
│   └── middleware/       # Auth middleware
└── tests/                # Pytest tests
```
