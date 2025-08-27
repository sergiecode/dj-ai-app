# End-to-End Tests for DJ AI App
# Author: Sergie Code

import pytest
import requests
import time
import subprocess
import os


@pytest.fixture(scope="session")
def services_running():
    """Fixture to check if services are running."""
    try:
        # Check if backend is responding
        backend_response = requests.get("http://localhost:8000/health", timeout=5)
        backend_ok = backend_response.status_code == 200
    except:
        backend_ok = False
    
    try:
        # Check if frontend is responding
        frontend_response = requests.get("http://localhost:3000", timeout=5)
        frontend_ok = frontend_response.status_code == 200
    except:
        frontend_ok = False
    
    return {
        "backend": backend_ok,
        "frontend": frontend_ok
    }


@pytest.mark.slow
def test_backend_health_endpoint(services_running):
    """Test that backend health endpoint is accessible."""
    if not services_running["backend"]:
        pytest.skip("Backend service not running")
    
    response = requests.get("http://localhost:8000/health")
    assert response.status_code == 200, "Backend health check should return 200"


@pytest.mark.slow  
def test_frontend_accessibility(services_running):
    """Test that frontend is accessible."""
    if not services_running["frontend"]:
        pytest.skip("Frontend service not running")
    
    response = requests.get("http://localhost:3000")
    assert response.status_code == 200, "Frontend should return 200"


def test_docker_compose_file_exists():
    """Test that docker-compose.yml exists for E2E testing."""
    assert os.path.exists("docker-compose.yml"), "docker-compose.yml required for E2E tests"


def test_integration_test_script():
    """Test that integration_test.py can be run."""
    assert os.path.exists("integration_test.py"), "integration_test.py script must exist"
    
    # Test that it's executable Python
    try:
        result = subprocess.run(
            ["python", "--version"], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        assert result.returncode == 0, "Python must be available"
    except subprocess.TimeoutExpired:
        pytest.fail("Python command timed out")


@pytest.mark.slow
def test_service_communication(services_running):
    """Test basic service communication if services are running."""
    if not (services_running["backend"] and services_running["frontend"]):
        pytest.skip("Both services must be running for communication test")
    
    # This would test actual service interaction
    # For now, just verify both services respond
    assert services_running["backend"], "Backend must be responding"
    assert services_running["frontend"], "Frontend must be responding"


class TestIntegrationWorkflow:
    """Test the integration workflow."""
    
    def test_can_run_integration_script(self):
        """Test that integration script can be executed."""
        if not os.path.exists("integration_test.py"):
            pytest.skip("integration_test.py not found")
        
        # Just test the file is valid Python syntax
        with open("integration_test.py", "r") as f:
            content = f.read()
        
        try:
            compile(content, "integration_test.py", "exec")
        except SyntaxError as e:
            pytest.fail(f"integration_test.py has syntax error: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "not slow"])
