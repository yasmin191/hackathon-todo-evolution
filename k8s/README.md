# Kubernetes Deployment Guide

This guide covers deploying the Todo App to Kubernetes using Minikube.

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) or Docker Engine
- [Minikube](https://minikube.sigs.k8s.io/docs/start/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [Helm](https://helm.sh/docs/intro/install/) (optional, for Helm deployment)

## Quick Start

### 1. Start Minikube

```bash
minikube start --driver=docker --memory=4096 --cpus=2
minikube addons enable ingress
minikube addons enable storage-provisioner
```

### 2. Configure Secrets

Copy the secret template and fill in your values:

```bash
cp k8s/base/secret.yaml.template k8s/base/secret.yaml
```

Edit `k8s/base/secret.yaml` with base64-encoded values:

```bash
# Generate base64 values
echo -n "postgresql://postgres:postgres@postgres:5432/tododb" | base64
echo -n "your-jwt-secret-here" | base64
echo -n "your-openai-api-key" | base64
```

### 3. Build Images

Build Docker images in Minikube's context:

```bash
eval $(minikube docker-env)
./scripts/build-images.sh
```

### 4. Deploy

**Option A: Using Helm (Recommended)**

```bash
./scripts/deploy-minikube.sh helm
```

**Option B: Using kubectl**

```bash
./scripts/deploy-minikube.sh kubectl
```

### 5. Access the Application

Add the Minikube IP to your hosts file:

```bash
echo "$(minikube ip) todo.local" | sudo tee -a /etc/hosts
```

Access the app at: http://todo.local

Or use NodePort directly: http://$(minikube ip):30080

## Project Structure

```
k8s/
├── base/                    # Raw Kubernetes manifests
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── secret.yaml.template
│   ├── ingress.yaml
│   ├── postgres/
│   │   ├── pvc.yaml
│   │   ├── statefulset.yaml
│   │   └── service.yaml
│   ├── backend/
│   │   ├── deployment.yaml
│   │   └── service.yaml
│   └── frontend/
│       ├── deployment.yaml
│       └── service.yaml
└── README.md

helm/
└── todo-app/               # Helm chart
    ├── Chart.yaml
    ├── values.yaml
    └── templates/
        ├── _helpers.tpl
        ├── namespace.yaml
        ├── configmap.yaml
        ├── secret.yaml
        ├── postgres-*.yaml
        ├── backend-*.yaml
        ├── frontend-*.yaml
        ├── ingress.yaml
        └── NOTES.txt

scripts/
├── build-images.sh         # Build Docker images
├── deploy-minikube.sh      # Deploy to Minikube
└── cleanup.sh              # Clean up deployment
```

## Helm Chart Configuration

Key values in `helm/todo-app/values.yaml`:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `namespace` | Kubernetes namespace | `todo-app` |
| `backend.replicaCount` | Backend replicas | `2` |
| `frontend.replicaCount` | Frontend replicas | `2` |
| `postgres.storage` | PostgreSQL storage size | `1Gi` |
| `ingress.enabled` | Enable ingress | `true` |
| `ingress.host` | Ingress hostname | `todo.local` |

Override values during deployment:

```bash
helm upgrade --install todo-app ./helm/todo-app \
  --set backend.replicaCount=3 \
  --set ingress.host=myapp.local
```

## Common Commands

```bash
# Check pod status
kubectl get pods -n todo-app

# View logs
kubectl logs -f deployment/todo-backend -n todo-app
kubectl logs -f deployment/todo-frontend -n todo-app

# Describe resources
kubectl describe pod <pod-name> -n todo-app

# Port forward for debugging
kubectl port-forward svc/todo-backend 8000:8000 -n todo-app
kubectl port-forward svc/todo-frontend 3000:3000 -n todo-app

# Execute into a pod
kubectl exec -it deployment/todo-backend -n todo-app -- /bin/bash

# Check ingress
kubectl get ingress -n todo-app
```

## Troubleshooting

### Pods stuck in Pending state

Check if storage class is available:
```bash
kubectl get storageclass
minikube addons enable storage-provisioner
```

### Cannot pull images

Ensure images are built in Minikube's Docker context:
```bash
eval $(minikube docker-env)
./scripts/build-images.sh
```

### Ingress not working

1. Verify ingress addon is enabled:
   ```bash
   minikube addons enable ingress
   ```

2. Check ingress controller:
   ```bash
   kubectl get pods -n ingress-nginx
   ```

3. Verify hosts file entry points to Minikube IP

### Database connection issues

1. Check PostgreSQL pod:
   ```bash
   kubectl get pods -l app=postgres -n todo-app
   kubectl logs statefulset/postgres -n todo-app
   ```

2. Verify secret values are correct:
   ```bash
   kubectl get secret todo-app-secrets -n todo-app -o yaml
   ```

## Cleanup

Remove the deployment:

```bash
./scripts/cleanup.sh
```

Remove everything including Docker images:

```bash
./scripts/cleanup.sh --all
```

## AIOps Tools (Phase IV Bonus)

Use AI-powered Kubernetes tools:

```bash
# kubectl-ai - Natural language kubectl
kubectl-ai "show all pods in todo-app namespace"
kubectl-ai "why is the backend pod failing"

# Gordon - Docker AI Agent
docker ai "build optimized images for production"

# Kagent - Kubernetes Agent
kagent "analyze cluster health and suggest improvements"
```
