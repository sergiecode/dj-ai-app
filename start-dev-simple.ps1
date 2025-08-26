# DJ AI App - Development Startup Script (Simple Version)
# Author: Sergie Code - Software Engineer & YouTube Programming Educator
# Purpose: Start the complete DJ AI development environment
# Compatible with: Windows PowerShell 5.1+

param(
    [switch]$Docker,
    [switch]$Manual,
    [switch]$Help
)

if ($Help) {
    Write-Host "DJ AI App Development Startup Script" -ForegroundColor Green
    Write-Host "Author: Sergie Code" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Usage:" -ForegroundColor Cyan
    Write-Host "  .\start-dev-simple.ps1          # Auto-detect best method"
    Write-Host "  .\start-dev-simple.ps1 -Docker  # Force Docker Compose"
    Write-Host "  .\start-dev-simple.ps1 -Manual  # Force manual startup"
    Write-Host "  .\start-dev-simple.ps1 -Help    # Show this help"
    exit
}

Write-Host "==================================================" -ForegroundColor Green
Write-Host "    DJ AI App - Development Environment" -ForegroundColor Green
Write-Host "    Author: Sergie Code" -ForegroundColor Yellow
Write-Host "    AI Tools for Musicians" -ForegroundColor Yellow
Write-Host "==================================================" -ForegroundColor Green
Write-Host ""

# Check prerequisites
Write-Host "Checking prerequisites..." -ForegroundColor Blue

try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Python not found - Please install Python 3.12+" -ForegroundColor Red
    exit 1
}

try {
    $nodeVersion = node --version 2>&1
    Write-Host "Node.js: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "Node.js not found - Please install Node.js" -ForegroundColor Red
    exit 1
}

try {
    $dockerVersion = docker --version 2>&1
    Write-Host "Docker: $dockerVersion" -ForegroundColor Green
    
    try {
        docker info > $null 2>&1
        $dockerRunning = $true
        Write-Host "Docker is running" -ForegroundColor Green
    } catch {
        $dockerRunning = $false
        Write-Host "Docker not running" -ForegroundColor Yellow
    }
} catch {
    Write-Host "Docker not found" -ForegroundColor Yellow
    $dockerRunning = $false
}

Write-Host ""

# Determine startup method
if ($Docker) {
    $useDocker = $true
} elseif ($Manual) {
    $useDocker = $false
} else {
    $useDocker = $dockerRunning
}

if ($useDocker) {
    Write-Host "Starting with Docker Compose..." -ForegroundColor Cyan
    Write-Host ""
    
    try {
        docker compose up --build
    } catch {
        Write-Host "Docker Compose failed. Switching to manual startup..." -ForegroundColor Yellow
        $useDocker = $false
    }
}

if (-not $useDocker) {
    Write-Host "Starting services manually..." -ForegroundColor Cyan
    Write-Host ""
    
    Write-Host "Starting backend server..." -ForegroundColor Blue
    
    # Start backend
    Start-Process powershell -ArgumentList @("-NoExit", "-Command", "Write-Host 'Starting DJ AI Backend...' -ForegroundColor Green; cd '../dj-ai-core'; python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    
    Write-Host "Backend starting in separate window" -ForegroundColor Green
    Write-Host ""
    
    Start-Sleep -Seconds 3
    
    Write-Host "Starting frontend server..." -ForegroundColor Blue
    
    # Start frontend
    Start-Process powershell -ArgumentList @("-NoExit", "-Command", "Write-Host 'Starting DJ AI Frontend...' -ForegroundColor Green; cd '../dj-ai-frontend'; npm run dev")
    
    Write-Host "Frontend starting in separate window" -ForegroundColor Green
    Write-Host ""
}

# Wait and test services
Write-Host "Waiting for services to start..." -ForegroundColor Blue
Start-Sleep -Seconds 5

Write-Host ""
Write-Host "Testing service availability..." -ForegroundColor Blue

# Test backend
try {
    $backendResponse = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 5 -ErrorAction Stop
    Write-Host "Backend is responding (HTTP $($backendResponse.StatusCode))" -ForegroundColor Green
} catch {
    Write-Host "Backend not yet responding (may still be starting)" -ForegroundColor Yellow
}

# Test frontend
try {
    $frontendResponse = Invoke-WebRequest -Uri "http://localhost:3000" -TimeoutSec 5 -ErrorAction Stop
    Write-Host "Frontend is responding (HTTP $($frontendResponse.StatusCode))" -ForegroundColor Green
} catch {
    Write-Host "Frontend not yet responding (may still be starting)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "==================================================" -ForegroundColor Green
Write-Host "    DJ AI App Started Successfully!" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
Write-Host ""

Write-Host "Access your applications:" -ForegroundColor Cyan
Write-Host "   Frontend:     http://localhost:3000"
Write-Host "   Backend API:  http://localhost:8000"
Write-Host "   API Docs:     http://localhost:8000/docs"
Write-Host ""

Write-Host "Test the integration:" -ForegroundColor Cyan
Write-Host "   python test-integration.py"
Write-Host ""

Write-Host "Development ready for YouTube content!" -ForegroundColor Yellow
Write-Host "   - AI-powered DJ recommendations"
Write-Host "   - Real-time audio analysis"
Write-Host "   - Waveform visualization"
Write-Host "   - Professional software architecture"
Write-Host ""

Write-Host "Happy coding!" -ForegroundColor Green
Write-Host "- Sergie Code" -ForegroundColor Yellow
