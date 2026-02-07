#!/bin/bash
# Build Docker images for the Todo App
# Usage: ./scripts/build-images.sh [--push]

set -e

# Configuration
REGISTRY=${REGISTRY:-""}
TAG=${TAG:-"latest"}
PUSH=${1:-""}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Building Todo App Docker Images${NC}"
echo -e "${GREEN}========================================${NC}"

# Navigate to project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

# Set image names
if [ -n "$REGISTRY" ]; then
    BACKEND_IMAGE="${REGISTRY}/todo-backend:${TAG}"
    FRONTEND_IMAGE="${REGISTRY}/todo-frontend:${TAG}"
else
    BACKEND_IMAGE="todo-backend:${TAG}"
    FRONTEND_IMAGE="todo-frontend:${TAG}"
fi

echo -e "\n${YELLOW}Building Backend Image: ${BACKEND_IMAGE}${NC}"
docker build -t "$BACKEND_IMAGE" -f docker/backend.Dockerfile ./backend

echo -e "\n${YELLOW}Building Frontend Image: ${FRONTEND_IMAGE}${NC}"
docker build -t "$FRONTEND_IMAGE" -f docker/frontend.Dockerfile ./frontend

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}Build Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "Backend:  ${BACKEND_IMAGE}"
echo -e "Frontend: ${FRONTEND_IMAGE}"

# Push images if requested
if [ "$PUSH" == "--push" ]; then
    echo -e "\n${YELLOW}Pushing images to registry...${NC}"
    docker push "$BACKEND_IMAGE"
    docker push "$FRONTEND_IMAGE"
    echo -e "${GREEN}Push complete!${NC}"
fi

# For Minikube: load images into Minikube's Docker daemon
if command -v minikube &> /dev/null; then
    echo -e "\n${YELLOW}Tip: To use these images in Minikube, run:${NC}"
    echo -e "  eval \$(minikube docker-env)"
    echo -e "  ./scripts/build-images.sh"
    echo -e "\nOr load existing images:"
    echo -e "  minikube image load ${BACKEND_IMAGE}"
    echo -e "  minikube image load ${FRONTEND_IMAGE}"
fi
