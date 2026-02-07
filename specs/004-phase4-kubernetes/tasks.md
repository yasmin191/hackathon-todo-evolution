# Tasks: Phase IV - Local Kubernetes (Minikube)

**Feature Branch**: `004-phase4-kubernetes`
**Created**: 2026-02-07
**Spec**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

---

## Phase Overview

Containerize and deploy the todo application to Minikube with:
- Production-ready Docker images
- Kubernetes manifests (Deployments, Services, ConfigMaps, Secrets)
- Helm charts for parameterized deployment
- Health checks and persistent storage

**Total Tasks**: 24 | **Estimated Complexity**: High

---

## Epic 1: Docker Configuration

### Task 1.1: Create Docker Directory Structure
**Priority**: P0 | **Type**: Setup | **Depends on**: None

Create directory structure for Docker files.

**Acceptance Criteria**:
- [ ] Create `docker/` directory
- [ ] Move existing Dockerfiles or create new ones
- [ ] Create `.dockerignore` files

**Test Cases**:
```
TC-1.1.1: Directory structure exists
TC-1.1.2: .dockerignore excludes node_modules, .venv, etc.
```

---

### Task 1.2: Create Backend Production Dockerfile
**Priority**: P0 | **Type**: Implementation | **Depends on**: 1.1

Create optimized multi-stage Dockerfile for backend.

**Acceptance Criteria**:
- [ ] Create `docker/backend.Dockerfile`
- [ ] Multi-stage build (builder + runtime)
- [ ] Install dependencies with UV
- [ ] Non-root user
- [ ] Health check command
- [ ] Expose port 8000

**Test Cases**:
```
TC-1.2.1: Image builds successfully
TC-1.2.2: Image size is under 500MB
TC-1.2.3: Health check passes
TC-1.2.4: Runs as non-root
```

---

### Task 1.3: Create Frontend Production Dockerfile
**Priority**: P0 | **Type**: Implementation | **Depends on**: 1.1

Create optimized multi-stage Dockerfile for frontend.

**Acceptance Criteria**:
- [ ] Create `docker/frontend.Dockerfile`
- [ ] Multi-stage build (deps + builder + runner)
- [ ] Next.js standalone output
- [ ] Non-root user
- [ ] Expose port 3000

**Test Cases**:
```
TC-1.3.1: Image builds successfully
TC-1.3.2: Image size is under 200MB
TC-1.3.3: Next.js serves correctly
TC-1.3.4: Runs as non-root
```

---

### Task 1.4: Update Next.js for Standalone Output
**Priority**: P0 | **Type**: Implementation | **Depends on**: 1.3

Configure Next.js for standalone Docker deployment.

**Acceptance Criteria**:
- [ ] Add `output: 'standalone'` to next.config.ts
- [ ] Verify build produces standalone folder
- [ ] Test standalone server works

**Test Cases**:
```
TC-1.4.1: Build creates .next/standalone
TC-1.4.2: Standalone server starts correctly
```

---

### Task 1.5: Create Build Script
**Priority**: P1 | **Type**: Implementation | **Depends on**: 1.2, 1.3

Create script to build Docker images.

**Acceptance Criteria**:
- [ ] Create `scripts/build-images.sh`
- [ ] Build both frontend and backend images
- [ ] Tag with version and latest
- [ ] Support Minikube Docker daemon

**Test Cases**:
```
TC-1.5.1: Script builds both images
TC-1.5.2: Images are properly tagged
```

---

## Epic 2: Kubernetes Base Manifests

### Task 2.1: Create K8s Directory Structure
**Priority**: P0 | **Type**: Setup | **Depends on**: None

Create directory structure for Kubernetes manifests.

**Acceptance Criteria**:
- [ ] Create `k8s/base/` directory
- [ ] Create subdirectories for each component
- [ ] Create `k8s/minikube/` for environment overlay

**Test Cases**:
```
TC-2.1.1: Directory structure matches plan
```

---

### Task 2.2: Create Namespace Manifest
**Priority**: P0 | **Type**: Implementation | **Depends on**: 2.1

Create namespace for the application.

**Acceptance Criteria**:
- [ ] Create `k8s/base/namespace.yaml`
- [ ] Namespace named `todo-app`
- [ ] Add appropriate labels

**Test Cases**:
```
TC-2.2.1: kubectl apply creates namespace
TC-2.2.2: Namespace has correct labels
```

---

### Task 2.3: Create ConfigMap Manifest
**Priority**: P0 | **Type**: Implementation | **Depends on**: 2.2

Create ConfigMap for non-sensitive configuration.

**Acceptance Criteria**:
- [ ] Create `k8s/base/configmap.yaml`
- [ ] Include CORS_ORIGINS, OPENAI_MODEL
- [ ] Add other non-sensitive env vars

**Test Cases**:
```
TC-2.3.1: ConfigMap created successfully
TC-2.3.2: All config values present
```

---

### Task 2.4: Create Secret Manifest Template
**Priority**: P0 | **Type**: Implementation | **Depends on**: 2.2

Create Secret template for sensitive data.

**Acceptance Criteria**:
- [ ] Create `k8s/base/secret.yaml.template`
- [ ] Include DATABASE_URL, BETTER_AUTH_SECRET, OPENAI_API_KEY
- [ ] Document how to create actual secret
- [ ] Add to .gitignore for actual secret file

**Test Cases**:
```
TC-2.4.1: Secret template has all required fields
TC-2.4.2: Actual secret not committed to git
```

---

### Task 2.5: Create PostgreSQL StatefulSet
**Priority**: P0 | **Type**: Implementation | **Depends on**: 2.4

Create PostgreSQL database deployment.

**Acceptance Criteria**:
- [ ] Create `k8s/base/postgres/statefulset.yaml`
- [ ] Create `k8s/base/postgres/service.yaml`
- [ ] Create `k8s/base/postgres/pvc.yaml`
- [ ] Configure persistent volume claim
- [ ] Set resource limits

**Test Cases**:
```
TC-2.5.1: StatefulSet creates pod
TC-2.5.2: PVC is bound
TC-2.5.3: Data persists across pod restart
```

---

### Task 2.6: Create Backend Deployment
**Priority**: P0 | **Type**: Implementation | **Depends on**: 2.4, 2.5

Create backend deployment manifest.

**Acceptance Criteria**:
- [ ] Create `k8s/base/backend/deployment.yaml`
- [ ] Create `k8s/base/backend/service.yaml`
- [ ] 2 replicas
- [ ] Environment from ConfigMap and Secret
- [ ] Liveness and readiness probes
- [ ] Resource limits

**Test Cases**:
```
TC-2.6.1: Deployment creates 2 pods
TC-2.6.2: Probes pass
TC-2.6.3: Service routes traffic to pods
```

---

### Task 2.7: Create Frontend Deployment
**Priority**: P0 | **Type**: Implementation | **Depends on**: 2.3

Create frontend deployment manifest.

**Acceptance Criteria**:
- [ ] Create `k8s/base/frontend/deployment.yaml`
- [ ] Create `k8s/base/frontend/service.yaml`
- [ ] 2 replicas
- [ ] Environment for API URL
- [ ] Liveness and readiness probes
- [ ] Resource limits
- [ ] NodePort or LoadBalancer service

**Test Cases**:
```
TC-2.7.1: Deployment creates 2 pods
TC-2.7.2: Service exposes frontend
TC-2.7.3: Frontend connects to backend
```

---

### Task 2.8: Create Ingress Manifest
**Priority**: P1 | **Type**: Implementation | **Depends on**: 2.6, 2.7

Create Ingress for external access.

**Acceptance Criteria**:
- [ ] Create `k8s/base/ingress.yaml`
- [ ] Route / to frontend
- [ ] Route /api to backend
- [ ] Configure for nginx ingress class

**Test Cases**:
```
TC-2.8.1: Ingress routes to frontend
TC-2.8.2: API routes work through ingress
```

---

## Epic 3: Helm Chart

### Task 3.1: Create Helm Chart Structure
**Priority**: P1 | **Type**: Setup | **Depends on**: 2.7

Create Helm chart directory structure.

**Acceptance Criteria**:
- [ ] Create `helm/todo-app/` directory
- [ ] Create `Chart.yaml`
- [ ] Create `values.yaml`
- [ ] Create `templates/` directory
- [ ] Create `templates/_helpers.tpl`

**Test Cases**:
```
TC-3.1.1: helm lint passes
TC-3.1.2: Chart.yaml has correct metadata
```

---

### Task 3.2: Create Helm Templates
**Priority**: P1 | **Type**: Implementation | **Depends on**: 3.1

Convert K8s manifests to Helm templates.

**Acceptance Criteria**:
- [ ] Create all templates from base manifests
- [ ] Parameterize replica counts
- [ ] Parameterize image names and tags
- [ ] Parameterize resource limits
- [ ] Use values.yaml for configuration

**Test Cases**:
```
TC-3.2.1: helm template renders correctly
TC-3.2.2: All values are parameterized
```

---

### Task 3.3: Create Default Values
**Priority**: P1 | **Type**: Implementation | **Depends on**: 3.2

Define default values for Helm chart.

**Acceptance Criteria**:
- [ ] Configure `values.yaml` with defaults
- [ ] Document all values
- [ ] Provide example for secrets
- [ ] Set sensible resource limits

**Test Cases**:
```
TC-3.3.1: Default values work out of the box
TC-3.3.2: All values are documented
```

---

### Task 3.4: Add Helm Notes
**Priority**: P2 | **Type**: Implementation | **Depends on**: 3.2

Create post-install notes.

**Acceptance Criteria**:
- [ ] Create `templates/NOTES.txt`
- [ ] Show how to access application
- [ ] Show how to get Minikube IP
- [ ] Document next steps

**Test Cases**:
```
TC-3.4.1: Notes display after install
TC-3.4.2: Instructions are accurate
```

---

## Epic 4: Deployment Scripts

### Task 4.1: Create Minikube Setup Script
**Priority**: P1 | **Type**: Implementation | **Depends on**: 1.5

Create script to set up Minikube environment.

**Acceptance Criteria**:
- [ ] Create `scripts/setup-minikube.sh`
- [ ] Start Minikube if not running
- [ ] Enable required addons (ingress, metrics-server)
- [ ] Configure Docker to use Minikube daemon

**Test Cases**:
```
TC-4.1.1: Script starts Minikube
TC-4.1.2: Addons are enabled
```

---

### Task 4.2: Create Deployment Script
**Priority**: P1 | **Type**: Implementation | **Depends on**: 2.8

Create script to deploy to Minikube.

**Acceptance Criteria**:
- [ ] Create `scripts/deploy-minikube.sh`
- [ ] Build images
- [ ] Apply manifests or install Helm chart
- [ ] Wait for pods to be ready
- [ ] Print access instructions

**Test Cases**:
```
TC-4.2.1: Script deploys successfully
TC-4.2.2: All pods are running
TC-4.2.3: Application is accessible
```

---

### Task 4.3: Create Cleanup Script
**Priority**: P2 | **Type**: Implementation | **Depends on**: 4.2

Create script to clean up deployment.

**Acceptance Criteria**:
- [ ] Create `scripts/cleanup.sh`
- [ ] Delete namespace or Helm release
- [ ] Optionally delete images
- [ ] Optionally stop Minikube

**Test Cases**:
```
TC-4.3.1: Script removes all resources
TC-4.3.2: Namespace is deleted
```

---

## Epic 5: Documentation

### Task 5.1: Create K8s README
**Priority**: P1 | **Type**: Documentation | **Depends on**: 4.2

Document Kubernetes deployment.

**Acceptance Criteria**:
- [ ] Create `k8s/README.md`
- [ ] Document prerequisites
- [ ] Document deployment steps
- [ ] Document troubleshooting

**Test Cases**:
```
TC-5.1.1: README is complete
TC-5.1.2: Steps work as documented
```

---

### Task 5.2: Update Main README
**Priority**: P1 | **Type**: Documentation | **Depends on**: 5.1

Update project README for Phase IV.

**Acceptance Criteria**:
- [ ] Add Kubernetes deployment section
- [ ] Update phase status
- [ ] Add Minikube prerequisites
- [ ] Document Helm installation

**Test Cases**:
```
TC-5.2.1: README reflects Phase IV
```

---

## Task Dependency Graph

```
1.1 ──┬── 1.2 ──┬── 1.5
      │         │
      └── 1.3 ──┤
          │     │
         1.4 ───┘

2.1 ── 2.2 ──┬── 2.3 ──┬── 2.7 ──┐
             │         │         │
             └── 2.4 ──┼── 2.5 ──┤── 2.8
                       │         │
                       └── 2.6 ──┘

3.1 ── 3.2 ── 3.3 ── 3.4

1.5 ── 4.1 ── 4.2 ── 4.3
       │
2.8 ───┘

4.2 ── 5.1 ── 5.2
```

---

## Implementation Order

### Wave 1: Docker (Tasks 1.1-1.5)
Build production-ready Docker images.

### Wave 2: K8s Base (Tasks 2.1-2.8)
Create all Kubernetes manifests.

### Wave 3: Helm (Tasks 3.1-3.4)
Create Helm chart for parameterized deployment.

### Wave 4: Scripts (Tasks 4.1-4.3)
Automation scripts for deployment.

### Wave 5: Docs (Tasks 5.1-5.2)
Documentation updates.

---

## Summary

| Epic | Tasks | Priority Mix |
|------|-------|--------------|
| 1. Docker | 5 | P0: 4, P1: 1 |
| 2. K8s Manifests | 8 | P0: 7, P1: 1 |
| 3. Helm Chart | 4 | P1: 3, P2: 1 |
| 4. Scripts | 3 | P1: 2, P2: 1 |
| 5. Documentation | 2 | P1: 2 |
| **Total** | **22** | P0: 11, P1: 9, P2: 2 |
