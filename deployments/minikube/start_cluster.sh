#!/bin/bash

# Start cluster
minikube start

# Build local Docker images
eval $(minikube -p minikube docker-env)
docker compose build

# Load Kubernetes services and deployments
minikube kubectl -- apply -f deployments/minikube/enc-server-py-db.yaml
minikube kubectl -- apply -f deployments/minikube/enc-server-py-be.yaml
minikube kubectl -- apply -f deployments/minikube/enc-server-py-fe.yaml
