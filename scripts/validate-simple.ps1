# DJ AI App - System Validation Script
# Author: Sergie Code
# Purpose: Comprehensive validation of the DJ AI orchestrator system

param(
    [switch]$Quick,
    [switch]$Repair,
    [switch]$Verbose
)

Write-Host "DJ AI App - System Validation" -ForegroundColor Cyan
Write-Host "Author: Sergie Code - AI Tools for Musicians" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Cyan

$global:issues = @()
$global:warnings = @()

function Add-Issue($message) {
    $global:issues += $message
    Write-Host "X $message" -ForegroundColor Red
}

function Add-Warning($message) {
    $global:warnings += $message
    Write-Host "! $message" -ForegroundColor Yellow
}

function Test-Success($message) {
    Write-Host "+ $message" -ForegroundColor Green
}

function Test-Section($title) {
    Write-Host ""
    Write-Host "--- $title ---" -ForegroundColor Cyan
}

# 1. Prerequisites Check
Test-Section "Prerequisites Validation"

# Check Docker
try {
    $dockerVersion = docker --version
    Test-Success "Docker installed: $dockerVersion"
} catch {
    Add-Issue "Docker not installed or not accessible"
    if ($Repair) {
        Write-Host "Install Docker Desktop from: https://www.docker.com/products/docker-desktop" -ForegroundColor Blue
    }
}

# Check Docker Compose
try {
    $composeVersion = docker-compose --version
    Test-Success "Docker Compose available: $composeVersion"
} catch {
    Add-Issue "Docker Compose not available"
}

# Check Python (for testing)
try {
    $pythonVersion = python --version
    Test-Success "Python available: $pythonVersion"
} catch {
    Add-Warning "Python not available (testing will be limited)"
}

# 2. File Structure Validation
Test-Section "Project Structure Validation"

$requiredFiles = @(
    "docker-compose.yml",
    "docker-compose.dev.yml",
    "docker-compose.prod.yml",
    ".env.development",
    ".env.production",
    "config/nginx.conf",
    "README.md",
    "scripts/setup.ps1",
    "scripts/start-dev.ps1",
    "scripts/start-prod.ps1",
    "scripts/health-check.ps1",
    "scripts/stop.ps1"
)

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Test-Success "Required file exists: $file"
    } else {
        Add-Issue "Missing required file: $file"
        if ($Repair) {
            Write-Host "This file should be recreated" -ForegroundColor Blue
        }
    }
}

$requiredDirs = @(
    "config",
    "scripts", 
    "data",
    "data/uploads",
    "data/models",
    "tests"
)

foreach ($dir in $requiredDirs) {
    if (Test-Path $dir) {
        Test-Success "Required directory exists: $dir"
    } else {
        Add-Issue "Missing required directory: $dir"
        if ($Repair) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
            Test-Success "Created directory: $dir"
        }
    }
}

# 3. Configuration File Validation
Test-Section "Configuration Files Validation"

# Check environment files
$envFiles = @(".env.development", ".env.production")
foreach ($envFile in $envFiles) {
    if (Test-Path $envFile) {
        $content = Get-Content $envFile -Raw
        
        # Check for required variables
        $requiredVars = @("API_HOST", "API_PORT", "CORS_ORIGINS", "REACT_APP_API_URL")
        $missingVars = @()
        
        foreach ($var in $requiredVars) {
            if ($content -notmatch $var) {
                $missingVars += $var
            }
        }
        
        if ($missingVars.Count -eq 0) {
            Test-Success "Environment file valid: $envFile"
        } else {
            Add-Warning "Missing variables in $envFile`: $($missingVars -join ', ')"
        }
    }
}

# 4. Docker Configuration Validation  
Test-Section "Docker Configuration Validation"

if (Test-Path "docker-compose.yml") {
    try {
        $composeResult = docker-compose config 2>&1
        if ($LASTEXITCODE -eq 0) {
            Test-Success "Docker Compose configuration is valid"
        } else {
            Add-Issue "Docker Compose configuration error: $composeResult"
        }
    } catch {
        Add-Warning "Could not validate Docker Compose configuration"
    }
}

# 5. Service Dependency Validation
Test-Section "Service Dependencies Validation"

# Check if required repositories exist
$repoPath = Split-Path -Parent (Get-Location)
$requiredRepos = @("dj-ai-core", "dj-ai-frontend")

foreach ($repo in $requiredRepos) {
    $repoFullPath = Join-Path $repoPath $repo
    if (Test-Path $repoFullPath) {
        Test-Success "Required repository found: $repo"
    } else {
        Add-Issue "Required repository missing: $repo"
        if ($Repair) {
            Write-Host "Clone with: git clone https://github.com/sergiecode/$repo.git ../$repo" -ForegroundColor Blue
        }
    }
}

# 6. Quick Service Test (if not quick mode)
if (-not $Quick) {
    Test-Section "Service Connectivity Test"
    
    # Check if services are running
    try {
        $services = docker-compose ps --format json 2>$null | ConvertFrom-Json
        
        if ($services) {
            Test-Success "Docker Compose services detected"
            
            # Test basic connectivity
            try {
                $backendTest = Invoke-RestMethod -Uri "http://localhost:8000/health" -TimeoutSec 5 -ErrorAction SilentlyContinue
                Test-Success "Backend health check successful"
            } catch {
                Add-Warning "Backend not responding (services may not be started)"
            }
            
            try {
                $frontendTest = Invoke-WebRequest -Uri "http://localhost:3000" -TimeoutSec 5 -UseBasicParsing -ErrorAction SilentlyContinue
                Test-Success "Frontend accessibility confirmed"
            } catch {
                Add-Warning "Frontend not responding (services may not be started)"
            }
        } else {
            Add-Warning "No Docker services running. Use .\scripts\start-dev.ps1 to start services"
        }
    } catch {
        Add-Warning "Could not check service status"
    }
}

# Summary
Test-Section "Validation Summary"

Write-Host ""
if ($global:issues.Count -eq 0 -and $global:warnings.Count -eq 0) {
    Write-Host "All validations passed! System is ready." -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Start development: .\scripts\start-dev.ps1" -ForegroundColor White
    Write-Host "  2. Run tests: .\scripts\run-tests.ps1" -ForegroundColor White
    Write-Host "  3. Check health: .\scripts\health-check.ps1" -ForegroundColor White
} else {
    if ($global:issues.Count -gt 0) {
        Write-Host "Critical Issues Found:" -ForegroundColor Red
        foreach ($issue in $global:issues) {
            Write-Host "   • $issue" -ForegroundColor Red
        }
    }
    
    if ($global:warnings.Count -gt 0) {
        Write-Host "Warnings:" -ForegroundColor Yellow
        foreach ($warning in $global:warnings) {
            Write-Host "   • $warning" -ForegroundColor Yellow
        }
    }
    
    Write-Host ""
    if ($global:issues.Count -gt 0) {
        Write-Host "Please resolve critical issues before proceeding." -ForegroundColor Red
        Write-Host "Run with -Repair flag to attempt automatic fixes." -ForegroundColor Blue
    } else {
        Write-Host "No critical issues. Warnings can be addressed later." -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "Happy coding!" -ForegroundColor Cyan
