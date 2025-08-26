# DJ AI App - Setup Script
# Author: Sergie Code
# Description: Initial setup for the DJ AI orchestrator project

Write-Host "🎵 DJ AI App - Initial Setup" -ForegroundColor Cyan
Write-Host "Author: Sergie Code - AI Tools for Musicians" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan

# Check prerequisites
Write-Host "Checking prerequisites..." -ForegroundColor Yellow

# Check Docker
try {
    docker version | Out-Null
    Write-Host "✓ Docker is installed" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker is not installed. Please install Docker Desktop." -ForegroundColor Red
    Write-Host "  Download from: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

# Check Docker Compose
try {
    docker-compose version | Out-Null
    Write-Host "✓ Docker Compose is available" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker Compose is not available." -ForegroundColor Red
    exit 1
}

# Check for required repositories
$requiredRepos = @("dj-ai-core", "dj-ai-frontend")
$missingRepos = @()

foreach ($repo in $requiredRepos) {
    $repoPath = Join-Path ".." $repo
    if (-not (Test-Path $repoPath)) {
        $missingRepos += $repo
    } else {
        Write-Host "✓ Found $repo repository" -ForegroundColor Green
    }
}

if ($missingRepos.Count -gt 0) {
    Write-Host ""
    Write-Host "✗ Missing required repositories:" -ForegroundColor Red
    foreach ($repo in $missingRepos) {
        Write-Host "  - $repo" -ForegroundColor Yellow
    }
    Write-Host ""
    Write-Host "Please clone the missing repositories:" -ForegroundColor Yellow
    foreach ($repo in $missingRepos) {
        Write-Host "  git clone https://github.com/sergiecode/$repo.git ../$repo" -ForegroundColor White
    }
    exit 1
}

# Create necessary directories
Write-Host ""
Write-Host "Creating data directories..." -ForegroundColor Yellow
$directories = @("data/uploads", "data/models", "config/ssl")
foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "✓ Created $dir" -ForegroundColor Green
    } else {
        Write-Host "✓ Directory $dir exists" -ForegroundColor Green
    }
}

# Copy environment file
Write-Host ""
Write-Host "Setting up environment configuration..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Copy-Item ".env.development" ".env"
    Write-Host "✓ Created .env from development template" -ForegroundColor Green
} else {
    Write-Host "✓ .env file already exists" -ForegroundColor Green
}

# Create sample audio files directory structure
Write-Host ""
Write-Host "Setting up sample data structure..." -ForegroundColor Yellow
$sampleDirs = @("data/uploads/samples", "data/uploads/user_tracks")
foreach ($dir in $sampleDirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "✓ Created $dir" -ForegroundColor Green
    }
}

# Create .gitkeep files for empty directories
$gitkeepDirs = @("data/uploads", "data/models", "data/uploads/samples", "data/uploads/user_tracks")
foreach ($dir in $gitkeepDirs) {
    $gitkeepPath = Join-Path $dir ".gitkeep"
    if (-not (Test-Path $gitkeepPath)) {
        New-Item -ItemType File -Path $gitkeepPath -Force | Out-Null
    }
}

Write-Host ""
Write-Host "🎉 Setup completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Start development: .\scripts\start-dev.ps1" -ForegroundColor White
Write-Host "  2. View services: docker-compose ps" -ForegroundColor White
Write-Host "  3. Check logs: docker-compose logs -f" -ForegroundColor White
Write-Host ""
Write-Host "Happy coding! 🎵💻" -ForegroundColor Cyan
