#!/usr/bin/env python3
"""Testar API para verificar carros AUTOPRUDENTE"""

import requests
import json
from collections import Counter

# Fazer request à API local
url = "http://localhost:8000/api/track-by-params"
payload = {
    "location": "Aeroporto de Faro",
    "start_date": "2024-11-12",
    "start_time": "15:00",
    "days": 5,
    "lang": "pt",
    "currency": "EUR"
}

print(f"🔍 Fazendo request à API...")
print(f"📍 Local: {payload['location']}")
print(f"📅 Data: {payload['start_date']}")
print(f"📆 Dias: {payload['days']}")
print()

# Fazer request (sem autenticação - vai falhar mas vamos tentar)
response = requests.post(url, json=payload)

print(f"📊 Status: {response.status_code}")

if response.status_code == 401:
    print("❌ Erro: Requer autenticação")
    print("\n💡 Solução: Vou ler os logs do servidor diretamente")
    print("\nPor favor, faz a pesquisa manualmente na automação de preços e partilha os logs do console!")
else:
    data = response.json()
    
    if data.get('ok') and data.get('items'):
        items = data['items']
        print(f"✅ Total de carros: {len(items)}\n")
        
        # Filtrar AUTOPRUDENTE
        autoprudente = [
            item for item in items 
            if 'autoprudente' in (item.get('supplier') or '').lower() or
               'auto prudente' in (item.get('supplier') or '').lower() or
               (item.get('supplier') or '').upper() == 'AUP'
        ]
        
        print(f"🚗 Carros AUTOPRUDENTE: {len(autoprudente)}\n")
        
        if autoprudente:
            # Agrupar por grupo
            grupos = Counter(item.get('group', 'Unknown') for item in autoprudente)
            
            print("📋 Distribuição por grupo:")
            for grupo, count in sorted(grupos.items()):
                print(f"  {grupo}: {count} carros")
            
            print("\n🔍 Primeiros 5 carros AUTOPRUDENTE:")
            for i, item in enumerate(autoprudente[:5], 1):
                print(f"{i}. {item.get('car', 'N/A')}")
                print(f"   Grupo: {item.get('group', 'N/A')}")
                print(f"   Preço: {item.get('price', 'N/A')}")
                print(f"   Supplier: {item.get('supplier', 'N/A')}")
                print()
        else:
            print("❌ Nenhum carro AUTOPRUDENTE encontrado!")
            
            # Mostrar alguns suppliers para debug
            all_suppliers = Counter(item.get('supplier', 'Unknown') for item in items)
            print("\n📋 Suppliers encontrados (top 10):")
            for supplier, count in all_suppliers.most_common(10):
                print(f"  {supplier}: {count} carros")
    else:
        print(f"❌ Erro: {data}")
