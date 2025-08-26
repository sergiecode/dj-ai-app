# DJ AI App - Test Configuration
# Author: Sergie Code
# Purpose: Testing framework configuration for the DJ AI orchestrator

import pytest
import os
import time
import requests
from pathlib import Path

# Test Configuration
TEST_TIMEOUT = 60  # seconds
API_TIMEOUT = 30   # seconds
HEALTH_CHECK_INTERVAL = 5  # seconds

# Service URLs
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"
NGINX_URL = "http://localhost:80"

# Test Data Paths
FIXTURES_DIR = Path(__file__).parent / "fixtures"
SAMPLE_AUDIO_DIR = FIXTURES_DIR / "audio"

@pytest.fixture(scope="session")
def docker_services():
    """Ensure Docker services are running before tests."""
    import subprocess
    
    # Check if Docker is running
    try:
        subprocess.run(["docker", "version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        pytest.skip("Docker is not running")
    
    # Check if services are up
    try:
        subprocess.run(["docker-compose", "ps"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        pytest.skip("Docker Compose services are not running")
    
    return True

@pytest.fixture(scope="session")
def wait_for_services(docker_services):
    """Wait for all services to be healthy."""
    services = {
        "backend": BACKEND_URL,
        "frontend": FRONTEND_URL
    }
    
    for service_name, url in services.items():
        max_attempts = TEST_TIMEOUT // HEALTH_CHECK_INTERVAL
        for attempt in range(max_attempts):
            try:
                if service_name == "backend":
                    response = requests.get(f"{url}/health", timeout=5)
                else:
                    response = requests.get(url, timeout=5)
                
                if response.status_code == 200:
                    print(f"✓ {service_name} is ready")
                    break
            except requests.exceptions.RequestException:
                pass
            
            if attempt == max_attempts - 1:
                pytest.fail(f"Service {service_name} failed to start within {TEST_TIMEOUT} seconds")
            
            time.sleep(HEALTH_CHECK_INTERVAL)
    
    return True

@pytest.fixture
def sample_audio_file():
    """Provide a sample audio file for testing."""
    # This would normally point to a real audio file
    # For now, we'll create a placeholder
    return SAMPLE_AUDIO_DIR / "sample.mp3"

@pytest.fixture
def api_client():
    """HTTP client for API testing."""
    return requests.Session()

class TestHelpers:
    """Helper functions for tests."""
    
    @staticmethod
    def wait_for_response(url, timeout=30, expected_status=200):
        """Wait for a specific URL to respond."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == expected_status:
                    return response
            except requests.exceptions.RequestException:
                pass
            time.sleep(1)
        
        raise TimeoutError(f"URL {url} did not respond with status {expected_status} within {timeout} seconds")
    
    @staticmethod
    def is_service_healthy(service_url):
        """Check if a service is healthy."""
        try:
            response = requests.get(f"{service_url}/health", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    @staticmethod
    def get_service_logs(service_name):
        """Get logs for a specific service."""
        import subprocess
        try:
            result = subprocess.run(
                ["docker-compose", "logs", service_name],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError:
            return ""

# Pytest configuration
def pytest_configure(config):
    """Pytest configuration."""
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
    config.addinivalue_line(
        "markers", "e2e: marks tests as end-to-end tests"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow running"
    )

def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically."""
    for item in items:
        # Add integration marker to integration tests
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        
        # Add unit marker to unit tests
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        
        # Add e2e marker to e2e tests
        if "e2e" in str(item.fspath):
            item.add_marker(pytest.mark.e2e)
