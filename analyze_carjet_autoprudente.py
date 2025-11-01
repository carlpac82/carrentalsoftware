#!/usr/bin/env python3
"""Analisar HTML do CarJet para ver carros AUTOPRUDENTE e seus preços"""

from bs4 import BeautifulSoup
import re
import sys

# Ler HTML do stdin ou arquivo
html_file = "/Users/filipepacheco/CascadeProjects/RentalPriceTrackerPerDay/carjet_autoprudente.html"

try:
    with open(html_file, 'r', encoding='utf-8') as f:
        html = f.read()
except FileNotFoundError:
    print(f"❌ Ficheiro não encontrado: {html_file}")
    print()
    print("💡 Como usar:")
    print("   1. Abre o CarJet com filtro AUTOPRUDENTE")
    print("   2. Clica direito → Guardar como → carjet_autoprudente.html")
    print("   3. Corre este script novamente")
    sys.exit(1)

soup = BeautifulSoup(html, 'html.parser')

print("🔍 ANÁLISE CARJET - AUTOPRUDENTE")
print("=" * 70)
print()

# Procurar carros na lista
cars = soup.select('section.newcarlist article, .newcarlist article, article.car')

print(f"📊 Total de artigos encontrados: {len(cars)}")
print()

if len(cars) == 0:
    print("⚠️  Nenhum carro encontrado no HTML!")
    print()
    print("Possíveis causas:")
    print("  - HTML truncado")
    print("  - Seletores CSS incorretos")
    print("  - Página não carregou completamente")
    sys.exit(1)

# Analisar cada carro
carros_autoprudente = []

for i, car in enumerate(cars, 1):
    try:
        # Nome do carro
        name_el = car.select_one('.veh-name, .vehicle-name, .model, .titleCar, .title, h3, h2')
        car_name = name_el.get_text(strip=True) if name_el else "N/A"
        
        # Supplier
        supplier = ""
        # Tentar logo alt
        logo_img = car.select_one('img[alt*="logo"], img[alt*="Logo"], img[src*="logo_"]')
        if logo_img:
            supplier = logo_img.get('alt', '').strip()
        
        if not supplier:
            sup_el = car.select_one('.supplier, .vendor, .partner, [class*="supplier"], [class*="vendor"]')
            supplier = sup_el.get_text(strip=True) if sup_el else ""
        
        # Categoria/Grupo
        cat_el = car.select_one('.category, .group, .vehicle-category, [class*="category"], [class*="group"]')
        category = cat_el.get_text(strip=True) if cat_el else ""
        
        # Preço
        card_text = car.get_text(strip=True)
        
        # Procurar "Preço por X dias"
        price_match = re.search(r'preço\s*por\s*\d+\s*dias[^\n€]*([€\s]*[0-9][0-9\.,]+)\s*€?', card_text, re.I)
        if price_match:
            price = price_match.group(1).strip()
            if '€' not in price:
                price += ' €'
        else:
            # Procurar qualquer valor em euros
            euros = re.findall(r'([0-9]+[,\.][0-9]{2})\s*€', card_text)
            price = euros[-1] + ' €' if euros else "N/A"
        
        # Verificar se é AUTOPRUDENTE
        is_autoprudente = (
            'autoprudente' in supplier.lower() or
            'auto prudente' in supplier.lower() or
            'auto-prudente' in supplier.lower() or
            supplier.upper() == 'AUP'
        )
        
        if is_autoprudente:
            carros_autoprudente.append({
                'nome': car_name,
                'categoria': category,
                'preco': price,
                'supplier': supplier
            })
            
            print(f"{len(carros_autoprudente)}. {car_name}")
            print(f"   Categoria: {category}")
            print(f"   Preço: {price}")
            print(f"   Supplier: {supplier}")
            print()
            
    except Exception as e:
        print(f"⚠️  Erro ao processar carro {i}: {e}")
        continue

print("=" * 70)
print(f"✅ Total AUTOPRUDENTE: {len(carros_autoprudente)} carros")
print()

# Agrupar por categoria
from collections import Counter
categorias = Counter([c['categoria'] for c in carros_autoprudente if c['categoria']])

if categorias:
    print("📋 Distribuição por Categoria:")
    for cat, count in categorias.most_common():
        print(f"   {cat}: {count} carros")
else:
    print("⚠️  Nenhuma categoria encontrada!")
    print("   Isto significa que os carros não têm categoria no HTML")
    print("   Ou o seletor CSS está errado")

print()
print("💡 PRÓXIMO PASSO:")
print("   Compara estas categorias com os grupos da automação")
print("   Se não houver categorias, precisamos melhorar o scraping")
