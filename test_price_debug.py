#!/usr/bin/env python3
"""
Test script to debug price parsing from CarJet URL
"""
import sys
import requests
from bs4 import BeautifulSoup

def debug_prices(url: str):
    """
    Fetch HTML and show ALL price elements found
    """
    print(f"📍 Fetching: {url}\n")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    resp = requests.get(url, headers=headers, timeout=30)
    html = resp.text
    
    soup = BeautifulSoup(html, "lxml")
    
    print("=" * 80)
    print("TODOS OS ELEMENTOS COM PREÇOS ENCONTRADOS:")
    print("=" * 80)
    
    # Tentar vários seletores
    selectors = [
        ".price",
        ".amount",
        "[class*='price']",
        ".nfoPriceDest",
        ".nfoPrice",
        "[data-price]",
        ".pr-euros",
        ".pr-libras",
        ".price-euros",
        ".price.pr-euros"
    ]
    
    for selector in selectors:
        elements = soup.select(selector)
        if elements:
            print(f"\n🔍 Seletor '{selector}' ({len(elements)} encontrados):")
            for idx, el in enumerate(elements[:5], 1):  # Mostrar primeiros 5
                text = el.get_text(strip=True)
                classes = el.get('class', [])
                print(f"  {idx}. '{text}' (classes: {classes})")
    
    print("\n" + "=" * 80)
    print("ANÁLISE DE CARDS/ARTIGOS:")
    print("=" * 80)
    
    # Procurar cards de carros
    cards = soup.select("section.newcarlist article, .newcarlist article, article.car, li.result")
    print(f"\nEncontrados {len(cards)} cards\n")
    
    for idx, card in enumerate(cards[:3], 1):  # Primeiros 3 cards
        print(f"\n--- CARD {idx} ---")
        
        # Nome do carro
        name_el = card.select_one(".veh-name, .vehicle-name, .model, .titleCar")
        car_name = name_el.get_text(strip=True) if name_el else "N/A"
        print(f"Carro: {car_name}")
        
        # TODOS os preços neste card
        price_els = card.select(".price, .amount, [class*='price']")
        print(f"Preços encontrados neste card ({len(price_els)}):")
        for p_idx, p_el in enumerate(price_els, 1):
            text = p_el.get_text(strip=True)
            classes = p_el.get('class', [])
            print(f"  {p_idx}. '{text}' (classes: {classes})")
        
        # Supplier
        supplier_imgs = card.select("img[src*='logo_']")
        if supplier_imgs:
            for img in supplier_imgs[:1]:
                src = img.get('src', '')
                print(f"Supplier logo: {src}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python test_price_debug.py <URL_CARJET>")
        print("\nExemplo:")
        print("python test_price_debug.py 'https://www.carjet.com/do/list/pt?s=...&b=...'")
        sys.exit(1)
    
    url = sys.argv[1]
    debug_prices(url)
