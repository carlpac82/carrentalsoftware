#!/usr/bin/env python3
"""Testar seletores Playwright para AUTOPRUDENTE"""

import sys
import re
from playwright.sync_api import sync_playwright

print("🧪 TESTE SELETORES PLAYWRIGHT - AUTOPRUDENTE")
print("=" * 70)
print()

# URL do CarJet com AUTOPRUDENTE filtrado
url = "https://www.carjet.com/do/list/pt?s=512a1ac5-8270-4643-913e-2aa0aef3dd20&b=d452abe6-1de3-4951-9103-97e795e8adcb"

print(f"📍 URL: {url}")
print()
print("🔄 Abrindo navegador...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # headless=False para ver
    context = browser.new_context(locale="pt-PT")
    page = context.new_page()
    
    print("🌐 Navegando para CarJet...")
    page.goto(url, wait_until="networkidle", timeout=60000)
    
    print("⏳ Aguardando 3 segundos...")
    page.wait_for_timeout(3000)
    
    # Clicar no filtro AUTOPRUDENTE
    print("🔍 Procurando checkbox AUTOPRUDENTE...")
    try:
        # Desmarcar todos primeiro
        page.evaluate("""
            document.querySelectorAll('input[name="frmPrv"]').forEach(cb => {
                if (cb.checked) cb.click();
            });
        """)
        page.wait_for_timeout(500)
        
        # Marcar apenas AUTOPRUDENTE
        aup_checkbox = page.query_selector('#chkAUP')
        if aup_checkbox:
            if not aup_checkbox.is_checked():
                aup_checkbox.click()
                print("✅ Checkbox AUTOPRUDENTE clicado")
                page.wait_for_load_state("networkidle", timeout=10000)
            else:
                print("✅ Checkbox AUTOPRUDENTE já estava marcado")
        else:
            print("❌ Checkbox AUTOPRUDENTE não encontrado!")
    except Exception as e:
        print(f"⚠️  Erro ao clicar checkbox: {e}")
    
    print()
    print("🔍 Procurando artigos de carros...")
    
    # Procurar artigos
    articles = page.query_selector_all("section.newcarlist article")
    print(f"📊 Encontrados {len(articles)} artigos")
    print()
    
    if len(articles) == 0:
        print("❌ NENHUM ARTIGO ENCONTRADO!")
        print()
        print("Possíveis causas:")
        print("  - Seletor CSS errado")
        print("  - Página não carregou")
        print("  - Filtro AUTOPRUDENTE não funcionou")
        
        # Tentar outros seletores
        print()
        print("🔍 Tentando outros seletores...")
        alt_selectors = [
            "article",
            ".newcarlist article",
            "article.car",
            "[data-car]",
            ".car-item"
        ]
        for sel in alt_selectors:
            count = len(page.query_selector_all(sel))
            print(f"  {sel}: {count} elementos")
        
        browser.close()
        sys.exit(1)
    
    # Analisar primeiro artigo em detalhe
    print("🔍 ANÁLISE DETALHADA DO PRIMEIRO CARRO:")
    print("-" * 70)
    
    first = articles[0]
    
    # Nome do carro
    print("\n1️⃣ NOME DO CARRO:")
    name_selectors = [
        ".titleCar",
        ".veh-name",
        ".vehicle-name",
        ".model",
        ".title",
        "h3",
        "h2"
    ]
    for sel in name_selectors:
        el = first.query_selector(sel)
        if el:
            text = el.inner_text().strip()
            print(f"  ✅ {sel}: '{text}'")
            break
    else:
        print("  ❌ Nome não encontrado!")
    
    # Preço
    print("\n2️⃣ PREÇO:")
    price_selectors = [
        ".nfoPriceDest",
        ".pr-euros",
        ".price.pr-euros",
        ".price",
        ".amount"
    ]
    for sel in price_selectors:
        el = first.query_selector(sel)
        if el:
            text = el.inner_text().strip()
            print(f"  ✅ {sel}: '{text}'")
        else:
            print(f"  ❌ {sel}: não encontrado")
    
    # Supplier
    print("\n3️⃣ SUPPLIER:")
    
    # Procurar logo
    logo = first.query_selector("img[src*='/prv/'], img[src*='logo_']")
    if logo:
        src = logo.get_attribute("src") or ""
        alt = logo.get_attribute("alt") or ""
        print(f"  ✅ Logo encontrado:")
        print(f"     src: {src}")
        print(f"     alt: {alt}")
        
        # Extrair código
        match = re.search(r'logo_([A-Z0-9]+)', src)
        if match:
            code = match.group(1)
            print(f"     código: {code}")
    else:
        print("  ❌ Logo não encontrado!")
        
        # Tentar outros seletores
        alt_imgs = first.query_selector_all("img")
        print(f"  ℹ️  Total de imagens: {len(alt_imgs)}")
        for img in alt_imgs[:3]:
            src = img.get_attribute("src") or ""
            alt = img.get_attribute("alt") or ""
            print(f"     - src: {src[:50]}... alt: {alt}")
    
    # Categoria
    print("\n4️⃣ CATEGORIA/GRUPO:")
    cat_selectors = [
        ".category",
        ".grupo",
        "[class*='category']",
        "[class*='grupo']"
    ]
    for sel in cat_selectors:
        el = first.query_selector(sel)
        if el:
            text = el.inner_text().strip()
            print(f"  ✅ {sel}: '{text}'")
            break
    else:
        print("  ❌ Categoria não encontrada!")
        
        # Procurar no texto
        card_text = first.inner_text()
        match = re.search(r'grupo\s+([A-Z][0-9]?)', card_text, re.I)
        if match:
            print(f"  ✅ Regex encontrou: 'Grupo {match.group(1)}'")
        else:
            print("  ❌ Regex não encontrou grupo")
    
    # Texto completo do card
    print("\n5️⃣ TEXTO COMPLETO DO CARD:")
    print("-" * 70)
    card_text = first.inner_text()
    print(card_text[:500])
    if len(card_text) > 500:
        print(f"\n... (truncado, total: {len(card_text)} caracteres)")
    
    print()
    print("=" * 70)
    print("✅ Teste concluído!")
    print()
    print("💡 Próximo passo:")
    print("   Verifica os seletores que funcionaram")
    print("   e ajusta o código do scraping")
    
    input("\n⏸️  Pressiona ENTER para fechar o navegador...")
    browser.close()
