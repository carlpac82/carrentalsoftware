#!/usr/bin/env python3
"""Testar endpoint de veículos"""

import sys
sys.path.insert(0, '/Users/filipepacheco/CascadeProjects/RentalPriceTrackerPerDay')

# Importar VEHICLES diretamente
from carjet_direct import VEHICLES

print("🔍 TESTE DICIONÁRIO VEHICLES")
print("=" * 70)
print()

print(f"📊 Total de veículos no carjet_direct.py: {len(VEHICLES)}")
print()

# Mostrar primeiros 10
print("📋 Primeiros 10 veículos:")
for i, (car, category) in enumerate(list(VEHICLES.items())[:10], 1):
    print(f"{i}. {car} → {category}")

print()
print("=" * 70)
print()

# Verificar se há dados na base de dados
import sqlite3
from pathlib import Path

DB_PATH = Path("/Users/filipepacheco/CascadeProjects/RentalPriceTrackerPerDay/data.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Verificar price_snapshots
try:
    cursor.execute("SELECT COUNT(*) FROM price_snapshots WHERE ts >= datetime('now', '-7 days')")
    count = cursor.fetchone()[0]
    print(f"📊 Registos em price_snapshots (últimos 7 dias): {count}")
    
    if count > 0:
        cursor.execute("""
            SELECT DISTINCT car 
            FROM price_snapshots 
            WHERE ts >= datetime('now', '-7 days')
            ORDER BY car
            LIMIT 10
        """)
        cars = cursor.fetchall()
        print()
        print("📋 Primeiros 10 carros em price_snapshots:")
        for i, (car,) in enumerate(cars, 1):
            print(f"{i}. {car}")
    else:
        print()
        print("⚠️  PROBLEMA: Não há dados recentes em price_snapshots!")
        print("   O endpoint /api/vehicles/with-originals precisa de dados!")
        print()
        print("💡 SOLUÇÃO:")
        print("   1. Faz uma pesquisa na automação de preços")
        print("   2. Ou modifica o endpoint para não depender de price_snapshots")
        
except Exception as e:
    print(f"❌ Erro ao verificar price_snapshots: {e}")

conn.close()

print()
print("=" * 70)
print()
print("🎯 CONCLUSÃO:")
print()
print("O dicionário VEHICLES tem 259 veículos categorizados.")
print("Mas o endpoint /api/vehicles/with-originals só mostra veículos")
print("que aparecem em price_snapshots nos últimos 7 dias.")
print()
print("Se não houver pesquisas recentes, a lista fica vazia!")
