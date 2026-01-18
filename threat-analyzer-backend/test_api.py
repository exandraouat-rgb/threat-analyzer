#!/usr/bin/env python3
"""
Script de test simple pour vérifier que le backend fonctionne
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test de santé du serveur"""
    print("\n✓ Test Health Check...")
    try:
        res = requests.get(f"{BASE_URL}/health")
        print(f"  Status: {res.status_code}")
        print(f"  Response: {res.json()}")
    except Exception as e:
        print(f"  ✗ Erreur: {e}")

def test_analyze():
    """Test de l'endpoint analyze"""
    print("\n✓ Test Analyze Endpoint...")
    try:
        data = {
            "project_name": "TestApp",
            "app_type": "Web Application",
            "architecture_description": "Microservices avec API REST"
        }
        
        res = requests.post(f"{BASE_URL}/analyze", data=data)
        print(f"  Status: {res.status_code}")
        response_json = res.json()
        print(f"  Keys: {list(response_json.keys())}")
        if "error" in response_json:
            print(f"  Error: {response_json['error']}")
        else:
            print(f"  Score: {response_json.get('score_risque')}")
            print(f"  Analysis keys: {list(response_json.get('analysis', {}).keys())}")
    except Exception as e:
        print(f"  ✗ Erreur: {e}")

if __name__ == "__main__":
    print("=== TEST DU BACKEND ===")
    test_health()
    test_analyze()
    print("\n=== FIN DES TESTS ===")
