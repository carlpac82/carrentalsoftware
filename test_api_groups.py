#!/usr/bin/env python3
"""Testar API para verificar se grupos estão corretos"""

import requests
import json
from datetime import datetime, timedelta

# Configuração
BASE_URL = "http://localhost:8000"
USERNAME = "admin"
PASSWORD = "admin123"

print("=" * 70)
print("TESTE DE GRUPOS NA API")
print("=" * 70)
print()

# 1. Login
print("1. Fazendo login...")
session = requests.Session()
login_response = session.post(
    f"{BASE_URL}/login",
    data={"username": USERNAME, "password": PASSWORD},
    allow_redirects=False
)

if login_response.status_code in (303, 302, 200):
    print("   ✅ Login bem sucedido")
else:
    print(f"   ❌ Login falhou: {login_response.status_code}")
    exit(1)

# 2. Fazer pesquisa em modo mock
print("\n2. Fazendo pesquisa em modo MOCK...")
start_date = datetime.now().date().isoformat()
search_data = {
    "location": "Faro Aeroporto",
    "start_date": start_date,
    "days": 7,
    "start_time": "10:00",
    "end_time": "10:00",
    "quick": True
}

response = session.post(
    f"{BASE_URL}/api/track-by-params",
    json=search_data
)

if response.status_code == 200:
    print("   ✅ Pesquisa bem sucedida")
    data = response.json()
    
    if data.get("ok"):
        items = data.get("items", [])
        print(f"\n   📊 Total de items: {len(items)}")
        
        # Agrupar por grupo
        grupos = {}
        for item in items:
            group = item.get("group", "Others")
            if group not in grupos:
                grupos[group] = []
            grupos[group].append(item)
        
        print(f"\n   📋 Grupos encontrados: {sorted(grupos.keys())}")
        print()
        print("   DETALHES POR GRUPO:")
        print("   " + "-" * 66)
        
        # Grupos esperados
        grupos_esperados = ["B1", "B2", "D", "E1", "E2", "F", "G", "J1", "J2", "L1", "L2", "M1", "M2", "N"]
        
        for group in sorted(grupos.keys()):
            count = len(grupos[group])
            status = "✅" if group in grupos_esperados or group == "Others" else "❌"
            print(f"   {status} {group:10s} - {count:2d} veículos")
            
            # Mostrar alguns exemplos
            for item in grupos[group][:2]:
                car = item.get("car", "N/A")
                category = item.get("category", "N/A")
                print(f"      • {car[:35]:35s} (cat: {category})")
        
        print()
        print("   " + "-" * 66)
        
        # Verificar se há grupos problemáticos
        grupos_problematicos = ["7 lugares", "9 lugares", "7 lugares automático"]
        problematicos_encontrados = [g for g in grupos.keys() if g in grupos_problematicos]
        
        if problematicos_encontrados:
            print(f"\n   ❌ GRUPOS PROBLEMÁTICOS ENCONTRADOS: {problematicos_encontrados}")
            print("      Estes devem ser mapeados para M1, M2, N")
        else:
            print("\n   ✅ NENHUM GRUPO PROBLEMÁTICO ENCONTRADO")
        
        # Verificar grupos em falta
        grupos_em_falta = [g for g in grupos_esperados if g not in grupos.keys()]
        if grupos_em_falta:
            print(f"\n   ℹ️  Grupos definidos mas não encontrados: {grupos_em_falta}")
            print("      (Normal se não houver veículos dessas categorias)")
        
    else:
        print(f"   ❌ Erro na resposta: {data.get('error', 'Unknown')}")
else:
    print(f"   ❌ Erro HTTP: {response.status_code}")
    print(f"   Response: {response.text[:200]}")

print()
print("=" * 70)
print("TESTE CONCLUÍDO")
print("=" * 70)
