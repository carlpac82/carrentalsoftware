#!/usr/bin/env python3
"""Testar mapeamento de categorias para códigos de grupos"""

# Import da função do main.py
import sys
sys.path.insert(0, '.')
from main import map_category_to_group

# Lista de categorias para testar
test_categories = [
    ("Mini 4 Doors", "B1"),
    ("Mini", "B2"),
    ("Economy", "D"),
    ("Mini Automatic", "E1"),
    ("Economy Automatic", "E2"),
    ("SUV", "F"),
    ("Premium", "G"),
    ("Crossover", "J1"),
    ("Estate/Station Wagon", "J2"),
    ("SUV Automatic", "L1"),
    ("Station Wagon Automatic", "L2"),
    ("7 Seater", "M1"),
    ("7 Seater Automatic", "M2"),
    ("9 Seater", "N"),
    ("7 lugares", "M1"),
    ("7 lugares Automatic", "M2"),
    ("9 lugares", "N"),
    ("Unknown Category", "Others"),
]

print("=" * 60)
print("TESTE DE MAPEAMENTO DE GRUPOS")
print("=" * 60)
print()

all_passed = True

for category, expected_group in test_categories:
    result = map_category_to_group(category)
    status = "✅" if result == expected_group else "❌"
    
    if result != expected_group:
        all_passed = False
        print(f"{status} {category:30s} -> {result:10s} (esperado: {expected_group})")
    else:
        print(f"{status} {category:30s} -> {result}")

print()
print("=" * 60)

if all_passed:
    print("✅ TODOS OS TESTES PASSARAM!")
else:
    print("❌ ALGUNS TESTES FALHARAM!")

print("=" * 60)
print()

# Testar todos os grupos definidos
print("GRUPOS DEFINIDOS:")
print("-" * 60)
grupos_esperados = ["B1", "B2", "D", "E1", "E2", "F", "G", "J1", "J2", "L1", "L2", "M1", "M2", "N", "Others"]
print(f"Total: {len(grupos_esperados)} grupos")
print(f"Grupos: {', '.join(grupos_esperados)}")
print()

# Verificar se há grupos a mais na UI (os que causam problema)
print("GRUPOS PROBLEMÁTICOS (que devem ser mapeados):")
print("-" * 60)
problematic = [
    ("7 lugares", "M1"),
    ("9 lugares", "N"),
    ("7 lugares automático", "M2"),
]

for cat, expected in problematic:
    result = map_category_to_group(cat)
    status = "✅" if result == expected else "❌"
    print(f"{status} '{cat}' -> {result} (esperado: {expected})")
