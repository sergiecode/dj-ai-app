#!/usr/bin/env python3
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
    
    print("\nIntegration test complete!")

if __name__ == "__main__":
    main()
