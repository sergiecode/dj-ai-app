# DJ AI App - Development Startup Script
# Author: Sergie Code
# Description: Starts the full DJ AI system in development mode

param(
    [switch]$Build,
    [switch]$Logs,
    [switch]$Clean
)

Write-Host "🎵 DJ AI App - Development Startup" -ForegroundColor Cyan
Write-Host "Author: Sergie Code - AI Tools for Musicians" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan

# Set environment
$env:COMPOSE_FILE = "docker-compose.yml;docker-compose.dev.yml"
$env:COMPOSE_PROJECT_NAME = "dj-ai-app-dev"

# Check if Docker is running
Write-Host "Checking Docker status..." -ForegroundColor Yellow
try {
    docker version | Out-Null
    Write-Host "✓ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker is not running. Please start Docker Desktop." -ForegroundColor Red
    exit 1
}

# Clean up if requested
if ($Clean) {
    Write-Host "🧹 Cleaning up containers and volumes..." -ForegroundColor Yellow
    docker-compose down -v --remove-orphans
    docker system prune -f
}

# Build if requested or if images don't exist
if ($Build) {
    Write-Host "🔨 Building Docker images..." -ForegroundColor Yellow
    docker-compose build --no-cache
}

# Start services
Write-Host "🚀 Starting DJ AI services..." -ForegroundColor Yellow
try {
    if ($Logs) {
        docker-compose up --build
    } else {
        docker-compose up -d --build
        
        Write-Host "✓ Services started successfully!" -ForegroundColor Green
        Write-Host ""
        Write-Host "🌐 Service URLs:" -ForegroundColor Cyan
        Write-Host "  Frontend:  http://localhost:3000" -ForegroundColor White
        Write-Host "  Backend:   http://localhost:8000" -ForegroundColor White
        Write-Host "  API Docs:  http://localhost:8000/docs" -ForegroundColor White
        Write-Host "  Health:    http://localhost:8000/health" -ForegroundColor White
        Write-Host ""
        Write-Host "📊 View logs with: docker-compose logs -f" -ForegroundColor Yellow
        Write-Host "🛑 Stop services with: docker-compose down" -ForegroundColor Yellow
        Write-Host ""
        
        # Wait for services to be healthy
        Write-Host "⏳ Waiting for services to be ready..." -ForegroundColor Yellow
        $timeout = 120
        $elapsed = 0
        
        do {
            Start-Sleep -Seconds 5
            $elapsed += 5
            $health = docker-compose ps --format json | ConvertFrom-Json
            $allHealthy = $true
            
            foreach ($service in $health) {
                if ($service.Health -and $service.Health -ne "healthy") {
                    $allHealthy = $false
                }
            }
            
            if ($allHealthy) {
                Write-Host "✓ All services are healthy!" -ForegroundColor Green
                break
            }
            
            if ($elapsed -ge $timeout) {
                Write-Host "⚠️ Timeout waiting for services. Check logs: docker-compose logs" -ForegroundColor Yellow
                break
            }
            
            Write-Host "." -NoNewline -ForegroundColor Yellow
        } while ($true)
    }
} catch {
    Write-Host "✗ Error starting services: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🎉 DJ AI App is ready for development!" -ForegroundColor Green
Write-Host "Happy coding! 🎵💻" -ForegroundColor Cyan
