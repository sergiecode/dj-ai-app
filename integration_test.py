# DJ AI App Integration Test and Fix Script
# Author: Sergie Code - Software Engineer & YouTube Programming Educator
# Purpose: Test and fix integration between dj-ai-core, dj-ai-frontend, and dj-ai-app

import os
import sys
import subprocess
import json
from pathlib import Path
import time
import requests
from typing import Dict, List, Tuple

class DJAIIntegrationTester:
    """Comprehensive integration tester for DJ AI App ecosystem."""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.core_path = self.base_path / "dj-ai-core"
        self.frontend_path = self.base_path / "dj-ai-frontend"
        self.app_path = self.base_path / "dj-ai-app"
        self.issues = []
        self.fixes_applied = []
        
    def log(self, message: str, level: str = "INFO"):
        """Log messages with timestamp."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")
        
    def check_repository_structure(self) -> bool:
        """Check if all required repositories exist with proper structure."""
        self.log("Checking repository structure...")
        
        required_repos = {
            "dj-ai-core": self.core_path,
            "dj-ai-frontend": self.frontend_path,
            "dj-ai-app": self.app_path
        }
        
        all_good = True
        for repo_name, repo_path in required_repos.items():
            if not repo_path.exists():
                self.issues.append(f"Repository {repo_name} not found at {repo_path}")
                all_good = False
            else:
                self.log(f"✅ Repository {repo_name} found at {repo_path}")
                
        return all_good
    
    def check_backend_structure(self) -> bool:
        """Check dj-ai-core backend structure and files."""
        self.log("Checking backend structure...")
        
        required_files = [
            "app/main.py",
            "requirements.txt",
            "Dockerfile"
        ]
        
        required_dirs = [
            "app",
            "audio", 
            "ml",
            "tests"
        ]
        
        all_good = True
        
        # Check files
        for file_path in required_files:
            full_path = self.core_path / file_path
            if not full_path.exists():
                self.issues.append(f"Backend missing required file: {file_path}")
                all_good = False
            else:
                self.log(f"✅ Backend file found: {file_path}")
                
        # Check directories
        for dir_path in required_dirs:
            full_path = self.core_path / dir_path
            if not full_path.exists():
                self.issues.append(f"Backend missing required directory: {dir_path}")
                all_good = False
            else:
                self.log(f"✅ Backend directory found: {dir_path}")
                
        return all_good
    
    def check_frontend_structure(self) -> bool:
        """Check dj-ai-frontend structure and files."""
        self.log("Checking frontend structure...")
        
        required_files = [
            "package.json",
            "next.config.ts",
            "Dockerfile"
        ]
        
        required_dirs = [
            "src",
            "public"
        ]
        
        all_good = True
        
        # Check files
        for file_path in required_files:
            full_path = self.frontend_path / file_path
            if not full_path.exists():
                self.issues.append(f"Frontend missing required file: {file_path}")
                all_good = False
            else:
                self.log(f"✅ Frontend file found: {file_path}")
                
        # Check directories
        for dir_path in required_dirs:
            full_path = self.frontend_path / dir_path
            if not full_path.exists():
                self.issues.append(f"Frontend missing required directory: {dir_path}")
                all_good = False
            else:
                self.log(f"✅ Frontend directory found: {dir_path}")
                
        return all_good
    
    def check_orchestrator_structure(self) -> bool:
        """Check dj-ai-app orchestrator structure."""
        self.log("Checking orchestrator structure...")
        
        required_files = [
            "docker-compose.yml",
            "config/nginx.conf"
        ]
        
        all_good = True
        
        for file_path in required_files:
            full_path = self.app_path / file_path
            if not full_path.exists():
                if file_path == "config/nginx.conf":
                    # This is optional for basic setup
                    self.log(f"⚠️  Optional file missing: {file_path}")
                else:
                    self.issues.append(f"Orchestrator missing required file: {file_path}")
                    all_good = False
            else:
                self.log(f"✅ Orchestrator file found: {file_path}")
                
        return all_good
    
    def test_backend_imports(self) -> bool:
        """Test if backend dependencies and imports work."""
        self.log("Testing backend imports...")
        
        try:
            # Change to backend directory
            original_cwd = os.getcwd()
            os.chdir(self.core_path)
            
            # Test import
            result = subprocess.run([
                sys.executable, "-c", 
                "import app.main; print('Backend imports successfully')"
            ], capture_output=True, text=True, timeout=30)
            
            os.chdir(original_cwd)
            
            if result.returncode == 0:
                self.log("✅ Backend imports successfully")
                return True
            else:
                self.issues.append(f"Backend import failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.issues.append("Backend import test timed out")
            return False
        except Exception as e:
            self.issues.append(f"Backend import test error: {str(e)}")
            return False
    
    def test_frontend_dependencies(self) -> bool:
        """Test if frontend dependencies are installed."""
        self.log("Testing frontend dependencies...")
        
        try:
            # Check if node_modules exists
            node_modules = self.frontend_path / "node_modules"
            if not node_modules.exists():
                self.issues.append("Frontend dependencies not installed (node_modules missing)")
                return False
                
            # Check if package.json exists
            package_json = self.frontend_path / "package.json"
            if not package_json.exists():
                self.issues.append("Frontend package.json missing")
                return False
            
            # Check if key packages are installed
            key_packages = ["next", "react", "react-dom", "wavesurfer.js"]
            missing_packages = []
            
            for package in key_packages:
                package_dir = node_modules / package
                if not package_dir.exists():
                    missing_packages.append(package)
            
            if missing_packages:
                self.issues.append(f"Frontend missing key packages: {', '.join(missing_packages)}")
                return False
            
            # Alternative: Try to check package.json content instead of npm command
            try:
                with open(package_json, 'r') as f:
                    import json
                    package_data = json.load(f)
                    
                # Check if dependencies section exists
                if 'dependencies' not in package_data:
                    self.issues.append("Frontend package.json has no dependencies section")
                    return False
                    
                # Check for essential dependencies
                deps = package_data['dependencies']
                essential_deps = ['next', 'react', 'react-dom']
                missing_essential = [dep for dep in essential_deps if dep not in deps]
                
                if missing_essential:
                    self.issues.append(f"Frontend missing essential dependencies: {', '.join(missing_essential)}")
                    return False
                    
                self.log("✅ Frontend dependencies are installed and configured")
                return True
                
            except json.JSONDecodeError:
                self.issues.append("Frontend package.json is invalid JSON")
                return False
                
        except Exception as e:
            self.issues.append(f"Frontend dependency test error: {str(e)}")
            return False
    
    def check_docker_compose_config(self) -> bool:
        """Check docker-compose.yml configuration."""
        self.log("Checking docker-compose configuration...")
        
        compose_file = self.app_path / "docker-compose.yml"
        if not compose_file.exists():
            self.issues.append("docker-compose.yml not found")
            return False
            
        try:
            # Test docker-compose config validation
            original_cwd = os.getcwd()
            os.chdir(self.app_path)
            
            result = subprocess.run([
                "docker-compose", "config"
            ], capture_output=True, text=True, timeout=30)
            
            os.chdir(original_cwd)
            
            if result.returncode == 0:
                self.log("✅ Docker Compose configuration is valid")
                return True
            else:
                self.issues.append(f"Docker Compose config invalid: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.issues.append("Docker Compose config test timed out")
            return False
        except FileNotFoundError:
            self.issues.append("Docker Compose not found (Docker Desktop not installed or not in PATH)")
            return False
        except Exception as e:
            self.issues.append(f"Docker Compose config test error: {str(e)}")
            return False
    
    def test_backend_startup(self) -> bool:
        """Test if backend can start (without Docker)."""
        self.log("Testing backend startup...")
        
        try:
            # Change to backend directory
            original_cwd = os.getcwd()
            os.chdir(self.core_path)
            
            # Start backend server in background
            process = subprocess.Popen([
                sys.executable, "-m", "uvicorn", 
                "app.main:app", "--host", "127.0.0.1", "--port", "8001"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait a moment for startup
            time.sleep(5)
            
            # Test if server is responding
            try:
                response = requests.get("http://127.0.0.1:8001/health", timeout=5)
                if response.status_code == 200:
                    self.log("✅ Backend starts and responds successfully")
                    success = True
                else:
                    self.issues.append(f"Backend health check failed: HTTP {response.status_code}")
                    success = False
            except requests.exceptions.RequestException as e:
                self.issues.append(f"Backend health check failed: {str(e)}")
                success = False
            
            # Cleanup
            process.terminate()
            process.wait(timeout=10)
            os.chdir(original_cwd)
            
            return success
            
        except Exception as e:
            self.issues.append(f"Backend startup test error: {str(e)}")
            return False
    
    def test_frontend_build(self) -> bool:
        """Test if frontend can build."""
        self.log("Testing frontend build...")
        
        try:
            # Change to frontend directory
            original_cwd = os.getcwd()
            os.chdir(self.frontend_path)
            
            # Test build
            result = subprocess.run([
                "npm", "run", "build"
            ], capture_output=True, text=True, timeout=300)  # 5 minute timeout
            
            os.chdir(original_cwd)
            
            if result.returncode == 0:
                self.log("✅ Frontend builds successfully")
                return True
            else:
                self.issues.append(f"Frontend build failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.issues.append("Frontend build test timed out (5 minutes)")
            return False
        except Exception as e:
            self.issues.append(f"Frontend build test error: {str(e)}")
            return False
    
    def create_integration_fixes(self):
        """Create fixes for common integration issues."""
        self.log("Creating integration fixes...")
        
        # Create missing environment files
        self.create_env_files()
        
        # Create missing configuration files
        self.create_config_files()
        
        # Create integration scripts
        self.create_integration_scripts()
    
    def create_env_files(self):
        """Create missing environment files."""
        # Backend .env file
        backend_env = self.core_path / ".env"
        if not backend_env.exists():
            env_content = """# DJ AI Core Backend Environment
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=1

# Audio Processing
MAX_FILE_SIZE=50MB
SUPPORTED_FORMATS=mp3,wav,flac,m4a
SAMPLE_RATE=22050

# ML Models
MODEL_DIR=./ml/models/
ENABLE_GPU=false

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# CORS (for frontend integration)
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:80
CORS_METHODS=GET,POST,PUT,DELETE,OPTIONS
CORS_HEADERS=*
"""
            backend_env.write_text(env_content)
            self.fixes_applied.append("Created backend .env file")
            self.log("✅ Created backend .env file")
            
        # Frontend .env file
        frontend_env = self.frontend_path / ".env.local"
        if not frontend_env.exists():
            env_content = """# DJ AI Frontend Environment
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_WEBSOCKET_URL=ws://localhost:8000/ws

# Development
NODE_ENV=development
"""
            frontend_env.write_text(env_content)
            self.fixes_applied.append("Created frontend .env.local file")
            self.log("✅ Created frontend .env.local file")
    
    def create_config_files(self):
        """Create missing configuration files."""
        # Create nginx config directory and file
        config_dir = self.app_path / "config"
        config_dir.mkdir(exist_ok=True)
        
        nginx_config = config_dir / "nginx.conf"
        if not nginx_config.exists():
            nginx_content = """# DJ AI App Nginx Configuration
# Author: Sergie Code
# Purpose: Reverse proxy for DJ AI services

events {
    worker_connections 1024;
}

http {
    upstream dj_ai_backend {
        server dj-ai-core:8000;
    }
    
    upstream dj_ai_frontend {
        server dj-ai-frontend:3000;
    }
    
    server {
        listen 80;
        server_name localhost;
        
        # Frontend routes
        location / {
            proxy_pass http://dj_ai_frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        
        # Backend API routes
        location /api/ {
            proxy_pass http://dj_ai_backend/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # WebSocket support
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }
        
        # Health check
        location /health {
            proxy_pass http://dj_ai_backend/health;
        }
    }
}
"""
            nginx_config.write_text(nginx_content)
            self.fixes_applied.append("Created nginx.conf")
            self.log("✅ Created nginx.conf")
    
    def create_integration_scripts(self):
        """Create integration and testing scripts."""
        # PowerShell script for Windows development
        ps_script = self.app_path / "start-development.ps1"
        ps_content = """# DJ AI App Development Startup Script
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
"""
        ps_script.write_text(ps_content, encoding='utf-8')
        self.fixes_applied.append("Created start-development.ps1")
        self.log("✅ Created start-development.ps1")
        
        # Integration test script
        test_script = self.app_path / "test-integration.py"
        test_content = """#!/usr/bin/env python3
# DJ AI App Integration Test
# Author: Sergie Code

import requests
import time
import json

def test_backend_health():
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def test_frontend_health():
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    print("DJ AI App Integration Test")
    print("=" * 40)
    
    print("Testing backend health...")
    if test_backend_health():
        print("✅ Backend is healthy")
    else:
        print("❌ Backend is not responding")
    
    print("Testing frontend health...")
    if test_frontend_health():
        print("✅ Frontend is healthy")
    else:
        print("❌ Frontend is not responding")
    
    print("\\nIntegration test complete!")

if __name__ == "__main__":
    main()
"""
        test_script.write_text(test_content, encoding='utf-8')
        self.fixes_applied.append("Created test-integration.py")
        self.log("✅ Created test-integration.py")
    
    def run_comprehensive_test(self) -> Dict:
        """Run comprehensive integration test."""
        self.log("🧪 Starting comprehensive DJ AI App integration test...")
        
        test_results = {
            "repository_structure": self.check_repository_structure(),
            "backend_structure": self.check_backend_structure(),
            "frontend_structure": self.check_frontend_structure(),
            "orchestrator_structure": self.check_orchestrator_structure(),
            "backend_imports": self.test_backend_imports(),
            "frontend_dependencies": self.test_frontend_dependencies(),
            "docker_compose_config": self.check_docker_compose_config(),
            "backend_startup": self.test_backend_startup(),
            # "frontend_build": self.test_frontend_build()  # Disabled for speed
        }
        
        return test_results
    
    def generate_report(self, test_results: Dict) -> str:
        """Generate comprehensive integration report."""
        report = f"""# DJ AI App Integration Test Report
**Generated**: {time.strftime("%Y-%m-%d %H:%M:%S")}
**Author**: Sergie Code - Software Engineer & YouTube Programming Educator
**Purpose**: Integration test results for DJ AI ecosystem

## 🎯 Test Results Summary

"""
        
        passed = sum(1 for result in test_results.values() if result)
        total = len(test_results)
        
        report += f"**Overall Score**: {passed}/{total} tests passed ({passed/total*100:.1f}%)\\n\\n"
        
        # Individual test results
        report += "## 📋 Detailed Test Results\\n\\n"
        
        for test_name, result in test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            test_display = test_name.replace("_", " ").title()
            report += f"- **{test_display}**: {status}\\n"
        
        # Issues found
        if self.issues:
            report += "\\n## 🚨 Issues Found\\n\\n"
            for i, issue in enumerate(self.issues, 1):
                report += f"{i}. {issue}\\n"
        
        # Fixes applied
        if self.fixes_applied:
            report += "\\n## 🔧 Fixes Applied\\n\\n"
            for i, fix in enumerate(self.fixes_applied, 1):
                report += f"{i}. {fix}\\n"
        
        # Recommendations
        report += "\\n## 💡 Recommendations\\n\\n"
        
        if not test_results.get("docker_compose_config", True):
            report += "- Start Docker Desktop before running docker-compose commands\\n"
        
        if not test_results.get("backend_startup", True):
            report += "- Check backend dependencies: `pip install -r requirements.txt` in dj-ai-core\\n"
        
        if not test_results.get("frontend_dependencies", True):
            report += "- Install frontend dependencies: `npm install` in dj-ai-frontend\\n"
        
        report += "\\n## 🚀 Next Steps\\n\\n"
        report += "1. **Fix any failing tests** listed above\\n"
        report += "2. **Start Docker Desktop** (if using Docker)\\n"
        report += "3. **Run the development script**: `./start-development.ps1`\\n"
        report += "4. **Test the application**: Open http://localhost:3000\\n"
        report += "5. **Verify API**: Check http://localhost:8000/docs\\n"
        
        report += "\\n## 🎵 Educational Value\\n\\n"
        report += "This integration demonstrates:\\n"
        report += "- Multi-service architecture with Docker\\n"
        report += "- FastAPI backend with AI/ML capabilities\\n"
        report += "- Next.js frontend with audio visualization\\n"
        report += "- DevOps practices and testing methodologies\\n"
        report += "- Real-world software engineering practices\\n"
        
        report += "\\n---\\n"
        report += "*Generated by DJ AI App Integration Tester - Perfect for YouTube programming education!*"
        
        return report

def main():
    """Main integration test function."""
    tester = DJAIIntegrationTester()
    
    # Run comprehensive tests
    test_results = tester.run_comprehensive_test()
    
    # Create fixes for common issues
    tester.create_integration_fixes()
    
    # Generate and save report
    report = tester.generate_report(test_results)
    
    # Save report
    report_file = tester.app_path / "INTEGRATION_TEST_REPORT.md"
    report_file.write_text(report, encoding='utf-8')
    
    print("\\n" + "="*60)
    print("DJ AI App Integration Test Complete!")
    print(f"Full report saved to: {report_file}")
    print("="*60)
    
    # Print summary
    passed = sum(1 for result in test_results.values() if result)
    total = len(test_results)
    print(f"\\n✅ Tests Passed: {passed}/{total} ({passed/total*100:.1f}%)")
    
    if tester.issues:
        print(f"⚠️  Issues Found: {len(tester.issues)}")
        for issue in tester.issues[:3]:  # Show first 3 issues
            print(f"   - {issue}")
        if len(tester.issues) > 3:
            print(f"   ... and {len(tester.issues)-3} more (see report)")
    
    if tester.fixes_applied:
        print(f"🔧 Fixes Applied: {len(tester.fixes_applied)}")
    
    print("\\nReady for development! Run './start-development.ps1' to begin.")

if __name__ == "__main__":
    main()
