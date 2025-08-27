# Unit Tests for DJ AI App
# Author: Sergie Code

import pytest
import os
import yaml


def test_project_structure():
    """Test that essential project files exist."""
    required_files = [
        "docker-compose.yml",
        "README.md",
        ".gitignore"
    ]
    
    for file in required_files:
        assert os.path.exists(file), f"Required file {file} not found"


def test_docker_compose_valid():
    """Test that docker-compose.yml is valid YAML."""
    with open("docker-compose.yml", "r") as f:
        compose_data = yaml.safe_load(f)
    
    assert "services" in compose_data, "Docker Compose must have services section"
    assert len(compose_data["services"]) > 0, "Must have at least one service defined"


def test_readme_exists():
    """Test that README.md exists and has content."""
    assert os.path.exists("README.md"), "README.md file must exist"
    
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()
    
    assert len(content) > 100, "README.md should have substantial content"
    assert "DJ AI" in content, "README should mention DJ AI"


def test_gitignore_exists():
    """Test that .gitignore exists."""
    assert os.path.exists(".gitignore"), ".gitignore file must exist"


def test_integration_test_file():
    """Test that integration test file exists and is executable."""
    assert os.path.exists("integration_test.py"), "integration_test.py must exist"
    
    # Check if it's a valid Python file
    with open("integration_test.py", "r") as f:
        content = f.read()
    
    assert "def " in content, "integration_test.py should contain functions"


def test_environment_setup():
    """Test basic environment setup."""
    # Test that we can import common libraries
    import subprocess
    import pathlib
    import sys
    
    assert sys.version_info >= (3, 8), "Python 3.8+ required"


class TestConfiguration:
    """Test configuration files."""
    
    def test_docker_compose_services(self):
        """Test Docker Compose service configuration."""
        with open("docker-compose.yml", "r") as f:
            compose_data = yaml.safe_load(f)
        
        services = compose_data.get("services", {})
        
        # Should have at least one service
        assert len(services) > 0, "Must have services defined"
        
        # Each service should have basic requirements
        for service_name, service_config in services.items():
            if "image" not in service_config and "build" not in service_config:
                pytest.fail(f"Service {service_name} must have either 'image' or 'build' configuration")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
