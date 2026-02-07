# Feature Specification: Phase IV - Local Kubernetes (Minikube)

**Feature Branch**: `004-phase4-kubernetes`
**Created**: 2026-02-07
**Status**: Draft
**Points**: 250

## Overview

Containerize the application and deploy it to a local Kubernetes cluster using Minikube. This phase focuses on cloud-native deployment patterns with Docker containers, Kubernetes manifests, and Helm charts.

## Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                         Minikube Cluster                           │
│                                                                     │
│  ┌─────────────────┐     ┌─────────────────┐     ┌──────────────┐ │
│  │   Frontend      │     │    Backend      │     │  PostgreSQL  │ │
│  │   Deployment    │────▶│   Deployment    │────▶│  StatefulSet │ │
│  │   (Next.js)     │     │   (FastAPI)     │     │              │ │
│  │   Replicas: 2   │     │   Replicas: 2   │     │  Replicas: 1 │ │
│  └────────┬────────┘     └────────┬────────┘     └──────────────┘ │
│           │                       │                                │
│  ┌────────▼────────┐     ┌────────▼────────┐                      │
│  │ Frontend Service│     │ Backend Service │                      │
│  │ (LoadBalancer)  │     │   (ClusterIP)   │                      │
│  └─────────────────┘     └─────────────────┘                      │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                      Ingress Controller                       │  │
│  │                   (NGINX or Traefik)                          │  │
│  └─────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────┘
```

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Build Docker Images (Priority: P0)

As a developer, I want to build Docker images for frontend and backend so that I can deploy them to Kubernetes.

**Why this priority**: Foundation for all Kubernetes deployment.

**Independent Test**: Run `docker build` and images are created successfully.

**Acceptance Scenarios**:

1. **Given** I have Docker installed, **When** I run `docker build` in backend/, **Then** a backend image is created
2. **Given** I have Docker installed, **When** I run `docker build` in frontend/, **Then** a frontend image is created
3. **Given** images are built, **When** I run them locally, **Then** the application works

---

### User Story 2 - Deploy to Minikube (Priority: P0)

As a developer, I want to deploy the application to Minikube so that I can test Kubernetes deployment locally.

**Why this priority**: Core requirement of Phase IV.

**Independent Test**: Run `kubectl apply` and pods are running.

**Acceptance Scenarios**:

1. **Given** Minikube is running, **When** I apply K8s manifests, **Then** pods are created
2. **Given** pods are running, **When** I check pod status, **Then** all pods are healthy
3. **Given** services are created, **When** I access the app, **Then** it responds correctly

---

### User Story 3 - Helm Chart Deployment (Priority: P1)

As a developer, I want to use Helm charts so that I can manage deployments with configuration.

**Why this priority**: Enables parameterized deployments.

**Independent Test**: Run `helm install` and application deploys.

**Acceptance Scenarios**:

1. **Given** Helm is installed, **When** I run `helm install`, **Then** the chart deploys
2. **Given** chart is deployed, **When** I change values.yaml, **Then** `helm upgrade` applies changes
3. **Given** chart is deployed, **When** I run `helm uninstall`, **Then** resources are removed

---

### User Story 4 - Health Checks and Probes (Priority: P1)

As an operator, I want Kubernetes to monitor application health so that unhealthy pods are restarted.

**Why this priority**: Essential for production reliability.

**Independent Test**: Kill a pod and Kubernetes restarts it.

**Acceptance Scenarios**:

1. **Given** pods have liveness probes, **When** app becomes unhealthy, **Then** pod is restarted
2. **Given** pods have readiness probes, **When** pod is not ready, **Then** traffic is not routed
3. **Given** pods are healthy, **When** I check probes, **Then** they report success

---

### User Story 5 - Environment Configuration (Priority: P1)

As a developer, I want to manage configuration via ConfigMaps and Secrets so that I can separate config from code.

**Why this priority**: Security and configurability.

**Independent Test**: Change a ConfigMap and the app reflects the change.

**Acceptance Scenarios**:

1. **Given** database URL is in Secret, **When** pod starts, **Then** it connects to database
2. **Given** CORS origins in ConfigMap, **When** I update it, **Then** app uses new value
3. **Given** OpenAI key in Secret, **When** chat is used, **Then** agent works

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Backend MUST be containerized with Docker
- **FR-002**: Frontend MUST be containerized with Docker  
- **FR-003**: Images MUST be buildable with `docker build`
- **FR-004**: Application MUST deploy to Minikube cluster
- **FR-005**: Kubernetes manifests MUST include Deployments, Services, ConfigMaps, Secrets
- **FR-006**: Helm chart MUST be provided for parameterized deployment
- **FR-007**: All pods MUST have liveness and readiness probes
- **FR-008**: Sensitive data MUST be stored in Kubernetes Secrets
- **FR-009**: Application MUST be accessible via Ingress or NodePort
- **FR-010**: Database MUST persist data via PersistentVolumeClaim

### Kubernetes Resources

| Resource | Name | Purpose |
|----------|------|---------|
| Deployment | todo-frontend | Frontend pods |
| Deployment | todo-backend | Backend pods |
| StatefulSet | todo-postgres | Database with persistent storage |
| Service | frontend-svc | Expose frontend |
| Service | backend-svc | Expose backend internally |
| Service | postgres-svc | Database access |
| ConfigMap | todo-config | Non-sensitive configuration |
| Secret | todo-secrets | Sensitive credentials |
| Ingress | todo-ingress | External access |
| PVC | postgres-pvc | Database storage |

### Docker Images

| Image | Base | Exposed Port |
|-------|------|--------------|
| todo-frontend | node:22-alpine | 3000 |
| todo-backend | python:3.13-slim | 8000 |

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Docker images build in under 5 minutes each
- **SC-002**: All pods reach Running state within 2 minutes of deployment
- **SC-003**: Health probes pass for all pods
- **SC-004**: Application accessible via `minikube service` or Ingress
- **SC-005**: Data persists across pod restarts
- **SC-006**: `helm install` deploys complete application
- **SC-007**: Zero downtime during `helm upgrade`
