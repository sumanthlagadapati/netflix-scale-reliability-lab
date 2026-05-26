#!/bin/bash

# Cleanup Script for Netflix Scale Lab (Bash)

echo "🛑 Starting cleanup of Netflix Scale Lab..."

# Delete Kubernetes resources
echo "🧹 Deleting Kubernetes services and deployments..."
echo "DEBUG: About to run: kubectl delete -f k8s/services/ --ignore-not-found"
kubectl delete -f k8s/services/ --ignore-not-found
echo "DEBUG: About to run: kubectl delete -f k8s/infrastructure/ --ignore-not-found"
kubectl delete -f k8s/infrastructure/ --ignore-not-found

# Remove log files and rotated logs for all services
echo "🗑️ Removing service log files..."
echo "DEBUG: About to run: rm -f services/catalog-service/*.log*"
rm -f services/catalog-service/*.log*
echo "DEBUG: About to run: rm -f services/playback-service/*.log*"
rm -f services/playback-service/*.log*
echo "DEBUG: About to run: rm -f services/user-service/*.log*"
rm -f services/user-service/*.log*
echo "DEBUG: About to run: rm -f services/edge-cache/*.log*"
rm -f services/edge-cache/*.log*
echo "DEBUG: About to run: rm -f chaos/*.log*"
rm -f chaos/*.log*

echo "✅ Cleanup complete! Resources removed."
