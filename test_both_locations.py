#!/usr/bin/env python3
"""Test API for both Faro and Albufeira locations"""
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

# Login first
session = requests.Session()
login_data = {"username": "admin", "password": "admin"}
r = session.post(f"{BASE_URL}/login", data=login_data, allow_redirects=False)
print(f"✅ Login Status: {r.status_code}\n")

# Test both locations
locations = [
    {"name": "Aeroporto de Faro", "location": "Faro"},
    {"name": "Albufeira", "location": "Albufeira"}
]

print("="*80)
print("TESTANDO API PARA OS DOIS LOCAIS: FARO E ALBUFEIRA")
print("="*80 + "\n")

# Use a date 7 days from today
start_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
days = 3

for loc in locations:
    print(f"\n{'='*80}")
    print(f"🏁 TESTANDO: {loc['name']}")
    print(f"{'='*80}")
    
    payload = {
        "location": loc['location'],
        "start_date": start_date,
        "start_time": "10:00",
        "days": days,
        "lang": "pt",
        "currency": "EUR"
    }
    
    print(f"\n📤 Request Payload:")
    print(json.dumps(payload, indent=2))
    
    try:
        print(f"\n⏳ Aguardando resposta do scraping (pode demorar 15-30 segundos)...")
        r = session.post(
            f"{BASE_URL}/api/track-by-params",
            json=payload,
            timeout=120  # 2 minutes timeout for scraping
        )
        
        print(f"\n📥 Response Status: {r.status_code}")
        
        if r.status_code == 200:
            data = r.json()
            
            if data.get('ok'):
                items = data.get('items', [])
                print(f"\n✅ SUCCESS! Encontrados {len(items)} carros")
                
                if items:
                    print(f"\n📊 Primeiros 5 resultados:")
                    print("-" * 80)
                    for i, item in enumerate(items[:5], 1):
                        print(f"\n{i}. {item.get('car', 'N/A')}")
                        print(f"   Categoria: {item.get('category', 'N/A')}")
                        print(f"   Fornecedor: {item.get('supplier', 'N/A')}")
                        print(f"   Preço: €{item.get('price', 'N/A')}/dia")
                else:
                    print(f"\n⚠️  API respondeu OK mas sem resultados")
            else:
                error = data.get('error', 'Unknown error')
                print(f"\n❌ API Error: {error}")
        else:
            print(f"\n❌ HTTP Error {r.status_code}")
            try:
                error_data = r.json()
                print(f"   Error details: {json.dumps(error_data, indent=2)}")
            except:
                print(f"   Response: {r.text[:500]}")
            
    except requests.Timeout:
        print(f"\n⏱️  TIMEOUT: O scraping demorou mais de 2 minutos")
    except Exception as e:
        print(f"\n❌ ERRO: {type(e).__name__}: {e}")

print(f"\n\n{'='*80}")
print("TESTE COMPLETO")
print("="*80)
