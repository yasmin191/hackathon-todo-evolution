# Phase V: Advanced Cloud Deployment - Implementation Plan

## Overview

This plan covers the three-part Phase V implementation:
- **Part A**: Advanced task features (priorities, tags, search, due dates, recurring)
- **Part B**: Dapr distributed runtime on Minikube
- **Part C**: Cloud Kubernetes deployment with CI/CD

## Architecture Decisions

### ADR-1: Priority System
**Decision**: Use enum-based priority with string values
**Rationale**: Simple to implement, easy to extend, works well with SQLAlchemy and Pydantic
**Values**: `low`, `medium`, `high`, `urgent`

### ADR-2: Tag Implementation
**Decision**: Many-to-many relationship with separate tags table
**Rationale**: Allows tag reuse, enables tag management (rename, color), supports filtering
**Alternative Rejected**: JSON array in task table (harder to query, no referential integrity)

### ADR-3: Search Implementation
**Decision**: PostgreSQL full-text search with `to_tsvector` and `to_tsquery`
**Rationale**: No external dependencies, good enough for our scale, native to PostgreSQL
**Alternative Rejected**: Elasticsearch (overkill for this use case)

### ADR-4: Recurrence Pattern Format
**Decision**: Simplified custom format (not full RRULE)
**Rationale**: Easier to implement and understand, covers common use cases
**Format**: `DAILY`, `WEEKLY:MON,WED,FRI`, `MONTHLY:15`, `CUSTOM:7`

### ADR-5: Dapr Pub/Sub Backend
**Decision**: Kafka via Strimzi operator on Kubernetes
**Rationale**: Production-grade, widely adopted, Dapr has excellent Kafka support
**Alternative**: Redis Streams (simpler but less durable)

### ADR-6: Cloud Provider
**Decision**: Support Azure AKS as primary, with templates for GKE/OKE
**Rationale**: Azure has good free tier, GitHub integration, comprehensive tooling

## Part A: Advanced Features Implementation

### A.1 Database Schema Updates

**Migration: Add priority and due_date to tasks**
```python
# backend/src/models/task.py
class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class Task(SQLModel, table=True):
    # Existing fields...
    priority: Priority = Field(default=Priority.MEDIUM)
    due_date: datetime | None = None
    reminder_at: datetime | None = None
    reminded: bool = Field(default=False)
    recurrence_rule: str | None = None
    parent_task_id: int | None = Field(foreign_key="task.id")
```

**New Tag model**
```python
# backend/src/models/tag.py
class Tag(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    name: str = Field(max_length=50)
    color: str = Field(default="#6366f1", max_length=7)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TaskTag(SQLModel, table=True):
    task_id: int = Field(foreign_key="task.id", primary_key=True)
    tag_id: int = Field(foreign_key="tag.id", primary_key=True)
```

### A.2 Service Layer Updates

**Task Service Extensions**
```python
# backend/src/services/task_service.py
def get_tasks(
    db: Session,
    user_id: str,
    status: str | None = None,
    priority: Priority | None = None,
    tag: str | None = None,
    search: str | None = None,
    due_before: datetime | None = None,
    overdue: bool = False,
    sort: str = "created_at",
    order: str = "desc"
) -> list[Task]:
    # Build query with filters
    ...
```

**Tag Service**
```python
# backend/src/services/tag_service.py
def create_tag(db, user_id, name, color) -> Tag
def get_tags(db, user_id) -> list[Tag]
def delete_tag(db, user_id, tag_id) -> bool
def add_tags_to_task(db, task_id, tag_ids) -> Task
def remove_tag_from_task(db, task_id, tag_id) -> Task
```

**Recurring Task Service**
```python
# backend/src/services/recurring_service.py
def parse_recurrence_rule(rule: str) -> RecurrenceConfig
def calculate_next_occurrence(task: Task) -> datetime
def create_next_occurrence(db, completed_task: Task) -> Task | None
```

### A.3 API Endpoints

**Tag Router**
```python
# backend/src/routers/tags.py
@router.get("/{user_id}/tags")
@router.post("/{user_id}/tags")
@router.delete("/{user_id}/tags/{tag_id}")
@router.post("/{user_id}/tasks/{task_id}/tags")
@router.delete("/{user_id}/tasks/{task_id}/tags/{tag_id}")
```

**Updated Task Router**
- Add query parameters: `priority`, `tag`, `search`, `due_before`, `overdue`, `sort`, `order`
- Add fields to create/update: `priority`, `due_date`, `reminder_at`, `recurrence_rule`

### A.4 Chat Agent Updates

**New Tool Functions**
```python
# backend/src/agents/tools.py
def add_task(..., priority: str = "medium", due_date: str = None, tags: list[str] = None)
def search_tasks(user_id: str, query: str) -> list[Task]
def filter_tasks(user_id: str, priority: str = None, tag: str = None, overdue: bool = False)
```

**Updated System Prompt**
```
You can manage tasks with the following capabilities:
- Set priority: "add high priority task to review code"
- Add tags: "add task buy milk with tag groceries"
- Set due dates: "add task submit report due tomorrow"
- Search: "find tasks about meeting"
- Filter: "show overdue tasks" or "show high priority tasks"
```

### A.5 Frontend Updates

**Task Card Component**
- Priority badge (color-coded)
- Tag pills
- Due date indicator (overdue = red, today = orange, upcoming = gray)
- Recurring icon

**Filter Panel**
- Priority dropdown
- Tag multi-select
- Date range picker
- Search input

## Part B: Dapr Integration

### B.1 Dapr Installation on Minikube

```bash
# Install Dapr CLI
curl -fsSL https://raw.githubusercontent.com/dapr/cli/master/install/install.sh | bash

# Initialize Dapr on Minikube
dapr init -k

# Verify
dapr status -k
```

### B.2 Kafka Setup (Strimzi)

```bash
# Install Strimzi operator
kubectl create namespace kafka
kubectl apply -f https://strimzi.io/install/latest?namespace=kafka

# Deploy Kafka cluster
kubectl apply -f k8s/dapr/kafka-cluster.yaml
```

**Kafka Cluster Manifest**
```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: todo-kafka
  namespace: kafka
spec:
  kafka:
    version: 3.6.0
    replicas: 1
    listeners:
      - name: plain
        port: 9092
        type: internal
        tls: false
    storage:
      type: ephemeral
  zookeeper:
    replicas: 1
    storage:
      type: ephemeral
```

### B.3 Dapr Components

**Directory Structure**
```
dapr/
├── components/
│   ├── pubsub.yaml         # Kafka pub/sub
│   ├── statestore.yaml     # PostgreSQL state
│   ├── secrets.yaml        # Kubernetes secrets
│   └── cron-binding.yaml   # Reminder scheduler
└── configuration.yaml      # Dapr config
```

### B.4 Event Service

```python
# backend/src/services/event_service.py
import httpx
from dapr.clients import DaprClient

DAPR_HTTP_PORT = 3500
PUBSUB_NAME = "task-pubsub"

async def publish_event(topic: str, event_type: str, user_id: str, task_id: int, data: dict):
    event = {
        "event_type": event_type,
        "user_id": user_id,
        "task_id": task_id,
        "timestamp": datetime.utcnow().isoformat(),
        "data": data
    }
    async with httpx.AsyncClient() as client:
        await client.post(
            f"http://localhost:{DAPR_HTTP_PORT}/v1.0/publish/{PUBSUB_NAME}/{topic}",
            json=event
        )
```

### B.5 Backend Dapr Annotations

```yaml
# k8s/dapr/backend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-backend
spec:
  template:
    metadata:
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "todo-backend"
        dapr.io/app-port: "8000"
        dapr.io/enable-api-logging: "true"
```

### B.6 Reminder Service

```python
# backend/src/services/reminder_service.py
@router.post("/reminders/check")
async def check_reminders():
    """Called by Dapr cron binding every 5 minutes"""
    now = datetime.utcnow()
    tasks = get_tasks_needing_reminder(db, now)
    for task in tasks:
        await publish_event("task-reminders", "reminder.due", task.user_id, task.id, {
            "title": task.title,
            "due_date": task.due_date.isoformat()
        })
        mark_reminded(db, task.id)
```

## Part C: Cloud Deployment

### C.1 GitHub Actions Workflows

**CI Workflow** (`.github/workflows/ci.yml`)
```yaml
name: CI
on: [pull_request]
jobs:
  test-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
      - run: cd backend && uv sync && uv run pytest

  build-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: cd frontend && npm ci && npm run build
```

**Build & Push Workflow** (`.github/workflows/build-push.yml`)
```yaml
name: Build and Push
on:
  push:
    branches: [main]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v5
        with:
          context: ./backend
          file: ./docker/backend.Dockerfile
          push: true
          tags: ghcr.io/${{ github.repository }}/backend:${{ github.sha }}
```

**Deploy Workflow** (`.github/workflows/deploy.yml`)
```yaml
name: Deploy
on:
  release:
    types: [published]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: azure/setup-kubectl@v3
      - uses: azure/k8s-set-context@v3
        with:
          kubeconfig: ${{ secrets.KUBE_CONFIG }}
      - run: |
          helm upgrade --install todo-app ./helm/todo-app \
            --set backend.image.tag=${{ github.sha }} \
            --set frontend.image.tag=${{ github.sha }}
```

### C.2 Azure AKS Setup

```bash
# Create resource group
az group create --name todo-rg --location eastus

# Create AKS cluster
az aks create \
  --resource-group todo-rg \
  --name todo-aks \
  --node-count 2 \
  --enable-addons monitoring \
  --generate-ssh-keys

# Get credentials
az aks get-credentials --resource-group todo-rg --name todo-aks
```

### C.3 Helm Values for Cloud

```yaml
# helm/todo-app/values-cloud.yaml
namespace: todo-app-prod

backend:
  image:
    repository: ghcr.io/yasmin191/hackathon-todo-evolution/backend
    tag: latest
    pullPolicy: Always
  replicaCount: 3
  resources:
    requests:
      memory: "256Mi"
      cpu: "100m"
    limits:
      memory: "512Mi"
      cpu: "500m"

frontend:
  image:
    repository: ghcr.io/yasmin191/hackathon-todo-evolution/frontend
    tag: latest
  replicaCount: 2

ingress:
  enabled: true
  className: nginx
  host: todo.example.com
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  tls:
    - secretName: todo-tls
      hosts:
        - todo.example.com

dapr:
  enabled: true
```

### C.4 Monitoring Setup

**Prometheus ServiceMonitor**
```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: todo-backend
spec:
  selector:
    matchLabels:
      app: todo-backend
  endpoints:
    - port: http
      path: /metrics
```

## Implementation Order

1. **Part A.1**: Database schema updates (priority, due_date fields)
2. **Part A.2**: Tag model and service
3. **Part A.3**: Task service with filtering and search
4. **Part A.4**: API endpoints for tags and enhanced tasks
5. **Part A.5**: Chat agent updates for new features
6. **Part A.6**: Frontend filter panel and task card updates
7. **Part B.1**: Dapr components configuration
8. **Part B.2**: Kafka setup with Strimzi
9. **Part B.3**: Event service for pub/sub
10. **Part B.4**: Reminder service with cron binding
11. **Part C.1**: CI workflow
12. **Part C.2**: Build and push workflow
13. **Part C.3**: Cloud-specific Helm values
14. **Part C.4**: Deploy workflow
15. **Part C.5**: Documentation

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Kafka complexity on Minikube | Use ephemeral storage, single replica for dev |
| Dapr learning curve | Start with pub/sub only, add features incrementally |
| Cloud costs | Use free tiers, clean up resources after demo |
| CI/CD secrets exposure | Use GitHub encrypted secrets, never commit credentials |

## Testing Strategy

- Unit tests for new services (tag, recurring, event)
- Integration tests for Dapr pub/sub
- E2E tests for search and filter
- Manual testing on Minikube before cloud deployment
