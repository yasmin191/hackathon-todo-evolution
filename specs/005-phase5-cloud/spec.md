# Phase V: Advanced Cloud Deployment Specification

## Overview

Phase V extends the Todo application with advanced features, Dapr distributed runtime integration, and production cloud deployment. This phase represents the culmination of the 5-phase evolution.

**Points**: 300  
**Due Date**: Jan 18, 2026

## Part A: Advanced Task Features

### A.1 Task Priorities

**Requirements**:
- Tasks have priority levels: `low`, `medium`, `high`, `urgent`
- Default priority is `medium`
- Priority affects task sorting and display
- Chat agent can set priority via natural language ("add high priority task...")

**Database Schema**:
```sql
ALTER TABLE tasks ADD COLUMN priority VARCHAR(10) DEFAULT 'medium';
```

**API Changes**:
- POST/PUT `/api/{user_id}/tasks` accepts `priority` field
- GET `/api/{user_id}/tasks` supports `?priority=high` filter
- GET `/api/{user_id}/tasks` supports `?sort=priority` ordering

### A.2 Task Tags

**Requirements**:
- Tasks can have multiple tags (labels)
- Tags are user-defined strings
- Support filtering by tag
- Chat agent understands "add task with tag work..."

**Database Schema**:
```sql
CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    name VARCHAR(50) NOT NULL,
    color VARCHAR(7) DEFAULT '#6366f1',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, name)
);

CREATE TABLE task_tags (
    task_id INTEGER REFERENCES tasks(id) ON DELETE CASCADE,
    tag_id INTEGER REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (task_id, tag_id)
);
```

**API Changes**:
- GET `/api/{user_id}/tags` - list user's tags
- POST `/api/{user_id}/tags` - create tag
- DELETE `/api/{user_id}/tags/{id}` - delete tag
- POST `/api/{user_id}/tasks/{id}/tags` - add tags to task
- GET `/api/{user_id}/tasks?tag=work` - filter by tag

### A.3 Search and Filter

**Requirements**:
- Full-text search across task titles and descriptions
- Filter by: status (complete/incomplete), priority, tags, date range
- Sort by: created_at, updated_at, priority, due_date
- Combine multiple filters

**API Changes**:
- GET `/api/{user_id}/tasks?search=groceries` - text search
- GET `/api/{user_id}/tasks?status=incomplete&priority=high` - combined filters
- GET `/api/{user_id}/tasks?sort=priority&order=desc` - sorting

### A.4 Due Dates and Reminders

**Requirements**:
- Tasks can have optional due dates
- Visual indicators for overdue and upcoming tasks
- Reminder notifications (via Dapr scheduled jobs)
- Chat agent understands "add task due tomorrow..."

**Database Schema**:
```sql
ALTER TABLE tasks ADD COLUMN due_date TIMESTAMP;
ALTER TABLE tasks ADD COLUMN reminder_at TIMESTAMP;
ALTER TABLE tasks ADD COLUMN reminded BOOLEAN DEFAULT FALSE;
```

**API Changes**:
- POST/PUT `/api/{user_id}/tasks` accepts `due_date`, `reminder_at`
- GET `/api/{user_id}/tasks?overdue=true` - filter overdue tasks
- GET `/api/{user_id}/tasks?due_before=2026-01-20` - filter by due date

### A.5 Recurring Tasks

**Requirements**:
- Tasks can recur: daily, weekly, monthly, custom
- When completed, create next occurrence automatically
- Store recurrence pattern (RRULE format or simplified)

**Database Schema**:
```sql
ALTER TABLE tasks ADD COLUMN recurrence_rule VARCHAR(255);
ALTER TABLE tasks ADD COLUMN parent_task_id INTEGER REFERENCES tasks(id);
```

**Recurrence Patterns**:
- `DAILY` - every day
- `WEEKLY:MON,WED,FRI` - specific days
- `MONTHLY:15` - specific day of month
- `CUSTOM:7` - every N days

## Part B: Dapr Integration (Minikube)

### B.1 Dapr Components

**Pub/Sub (Kafka)**:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: task-pubsub
spec:
  type: pubsub.kafka
  metadata:
    - name: brokers
      value: "kafka:9092"
    - name: consumerGroup
      value: "todo-app"
```

**State Store (PostgreSQL)**:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
spec:
  type: state.postgresql
  metadata:
    - name: connectionString
      secretKeyRef:
        name: todo-secrets
        key: DATABASE_URL
```

**Secrets Store (Kubernetes)**:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kubernetes-secrets
spec:
  type: secretstores.kubernetes
```

**Scheduled Jobs (Reminders)**:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: reminder-scheduler
spec:
  type: bindings.cron
  metadata:
    - name: schedule
      value: "*/5 * * * *"  # Every 5 minutes
```

### B.2 Event-Driven Architecture

**Topics**:
| Topic | Producer | Consumer | Purpose |
|-------|----------|----------|---------|
| `task-events` | Chat API | Audit Service, Analytics | All CRUD operations |
| `task-reminders` | Scheduler | Notification Service | Due date reminders |
| `task-completed` | Chat API | Recurring Task Service | Trigger next occurrence |

**Event Schema**:
```json
{
  "event_type": "task.created|updated|completed|deleted",
  "user_id": "string",
  "task_id": "integer",
  "timestamp": "ISO8601",
  "data": { ... }
}
```

### B.3 Service Invocation

Use Dapr service invocation for inter-service communication:
- Frontend → Backend via Dapr sidecar
- Backend → Notification Service via Dapr

## Part C: Cloud Deployment

### C.1 Target Platforms

Support deployment to (choose one):
- **Azure AKS** (Azure Kubernetes Service)
- **Google GKE** (Google Kubernetes Engine)
- **Oracle OKE** (Oracle Container Engine)

### C.2 Infrastructure Components

**Kafka/Redpanda**:
- Option 1: Strimzi Kafka Operator (self-hosted on K8s)
- Option 2: Redpanda Cloud (managed)
- Option 3: Confluent Cloud (managed)

**Database**:
- Continue using Neon PostgreSQL (serverless)
- Or Azure Database for PostgreSQL / Cloud SQL / OCI DB

**Container Registry**:
- GitHub Container Registry (ghcr.io)
- Or cloud provider registry (ACR/GCR/OCIR)

### C.3 CI/CD Pipeline (GitHub Actions)

**Workflows**:

1. **Build & Test** (on PR):
   ```yaml
   - Run backend tests
   - Run frontend build
   - Lint and type check
   ```

2. **Build & Push Images** (on main):
   ```yaml
   - Build Docker images
   - Push to container registry
   - Tag with commit SHA
   ```

3. **Deploy to Cloud** (on release):
   ```yaml
   - Update Helm values
   - Deploy to staging
   - Run smoke tests
   - Deploy to production
   ```

### C.4 Monitoring and Observability

**Logging**:
- Structured JSON logging
- Centralized log aggregation (cloud provider or ELK)

**Metrics**:
- Prometheus metrics endpoint `/metrics`
- Grafana dashboards for visualization

**Tracing**:
- OpenTelemetry integration
- Distributed tracing via Dapr

## Technology Stack

| Component | Technology |
|-----------|------------|
| Event Streaming | Kafka (Strimzi) or Redpanda |
| Distributed Runtime | Dapr 1.12+ |
| Cloud Kubernetes | Azure AKS / GKE / Oracle OKE |
| CI/CD | GitHub Actions |
| Container Registry | GitHub Container Registry |
| Monitoring | Prometheus + Grafana |
| Secrets | Kubernetes Secrets + Dapr |

## Deliverables

```
hackathon-todo/
├── backend/
│   └── src/
│       ├── models/
│       │   ├── tag.py           # Tag model
│       │   └── task.py          # Updated with priority, due_date, etc.
│       ├── services/
│       │   ├── task_service.py  # Updated with filtering, search
│       │   ├── tag_service.py   # Tag CRUD
│       │   └── event_service.py # Dapr pub/sub
│       └── routers/
│           └── tags.py          # Tag endpoints
├── dapr/
│   ├── components/
│   │   ├── pubsub.yaml
│   │   ├── statestore.yaml
│   │   ├── secrets.yaml
│   │   └── bindings.yaml
│   └── configuration.yaml
├── k8s/
│   ├── cloud/
│   │   ├── aks/                 # Azure-specific
│   │   ├── gke/                 # GCP-specific
│   │   └── oke/                 # Oracle-specific
│   └── dapr/
│       └── *.yaml               # Dapr-enabled manifests
├── .github/
│   └── workflows/
│       ├── ci.yml               # Build and test
│       ├── build-push.yml       # Build and push images
│       └── deploy.yml           # Deploy to cloud
└── specs/005-phase5-cloud/
    ├── spec.md
    ├── plan.md
    └── tasks.md
```

## Acceptance Criteria

### Part A: Advanced Features
- [ ] Tasks support priority levels (low, medium, high, urgent)
- [ ] Tasks support multiple tags with CRUD operations
- [ ] Full-text search works across title and description
- [ ] Filtering by status, priority, tags, and date range works
- [ ] Due dates can be set and overdue tasks are highlighted
- [ ] Recurring tasks auto-generate next occurrence on completion
- [ ] Chat agent understands priority, tags, and due dates

### Part B: Dapr Integration
- [ ] Dapr sidecar runs alongside backend
- [ ] Pub/sub events published on task operations
- [ ] State store configured for conversation state
- [ ] Scheduled jobs check for reminders
- [ ] Service invocation works between services

### Part C: Cloud Deployment
- [ ] Application deployed to cloud Kubernetes
- [ ] Kafka/Redpanda operational for event streaming
- [ ] CI/CD pipeline automates build and deploy
- [ ] Monitoring dashboards available
- [ ] Documentation covers cloud deployment process

## Non-Goals

- Push notifications to mobile devices
- Real-time WebSocket updates (future phase)
- Multi-tenant SaaS features
- Payment/subscription handling
