#!/usr/bin/env python3
"""Gerar URL de Faro via POST direto"""
import asyncio
from playwright.async_api import async_playwright

async def get_faro_url():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print("Navegando e fazendo POST direto...")
        await page.goto("https://www.carjet.com/aluguel-carros/index.htm", wait_until="domcontentloaded")
        
        # Aceitar cookies
        try:
            await page.evaluate("try { document.getElementById('cookiesModal').style.display='none' } catch(e){}")
        except:
            pass
        
        # POST direto via evaluate
        await page.evaluate("""
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = 'https://www.carjet.com/do/list/pt';
            
            const fields = {
                'pickup': 'Faro Aeroporto (FAO)',
                'dropoff': 'Faro Aeroporto (FAO)',
                'fechaRecogida': '20/12/2025',
                'fechaEntrega': '25/12/2025',
                'fechaRecogidaSelHour': '10:00',
                'fechaEntregaSelHour': '10:00',
                'idioma': 'PT',
                'moneda': 'EUR',
                'chkOneWay': 'SI'
            };
            
            for (const [name, value] of Object.entries(fields)) {
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = name;
                input.value = value;
                form.appendChild(input);
            }
            
            document.body.appendChild(form);
            form.submit();
        """)
        
        print("Aguardando navegação...")
        try:
            await page.wait_for_load_state("networkidle", timeout=30000)
        except:
            pass
        
        await page.wait_for_timeout(5000)
        
        url = page.url
        html = await page.content()
        
        print(f"\n=== RESULTADO ===")
        print(f"URL: {url}")
        
        # Verificar tipo
        if '"hrental_pagetype": "list"' in html or '"hrental_pagetype": "results"' in html:
            print("✓ Página de resultados!")
        elif '"hrental_pagetype": "home"' in html:
            print("✗ Homepage (falhou)")
        
        # Contar carros
        cars = await page.locator("article.car, .newcarlist article").count()
        print(f"Carros: {cars}")
        
        # Screenshot
        try:
            await page.screenshot(path="/tmp/faro_results.png", full_page=True)
            print("Screenshot: /tmp/faro_results.png")
        except:
            pass
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(get_faro_url())
