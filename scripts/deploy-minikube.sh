#!/bin/bash
# Deploy Todo App to Minikube
# Usage: ./scripts/deploy-minikube.sh [helm|kubectl]

set -e

# Configuration
DEPLOY_METHOD=${1:-"helm"}
NAMESPACE="todo-app"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Deploying Todo App to Minikube${NC}"
echo -e "${GREEN}========================================${NC}"

# Navigate to project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

# Check prerequisites
echo -e "\n${YELLOW}Checking prerequisites...${NC}"

if ! command -v minikube &> /dev/null; then
    echo -e "${RED}Error: minikube is not installed${NC}"
    exit 1
fi

if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}Error: kubectl is not installed${NC}"
    exit 1
fi

# Check if Minikube is running
if ! minikube status | grep -q "Running"; then
    echo -e "${YELLOW}Starting Minikube...${NC}"
    minikube start --driver=docker --memory=4096 --cpus=2
fi

# Enable required addons
echo -e "\n${YELLOW}Enabling Minikube addons...${NC}"
minikube addons enable ingress
minikube addons enable storage-provisioner

# Build images in Minikube's Docker context
echo -e "\n${YELLOW}Building images in Minikube context...${NC}"
eval $(minikube docker-env)
./scripts/build-images.sh

# Check for secrets file
if [ ! -f "k8s/base/secret.yaml" ]; then
    echo -e "${RED}Error: k8s/base/secret.yaml not found${NC}"
    echo -e "Please create it from the template:"
    echo -e "  cp k8s/base/secret.yaml.template k8s/base/secret.yaml"
    echo -e "  # Edit with your base64-encoded values"
    exit 1
fi

if [ "$DEPLOY_METHOD" == "helm" ]; then
    echo -e "\n${YELLOW}Deploying with Helm...${NC}"

    if ! command -v helm &> /dev/null; then
        echo -e "${RED}Error: helm is not installed${NC}"
        echo -e "Install it or use: ./scripts/deploy-minikube.sh kubectl"
        exit 1
    fi

    # Create namespace if not exists
    kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

    # Apply secrets first (not managed by Helm for security)
    kubectl apply -f k8s/base/secret.yaml -n $NAMESPACE

    # Install/upgrade with Helm
    helm upgrade --install todo-app ./helm/todo-app \
        --namespace $NAMESPACE \
        --set backend.image.pullPolicy=Never \
        --set frontend.image.pullPolicy=Never \
        --wait --timeout=5m

else
    echo -e "\n${YELLOW}Deploying with kubectl...${NC}"

    # Apply all manifests
    kubectl apply -f k8s/base/namespace.yaml
    kubectl apply -f k8s/base/configmap.yaml
    kubectl apply -f k8s/base/secret.yaml
    kubectl apply -f k8s/base/postgres/

    # Wait for PostgreSQL
    echo -e "${YELLOW}Waiting for PostgreSQL...${NC}"
    kubectl wait --for=condition=ready pod -l app=postgres -n $NAMESPACE --timeout=120s

    kubectl apply -f k8s/base/backend/
    kubectl apply -f k8s/base/frontend/
    kubectl apply -f k8s/base/ingress.yaml
fi

# Wait for deployments
echo -e "\n${YELLOW}Waiting for deployments to be ready...${NC}"
kubectl wait --for=condition=available deployment/todo-backend -n $NAMESPACE --timeout=120s || true
kubectl wait --for=condition=available deployment/todo-frontend -n $NAMESPACE --timeout=120s || true

# Get access info
echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}"

MINIKUBE_IP=$(minikube ip)
echo -e "\nMinikube IP: ${MINIKUBE_IP}"
echo -e "\nAdd to /etc/hosts:"
echo -e "  ${MINIKUBE_IP} todo.local"
echo -e "\nAccess the app at:"
echo -e "  http://todo.local"
echo -e "\nOr use NodePort:"
echo -e "  http://${MINIKUBE_IP}:30080"
echo -e "\nCheck pod status:"
echo -e "  kubectl get pods -n ${NAMESPACE}"
