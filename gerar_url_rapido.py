#!/usr/bin/env python3
"""Gerar URL s/b rapidamente via Playwright"""
import asyncio
import sys
from playwright.async_api import async_playwright
from datetime import datetime

async def gerar_url(location, start_date, days):
    """Gera URL s/b para CarJet"""
    try:
        from datetime import timedelta
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = start + timedelta(days=days)
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # Navegar
            await page.goto("https://www.carjet.com/aluguel-carros/index.htm", wait_until="domcontentloaded", timeout=20000)
            
            # Fechar cookies via JS
            await page.evaluate("try { document.querySelectorAll('[id*=cookie], [class*=cookie]').forEach(el => el.remove()); } catch(e) {}")
            
            # Preencher via JS
            js_code = """
                (params) => {
                    function fill(sel, val) {
                        const el = document.querySelector(sel);
                        if (el) { el.value = val; el.dispatchEvent(new Event('change', {bubbles: true})); }
                    }
                    fill('input[name="pickup"]', params.loc);
                    fill('input[name="dropoff"]', params.loc);
                    fill('input[name="fechaRecogida"]', params.start);
                    fill('input[name="fechaEntrega"]', params.end);
                    const h1 = document.querySelector('select[name="fechaRecogidaSelHour"]');
                    const h2 = document.querySelector('select[name="fechaEntregaSelHour"]');
                    if (h1) h1.value = '10:00';
                    if (h2) h2.value = '10:00';
                }
            """
            await page.evaluate(js_code, {
                'loc': location,
                'start': start.strftime("%d/%m/%Y"),
                'end': end.strftime("%d/%m/%Y")
            })
            
            await page.wait_for_timeout(500)
            
            # Submit
            await page.evaluate("document.querySelector('form').submit();")
            await page.wait_for_timeout(8000)
            
            url = page.url
            await browser.close()
            
            if 's=' in url and 'b=' in url:
                return url
            return None
            
    except Exception as e:
        print(f"Erro: {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 4:
        print("Uso: python3 gerar_url_rapido.py LOCATION START_DATE DAYS")
        print("Ex: python3 gerar_url_rapido.py 'Faro Aeroporto (FAO)' 2025-12-20 5")
        sys.exit(1)
    
    loc = sys.argv[1]
    date = sys.argv[2]
    days = int(sys.argv[3])
    
    url = asyncio.run(gerar_url(loc, date, days))
    if url:
        print(url)
    else:
        sys.exit(1)
