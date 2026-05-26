# Cleanup Script for Netflix Scale Lab (PowerShell)

Write-Host "🛑 Starting cleanup of Netflix Scale Lab..." -ForegroundColor Red

# Delete Kubernetes resources
Write-Host "🧹 Deleting Kubernetes services and deployments..."
Write-Host "DEBUG: About to run: kubectl delete -f k8s/services/ --ignore-not-found"
kubectl delete -f k8s/services/ --ignore-not-found
Write-Host "DEBUG: About to run: kubectl delete -f k8s/infrastructure/ --ignore-not-found"
kubectl delete -f k8s/infrastructure/ --ignore-not-found

# Delete local Docker images (optional, commented out for safety)
# Write-Host "🐳 Removing Docker images..."
# docker rmi netflix-user-service:v1 netflix-catalog-service:v1 netflix-playback-service:v1 netflix-edge-cache:v1

# Remove log files and rotated logs for all services
Write-Host "🗑️ Removing service log files..."
$logPatterns = @(
    "services/catalog-service/*.log*",
    "services/playback-service/*.log*",
    "services/user-service/*.log*",
    "services/edge-cache/*.log*",
    "chaos/*.log*"
)
foreach ($pattern in $logPatterns) {
    Write-Host "DEBUG: About to run: Remove-Item $pattern"
    Get-ChildItem -Path $pattern -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
}

Write-Host "✅ Cleanup complete! Resources removed." -ForegroundColor Green
