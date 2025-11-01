#!/usr/bin/env python3
"""Testar API para verificar se obtém preços AUTOPRUDENTE"""

import requests
import json
import time

print("🧪 TESTE API - Filtro AUTOPRUDENTE")
print("=" * 70)
print()

# Configuração do teste
url = "http://localhost:8000/api/track-by-params"
payload = {
    "location": "Aeroporto de Faro",
    "start_date": "2024-11-12",
    "start_time": "15:00",
    "days": 5,
    "lang": "pt",
    "currency": "EUR"
}

print(f"📍 Local: {payload['location']}")
print(f"📅 Data: {payload['start_date']}")
print(f"📆 Dias: {payload['days']}")
print()

print("🔄 Fazendo request à API...")
print("⚠️  NOTA: Isto pode demorar 30-60 segundos (scraping com Playwright)")
print()

start_time = time.time()

try:
    # Fazer request SEM autenticação (vai falhar)
    response = requests.post(url, json=payload, timeout=120)
    
    elapsed = time.time() - start_time
    print(f"⏱️  Tempo: {elapsed:.1f}s")
    print(f"📊 Status: {response.status_code}")
    print()
    
    if response.status_code == 401:
        print("❌ ERRO: Requer autenticação")
        print()
        print("💡 SOLUÇÃO:")
        print("   1. Abre o navegador: http://localhost:8000/price-automation")
        print("   2. Faz login se necessário")
        print("   3. Faz uma pesquisa manualmente")
        print("   4. Verifica os logs do console (F12)")
        print()
        print("📋 Logs esperados:")
        print("   [DEBUG] Suppliers encontrados: [...]")
        print("   X dias - Y carros AUTOPRUDENTE encontrados")
        print("   [DEBUG Xd] Grupos com AUTOPRUDENTE: { ... }")
        
    elif response.status_code == 200:
        data = response.json()
        
        if data.get('ok') and data.get('items'):
            items = data['items']
            print(f"✅ Sucesso! {len(items)} carros encontrados")
            print()
            
            # Verificar se são todos AUTOPRUDENTE
            autoprudente_items = [
                item for item in items
                if 'autoprudente' in (item.get('supplier') or '').lower() or
                   (item.get('supplier') or '').upper() == 'AUP'
            ]
            
            print(f"🚗 Carros AUTOPRUDENTE: {len(autoprudente_items)}/{len(items)}")
            print()
            
            if len(autoprudente_items) == len(items):
                print("✅ PERFEITO! Todos os carros são AUTOPRUDENTE!")
            else:
                print("⚠️  ATENÇÃO! Há carros de outros suppliers:")
                outros = [item for item in items if item not in autoprudente_items]
                for item in outros[:5]:
                    print(f"   - {item.get('car')} ({item.get('supplier')})")
            
            print()
            print("📋 Distribuição por grupo:")
            grupos = {}
            for item in autoprudente_items:
                grupo = item.get('group', 'Unknown')
                if grupo not in grupos:
                    grupos[grupo] = 0
                grupos[grupo] += 1
            
            for grupo, count in sorted(grupos.items()):
                print(f"   {grupo}: {count} carros")
            
            print()
            print("🔍 Primeiros 3 carros AUTOPRUDENTE:")
            for i, item in enumerate(autoprudente_items[:3], 1):
                print(f"{i}. {item.get('car', 'N/A')}")
                print(f"   Grupo: {item.get('group', 'N/A')}")
                print(f"   Preço: {item.get('price', 'N/A')}")
                print(f"   Supplier: {item.get('supplier', 'N/A')}")
                print()
        else:
            print(f"❌ Erro: {data}")
    else:
        print(f"❌ Erro HTTP {response.status_code}")
        print(response.text[:500])
        
except requests.exceptions.Timeout:
    print("❌ TIMEOUT: Request demorou mais de 120 segundos")
    print()
    print("💡 Isto pode acontecer se:")
    print("   - Playwright está a demorar muito")
    print("   - CarJet está lento")
    print("   - Há problemas de rede")
    
except Exception as e:
    print(f"❌ ERRO: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 70)
