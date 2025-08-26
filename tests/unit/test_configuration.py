# DJ AI App - Unit Tests
# Author: Sergie Code
# Purpose: Unit tests for individual components and configurations

import pytest
import yaml
import json
import os
from pathlib import Path

class TestDockerComposeConfiguration:
    """Test Docker Compose configuration files."""
    
    def test_main_docker_compose_structure(self):
        """Test the main docker-compose.yml structure."""
        compose_file = Path("docker-compose.yml")
        assert compose_file.exists(), "docker-compose.yml not found"
        
        with open(compose_file, 'r') as f:
            compose_data = yaml.safe_load(f)
        
        # Test structure
        assert "version" in compose_data
        assert "services" in compose_data
        assert "networks" in compose_data
        
        # Test required services
        services = compose_data["services"]
        assert "dj-ai-core" in services
        assert "dj-ai-frontend" in services
        
        # Test backend service configuration
        backend = services["dj-ai-core"]
        assert "build" in backend
        assert "ports" in backend
        assert "environment" in backend
        assert "healthcheck" in backend
        
        # Test frontend service configuration
        frontend = services["dj-ai-frontend"]
        assert "build" in frontend
        assert "ports" in frontend
        assert "depends_on" in frontend
    
    def test_development_docker_compose_override(self):
        """Test the development Docker Compose override."""
        dev_file = Path("docker-compose.dev.yml")
        assert dev_file.exists(), "docker-compose.dev.yml not found"
        
        with open(dev_file, 'r') as f:
            dev_data = yaml.safe_load(f)
        
        assert "version" in dev_data
        assert "services" in dev_data
        
        # Test development-specific configurations
        services = dev_data["services"]
        if "dj-ai-core" in services:
            backend = services["dj-ai-core"]
            # Should have development-specific environment
            if "environment" in backend:
                env_vars = backend["environment"]
                # Look for debug-related variables
                debug_vars = [var for var in env_vars if "DEBUG" in str(var) or "LOG_LEVEL" in str(var)]
                assert len(debug_vars) > 0, "No debug configuration found in development override"
    
    def test_production_docker_compose_override(self):
        """Test the production Docker Compose override."""
        prod_file = Path("docker-compose.prod.yml")
        assert prod_file.exists(), "docker-compose.prod.yml not found"
        
        with open(prod_file, 'r') as f:
            prod_data = yaml.safe_load(f)
        
        assert "version" in prod_data
        assert "services" in prod_data


class TestEnvironmentConfiguration:
    """Test environment configuration files."""
    
    def test_development_environment_file(self):
        """Test development environment configuration."""
        env_file = Path(".env.development")
        assert env_file.exists(), ".env.development not found"
        
        with open(env_file, 'r') as f:
            content = f.read()
        
        # Test required environment variables
        required_vars = [
            "API_HOST",
            "API_PORT",
            "CORS_ORIGINS",
            "REACT_APP_API_URL",
            "NODE_ENV"
        ]
        
        for var in required_vars:
            assert var in content, f"Required environment variable {var} not found"
        
        # Test development-specific values
        assert "NODE_ENV=development" in content
        assert "localhost" in content
    
    def test_production_environment_file(self):
        """Test production environment configuration."""
        env_file = Path(".env.production")
        assert env_file.exists(), ".env.production not found"
        
        with open(env_file, 'r') as f:
            content = f.read()
        
        # Test required environment variables
        required_vars = [
            "API_HOST",
            "API_PORT",
            "API_WORKERS",
            "NODE_ENV"
        ]
        
        for var in required_vars:
            assert var in content, f"Required environment variable {var} not found"
        
        # Test production-specific values
        assert "NODE_ENV=production" in content


class TestNginxConfiguration:
    """Test Nginx configuration."""
    
    def test_nginx_config_exists(self):
        """Test that Nginx configuration file exists."""
        nginx_config = Path("config/nginx.conf")
        assert nginx_config.exists(), "nginx.conf not found"
    
    def test_nginx_config_structure(self):
        """Test Nginx configuration structure."""
        nginx_config = Path("config/nginx.conf")
        
        with open(nginx_config, 'r') as f:
            content = f.read()
        
        # Test required sections
        assert "events {" in content
        assert "http {" in content
        assert "server {" in content
        
        # Test upstream configurations
        assert "upstream dj-ai-backend" in content
        assert "upstream dj-ai-frontend" in content
        
        # Test rate limiting
        assert "limit_req_zone" in content
        
        # Test location blocks
        assert "location /" in content
        assert "location /api/" in content
        
        # Test security headers
        assert "add_header" in content


class TestProjectStructure:
    """Test project directory structure."""
    
    def test_required_directories(self):
        """Test that all required directories exist."""
        required_dirs = [
            "config",
            "scripts",
            "data",
            "data/uploads",
            "data/models",
            "tests",
            "tests/integration",
            "tests/unit",
            "tests/e2e",
            "tests/fixtures"
        ]
        
        for dir_path in required_dirs:
            assert Path(dir_path).exists(), f"Required directory {dir_path} not found"
    
    def test_required_files(self):
        """Test that all required files exist."""
        required_files = [
            "README.md",
            "docker-compose.yml",
            "docker-compose.dev.yml", 
            "docker-compose.prod.yml",
            ".env.development",
            ".env.production",
            ".gitignore",
            ".dockerignore",
            "config/nginx.conf",
            "CHANGELOG.md",
            "COMMANDS.md"
        ]
        
        for file_path in required_files:
            assert Path(file_path).exists(), f"Required file {file_path} not found"
    
    def test_gitkeep_files(self):
        """Test that .gitkeep files exist in empty directories."""
        gitkeep_dirs = [
            "data/uploads",
            "data/models"
        ]
        
        for dir_path in gitkeep_dirs:
            gitkeep_file = Path(dir_path) / ".gitkeep"
            assert gitkeep_file.exists(), f".gitkeep file missing in {dir_path}"


class TestScriptFiles:
    """Test PowerShell script files."""
    
    def test_script_files_exist(self):
        """Test that all script files exist."""
        script_files = [
            "scripts/setup.ps1",
            "scripts/start-dev.ps1",
            "scripts/start-prod.ps1",
            "scripts/stop.ps1",
            "scripts/health-check.ps1"
        ]
        
        for script_file in script_files:
            assert Path(script_file).exists(), f"Script file {script_file} not found"
    
    def test_script_permissions(self):
        """Test that script files are readable."""
        script_files = [
            "scripts/setup.ps1",
            "scripts/start-dev.ps1",
            "scripts/start-prod.ps1",
            "scripts/stop.ps1",
            "scripts/health-check.ps1"
        ]
        
        for script_file in script_files:
            script_path = Path(script_file)
            assert script_path.is_file(), f"Script {script_file} is not a file"
            assert os.access(script_path, os.R_OK), f"Script {script_file} is not readable"
    
    def test_script_content_structure(self):
        """Test basic structure of PowerShell scripts."""
        script_files = [
            "scripts/setup.ps1",
            "scripts/start-dev.ps1", 
            "scripts/health-check.ps1"
        ]
        
        for script_file in script_files:
            with open(script_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Test that scripts have author attribution
            assert "Sergie Code" in content, f"Script {script_file} missing author attribution"
            
            # Test that scripts have proper PowerShell syntax indicators
            assert any(indicator in content for indicator in ["param(", "Write-Host", "$"]), \
                f"Script {script_file} doesn't appear to be a valid PowerShell script"


class TestDocumentationFiles:
    """Test documentation files."""
    
    def test_readme_structure(self):
        """Test README.md structure."""
        readme_file = Path("README.md")
        assert readme_file.exists(), "README.md not found"
        
        with open(readme_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Test required sections
        required_sections = [
            "# DJ AI App",
            "## 🎯 Project Overview",
            "## 🚀 Quick Start",
            "## 🏗️ System Architecture",
            "Sergie Code"
        ]
        
        for section in required_sections:
            assert section in content, f"Required section '{section}' not found in README"
    
    def test_changelog_structure(self):
        """Test CHANGELOG.md structure."""
        changelog_file = Path("CHANGELOG.md")
        assert changelog_file.exists(), "CHANGELOG.md not found"
        
        with open(changelog_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Test changelog format
        assert "# Changelog" in content
        assert "[1.0.0]" in content
        assert "Sergie Code" in content
    
    def test_commands_reference(self):
        """Test COMMANDS.md reference file."""
        commands_file = Path("COMMANDS.md")
        assert commands_file.exists(), "COMMANDS.md not found"
        
        with open(commands_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Test required command categories
        required_sections = [
            "SETUP COMMANDS",
            "DEVELOPMENT COMMANDS", 
            "MONITORING COMMANDS",
            "CLEANUP COMMANDS"
        ]
        
        for section in required_sections:
            assert section in content, f"Required command section '{section}' not found"


class TestConfigurationValidation:
    """Test configuration file validation."""
    
    def test_docker_compose_yaml_syntax(self):
        """Test that Docker Compose files have valid YAML syntax."""
        compose_files = [
            "docker-compose.yml",
            "docker-compose.dev.yml",
            "docker-compose.prod.yml"
        ]
        
        for compose_file in compose_files:
            file_path = Path(compose_file)
            assert file_path.exists(), f"Compose file {compose_file} not found"
            
            with open(file_path, 'r') as f:
                try:
                    yaml.safe_load(f)
                except yaml.YAMLError as e:
                    pytest.fail(f"Invalid YAML syntax in {compose_file}: {e}")
    
    def test_port_configuration_consistency(self):
        """Test that port configurations are consistent across files."""
        # Check docker-compose.yml
        with open("docker-compose.yml", 'r') as f:
            compose_data = yaml.safe_load(f)
        
        # Check environment files
        with open(".env.development", 'r') as f:
            dev_env = f.read()
        
        # Verify backend port consistency
        backend_service = compose_data["services"]["dj-ai-core"]
        ports = backend_service["ports"]
        
        # Should have 8000:8000 mapping
        assert "8000:8000" in ports
        
        # Should match environment configuration
        assert "API_PORT=8000" in dev_env
