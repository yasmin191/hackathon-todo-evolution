# Dapr Integration Guide

This guide covers the Dapr (Distributed Application Runtime) integration for the Todo App.

## Overview

Dapr provides building blocks for distributed applications:
- **Pub/Sub** - Event-driven messaging via Kafka
- **State Management** - State persistence via PostgreSQL
- **Secrets** - Kubernetes secrets integration
- **Bindings** - Scheduled tasks via cron binding

## Prerequisites

- Minikube with at least 6GB memory and 4 CPUs
- Dapr CLI installed
- kubectl configured

### Install Dapr CLI

```bash
# macOS/Linux
curl -fsSL https://raw.githubusercontent.com/dapr/cli/master/install/install.sh | bash

# Windows (PowerShell)
powershell -Command "iwr -useb https://raw.githubusercontent.com/dapr/cli/master/install/install.ps1 | iex"

# Verify installation
dapr --version
```

## Quick Start

Deploy the complete stack with Dapr:

```bash
./scripts/deploy-dapr.sh
```

This script will:
1. Start Minikube with adequate resources
2. Initialize Dapr on Kubernetes
3. Install Strimzi Kafka operator
4. Deploy Kafka cluster with topics
5. Apply Dapr components
6. Deploy the application with Dapr sidecars

## Components

### Pub/Sub (Kafka)

**File**: `dapr/components/pubsub.yaml`

Enables event-driven architecture:

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: task-pubsub
spec:
  type: pubsub.kafka
  metadata:
    - name: brokers
      value: "todo-kafka-kafka-bootstrap.kafka.svc.cluster.local:9092"
```

**Topics**:
| Topic | Purpose |
|-------|---------|
| `task-events` | All CRUD operations |
| `task-reminders` | Due date reminders |
| `task-completed` | Completed task events |

### State Store (PostgreSQL)

**File**: `dapr/components/statestore.yaml`

Provides state management:

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
        name: todo-app-secrets
        key: DATABASE_URL
```

### Secrets Store (Kubernetes)

**File**: `dapr/components/secrets.yaml`

Integrates with Kubernetes secrets:

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kubernetes-secrets
spec:
  type: secretstores.kubernetes
```

### Cron Binding (Reminders)

**File**: `dapr/components/cron-binding.yaml`

Schedules reminder checks every 5 minutes:

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: reminder-scheduler
spec:
  type: bindings.cron
  metadata:
    - name: schedule
      value: "*/5 * * * *"
```

## Event Schema

Events use CloudEvents format:

```json
{
  "id": "task.created-123-1704067200",
  "source": "todo-backend",
  "type": "task.created",
  "specversion": "1.0",
  "datacontenttype": "application/json",
  "data": {
    "event_type": "task.created",
    "user_id": "user123",
    "task_id": 123,
    "timestamp": "2026-01-01T12:00:00Z",
    "title": "Buy groceries"
  }
}
```

## Publishing Events

The backend publishes events using the Dapr HTTP API:

```python
from src.services import event_service

# Publish task created event
await event_service.publish_task_created(
    user_id="user123",
    task_id=1,
    title="Buy groceries"
)

# Publish task completed event
await event_service.publish_task_completed(
    user_id="user123",
    task_id=1,
    title="Buy groceries"
)
```

## Debugging

### View Dapr Dashboard

```bash
dapr dashboard -k
```

Opens at http://localhost:8080

### Check Dapr Sidecar Status

```bash
kubectl get pods -n todo-app -o wide
```

Each pod should have 2/2 containers (app + daprd sidecar).

### View Dapr Logs

```bash
# Sidecar logs
kubectl logs deployment/todo-backend -c daprd -n todo-app

# Application logs
kubectl logs deployment/todo-backend -c backend -n todo-app
```

### Test Pub/Sub

```bash
# Port-forward to Dapr sidecar
kubectl port-forward deployment/todo-backend 3500:3500 -n todo-app

# Publish test event
curl -X POST http://localhost:3500/v1.0/publish/task-pubsub/task-events \
  -H "Content-Type: application/json" \
  -d '{"data": {"test": true}}'
```

### Check Kafka Topics

```bash
# List topics
kubectl exec -it todo-kafka-kafka-0 -n kafka -- bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 --list

# Describe topic
kubectl exec -it todo-kafka-kafka-0 -n kafka -- bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 --describe --topic task-events
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DAPR_ENABLED` | Enable Dapr integration | `false` |
| `DAPR_HTTP_PORT` | Dapr sidecar HTTP port | `3500` |

## Troubleshooting

### Sidecar Not Injected

Ensure Dapr annotations are present:

```yaml
annotations:
  dapr.io/enabled: "true"
  dapr.io/app-id: "todo-backend"
  dapr.io/app-port: "8000"
```

### Kafka Connection Failed

1. Check Kafka pods are running:
   ```bash
   kubectl get pods -n kafka
   ```

2. Verify Kafka service:
   ```bash
   kubectl get svc -n kafka
   ```

3. Check Strimzi operator logs:
   ```bash
   kubectl logs deployment/strimzi-cluster-operator -n kafka
   ```

### Events Not Publishing

1. Ensure `DAPR_ENABLED=true` in environment
2. Check sidecar is running with correct port
3. Verify pub/sub component is loaded:
   ```bash
   dapr components -k -n todo-app
   ```
