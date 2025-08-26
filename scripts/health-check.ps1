# DJ AI App - Health Check Script
# Author: Sergie Code
# Description: Checks the health of all services

Write-Host "🏥 DJ AI App - Health Check" -ForegroundColor Cyan
Write-Host "Author: Sergie Code" -ForegroundColor Green
Write-Host "=========================" -ForegroundColor Cyan

# Check Docker
Write-Host "Checking Docker..." -ForegroundColor Yellow
try {
    docker version | Out-Null
    Write-Host "✓ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker is not running" -ForegroundColor Red
    exit 1
}

# Check services
Write-Host "`nChecking services..." -ForegroundColor Yellow
$services = docker-compose ps --format json | ConvertFrom-Json

if ($services) {
    foreach ($service in $services) {
        $name = $service.Name
        $status = $service.State
        $health = $service.Health
        
        Write-Host "Service: $name" -ForegroundColor White
        
        if ($status -eq "running") {
            Write-Host "  Status: ✓ Running" -ForegroundColor Green
        } else {
            Write-Host "  Status: ✗ $status" -ForegroundColor Red
        }
        
        if ($health) {
            if ($health -eq "healthy") {
                Write-Host "  Health: ✓ Healthy" -ForegroundColor Green
            } else {
                Write-Host "  Health: ⚠️ $health" -ForegroundColor Yellow
            }
        }
        Write-Host ""
    }
} else {
    Write-Host "No services found. Run start-dev.ps1 or start-prod.ps1 first." -ForegroundColor Yellow
}

# Check endpoints
Write-Host "Checking endpoints..." -ForegroundColor Yellow

$endpoints = @(
    @{ Name = "Backend Health"; Url = "http://localhost:8000/health" },
    @{ Name = "Backend API"; Url = "http://localhost:8000" },
    @{ Name = "Frontend"; Url = "http://localhost:3000" },
    @{ Name = "API Documentation"; Url = "http://localhost:8000/docs" }
)

foreach ($endpoint in $endpoints) {
    try {
        $response = Invoke-WebRequest -Uri $endpoint.Url -TimeoutSec 5 -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-Host "✓ $($endpoint.Name): Available" -ForegroundColor Green
        } else {
            Write-Host "⚠️ $($endpoint.Name): Status $($response.StatusCode)" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "✗ $($endpoint.Name): Not available" -ForegroundColor Red
    }
}

Write-Host "`n🎉 Health check completed!" -ForegroundColor Green
