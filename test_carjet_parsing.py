#!/usr/bin/env python3
"""
Test CarJet URL parsing to debug missing results
URL: https://www.carjet.com/do/list/pt?s=0b423c17-68e5-4b1e-b244-362abf67048a&b=65049ac0-a180-4cde-a0ff-b5faf5c074af
"""

import requests
from bs4 import BeautifulSoup

# URL do CarJet fornecida
url = "https://www.carjet.com/do/list/pt?s=0b423c17-68e5-4b1e-b244-362abf67048a&b=65049ac0-a180-4cde-a0ff-b5faf5c074af"

print("[TEST] Fetching CarJet URL...")
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
}

try:
    resp = requests.get(url, headers=headers, timeout=30)
    print(f"[TEST] Status: {resp.status_code}")
    
    if resp.status_code == 200:
        html = resp.text
        soup = BeautifulSoup(html, 'lxml')
        
        # Contar cards diferentes
        card_selectors = [
            '.vehicle-card',
            '.car-card',
            '[class*="result"]',
            '[class*="vehicle"]',
            '[class*="offer"]',
            '.carProduct',
            '.listItem',
        ]
        
        print("\n[TEST] Tentando diferentes seletores de cards:")
        for selector in card_selectors:
            cards = soup.select(selector)
            if cards:
                print(f"  ✓ {selector}: {len(cards)} cards encontrados")
            else:
                print(f"  ✗ {selector}: 0 cards")
        
        # Tentar encontrar todos os preços
        print("\n[TEST] Procurando preços:")
        price_selectors = [
            '.price',
            '[class*="price"]',
            '[class*="Price"]',
            '.nfoPriceDest',
            '.nfoPrice',
        ]
        
        all_prices = set()
        for selector in price_selectors:
            elems = soup.select(selector)
            for elem in elems:
                text = elem.get_text(strip=True)
                if '€' in text or 'EUR' in text:
                    all_prices.add(text)
        
        print(f"  Total de preços únicos encontrados: {len(all_prices)}")
        if all_prices:
            print(f"  Exemplos: {list(all_prices)[:5]}")
        
        # Procurar nomes de carros
        print("\n[TEST] Procurando nomes de carros:")
        car_text = []
        for tag in soup.find_all(['h2', 'h3', 'h4', 'strong']):
            text = tag.get_text(strip=True)
            if len(text) > 5 and len(text) < 50:
                if any(brand in text.lower() for brand in ['fiat', 'renault', 'peugeot', 'toyota', 'ford', 'volkswagen', 'opel', 'seat', 'hyundai', 'kia', 'nissan']):
                    car_text.append(text)
        
        print(f"  Carros identificados: {len(car_text)}")
        if car_text:
            print(f"  Primeiros 10: {car_text[:10]}")
        
        # Salvar HTML para análise
        with open('/Users/filipepacheco/CascadeProjects/RentalPriceTrackerPerDay/carjet_test.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("\n[TEST] HTML salvo em carjet_test.html")
        
except Exception as e:
    print(f"[TEST] ERRO: {e}")
    import traceback
    traceback.print_exc()
