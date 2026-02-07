# Phase V: Advanced Cloud Deployment - Tasks

## Part A: Advanced Task Features

### Task A.1: Add Priority Field to Task Model
**Status**: pending  
**File**: `backend/src/models/task.py`

**Changes**:
- [ ] Create `Priority` enum with values: `low`, `medium`, `high`, `urgent`
- [ ] Add `priority` field with default `medium`
- [ ] Add `due_date` field (optional datetime)
- [ ] Add `reminder_at` field (optional datetime)
- [ ] Add `reminded` boolean field (default False)
- [ ] Add `recurrence_rule` field (optional string)
- [ ] Add `parent_task_id` field (optional self-reference)

**Test Cases**:
- [ ] Task created with default priority is `medium`
- [ ] Task can be created with explicit priority
- [ ] Due date accepts valid datetime

---

### Task A.2: Create Tag Model
**Status**: pending  
**File**: `backend/src/models/tag.py`

**Changes**:
- [ ] Create `Tag` SQLModel with fields: id, user_id, name, color, created_at
- [ ] Create `TaskTag` junction table with task_id, tag_id
- [ ] Add unique constraint on (user_id, name)
- [ ] Export from `backend/src/models/__init__.py`

**Test Cases**:
- [ ] Tag can be created with name and color
- [ ] Duplicate tag names for same user rejected
- [ ] Tags can be associated with tasks

---

### Task A.3: Create Tag Service
**Status**: pending  
**File**: `backend/src/services/tag_service.py`

**Changes**:
- [ ] `create_tag(db, user_id, name, color)` - create new tag
- [ ] `get_tags(db, user_id)` - list user's tags
- [ ] `get_tag_by_id(db, user_id, tag_id)` - get single tag
- [ ] `update_tag(db, user_id, tag_id, name, color)` - update tag
- [ ] `delete_tag(db, user_id, tag_id)` - delete tag
- [ ] `add_tags_to_task(db, task_id, tag_ids)` - associate tags
- [ ] `remove_tag_from_task(db, task_id, tag_id)` - remove association
- [ ] `get_task_tags(db, task_id)` - get tags for task

**Test Cases**:
- [ ] Create tag returns new tag with id
- [ ] Get tags returns only user's tags
- [ ] Delete tag removes tag and associations
- [ ] Add tags creates junction records

---

### Task A.4: Update Task Service with Filtering
**Status**: pending  
**File**: `backend/src/services/task_service.py`

**Changes**:
- [ ] Add filter parameters: `priority`, `tag`, `search`, `due_before`, `overdue`
- [ ] Add sort parameters: `sort`, `order`
- [ ] Implement PostgreSQL full-text search for `search` parameter
- [ ] Filter by priority enum value
- [ ] Filter by tag name (join with task_tags and tags)
- [ ] Filter overdue tasks (due_date < now and not completed)
- [ ] Sort by created_at, updated_at, priority, due_date

**Test Cases**:
- [ ] Filter by priority returns matching tasks
- [ ] Search finds tasks by title substring
- [ ] Search finds tasks by description substring
- [ ] Overdue filter returns past-due incomplete tasks
- [ ] Sort by priority orders correctly

---

### Task A.5: Create Recurring Task Service
**Status**: pending  
**File**: `backend/src/services/recurring_service.py`

**Changes**:
- [ ] `parse_recurrence_rule(rule)` - parse rule string to config
- [ ] `calculate_next_occurrence(task)` - compute next due date
- [ ] `create_next_occurrence(db, task)` - create next task instance
- [ ] Handle rules: DAILY, WEEKLY:days, MONTHLY:day, CUSTOM:n

**Test Cases**:
- [ ] DAILY rule calculates next day
- [ ] WEEKLY:MON,WED calculates next matching day
- [ ] MONTHLY:15 calculates 15th of next month
- [ ] CUSTOM:7 calculates 7 days later
- [ ] Next occurrence created with same properties

---

### Task A.6: Create Tag Router
**Status**: pending  
**File**: `backend/src/routers/tags.py`

**Changes**:
- [ ] `GET /{user_id}/tags` - list tags
- [ ] `POST /{user_id}/tags` - create tag
- [ ] `PUT /{user_id}/tags/{tag_id}` - update tag
- [ ] `DELETE /{user_id}/tags/{tag_id}` - delete tag
- [ ] `POST /{user_id}/tasks/{task_id}/tags` - add tags to task
- [ ] `DELETE /{user_id}/tasks/{task_id}/tags/{tag_id}` - remove tag from task
- [ ] Register router in main.py

**Test Cases**:
- [ ] Create tag returns 201 with tag data
- [ ] List tags returns array of user's tags
- [ ] Delete tag returns 204
- [ ] Add tag to task returns updated task

---

### Task A.7: Update Task Router with Filters
**Status**: pending  
**File**: `backend/src/routers/tasks.py`

**Changes**:
- [ ] Add query parameters: priority, tag, search, due_before, overdue, sort, order
- [ ] Update create/update schemas for priority, due_date, reminder_at, recurrence_rule
- [ ] On task completion with recurrence_rule, create next occurrence
- [ ] Include tags in task response

**Test Cases**:
- [ ] GET with priority filter works
- [ ] GET with search filter works
- [ ] GET with multiple filters works
- [ ] POST with priority creates task with priority
- [ ] Completing recurring task creates next occurrence

---

### Task A.8: Update Chat Agent Tools
**Status**: pending  
**File**: `backend/src/agents/tools.py`

**Changes**:
- [ ] Update `add_task` to accept priority, due_date, tags parameters
- [ ] Add `search_tasks(user_id, query)` tool
- [ ] Add `filter_tasks(user_id, priority, tag, overdue)` tool
- [ ] Add `set_task_priority(user_id, task_id, priority)` tool
- [ ] Add `add_task_tag(user_id, task_id, tag_name)` tool
- [ ] Add `set_due_date(user_id, task_id, due_date)` tool

**Test Cases**:
- [ ] add_task with priority sets priority
- [ ] search_tasks finds matching tasks
- [ ] filter_tasks returns filtered results

---

### Task A.9: Update Chat Agent System Prompt
**Status**: pending  
**File**: `backend/src/agents/task_agent.py`

**Changes**:
- [ ] Document priority feature in system prompt
- [ ] Document tag feature in system prompt
- [ ] Document due date feature in system prompt
- [ ] Document search and filter capabilities
- [ ] Add examples for natural language patterns

---

### Task A.10: Frontend - Add Priority Badge Component
**Status**: pending  
**File**: `frontend/src/components/PriorityBadge.tsx`

**Changes**:
- [ ] Create PriorityBadge component
- [ ] Color coding: urgent=red, high=orange, medium=blue, low=gray
- [ ] Display priority text

---

### Task A.11: Frontend - Add Tag Pill Component
**Status**: pending  
**File**: `frontend/src/components/TagPill.tsx`

**Changes**:
- [ ] Create TagPill component with tag color
- [ ] Support remove button for editing
- [ ] Display tag name

---

### Task A.12: Frontend - Update Task Card
**Status**: pending  
**File**: `frontend/src/components/TaskCard.tsx`

**Changes**:
- [ ] Add PriorityBadge display
- [ ] Add TagPill list
- [ ] Add due date indicator
- [ ] Add overdue styling (red border/text)
- [ ] Add recurring icon for recurring tasks

---

### Task A.13: Frontend - Add Filter Panel
**Status**: pending  
**File**: `frontend/src/components/FilterPanel.tsx`

**Changes**:
- [ ] Priority dropdown filter
- [ ] Tag multi-select filter
- [ ] Search input
- [ ] Date range picker for due date
- [ ] Overdue toggle
- [ ] Clear filters button

---

### Task A.14: Frontend - Update Tasks Page with Filters
**Status**: pending  
**File**: `frontend/src/app/tasks/page.tsx`

**Changes**:
- [ ] Integrate FilterPanel component
- [ ] Pass filter state to API calls
- [ ] Update task list based on filters
- [ ] Add sorting controls

---

## Part B: Dapr Integration

### Task B.1: Create Dapr Components Directory
**Status**: pending  
**File**: `dapr/components/`

**Changes**:
- [ ] Create `dapr/components/` directory
- [ ] Create `dapr/configuration.yaml` with tracing config

---

### Task B.2: Create Pub/Sub Component
**Status**: pending  
**File**: `dapr/components/pubsub.yaml`

**Changes**:
- [ ] Configure Kafka pub/sub component
- [ ] Set broker address
- [ ] Configure consumer group

---

### Task B.3: Create State Store Component
**Status**: pending  
**File**: `dapr/components/statestore.yaml`

**Changes**:
- [ ] Configure PostgreSQL state store
- [ ] Reference DATABASE_URL from secrets
- [ ] Set actor state store configuration

---

### Task B.4: Create Secrets Store Component
**Status**: pending  
**File**: `dapr/components/secrets.yaml`

**Changes**:
- [ ] Configure Kubernetes secrets store
- [ ] Reference todo-app-secrets

---

### Task B.5: Create Cron Binding Component
**Status**: pending  
**File**: `dapr/components/cron-binding.yaml`

**Changes**:
- [ ] Configure cron binding for reminders
- [ ] Set 5-minute schedule
- [ ] Configure callback route

---

### Task B.6: Create Kafka Cluster Manifest
**Status**: pending  
**File**: `k8s/dapr/kafka-cluster.yaml`

**Changes**:
- [ ] Define Strimzi Kafka cluster
- [ ] Single replica for development
- [ ] Ephemeral storage
- [ ] Plain listener on port 9092

---

### Task B.7: Create Event Service
**Status**: pending  
**File**: `backend/src/services/event_service.py`

**Changes**:
- [ ] Create `publish_event(topic, event_type, user_id, task_id, data)` function
- [ ] Use Dapr HTTP API for publishing
- [ ] Define event schema
- [ ] Handle publish errors gracefully

**Test Cases**:
- [ ] Event published successfully
- [ ] Error handled when Dapr unavailable

---

### Task B.8: Integrate Events into Task Service
**Status**: pending  
**File**: `backend/src/services/task_service.py`

**Changes**:
- [ ] Publish `task.created` on create
- [ ] Publish `task.updated` on update
- [ ] Publish `task.completed` on completion
- [ ] Publish `task.deleted` on delete
- [ ] Make publishing optional (for non-Dapr environments)

---

### Task B.9: Create Reminder Service
**Status**: pending  
**File**: `backend/src/services/reminder_service.py`

**Changes**:
- [ ] Create endpoint for cron binding callback
- [ ] Query tasks with reminder_at <= now and reminded=False
- [ ] Publish reminder events
- [ ] Mark tasks as reminded

---

### Task B.10: Create Reminder Router
**Status**: pending  
**File**: `backend/src/routers/reminders.py`

**Changes**:
- [ ] POST `/reminders/check` endpoint for Dapr cron binding
- [ ] Register router in main.py

---

### Task B.11: Create Dapr-Enabled Backend Deployment
**Status**: pending  
**File**: `k8s/dapr/backend-deployment.yaml`

**Changes**:
- [ ] Copy from base deployment
- [ ] Add Dapr annotations
- [ ] Configure app-id, app-port
- [ ] Enable API logging

---

### Task B.12: Create Dapr Deploy Script
**Status**: pending  
**File**: `scripts/deploy-dapr.sh`

**Changes**:
- [ ] Install Dapr on Minikube
- [ ] Install Strimzi operator
- [ ] Deploy Kafka cluster
- [ ] Apply Dapr components
- [ ] Deploy application with Dapr sidecars

---

## Part C: Cloud Deployment

### Task C.1: Create CI Workflow
**Status**: pending  
**File**: `.github/workflows/ci.yml`

**Changes**:
- [ ] Trigger on pull_request
- [ ] Job: test-backend (pytest)
- [ ] Job: build-frontend (npm build)
- [ ] Job: lint (ruff, eslint)

---

### Task C.2: Create Build and Push Workflow
**Status**: pending  
**File**: `.github/workflows/build-push.yml`

**Changes**:
- [ ] Trigger on push to main
- [ ] Login to ghcr.io
- [ ] Build backend image
- [ ] Build frontend image
- [ ] Push with commit SHA tag
- [ ] Push with latest tag

---

### Task C.3: Create Deploy Workflow
**Status**: pending  
**File**: `.github/workflows/deploy.yml`

**Changes**:
- [ ] Trigger on release published
- [ ] Configure kubectl with secrets
- [ ] Helm upgrade with new image tags
- [ ] Optional: staging then production

---

### Task C.4: Create Cloud Helm Values
**Status**: pending  
**File**: `helm/todo-app/values-cloud.yaml`

**Changes**:
- [ ] Set ghcr.io image repositories
- [ ] Configure production replicas
- [ ] Set resource limits
- [ ] Configure TLS ingress
- [ ] Enable Dapr

---

### Task C.5: Create AKS Deployment Guide
**Status**: pending  
**File**: `k8s/cloud/aks/README.md`

**Changes**:
- [ ] Document AKS cluster creation
- [ ] Document Azure CLI commands
- [ ] Document secrets configuration
- [ ] Document Dapr installation on AKS
- [ ] Document Strimzi installation

---

### Task C.6: Create AKS-Specific Manifests
**Status**: pending  
**File**: `k8s/cloud/aks/`

**Changes**:
- [ ] Create ingress with Azure Application Gateway annotations
- [ ] Create storage class for Azure Disk
- [ ] Create service account for ACR pull

---

### Task C.7: Add Prometheus Metrics Endpoint
**Status**: pending  
**File**: `backend/src/main.py`

**Changes**:
- [ ] Add prometheus-fastapi-instrumentator
- [ ] Configure /metrics endpoint
- [ ] Add custom metrics for task operations

---

### Task C.8: Create ServiceMonitor for Prometheus
**Status**: pending  
**File**: `k8s/monitoring/servicemonitor.yaml`

**Changes**:
- [ ] Define ServiceMonitor for backend
- [ ] Configure scrape interval
- [ ] Set metric path

---

### Task C.9: Update Main README with Phase V
**Status**: pending  
**File**: `README.md`

**Changes**:
- [ ] Document advanced features
- [ ] Document Dapr integration
- [ ] Document cloud deployment options
- [ ] Add architecture diagram
- [ ] Update feature list

---

### Task C.10: Create Dapr Documentation
**Status**: pending  
**File**: `dapr/README.md`

**Changes**:
- [ ] Document Dapr setup
- [ ] Document component configuration
- [ ] Document event schema
- [ ] Document troubleshooting

---

## Summary

| Part | Tasks | Description |
|------|-------|-------------|
| A | 14 | Advanced task features |
| B | 12 | Dapr integration |
| C | 10 | Cloud deployment |
| **Total** | **36** | |
