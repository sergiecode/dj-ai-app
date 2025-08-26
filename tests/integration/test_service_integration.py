# DJ AI App - Integration Tests
# Author: Sergie Code
# Purpose: Test the integration between frontend and backend services

import pytest
import requests
import time
import json
from pathlib import Path

class TestServiceIntegration:
    """Test integration between DJ AI services."""
    
    def test_backend_health_endpoint(self, wait_for_services, api_client):
        """Test that the backend health endpoint is working."""
        response = api_client.get("http://localhost:8000/health")
        
        assert response.status_code == 200
        health_data = response.json()
        
        # Verify health response structure
        assert "status" in health_data
        assert "timestamp" in health_data
        assert health_data["status"] in ["healthy", "ok"]
    
    def test_backend_api_info(self, wait_for_services, api_client):
        """Test the main API info endpoint."""
        response = api_client.get("http://localhost:8000/")
        
        assert response.status_code == 200
        api_info = response.json()
        
        # Verify API info structure
        assert "name" in api_info
        assert "version" in api_info
        assert "description" in api_info
    
    def test_backend_docs_endpoint(self, wait_for_services, api_client):
        """Test that API documentation is accessible."""
        response = api_client.get("http://localhost:8000/docs")
        
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
    
    def test_backend_supported_formats(self, wait_for_services, api_client):
        """Test the supported formats endpoint."""
        response = api_client.get("http://localhost:8000/supported-formats")
        
        assert response.status_code == 200
        formats = response.json()
        
        # Verify supported formats
        expected_formats = ["mp3", "wav", "flac", "m4a"]
        assert "formats" in formats
        
        for fmt in expected_formats:
            assert fmt in formats["formats"]
    
    def test_frontend_accessibility(self, wait_for_services, api_client):
        """Test that the frontend is accessible."""
        response = api_client.get("http://localhost:3000")
        
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
    
    def test_cors_configuration(self, wait_for_services, api_client):
        """Test CORS headers for frontend-backend communication."""
        # Options request to check CORS
        response = api_client.options(
            "http://localhost:8000/health",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET"
            }
        )
        
        assert response.status_code in [200, 204]
        
        # Check CORS headers
        cors_headers = response.headers
        assert "Access-Control-Allow-Origin" in cors_headers
    
    @pytest.mark.slow
    def test_service_startup_order(self, docker_services):
        """Test that services start in the correct order."""
        import subprocess
        
        # Stop services
        subprocess.run(["docker-compose", "down"], capture_output=True)
        
        # Start services
        subprocess.run(["docker-compose", "up", "-d"], capture_output=True)
        
        # Wait and check that backend starts before frontend
        max_wait = 60
        backend_ready = False
        frontend_ready = False
        
        for i in range(max_wait):
            time.sleep(1)
            
            # Check backend
            if not backend_ready:
                try:
                    response = requests.get("http://localhost:8000/health", timeout=2)
                    if response.status_code == 200:
                        backend_ready = True
                        backend_start_time = i
                except requests.exceptions.RequestException:
                    pass
            
            # Check frontend (should start after backend)
            if backend_ready and not frontend_ready:
                try:
                    response = requests.get("http://localhost:3000", timeout=2)
                    if response.status_code == 200:
                        frontend_ready = True
                        frontend_start_time = i
                        break
                except requests.exceptions.RequestException:
                    pass
        
        assert backend_ready, "Backend failed to start"
        assert frontend_ready, "Frontend failed to start"
        # Frontend should start after backend (dependency check)
        assert frontend_start_time > backend_start_time


class TestAPIIntegration:
    """Test API endpoints integration."""
    
    def test_api_endpoints_reachable(self, wait_for_services, api_client):
        """Test that all documented API endpoints are reachable."""
        endpoints = [
            ("/", "GET"),
            ("/health", "GET"),
            ("/docs", "GET"),
            ("/supported-formats", "GET"),
        ]
        
        for endpoint, method in endpoints:
            url = f"http://localhost:8000{endpoint}"
            response = api_client.request(method, url)
            
            assert response.status_code in [200, 201], f"Endpoint {endpoint} failed with status {response.status_code}"
    
    def test_api_error_handling(self, wait_for_services, api_client):
        """Test API error handling for invalid endpoints."""
        # Test 404 for non-existent endpoint
        response = api_client.get("http://localhost:8000/non-existent-endpoint")
        assert response.status_code == 404
        
        # Test invalid method
        response = api_client.delete("http://localhost:8000/health")
        assert response.status_code == 405
    
    def test_file_upload_endpoint_structure(self, wait_for_services, api_client):
        """Test the structure of file upload endpoint (without actual file)."""
        # Test POST without file (should return validation error)
        response = api_client.post("http://localhost:8000/analyze-track")
        
        # Should return 422 (validation error) not 500 (server error)
        assert response.status_code == 422
        
        error_detail = response.json()
        assert "detail" in error_detail
    
    def test_recommendations_endpoint_structure(self, wait_for_services, api_client):
        """Test the structure of recommendations endpoint."""
        # Test POST without proper JSON (should return validation error)
        response = api_client.post("http://localhost:8000/recommend-transitions")
        
        assert response.status_code == 422
        
        # Test with invalid JSON structure
        invalid_data = {"invalid": "data"}
        response = api_client.post(
            "http://localhost:8000/recommend-transitions",
            json=invalid_data
        )
        
        assert response.status_code == 422


class TestDockerIntegration:
    """Test Docker integration and orchestration."""
    
    def test_docker_compose_services_running(self, docker_services):
        """Test that all Docker Compose services are running."""
        import subprocess
        
        result = subprocess.run(
            ["docker-compose", "ps", "--format", "json"],
            capture_output=True,
            text=True,
            check=True
        )
        
        services = []
        for line in result.stdout.strip().split('\n'):
            if line:
                services.append(json.loads(line))
        
        # Verify expected services are running
        service_names = [service["Name"] for service in services]
        expected_services = ["dj-ai-core", "dj-ai-frontend"]
        
        for expected in expected_services:
            assert any(expected in name for name in service_names), f"Service {expected} not found"
    
    def test_docker_networks(self, docker_services):
        """Test Docker network configuration."""
        import subprocess
        
        result = subprocess.run(
            ["docker", "network", "ls", "--format", "{{.Name}}"],
            capture_output=True,
            text=True,
            check=True
        )
        
        networks = result.stdout.strip().split('\n')
        assert "dj-ai-network" in networks
    
    def test_docker_volumes(self, docker_services):
        """Test Docker volume configuration."""
        import subprocess
        
        result = subprocess.run(
            ["docker", "volume", "ls", "--format", "{{.Name}}"],
            capture_output=True,
            text=True,
            check=True
        )
        
        volumes = result.stdout.strip().split('\n')
        # Check if project volumes exist
        project_volumes = [vol for vol in volumes if "dj-ai-app" in vol]
        assert len(project_volumes) > 0, "No project volumes found"


class TestEnvironmentConfiguration:
    """Test environment configuration and variables."""
    
    def test_backend_environment_variables(self, wait_for_services, api_client):
        """Test that backend is using correct environment configuration."""
        # Test CORS configuration by making a cross-origin request
        response = api_client.get(
            "http://localhost:8000/health",
            headers={"Origin": "http://localhost:3000"}
        )
        
        assert response.status_code == 200
        
        # Check CORS headers are present
        assert "Access-Control-Allow-Origin" in response.headers
    
    def test_service_ports(self, wait_for_services):
        """Test that services are running on expected ports."""
        import socket
        
        # Test backend port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 8000))
        sock.close()
        assert result == 0, "Backend not listening on port 8000"
        
        # Test frontend port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 3000))
        sock.close()
        assert result == 0, "Frontend not listening on port 3000"
