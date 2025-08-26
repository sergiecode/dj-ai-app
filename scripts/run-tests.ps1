# DJ AI App - Test Runner Script
# Author: Sergie Code
# Purpose: Run comprehensive tests for the DJ AI orchestrator

param(
    [string]$TestType = "all",  # all, unit, integration, e2e
    [switch]$Coverage,
    [switch]$Html,
    [switch]$Verbose,
    [switch]$Fast,
    [switch]$Install
)

Write-Host "🧪 DJ AI App - Test Suite" -ForegroundColor Cyan
Write-Host "Author: Sergie Code - AI Tools for Musicians" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Cyan

# Install test dependencies if requested
if ($Install) {
    Write-Host "📦 Installing test dependencies..." -ForegroundColor Yellow
    try {
        python -m pip install -r requirements-test.txt
        Write-Host "✓ Test dependencies installed successfully" -ForegroundColor Green
    } catch {
        Write-Host "✗ Failed to install test dependencies: $_" -ForegroundColor Red
        exit 1
    }
}

# Check if pytest is available
try {
    python -m pytest --version | Out-Null
    Write-Host "✓ Pytest is available" -ForegroundColor Green
} catch {
    Write-Host "✗ Pytest not found. Install with: pip install -r requirements-test.txt" -ForegroundColor Red
    exit 1
}

# Create reports directory
if (-not (Test-Path "reports")) {
    New-Item -ItemType Directory -Path "reports" -Force | Out-Null
    Write-Host "✓ Created reports directory" -ForegroundColor Green
}

# Build pytest command
$pytestArgs = @()

# Test selection based on type
switch ($TestType.ToLower()) {
    "unit" {
        $pytestArgs += "tests/unit"
        Write-Host "🔬 Running unit tests only" -ForegroundColor Yellow
    }
    "integration" {
        $pytestArgs += "tests/integration"
        Write-Host "🔗 Running integration tests only" -ForegroundColor Yellow
    }
    "e2e" {
        $pytestArgs += "tests/e2e"
        Write-Host "🌐 Running end-to-end tests only" -ForegroundColor Yellow
    }
    "all" {
        $pytestArgs += "tests"
        Write-Host "🚀 Running all tests" -ForegroundColor Yellow
    }
    default {
        Write-Host "❌ Invalid test type. Use: unit, integration, e2e, or all" -ForegroundColor Red
        exit 1
    }
}

# Add marker filters for fast mode
if ($Fast) {
    $pytestArgs += "-m"
    $pytestArgs += "not slow"
    Write-Host "⚡ Fast mode: Skipping slow tests" -ForegroundColor Yellow
}

# Add verbose flag
if ($Verbose) {
    $pytestArgs += "-vv"
}

# Add coverage if requested
if ($Coverage) {
    $pytestArgs += "--cov=."
    $pytestArgs += "--cov-report=term-missing"
    Write-Host "📊 Coverage reporting enabled" -ForegroundColor Yellow
}

# Add HTML report if requested
if ($Html) {
    $pytestArgs += "--html=reports/test_report.html"
    $pytestArgs += "--self-contained-html"
    Write-Host "📄 HTML report will be generated" -ForegroundColor Yellow
}

# Check if Docker services are needed
if ($TestType -in @("integration", "e2e", "all")) {
    Write-Host "🐳 Checking Docker services..." -ForegroundColor Yellow
    
    try {
        docker version | Out-Null
        Write-Host "✓ Docker is running" -ForegroundColor Green
    } catch {
        Write-Host "⚠️ Docker not running. Some tests may be skipped." -ForegroundColor Yellow
    }
    
    # Check if services are running
    try {
        $services = docker-compose ps --format json | ConvertFrom-Json
        if ($services) {
            Write-Host "✓ Docker Compose services detected" -ForegroundColor Green
        } else {
            Write-Host "⚠️ No Docker Compose services running. Starting services..." -ForegroundColor Yellow
            & ".\scripts\start-dev.ps1"
            Start-Sleep -Seconds 10
        }
    } catch {
        Write-Host "⚠️ Could not check Docker Compose services" -ForegroundColor Yellow
    }
}

# Run tests
Write-Host ""
Write-Host "🏃‍♂️ Running tests..." -ForegroundColor Cyan
try {
    $startTime = Get-Date
    
    # Execute pytest with arguments
    python -m pytest @pytestArgs
    
    $endTime = Get-Date
    $duration = $endTime - $startTime
    
    Write-Host ""
    Write-Host "✅ Tests completed successfully!" -ForegroundColor Green
    Write-Host "⏱️ Duration: $($duration.ToString('mm\:ss'))" -ForegroundColor White
    
    # Show report locations
    if ($Html) {
        Write-Host "📄 HTML Report: reports/test_report.html" -ForegroundColor Cyan
    }
    
    if ($Coverage) {
        Write-Host "📊 Coverage Report: htmlcov/index.html" -ForegroundColor Cyan
    }
    
} catch {
    Write-Host ""
    Write-Host "❌ Tests failed!" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🎉 Test run completed!" -ForegroundColor Green
Write-Host "Happy coding! 🎵💻" -ForegroundColor Cyan
