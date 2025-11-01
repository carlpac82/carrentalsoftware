#!/usr/bin/env python3
import requests
import json

# Login
session = requests.Session()
login_url = "https://carrental-api-5f8q.onrender.com/login"
export_url = "https://carrental-api-5f8q.onrender.com/admin/export-vehicles-json"

# Fazer login (use suas credenciais)
print("Fazendo login...")
login_data = {
    "username": "admin",
    "password": "admin"
}

response = session.post(login_url, data=login_data, allow_redirects=True)
print(f"Login status: {response.status_code}")

# Baixar dados
print("Baixando veículos...")
response = session.get(export_url)
print(f"Export status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    
    # Salvar em arquivo
    with open("vehicles_backup.json", "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Baixado {data.get('count', 0)} veículos!")
    print("Arquivo salvo: vehicles_backup.json")
else:
    print(f"❌ Erro: {response.text}")
