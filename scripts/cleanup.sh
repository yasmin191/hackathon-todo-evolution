#!/bin/bash
# Cleanup Todo App deployment from Minikube
# Usage: ./scripts/cleanup.sh [--all]

set -e

# Configuration
NAMESPACE="todo-app"
CLEAN_ALL=${1:-""}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}Cleaning up Todo App${NC}"
echo -e "${YELLOW}========================================${NC}"

# Check if Helm release exists
if command -v helm &> /dev/null; then
    if helm list -n $NAMESPACE | grep -q "todo-app"; then
        echo -e "\n${YELLOW}Uninstalling Helm release...${NC}"
        helm uninstall todo-app -n $NAMESPACE
    fi
fi

# Delete namespace (this removes all resources in it)
echo -e "\n${YELLOW}Deleting namespace ${NAMESPACE}...${NC}"
kubectl delete namespace $NAMESPACE --ignore-not-found=true

# Clean up local images if requested
if [ "$CLEAN_ALL" == "--all" ]; then
    echo -e "\n${YELLOW}Cleaning up Docker images...${NC}"

    # Switch to Minikube's Docker context
    if command -v minikube &> /dev/null && minikube status | grep -q "Running"; then
        eval $(minikube docker-env)
    fi

    docker rmi todo-backend:latest 2>/dev/null || true
    docker rmi todo-frontend:latest 2>/dev/null || true

    echo -e "${GREEN}Docker images cleaned${NC}"
fi

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}Cleanup Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
