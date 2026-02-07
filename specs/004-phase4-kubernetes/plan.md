# Implementation Plan: Phase IV - Local Kubernetes (Minikube)

**Branch**: `004-phase4-kubernetes` | **Date**: 2026-02-07 | **Spec**: [spec.md](spec.md)

## Summary

Containerize the todo application and deploy it to a local Kubernetes cluster using Minikube. Create Docker images for frontend and backend, Kubernetes manifests for all resources, and Helm charts for parameterized deployment.

## Project Structure

```
hackathon-todo/
├── docker/
│   ├── backend.Dockerfile
│   └── frontend.Dockerfile
├── k8s/
│   ├── base/
│   │   ├── namespace.yaml
│   │   ├── configmap.yaml
│   │   ├── secret.yaml
│   │   ├── postgres/
│   │   │   ├── statefulset.yaml
│   │   │   ├── service.yaml
│   │   │   └── pvc.yaml
│   │   ├── backend/
│   │   │   ├── deployment.yaml
│   │   │   └── service.yaml
│   │   ├── frontend/
│   │   │   ├── deployment.yaml
│   │   │   └── service.yaml
│   │   └── ingress.yaml
│   └── minikube/
│       └── kustomization.yaml
├── helm/
│   └── todo-app/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│           ├── _helpers.tpl
│           ├── namespace.yaml
│           ├── configmap.yaml
│           ├── secret.yaml
│           ├── postgres-statefulset.yaml
│           ├── postgres-service.yaml
│           ├── backend-deployment.yaml
│           ├── backend-service.yaml
│           ├── frontend-deployment.yaml
│           ├── frontend-service.yaml
│           └── ingress.yaml
└── scripts/
    ├── build-images.sh
    ├── deploy-minikube.sh
    └── cleanup.sh
```

## Docker Configuration

### Backend Dockerfile

```dockerfile
FROM python:3.13-slim AS builder
WORKDIR /app
RUN pip install uv
COPY pyproject.toml README.md ./
COPY src ./src
RUN uv sync --no-dev

FROM python:3.13-slim
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY src ./src
ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s CMD curl -f http://localhost:8000/health || exit 1
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Dockerfile

```dockerfile
FROM node:22-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

FROM node:22-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM node:22-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
RUN addgroup -g 1001 -S nodejs && adduser -S nextjs -u 1001
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
USER nextjs
EXPOSE 3000
CMD ["node", "server.js"]
```

## Kubernetes Resources

### Namespace
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: todo-app
```

### ConfigMap
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: todo-config
  namespace: todo-app
data:
  CORS_ORIGINS: "http://localhost:3000"
  OPENAI_MODEL: "gpt-4o-mini"
```

### Secret
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: todo-secrets
  namespace: todo-app
type: Opaque
stringData:
  DATABASE_URL: "postgresql://..."
  BETTER_AUTH_SECRET: "..."
  OPENAI_API_KEY: "sk-..."
```

### Backend Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-backend
  namespace: todo-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: todo-backend
  template:
    metadata:
      labels:
        app: todo-backend
    spec:
      containers:
      - name: backend
        image: todo-backend:latest
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: todo-config
        - secretRef:
            name: todo-secrets
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

## Helm Chart Values

```yaml
# values.yaml
replicaCount:
  frontend: 2
  backend: 2

image:
  frontend:
    repository: todo-frontend
    tag: latest
    pullPolicy: IfNotPresent
  backend:
    repository: todo-backend
    tag: latest
    pullPolicy: IfNotPresent

service:
  frontend:
    type: NodePort
    port: 3000
  backend:
    type: ClusterIP
    port: 8000

ingress:
  enabled: true
  className: nginx
  hosts:
    - host: todo.local
      paths:
        - path: /
          pathType: Prefix

postgresql:
  enabled: true
  persistence:
    size: 1Gi

config:
  corsOrigins: "http://todo.local"
  openaiModel: "gpt-4o-mini"

secrets:
  databaseUrl: ""
  betterAuthSecret: ""
  openaiApiKey: ""
```

## Deployment Commands

### Build Images for Minikube
```bash
# Use Minikube's Docker daemon
eval $(minikube docker-env)

# Build images
docker build -t todo-backend:latest -f docker/backend.Dockerfile ./backend
docker build -t todo-frontend:latest -f docker/frontend.Dockerfile ./frontend
```

### Deploy with kubectl
```bash
# Apply all manifests
kubectl apply -f k8s/base/namespace.yaml
kubectl apply -f k8s/base/

# Check status
kubectl get pods -n todo-app
kubectl get services -n todo-app
```

### Deploy with Helm
```bash
# Install chart
helm install todo-app ./helm/todo-app -n todo-app --create-namespace

# Upgrade
helm upgrade todo-app ./helm/todo-app -n todo-app

# Uninstall
helm uninstall todo-app -n todo-app
```

### Access Application
```bash
# Get Minikube IP
minikube ip

# Access via NodePort
minikube service todo-frontend -n todo-app

# Or use ingress
echo "$(minikube ip) todo.local" | sudo tee -a /etc/hosts
```

## Implementation Order

1. **Docker Images** - Update Dockerfiles for production
2. **K8s Base Manifests** - Namespace, ConfigMap, Secret
3. **PostgreSQL** - StatefulSet with PVC
4. **Backend** - Deployment and Service
5. **Frontend** - Deployment and Service
6. **Ingress** - External access
7. **Helm Chart** - Parameterized deployment
8. **Scripts** - Automation for build/deploy
9. **Testing** - Verify deployment

## Complexity Tracking

| Aspect | Decision | Rationale |
|--------|----------|-----------|
| Container Runtime | Docker | Standard, works with Minikube |
| K8s Distribution | Minikube | Local development, hackathon requirement |
| Package Manager | Helm | Industry standard, parameterized |
| Ingress | NGINX | Widely supported, easy setup |
| DB Storage | PVC | Persistent across restarts |
