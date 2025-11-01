#!/usr/bin/env python3
"""
Script para gerar URLs válidas do CarJet para Albufeira
Executa Selenium para fazer scraping e extrair URLs s/b
"""
import os
import sys
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def generate_url(location, days_ahead=15, rental_days=7):
    """Gera URL válida do CarJet"""
    
    # Configurar Chrome
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    
    try:
        print(f"[1/5] Abrindo CarJet...")
        driver.get("https://www.carjet.com/pt")
        time.sleep(3)
        
        # Aceitar cookies se aparecer
        try:
            cookie_btn = driver.find_element(By.ID, "onetrust-accept-btn-handler")
            cookie_btn.click()
            time.sleep(1)
        except:
            pass
        
        print(f"[2/5] Preenchendo localização: {location}...")
        location_input = driver.find_element(By.ID, "pickup")
        location_input.clear()
        location_input.send_keys(location)
        time.sleep(2)
        
        # Selecionar primeira sugestão
        try:
            first_suggestion = driver.find_element(By.CSS_SELECTOR, ".ui-menu-item")
            first_suggestion.click()
            time.sleep(1)
        except:
            pass
        
        print(f"[3/5] Configurando datas...")
        # Data retirada
        pickup_date = datetime.now() + timedelta(days=days_ahead)
        pickup_str = pickup_date.strftime("%d/%m/%Y")
        
        date_input = driver.find_element(By.ID, "pickup_date")
        driver.execute_script(f"arguments[0].value = '{pickup_str}'", date_input)
        
        # Data devolução  
        dropoff_date = pickup_date + timedelta(days=rental_days)
        dropoff_str = dropoff_date.strftime("%d/%m/%Y")
        
        dropoff_input = driver.find_element(By.ID, "dropoff_date")
        driver.execute_script(f"arguments[0].value = '{dropoff_str}'", dropoff_input)
        
        time.sleep(1)
        
        print(f"[4/5] Submetendo formulário...")
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_btn.click()
        
        # Aguardar URL /do/list/pt
        print(f"[5/5] Aguardando resultados...")
        WebDriverWait(driver, 30).until(
            lambda d: "/do/list/pt" in d.current_url and ("?s=" in d.current_url or "?_" in d.current_url)
        )
        
        final_url = driver.current_url
        print(f"\n✅ URL GERADA:")
        print(f"{final_url}\n")
        
        return final_url
        
    finally:
        driver.quit()

if __name__ == "__main__":
    print("=" * 60)
    print("GERADOR DE URLs VÁLIDAS - CARJET")
    print("=" * 60)
    
    location = "Albufeira"
    rental_days = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    
    print(f"\nLocalização: {location}")
    print(f"Dias de aluguer: {rental_days}")
    print(f"Data retirada: +15 dias (para ter disponibilidade)")
    print()
    
    try:
        url = generate_url(location, days_ahead=15, rental_days=rental_days)
        
        # Sugerir linha para .env
        env_key = f"ALBUFEIRA_{rental_days}D"
        print(f"Adicionar ao .env:")
        print(f"{env_key}={url}")
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
