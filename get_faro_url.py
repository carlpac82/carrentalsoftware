#!/usr/bin/env python3
"""Gerar URL s/b válida para Faro"""
import asyncio
from playwright.async_api import async_playwright
from datetime import datetime, timedelta

async def get_faro_url():
    print("Iniciando Playwright...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print("Navegando para CarJet...")
        await page.goto("https://www.carjet.com/aluguel-carros/index.htm", wait_until="networkidle", timeout=30000)
        
        # Aceitar cookies/consent
        try:
            for sel in [
                "#didomi-notice-agree-button",
                ".didomi-continue-without-agreeing",
                "button:has-text('Aceitar')",
                "button:has-text('Accept')",
                "#cookiesModal button.accept",
                ".cookies-container button",
            ]:
                try:
                    btn = page.locator(sel)
                    if await btn.count() > 0:
                        await btn.first.click(timeout=2000)
                        await page.wait_for_timeout(500)
                        break
                except:
                    pass
        except:
            pass
        
        # Forçar fechar modal cookies via JavaScript
        try:
            await page.evaluate("""
                try {
                    const modal = document.getElementById('cookiesModal');
                    if (modal) modal.style.display = 'none';
                    document.querySelectorAll('.cookies-container').forEach(el => el.style.display = 'none');
                } catch(e) {}
            """)
        except:
            pass
        
        print("Preenchendo formulário Faro...")
        
        # Preencher local
        try:
            loc = await page.query_selector("input[name='pickup']")
            if loc:
                await loc.click()
                await loc.fill("")
                await loc.type("Faro", delay=100)
                await page.wait_for_timeout(1500)
                
                # Clicar na opção aeroporto
                opts = await page.query_selector_all(".ui-menu-item")
                for opt in opts:
                    text = await opt.inner_text()
                    if "aeroporto" in text.lower() or "fao" in text.lower():
                        print(f"Selecionando: {text}")
                        await opt.click()
                        break
                
                await page.wait_for_timeout(1000)
        except Exception as e:
            print(f"Erro local: {e}")
        
        # Preencher datas (20/12 a 25/12)
        try:
            start = datetime(2025, 12, 20, 10, 0)
            end = datetime(2025, 12, 25, 10, 0)
            
            # Datas
            fecha_rec = await page.query_selector("input[name='fechaRecogida']")
            if fecha_rec:
                await fecha_rec.fill(start.strftime('%d/%m/%Y'))
            
            fecha_ent = await page.query_selector("input[name='fechaEntrega']")
            if fecha_ent:
                await fecha_ent.fill(end.strftime('%d/%m/%Y'))
            
            # Horas
            hora_rec = await page.query_selector("input[name='fechaRecogidaSelHour']")
            if hora_rec:
                await hora_rec.select_option("10:00")
            
            hora_ent = await page.query_selector("input[name='fechaEntregaSelHour']")
            if hora_ent:
                await hora_ent.select_option("10:00")
            
            await page.wait_for_timeout(500)
        except Exception as e:
            print(f"Erro datas: {e}")
        
        # Submeter
        print("Submetendo formulário...")
        try:
            submit = await page.query_selector("button[type='submit'], input[type='submit']")
            if submit:
                await submit.click()
                await page.wait_for_load_state("networkidle", timeout=40000)
            
            # Aguardar URL s/b
            await page.wait_for_timeout(3000)
            
            final_url = page.url
            print(f"\n=== URL GERADA ===")
            print(final_url)
            print(f"\nTipo de página: ", end="")
            
            # Verificar se chegou aos resultados
            html = await page.content()
            if "hrental_pagetype" in html:
                if '"home"' in html:
                    print("HOME (falhou)")
                elif '"list"' in html or '"results"' in html:
                    print("RESULTADOS (sucesso!)")
                else:
                    print("Desconhecido")
            
            # Contar carros
            cars = await page.locator("article.car, .newcarlist article, .car-item").count()
            print(f"Carros encontrados: {cars}")
            
        except Exception as e:
            print(f"Erro submit: {e}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(get_faro_url())
