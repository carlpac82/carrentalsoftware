#!/usr/bin/env python3
"""
Script para gerar URL s/b válida do CarJet para Faro
Uso: python3 gerar_url_faro.py
"""
import asyncio
from playwright.async_api import async_playwright
from datetime import datetime

async def gerar_url_faro():
    print("🚀 Iniciando geração de URL para Faro...")
    
    async with async_playwright() as p:
        # Usar Chromium com User-Agent Chrome
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            locale="pt-PT",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        )
        page = await context.new_page()
        
        # 1. Navegar para homepage
        print("📄 Carregando homepage CarJet...")
        await page.goto("https://www.carjet.com/aluguel-carros/index.htm", wait_until="domcontentloaded", timeout=45000)
        await page.wait_for_timeout(3000)
        
        # 2. Aceitar cookies de forma agressiva
        print("🍪 Aceitando cookies...")
        try:
            # Tentar múltiplos seletores
            for sel in [
                "#didomi-notice-agree-button",
                ".didomi-continue-without-agreeing", 
                "button:has-text('Aceitar')",
                "button:has-text('Accept')",
                "button:has-text('I agree')",
                "#cookiesModal button",
                ".cookies-container button",
            ]:
                try:
                    btn = page.locator(sel).first
                    if await btn.is_visible(timeout=1000):
                        await btn.click(timeout=2000)
                        await page.wait_for_timeout(500)
                        print(f"   ✓ Clicou em {sel}")
                        break
                except:
                    pass
        except:
            pass
        
        # Forçar fechar modais via JavaScript
        await page.evaluate("""
            try {
                document.querySelectorAll('#cookiesModal, .cookies-container, [id*=cookie], [class*=cookie]').forEach(el => {
                    el.style.display = 'none';
                    el.remove();
                });
            } catch(e) {}
        """)
        
        # 3. Preencher formulário com JavaScript (mais confiável)
        print("✍️  Preenchendo formulário Faro...")
        
        await page.evaluate("""
            // Função helper para preencher campo
            function fillField(selector, value) {
                const el = document.querySelector(selector);
                if (el) {
                    el.value = value;
                    el.dispatchEvent(new Event('input', {bubbles: true}));
                    el.dispatchEvent(new Event('change', {bubbles: true}));
                    return true;
                }
                return false;
            }
            
            // Preencher pickup/dropoff
            fillField('input[name="pickup"]', 'Faro Aeroporto (FAO)');
            fillField('input[name="dropoff"]', 'Faro Aeroporto (FAO)');
            
            // Preencher datas
            fillField('input[name="fechaRecogida"]', '20/12/2025');
            fillField('input[name="fechaEntrega"]', '25/12/2025');
            
            // Preencher horas - IMPORTANTE: Entrega 15:00 (CarJet valida)
            const horaRec = document.querySelector('select[name="fechaRecogidaSelHour"]');
            if (horaRec) horaRec.value = '10:00';
            
            const horaEnt = document.querySelector('select[name="fechaEntregaSelHour"]');
            if (horaEnt) horaEnt.value = '15:00';
            
            // Preencher hidden fields se existirem
            fillField('input[name="pickupId"]', '');
            fillField('input[name="idioma"]', 'PT');
            fillField('input[name="moneda"]', 'EUR');
        """)
        
        await page.wait_for_timeout(1000)
        
        # 4. Submeter formulário
        print("📤 Submetendo formulário...")
        
        # Tentar clicar no botão de submit
        submit_clicked = False
        for sel in [
            "button[type='submit']",
            "input[type='submit']",
            "button:has-text('Pesquisar')",
            "button:has-text('Buscar')",
            ".btn-submit",
        ]:
            try:
                btn = page.locator(sel).first
                if await btn.is_visible(timeout=1000):
                    await btn.click(timeout=3000)
                    submit_clicked = True
                    print(f"   ✓ Clicou em {sel}")
                    break
            except:
                pass
        
        # Fallback: submeter via JavaScript
        if not submit_clicked:
            print("   ⚠️  Botão não encontrado, submetendo via JS...")
            await page.evaluate("""
                const form = document.querySelector('form[name="menu_tarifas"], form');
                if (form) form.submit();
            """)
        
        # 5. Aguardar navegação
        print("⏳ Aguardando resultados...")
        try:
            await page.wait_for_url("**/do/list/**", timeout=40000)
        except:
            pass
        
        try:
            await page.wait_for_load_state("networkidle", timeout=30000)
        except:
            pass
        
        await page.wait_for_timeout(5000)
        
        # 6. Verificar resultado
        final_url = page.url
        html = await page.content()
        
        print("\n" + "="*60)
        print("📊 RESULTADO")
        print("="*60)
        print(f"\n🔗 URL: {final_url}\n")
        
        # Verificar tipo de página
        sucesso = False
        if 's=' in final_url and 'b=' in final_url:
            print("✅ URL s/b GERADA COM SUCESSO!")
            sucesso = True
        elif 'war=' in final_url:
            print("❌ ERRO: Redirecionado para homepage (war=X)")
            print(f"   Possível problema: formulário mal preenchido")
        elif final_url.endswith('/do/list/pt') or final_url.endswith('/do/list/pt/'):
            print("⚠️  URL sem parâmetros s/b")
        else:
            print("❓ URL inesperada")
        
        # Contar carros
        cars = await page.locator("article.car, .newcarlist article, section.newcarlist article").count()
        print(f"\n🚗 Carros encontrados: {cars}")
        
        if cars > 0:
            print("✅ Página de resultados válida!")
            sucesso = True
        
        # Tipo de página via JS
        try:
            page_type = await page.evaluate("""
                try {
                    return window.dataLayer?.find(d => d.hrental_pagetype)?.hrental_pagetype || 'unknown';
                } catch(e) { return 'unknown'; }
            """)
            print(f"📄 Tipo de página: {page_type}")
        except:
            pass
        
        # Screenshot para debug
        try:
            screenshot_path = "/tmp/faro_carjet.png"
            await page.screenshot(path=screenshot_path, full_page=True)
            print(f"📸 Screenshot: {screenshot_path}")
        except:
            pass
        
        print("\n" + "="*60)
        
        if sucesso:
            print("\n✅ SUCESSO! URL válida gerada.")
            print(f"\n   {final_url}\n")
        else:
            print("\n❌ FALHOU. Verifique o screenshot para debug.")
        
        await browser.close()
        
        return final_url if sucesso else None

if __name__ == "__main__":
    url = asyncio.run(gerar_url_faro())
    if url:
        print(f"\n💾 URL para usar:\n{url}")
    else:
        print("\n⚠️  Não foi possível gerar URL válida.")
