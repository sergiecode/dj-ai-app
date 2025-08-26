# DJ AI App Development Startup Script
# Author: Sergie Code
# Purpose: Start all DJ AI services for development

Write-Host "Starting DJ AI App Development Environment" -ForegroundColor Green
Write-Host "Author: Sergie Code - Software Engineer & YouTube Programming Educator" -ForegroundColor Yellow

# Check prerequisites
Write-Host "Checking prerequisites..." -ForegroundColor Blue

# Check Docker
try {
    docker --version | Out-Null
    Write-Host "✅ Docker is available" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker not found. Please install Docker Desktop." -ForegroundColor Red
    exit 1
}

# Check Node.js
try {
    node --version | Out-Null
    Write-Host "✅ Node.js is available" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js not found. Please install Node.js." -ForegroundColor Red
    exit 1
}

# Check Python
try {
    python --version | Out-Null
    Write-Host "✅ Python is available" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.12+." -ForegroundColor Red
    exit 1
}

# Start services
Write-Host "Starting DJ AI services..." -ForegroundColor Blue

# Option 1: Docker Compose (recommended)
Write-Host "Option 1: Starting with Docker Compose" -ForegroundColor Cyan
docker-compose up --build

# If Docker fails, provide manual startup instructions
if ($LASTEXITCODE -ne 0) {
    Write-Host "Docker Compose failed. Starting services manually..." -ForegroundColor Yellow
    
    Write-Host "Starting backend..." -ForegroundColor Blue
    Start-Process powershell -ArgumentList "-Command", "cd ../dj-ai-core; python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
    
    Write-Host "Starting frontend..." -ForegroundColor Blue
    Start-Process powershell -ArgumentList "-Command", "cd ../dj-ai-frontend; npm run dev"
    
    Write-Host "Services started manually. Check separate terminal windows." -ForegroundColor Green
    Write-Host "Backend: http://localhost:8000" -ForegroundColor Cyan
    Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan
}
