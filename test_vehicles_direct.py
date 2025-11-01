#!/usr/bin/env python3
"""Testar endpoint /api/vehicles/with-originals diretamente"""

import sys
sys.path.insert(0, '/Users/filipepacheco/CascadeProjects/RentalPriceTrackerPerDay')

print("🧪 TESTE DIRETO - /api/vehicles/with-originals")
print("=" * 70)
print()

# Simular o que o endpoint faz
try:
    # Recarregar módulo
    import carjet_direct
    import importlib
    importlib.reload(carjet_direct)
    from carjet_direct import VEHICLES
    
    print(f"✅ VEHICLES importado com sucesso")
    print(f"📊 Total no dicionário: {len(VEHICLES)}")
    print()
    
    # Criar mapeamento como o endpoint faz
    originals_map = {}
    
    # Primeiro, adicionar TODOS os veículos do dicionário
    for clean_name, category in VEHICLES.items():
        originals_map[clean_name] = {
            'original': clean_name,
            'clean': clean_name,
            'category': category
        }
    
    print(f"✅ Mapeamento criado: {len(originals_map)} veículos")
    print()
    
    # Mostrar primeiros 10
    print("📋 Primeiros 10 veículos no mapeamento:")
    for i, (clean, data) in enumerate(list(originals_map.items())[:10], 1):
        print(f"{i}. {clean} → {data['category']}")
    
    print()
    print("=" * 70)
    print()
    
    if len(originals_map) == 0:
        print("❌ PROBLEMA: originals_map está VAZIO!")
        print()
        print("Possíveis causas:")
        print("  1. VEHICLES está vazio em carjet_direct.py")
        print("  2. Erro ao importar o módulo")
        print("  3. Ficheiro carjet_direct.py foi modificado")
    else:
        print(f"✅ SUCESSO: {len(originals_map)} veículos prontos para retornar")
        print()
        print("Se o endpoint retorna vazio mas este script mostra veículos,")
        print("o problema pode ser:")
        print("  1. Erro de autenticação (401)")
        print("  2. Exceção no endpoint que não está a ser capturada")
        print("  3. Problema no JSON encoding")
        
except Exception as e:
    print(f"❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
