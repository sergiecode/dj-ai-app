# DJ AI App - Stop and Cleanup Script
# Author: Sergie Code
# Description: Stops all services and optionally cleans up resources

param(
    [switch]$Clean,
    [switch]$All,
    [switch]$Volumes
)

Write-Host "🛑 DJ AI App - Stop Services" -ForegroundColor Red
Write-Host "Author: Sergie Code" -ForegroundColor Green
Write-Host "=========================" -ForegroundColor Red

if ($All) {
    Write-Host "Stopping all DJ AI containers..." -ForegroundColor Yellow
    docker stop $(docker ps -q --filter "name=dj-ai")
    docker rm $(docker ps -aq --filter "name=dj-ai")
} else {
    Write-Host "Stopping Docker Compose services..." -ForegroundColor Yellow
    docker-compose down
}

if ($Volumes) {
    Write-Host "Removing volumes..." -ForegroundColor Yellow
    docker-compose down -v
}

if ($Clean) {
    Write-Host "Cleaning up Docker resources..." -ForegroundColor Yellow
    docker system prune -f
    docker volume prune -f
    docker network prune -f
}

Write-Host "✓ Services stopped successfully!" -ForegroundColor Green
