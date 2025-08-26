# DJ AI App - Quick Commands Reference
# Author: Sergie Code
# Usage: Copy and paste commands into PowerShell

# ========================================
# SETUP COMMANDS
# ========================================

# Initial setup (run once)
.\scripts\setup.ps1

# Check prerequisites
docker --version
docker-compose --version

# ========================================
# DEVELOPMENT COMMANDS
# ========================================

# Start development environment
.\scripts\start-dev.ps1

# Start with build
.\scripts\start-dev.ps1 -Build

# Start with logs
.\scripts\start-dev.ps1 -Logs

# Start with clean rebuild
.\scripts\start-dev.ps1 -Clean -Build

# ========================================
# MONITORING COMMANDS
# ========================================

# Check service health
.\scripts\health-check.ps1

# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f dj-ai-core
docker-compose logs -f dj-ai-frontend

# Check running services
docker-compose ps

# ========================================
# PRODUCTION COMMANDS
# ========================================

# Start production environment
.\scripts\start-prod.ps1

# Start production with SSL
.\scripts\start-prod.ps1 -SSL

# Start production with monitoring
.\scripts\start-prod.ps1 -Monitor

# ========================================
# CLEANUP COMMANDS
# ========================================

# Stop services
.\scripts\stop.ps1

# Stop and clean
.\scripts\stop.ps1 -Clean

# Stop all containers
.\scripts\stop.ps1 -All

# Remove volumes
.\scripts\stop.ps1 -Volumes

# ========================================
# DEBUGGING COMMANDS
# ========================================

# Enter backend container
docker-compose exec dj-ai-core bash

# Enter frontend container
docker-compose exec dj-ai-frontend sh

# Check backend API directly
curl http://localhost:8000/health

# Check frontend
curl http://localhost:3000

# View Docker resources
docker system df

# Clean up Docker system
docker system prune -a --volumes

# ========================================
# TESTING COMMANDS
# ========================================

# Test API endpoints
Invoke-RestMethod -Uri "http://localhost:8000/health"
Invoke-RestMethod -Uri "http://localhost:8000"
Invoke-RestMethod -Uri "http://localhost:8000/supported-formats"

# Test file upload (example)
$file = Get-Item "sample.mp3"
$form = @{ file = $file }
Invoke-RestMethod -Uri "http://localhost:8000/analyze-track" -Method Post -Form $form

# ========================================
# MAINTENANCE COMMANDS
# ========================================

# Update images
docker-compose pull

# Rebuild images
docker-compose build --no-cache

# View image sizes
docker images | grep dj-ai

# Clean up unused images
docker image prune -f

# ========================================
# ENVIRONMENT SWITCHING
# ========================================

# Development mode
$env:COMPOSE_FILE = "docker-compose.yml;docker-compose.dev.yml"
docker-compose up -d

# Production mode
$env:COMPOSE_FILE = "docker-compose.yml;docker-compose.prod.yml"
docker-compose up -d

# Reset environment
Remove-Item Env:\COMPOSE_FILE
