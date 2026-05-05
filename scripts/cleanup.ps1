# Cleanup Script for Netflix Scale Lab (PowerShell)

Write-Host "🛑 Starting cleanup of Netflix Scale Lab..." -ForegroundColor Red

# Delete Kubernetes resources
Write-Host "🧹 Deleting Kubernetes services and deployments..."
kubectl delete -f k8s/services/ --ignore-not-found
kubectl delete -f k8s/infrastructure/ --ignore-not-found

# Delete local Docker images (optional, commented out for safety)
# Write-Host "🐳 Removing Docker images..."
# docker rmi netflix-user-service:v1 netflix-catalog-service:v1 netflix-playback-service:v1 netflix-edge-cache:v1

Write-Host "✅ Cleanup complete! Resources removed." -ForegroundColor Green
