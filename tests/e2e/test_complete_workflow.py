# DJ AI App - End-to-End Tests
# Author: Sergie Code
# Purpose: Complete workflow testing for the DJ AI system

import pytest
import requests
import time
import json
import subprocess
from pathlib import Path

class TestCompleteWorkflow:
    """Test complete DJ AI workflow from start to finish."""
    
    @pytest.mark.slow
    def test_full_system_startup_workflow(self, docker_services):
        """Test the complete system startup workflow."""
        # Stop any running services
        subprocess.run(["docker-compose", "down"], capture_output=True)
        
        # Start services using the development script
        result = subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-File", "scripts/start-dev.ps1"],
            capture_output=True,
            text=True,
            cwd=Path.cwd()
        )
        
        # Wait for services to be ready
        max_wait = 120  # 2 minutes
        services_ready = False
        
        for i in range(max_wait):
            time.sleep(1)
            
            try:
                # Check backend
                backend_response = requests.get("http://localhost:8000/health", timeout=2)
                # Check frontend
                frontend_response = requests.get("http://localhost:3000", timeout=2)
                
                if backend_response.status_code == 200 and frontend_response.status_code == 200:
                    services_ready = True
                    break
            except requests.exceptions.RequestException:
                continue
        
        assert services_ready, "Services failed to start within the timeout period"
    
    @pytest.mark.slow
    def test_api_workflow_simulation(self, wait_for_services, api_client):
        """Test a complete API workflow simulation."""
        # 1. Check system health
        health_response = api_client.get("http://localhost:8000/health")
        assert health_response.status_code == 200
        
        # 2. Get supported formats
        formats_response = api_client.get("http://localhost:8000/supported-formats")
        assert formats_response.status_code == 200
        formats_data = formats_response.json()
        assert "formats" in formats_data
        
        # 3. Test API documentation access
        docs_response = api_client.get("http://localhost:8000/docs")
        assert docs_response.status_code == 200
        
        # 4. Test OpenAPI spec
        openapi_response = api_client.get("http://localhost:8000/openapi.json")
        assert openapi_response.status_code == 200
        openapi_data = openapi_response.json()
        assert "openapi" in openapi_data
        assert "paths" in openapi_data
    
    def test_frontend_backend_communication(self, wait_for_services, api_client):
        """Test frontend to backend communication simulation."""
        # Simulate a frontend request to backend
        headers = {
            "Origin": "http://localhost:3000",
            "Referer": "http://localhost:3000/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        # Test CORS preflight
        options_response = api_client.options(
            "http://localhost:8000/health",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
                "Access-Control-Request-Headers": "Content-Type"
            }
        )
        
        assert options_response.status_code in [200, 204]
        
        # Test actual request from frontend
        get_response = api_client.get(
            "http://localhost:8000/health",
            headers=headers
        )
        
        assert get_response.status_code == 200
        assert "Access-Control-Allow-Origin" in get_response.headers
    
    def test_error_handling_workflow(self, wait_for_services, api_client):
        """Test error handling across the system."""
        # Test 404 errors
        response_404 = api_client.get("http://localhost:8000/nonexistent")
        assert response_404.status_code == 404
        
        # Test method not allowed
        response_405 = api_client.post("http://localhost:8000/health")
        assert response_405.status_code == 405
        
        # Test validation errors for API endpoints
        response_422 = api_client.post("http://localhost:8000/analyze-track")
        assert response_422.status_code == 422
        
        # Verify error response format
        error_data = response_422.json()
        assert "detail" in error_data


class TestLoadAndStress:
    """Test system under load conditions."""
    
    @pytest.mark.slow
    def test_concurrent_health_checks(self, wait_for_services):
        """Test concurrent requests to health endpoint."""
        import threading
        import queue
        
        results = queue.Queue()
        
        def make_request():
            try:
                response = requests.get("http://localhost:8000/health", timeout=5)
                results.put(response.status_code)
            except Exception as e:
                results.put(f"Error: {e}")
        
        # Create 10 concurrent threads
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Check results
        status_codes = []
        while not results.empty():
            status_codes.append(results.get())
        
        # All requests should succeed
        assert len(status_codes) == 10
        assert all(code == 200 for code in status_codes)
    
    def test_rapid_sequential_requests(self, wait_for_services, api_client):
        """Test rapid sequential requests."""
        # Make 20 rapid requests
        responses = []
        for _ in range(20):
            response = api_client.get("http://localhost:8000/health")
            responses.append(response.status_code)
            time.sleep(0.1)  # Small delay
        
        # All should succeed
        assert all(status == 200 for status in responses)


class TestRecoveryAndResilience:
    """Test system recovery and resilience."""
    
    @pytest.mark.slow
    def test_service_restart_recovery(self, docker_services):
        """Test system recovery after service restart."""
        # Restart backend service
        subprocess.run(["docker-compose", "restart", "dj-ai-core"], capture_output=True)
        
        # Wait for recovery
        max_wait = 60
        recovered = False
        
        for i in range(max_wait):
            time.sleep(1)
            try:
                response = requests.get("http://localhost:8000/health", timeout=2)
                if response.status_code == 200:
                    recovered = True
                    break
            except requests.exceptions.RequestException:
                continue
        
        assert recovered, "Backend service failed to recover after restart"
        
        # Test that frontend is still accessible
        frontend_response = requests.get("http://localhost:3000", timeout=5)
        assert frontend_response.status_code == 200
    
    @pytest.mark.slow  
    def test_network_interruption_simulation(self, wait_for_services):
        """Test behavior during simulated network issues."""
        # Test with short timeout to simulate network issues
        try:
            response = requests.get("http://localhost:8000/health", timeout=0.001)
            # If this succeeds, the network is very fast
            assert response.status_code == 200
        except requests.exceptions.Timeout:
            # This is expected for very short timeout
            pass
        
        # Test normal request after "network recovery"
        response = requests.get("http://localhost:8000/health", timeout=5)
        assert response.status_code == 200


class TestProductionReadiness:
    """Test production readiness aspects."""
    
    def test_security_headers(self, wait_for_services, api_client):
        """Test security headers are present."""
        response = api_client.get("http://localhost:8000/health")
        
        # While we can't test all Nginx headers in development mode,
        # we can test basic security practices
        assert response.status_code == 200
        
        # Check that sensitive information is not exposed
        assert "Server" not in response.headers or "nginx" not in response.headers.get("Server", "").lower()
    
    def test_api_response_consistency(self, wait_for_services, api_client):
        """Test API response consistency across multiple requests."""
        responses = []
        
        # Make multiple requests
        for _ in range(5):
            response = api_client.get("http://localhost:8000/health")
            responses.append(response.json())
            time.sleep(0.5)
        
        # All responses should have consistent structure
        first_response = responses[0]
        for response in responses[1:]:
            assert set(response.keys()) == set(first_response.keys())
            assert response.get("status") == first_response.get("status")
    
    def test_service_dependencies(self, wait_for_services):
        """Test service dependency configuration."""
        import subprocess
        
        # Get service information
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
        
        # Verify services are healthy
        for service in services:
            if "Health" in service:
                assert service["Health"] == "healthy", f"Service {service['Name']} is not healthy"


class TestMonitoringAndObservability:
    """Test monitoring and observability features."""
    
    def test_health_check_completeness(self, wait_for_services, api_client):
        """Test that health checks provide comprehensive information."""
        response = api_client.get("http://localhost:8000/health")
        assert response.status_code == 200
        
        health_data = response.json()
        
        # Should include basic health information
        required_fields = ["status", "timestamp"]
        for field in required_fields:
            assert field in health_data, f"Health check missing required field: {field}"
    
    def test_logging_accessibility(self, docker_services):
        """Test that logs are accessible and contain useful information."""
        import subprocess
        
        # Get logs for backend service
        result = subprocess.run(
            ["docker-compose", "logs", "--tail", "10", "dj-ai-core"],
            capture_output=True,
            text=True
        )
        
        logs = result.stdout
        
        # Logs should contain startup information
        assert len(logs) > 0, "No logs found for backend service"
        
        # Get logs for frontend service
        result = subprocess.run(
            ["docker-compose", "logs", "--tail", "10", "dj-ai-frontend"],
            capture_output=True,
            text=True
        )
        
        frontend_logs = result.stdout
        assert len(frontend_logs) > 0, "No logs found for frontend service"
