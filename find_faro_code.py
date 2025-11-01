#!/usr/bin/env python3
"""Script para descobrir o código correto de Faro no CarJet"""
import asyncio
from playwright.async_api import async_playwright

async def find_faro_code():
    print("Iniciando Playwright...")
    async with async_playwright() as p:
        print("Lançando browser...")
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Ir para homepage
        await page.goto("https://www.carjet.com/aluguel-carros/index.htm")
        await page.wait_for_timeout(2000)
        
        # Preencher campo de local
        try:
            loc_input = await page.query_selector("input[name='pickup']")
            if loc_input:
                await loc_input.click()
                await loc_input.fill("")
                await loc_input.type("Faro", delay=100)
                await page.wait_for_timeout(1500)
                
                # Capturar dropdown options
                print("\n=== Opções de Autocomplete ===")
                options = await page.query_selector_all(".ui-menu-item")
                for i, opt in enumerate(options[:10]):
                    text = await opt.inner_text()
                    print(f"{i+1}. {text}")
                
                # Clicar na primeira opção do aeroporto
                for opt in options:
                    text = await opt.inner_text()
                    if "aeroporto" in text.lower() or "airport" in text.lower():
                        print(f"\nSelecionando: {text}")
                        await opt.click()
                        break
                
                await page.wait_for_timeout(1000)
                
                # Extrair código do campo hidden
                pickup_id = await page.evaluate("document.querySelector('input[name=pickupId]')?.value")
                dst_id = await page.evaluate("document.querySelector('input[name=dst_id]')?.value")
                zone_code = await page.evaluate("() => { try { return zoneCode || ''; } catch { return ''; } }")
                
                print(f"\n=== Códigos Encontrados ===")
                print(f"pickupId: {pickup_id}")
                print(f"dst_id: {dst_id}")
                print(f"zoneCode: {zone_code}")
                
        except Exception as e:
            print(f"Erro: {e}")
        
        await page.wait_for_timeout(3000)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(find_faro_code())
