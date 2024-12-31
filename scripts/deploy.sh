#!/usr/bin/env bash
# scripts/deploy.sh

# Example: Build Docker images, optionally push them to a registry, then launch with docker-compose.

set -e  # Exit on error
set -u  # Treat unset variables as errors

echo "Starting deployment process..."

# 1. Build Docker image
IMAGE_NAME="code-analyzer"
TAG="latest"

echo "Building Docker image: $IMAGE_NAME:$TAG"
docker build -t $IMAGE_NAME:$TAG .

# 2. Optional: Tag & push to a registry
# Uncomment if you have a registry:
# REGISTRY="your-registry.com/your-namespace"
# docker tag $IMAGE_NAME:$TAG $REGISTRY/$IMAGE_NAME:$TAG
# docker push $REGISTRY/$IMAGE_NAME:$TAG

# 3. Run docker-compose or other steps
echo "Launching with docker-compose..."
docker-compose up -d --build

echo "Deployment completed!"
