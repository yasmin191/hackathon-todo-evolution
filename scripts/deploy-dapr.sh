#!/bin/bash
# Deploy Todo App with Dapr on Minikube
# Usage: ./scripts/deploy-dapr.sh

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Deploying Todo App with Dapr${NC}"
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

if ! command -v dapr &> /dev/null; then
    echo -e "${RED}Error: Dapr CLI is not installed${NC}"
    echo -e "Install with: curl -fsSL https://raw.githubusercontent.com/dapr/cli/master/install/install.sh | bash"
    exit 1
fi

# Start Minikube if not running
if ! minikube status | grep -q "Running"; then
    echo -e "${YELLOW}Starting Minikube...${NC}"
    minikube start --driver=docker --memory=6144 --cpus=4
fi

# Enable required addons
echo -e "\n${YELLOW}Enabling Minikube addons...${NC}"
minikube addons enable ingress
minikube addons enable storage-provisioner

# Initialize Dapr on Kubernetes
echo -e "\n${YELLOW}Initializing Dapr on Kubernetes...${NC}"
if ! dapr status -k 2>/dev/null | grep -q "Running"; then
    dapr init -k --wait
else
    echo "Dapr already initialized"
fi

# Install Strimzi Kafka operator
echo -e "\n${YELLOW}Installing Strimzi Kafka operator...${NC}"
kubectl create namespace kafka --dry-run=client -o yaml | kubectl apply -f -

if ! kubectl get deployment strimzi-cluster-operator -n kafka 2>/dev/null; then
    kubectl apply -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka
    echo "Waiting for Strimzi operator to be ready..."
    kubectl wait --for=condition=available deployment/strimzi-cluster-operator -n kafka --timeout=300s
else
    echo "Strimzi operator already installed"
fi

# Deploy Kafka cluster
echo -e "\n${YELLOW}Deploying Kafka cluster...${NC}"
kubectl apply -f k8s/dapr/kafka-cluster.yaml

echo "Waiting for Kafka cluster to be ready..."
kubectl wait kafka/todo-kafka --for=condition=Ready --timeout=600s -n kafka || {
    echo -e "${YELLOW}Kafka taking longer than expected. Continuing...${NC}"
}

# Build images in Minikube context
echo -e "\n${YELLOW}Building images in Minikube context...${NC}"
eval $(minikube docker-env)
./scripts/build-images.sh

# Create namespace and apply base resources
echo -e "\n${YELLOW}Deploying application resources...${NC}"
kubectl apply -f k8s/base/namespace.yaml
kubectl apply -f k8s/base/configmap.yaml

# Check for secrets
if [ ! -f "k8s/base/secret.yaml" ]; then
    echo -e "${RED}Error: k8s/base/secret.yaml not found${NC}"
    echo -e "Please create it from the template"
    exit 1
fi
kubectl apply -f k8s/base/secret.yaml

# Apply Dapr configuration
echo -e "\n${YELLOW}Applying Dapr configuration...${NC}"
kubectl apply -f dapr/configuration.yaml
kubectl apply -f dapr/components/

# Deploy PostgreSQL
echo -e "\n${YELLOW}Deploying PostgreSQL...${NC}"
kubectl apply -f k8s/base/postgres/

echo "Waiting for PostgreSQL..."
kubectl wait --for=condition=ready pod -l app=postgres -n todo-app --timeout=120s

# Deploy backend with Dapr sidecar
echo -e "\n${YELLOW}Deploying backend with Dapr...${NC}"
kubectl apply -f k8s/dapr/backend-deployment.yaml
kubectl apply -f k8s/base/backend/service.yaml

# Deploy frontend
echo -e "\n${YELLOW}Deploying frontend...${NC}"
kubectl apply -f k8s/base/frontend/

# Deploy ingress
kubectl apply -f k8s/base/ingress.yaml

# Wait for deployments
echo -e "\n${YELLOW}Waiting for deployments to be ready...${NC}"
kubectl wait --for=condition=available deployment/todo-backend -n todo-app --timeout=180s || true
kubectl wait --for=condition=available deployment/todo-frontend -n todo-app --timeout=120s || true

# Show status
echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}"

MINIKUBE_IP=$(minikube ip)
echo -e "\nMinikube IP: ${MINIKUBE_IP}"
echo -e "\nAdd to /etc/hosts:"
echo -e "  ${MINIKUBE_IP} todo.local"
echo -e "\nAccess the app at:"
echo -e "  http://todo.local"

echo -e "\n${YELLOW}Dapr Dashboard:${NC}"
echo -e "  Run: dapr dashboard -k"

echo -e "\n${YELLOW}Check pod status:${NC}"
kubectl get pods -n todo-app

echo -e "\n${YELLOW}Check Dapr sidecar status:${NC}"
kubectl get pods -n todo-app -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[*].name}{"\n"}{end}'
