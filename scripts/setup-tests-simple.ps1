# DJ AI App - Test Setup Script (Simple)
# Author: Sergie Code

Write-Host "DJ AI App - Test Environment Setup" -ForegroundColor Cyan
Write-Host "Author: Sergie Code - AI Tools for Musicians" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "+ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "X Python not found. Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Check pip
try {
    pip --version | Out-Null
    Write-Host "+ pip is available" -ForegroundColor Green
} catch {
    Write-Host "X pip not found" -ForegroundColor Red
    exit 1
}

# Install test dependencies
Write-Host ""
Write-Host "Installing test dependencies..." -ForegroundColor Yellow
try {
    python -m pip install --upgrade pip
    python -m pip install -r requirements-test.txt
    Write-Host "+ Test dependencies installed" -ForegroundColor Green
} catch {
    Write-Host "X Failed to install test dependencies" -ForegroundColor Red
    exit 1
}

# Create necessary directories
Write-Host ""
Write-Host "Setting up test directories..." -ForegroundColor Yellow
$testDirs = @(
    "tests/fixtures/audio",
    "reports",
    "htmlcov"
)

foreach ($dir in $testDirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "+ Created $dir" -ForegroundColor Green
    } else {
        Write-Host "+ Directory $dir exists" -ForegroundColor Green
    }
}

# Verify pytest installation
Write-Host ""
Write-Host "Verifying pytest installation..." -ForegroundColor Yellow
try {
    $pytestVersion = python -m pytest --version
    Write-Host "+ $pytestVersion" -ForegroundColor Green
} catch {
    Write-Host "X Pytest verification failed" -ForegroundColor Red
    exit 1
}

# Check Docker (optional)
Write-Host ""
Write-Host "Checking Docker availability..." -ForegroundColor Yellow
try {
    docker version | Out-Null
    Write-Host "+ Docker is available" -ForegroundColor Green
} catch {
    Write-Host "! Docker not available. Integration tests may be skipped." -ForegroundColor Yellow
}

# Create test configuration
Write-Host ""
Write-Host "Creating test configuration..." -ForegroundColor Yellow

# Create .env.test if it doesn't exist
if (-not (Test-Path ".env.test")) {
    $testEnvContent = @"
# Test Environment Configuration
API_HOST=localhost
API_PORT=8000
FRONTEND_PORT=3000
TEST_TIMEOUT=60
LOG_LEVEL=DEBUG
"@
    Set-Content -Path ".env.test" -Value $testEnvContent
    Write-Host "+ Created .env.test" -ForegroundColor Green
} else {
    Write-Host "+ .env.test already exists" -ForegroundColor Green
}

Write-Host ""
Write-Host "Test environment setup completed!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Run all tests: .\scripts\run-tests.ps1" -ForegroundColor White
Write-Host "  2. Run unit tests only: .\scripts\run-tests.ps1 -TestType unit" -ForegroundColor White
Write-Host "  3. Run with coverage: .\scripts\run-tests.ps1 -Coverage" -ForegroundColor White
Write-Host "  4. Generate HTML report: .\scripts\run-tests.ps1 -Html" -ForegroundColor White
Write-Host ""
Write-Host "Happy testing!" -ForegroundColor Cyan
