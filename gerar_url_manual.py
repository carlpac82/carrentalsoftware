#!/usr/bin/env python3
"""
Script para MANUAL gerar URLs do CarJet
O browser abre VISÍVEL para tu submeteres o formulário
"""
import asyncio
from playwright.async_api import async_playwright
from datetime import datetime, timedelta

async def gerar_urls_manual():
    print("\n" + "="*70)
    print("🔧 MODO MANUAL - Browser Visível")
    print("="*70)
    print("\n📋 INSTRUÇÕES:")
    print("1. Browser vai abrir VISÍVEL")
    print("2. Preenche o formulário MANUALMENTE:")
    print("   - Local: Aeroporto de Faro")
    print("   - Datas: Qualquer data futura")
    print("   - Horário: 10:00")
    print("3. Clica em 'Pesquisar'")
    print("4. AGUARDA os resultados carregarem")
    print("5. Copia a URL que aparece")
    print("\n6. REPETE para Albufeira")
    print("\n⏳ A abrir browser em 3 segundos...\n")
    await asyncio.sleep(3)
    
    async with async_playwright() as p:
        # Browser VISÍVEL (headless=False)
        browser = await p.chromium.launch(
            headless=False,
            slow_mo=500  # Mais lento para veres
        )
        context = await browser.new_context(
            locale="pt-PT",
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        )
        page = await context.new_page()
        
        # === FARO ===
        print("\n" + "="*70)
        print("🏁 PASSO 1: FARO")
        print("="*70)
        
        await page.goto("https://www.carjet.com/aluguel-carros/index.htm", wait_until="domcontentloaded")
        print("✅ Página CarJet carregada")
        print("\n🟢 AÇÃO: Preenche formulário MANUALMENTE para FARO")
        print("   - Pickup: Aeroporto de Faro (ou Faro Aeroporto FAO)")
        print("   - Dropoff: Mesmo local")
        print("   - Data: Qualquer data futura (ex: 7 dias à frente)")
        print("   - Horário: 10:00")
        print("\n⏸️  DEPOIS de clicar 'Pesquisar', AGUARDA a página carregar...")
        print("   Quando vires os carros, COPIA a URL do browser")
        print("\n⌨️  Prima ENTER depois de copiar a URL de FARO...")
        input()
        
        faro_url = page.url
        print(f"\n📋 URL de Faro capturada:")
        print(f"   {faro_url}")
        
        # Verificar se é válida
        if 's=' in faro_url and 'b=' in faro_url:
            print("   ✅ URL válida!")
        else:
            print("   ⚠️  URL pode não ter parâmetros s/b")
        
        # === ALBUFEIRA ===
        print("\n" + "="*70)
        print("🏖️  PASSO 2: ALBUFEIRA")
        print("="*70)
        
        await page.goto("https://www.carjet.com/aluguel-carros/index.htm", wait_until="domcontentloaded")
        print("✅ Página CarJet recarregada")
        print("\n🟢 AÇÃO: Preenche formulário MANUALMENTE para ALBUFEIRA")
        print("   - Pickup: Albufeira")
        print("   - Dropoff: Albufeira")
        print("   - Data: MESMA data que usaste para Faro")
        print("   - Horário: 10:00")
        print("\n⏸️  DEPOIS de clicar 'Pesquisar', AGUARDA a página carregar...")
        print("   Quando vires os carros, COPIA a URL do browser")
        print("\n⌨️  Prima ENTER depois de copiar a URL de ALBUFEIRA...")
        input()
        
        albufeira_url = page.url
        print(f"\n📋 URL de Albufeira capturada:")
        print(f"   {albufeira_url}")
        
        # Verificar se é válida
        if 's=' in albufeira_url and 'b=' in albufeira_url:
            print("   ✅ URL válida!")
        else:
            print("   ⚠️  URL pode não ter parâmetros s/b")
        
        # === RESULTADO ===
        print("\n" + "="*70)
        print("📊 RESULTADO FINAL")
        print("="*70)
        
        print(f"\n🏁 FARO:")
        print(f"   {faro_url}")
        
        print(f"\n🏖️  ALBUFEIRA:")
        print(f"   {albufeira_url}")
        
        print("\n" + "="*70)
        print("💾 PRÓXIMO PASSO: Atualizar .env")
        print("="*70)
        print("\nCopia as linhas abaixo para o ficheiro .env:")
        print()
        print("TEST_MODE_LOCAL=1")
        print(f'TEST_FARO_URL={faro_url}')
        print(f'TEST_ALBUFEIRA_URL={albufeira_url}')
        print()
        
        await browser.close()
        
        return faro_url, albufeira_url

if __name__ == "__main__":
    try:
        asyncio.run(gerar_urls_manual())
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrompido pelo utilizador")
