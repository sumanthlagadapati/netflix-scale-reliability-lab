#!/bin/bash

# Cleanup Script for Netflix Scale Lab (Bash)

echo "🛑 Starting cleanup of Netflix Scale Lab..."

# Delete Kubernetes resources
echo "🧹 Deleting Kubernetes services and deployments..."
kubectl delete -f k8s/services/ --ignore-not-found
kubectl delete -f k8s/infrastructure/ --ignore-not-found

echo "✅ Cleanup complete! Resources removed."
