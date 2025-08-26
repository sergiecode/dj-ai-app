# DJ AI App - Production Startup Script
# Author: Sergie Code
# Description: Starts the full DJ AI system in production mode

param(
    [switch]$Build,
    [switch]$SSL,
    [switch]$Monitor
)

Write-Host "🎵 DJ AI App - Production Deployment" -ForegroundColor Cyan
Write-Host "Author: Sergie Code - AI Tools for Musicians" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan

# Set environment
$env:COMPOSE_FILE = "docker-compose.yml;docker-compose.prod.yml"
$env:COMPOSE_PROJECT_NAME = "dj-ai-app-prod"

# Check if Docker is running
Write-Host "Checking Docker status..." -ForegroundColor Yellow
try {
    docker version | Out-Null
    Write-Host "✓ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker is not running. Please start Docker Desktop." -ForegroundColor Red
    exit 1
}

# Build if requested
if ($Build) {
    Write-Host "🔨 Building production images..." -ForegroundColor Yellow
    docker-compose build --no-cache
}

# SSL Configuration
if ($SSL) {
    Write-Host "🔒 Configuring SSL..." -ForegroundColor Yellow
    if (-not (Test-Path "config/ssl")) {
        New-Item -ItemType Directory -Path "config/ssl" -Force
    }
    
    # Generate self-signed certificate if none exists
    if (-not (Test-Path "config/ssl/cert.pem")) {
        Write-Host "Generating self-signed SSL certificate..." -ForegroundColor Yellow
        openssl req -x509 -newkey rsa:4096 -keyout config/ssl/key.pem -out config/ssl/cert.pem -days 365 -nodes -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
    }
}

# Start services
Write-Host "🚀 Starting production services..." -ForegroundColor Yellow
try {
    docker-compose up -d --build
    
    Write-Host "✓ Production services started!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🌐 Production URLs:" -ForegroundColor Cyan
    Write-Host "  Application: http://localhost" -ForegroundColor White
    if ($SSL) {
        Write-Host "  Secure:      https://localhost" -ForegroundColor White
    }
    Write-Host "  Health:      http://localhost/health" -ForegroundColor White
    Write-Host ""
    
    # Monitor if requested
    if ($Monitor) {
        Write-Host "📊 Monitoring services..." -ForegroundColor Yellow
        docker-compose logs -f
    } else {
        Write-Host "📊 View logs with: docker-compose logs -f" -ForegroundColor Yellow
        Write-Host "🛑 Stop services with: docker-compose down" -ForegroundColor Yellow
    }
    
} catch {
    Write-Host "✗ Error starting production services: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🎉 DJ AI App is running in production mode!" -ForegroundColor Green
