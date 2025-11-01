#!/usr/bin/env python3
"""Script para verificar carros AUTOPRUDENTE no CarJet"""

import requests
from bs4 import BeautifulSoup
from collections import Counter

# URL do CarJet fornecida pelo usuário
url = "https://www.carjet.com/do/list/pt?s=512a1ac5-8270-4643-913e-2aa0aef3dd20&b=d452abe6-1de3-4951-9103-97e795e8adcb"

print(f"🔍 Fazendo scraping de: {url}\n")

# Fazer request
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# Procurar por cards de carros
cards = soup.find_all('article', class_='car') or soup.find_all('div', class_='car-item') or soup.find_all('li', class_='result')

print(f"📊 Total de cards encontrados: {len(cards)}\n")

# Procurar por AUTOPRUDENTE
autoprudente_cars = []
all_suppliers = []

for card in cards:
    # Procurar supplier
    supplier_img = card.find('img', src=lambda x: x and 'logo_' in x if x else False)
    supplier_text = card.find(text=lambda t: 'autoprudente' in t.lower() if t else False)
    
    supplier = None
    if supplier_img and 'alt' in supplier_img.attrs:
        supplier = supplier_img['alt']
    elif supplier_img and 'src' in supplier_img.attrs:
        # Extrair do src: /cdn/img/prv/flat/mid/logo_AUP.png
        src = supplier_img['src']
        if 'logo_' in src:
            code = src.split('logo_')[1].split('.')[0]
            supplier = code
    elif supplier_text:
        supplier = "AUTOPRUDENTE"
    
    if supplier:
        all_suppliers.append(supplier)
        
        # Verificar se é AUTOPRUDENTE
        if 'autoprudente' in supplier.lower() or supplier.upper() == 'AUP':
            # Procurar nome do carro
            car_name = card.find('h3') or card.find('h2') or card.find(class_='car-name')
            car_name = car_name.get_text(strip=True) if car_name else "Desconhecido"
            
            # Procurar preço
            price = card.find(class_='price') or card.find(class_='amount')
            price = price.get_text(strip=True) if price else "N/A"
            
            autoprudente_cars.append({
                'car': car_name,
                'price': price,
                'supplier': supplier
            })

print(f"🚗 Carros AUTOPRUDENTE encontrados: {len(autoprudente_cars)}\n")

if autoprudente_cars:
    print("=" * 60)
    for i, car in enumerate(autoprudente_cars, 1):
        print(f"{i}. {car['car']}")
        print(f"   Supplier: {car['supplier']}")
        print(f"   Preço: {car['price']}")
        print("-" * 60)
else:
    print("❌ Nenhum carro AUTOPRUDENTE encontrado!\n")

# Mostrar todos os suppliers únicos
print("\n📋 Todos os suppliers encontrados:")
supplier_counts = Counter(all_suppliers)
for supplier, count in supplier_counts.most_common():
    mark = "✅" if 'autoprudente' in supplier.lower() or supplier.upper() == 'AUP' else ""
    print(f"  {mark} {supplier}: {count} carros")

print(f"\n✅ Total de suppliers únicos: {len(supplier_counts)}")
print(f"✅ Total de carros: {len(all_suppliers)}")
