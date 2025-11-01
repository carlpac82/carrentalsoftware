#!/usr/bin/env python3
"""Testar API para várias datas e dias"""
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

# Login primeiro
session = requests.Session()
login_data = {"username": "admin", "password": "admin"}
r = session.post(f"{BASE_URL}/login", data=login_data, allow_redirects=False)
print(f"✅ Login: {r.status_code}")

# Testar para várias configurações
tests = [
    {"location": "Aeroporto de Faro", "days": 1, "date": "2025-11-01"},
    {"location": "Aeroporto de Faro", "days": 3, "date": "2025-11-01"},
    {"location": "Aeroporto de Faro", "days": 7, "date": "2025-11-01"},
    {"location": "Albufeira", "days": 1, "date": "2025-11-01"},
]

print("\n" + "="*60)
print("TESTANDO API PARA VÁRIAS CONFIGURAÇÕES")
print("="*60 + "\n")

for i, test in enumerate(tests, 1):
    print(f"\n[TEST {i}] {test['location']} - {test['days']} dias")
    print("-" * 60)
    
    # Calcular start_date (pickup) = date - days
    end_date = datetime.strptime(test['date'], '%Y-%m-%d')
    start_date = end_date - timedelta(days=test['days'])
    
    payload = {
        "location": test['location'],
        "start_date": start_date.strftime('%Y-%m-%d'),
        "start_time": "10:00",
        "days": test['days'],
        "lang": "pt",
        "currency": "EUR"
    }
    
    print(f"📤 Request: {json.dumps(payload, indent=2)}")
    
    try:
        r = session.post(
            f"{BASE_URL}/api/track-by-params",
            json=payload,
            timeout=60
        )
        
        if r.status_code == 200:
            data = r.json()
            items_count = len(data.get('items', []))
            
            if items_count > 0:
                print(f"✅ SUCCESS: {items_count} carros encontrados!")
                print(f"   Primeiro carro: {data['items'][0].get('car', 'N/A')}")
                print(f"   Preço: {data['items'][0].get('price', 'N/A')}")
            else:
                print(f"⚠️  0 resultados")
        else:
            print(f"❌ HTTP {r.status_code}")
            
    except Exception as e:
        print(f"❌ ERRO: {e}")

print("\n" + "="*60)
print("TESTE COMPLETO")
print("="*60)
