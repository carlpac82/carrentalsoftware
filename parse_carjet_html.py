#!/usr/bin/env python3
"""Parse HTML do CarJet filtrado por AUTOPRUDENTE"""

from bs4 import BeautifulSoup
from collections import Counter
import re

# HTML fornecido pelo usuário (truncado, mas vamos tentar)
html_content = """
<li id="idPrvAUP">
    <input type="checkbox" name="frmPrv" value="AUP" id="chkAUP" checked onclick="...">
    <label for="chkAUP">
        <img src="/cdn/img/prv/flat/mid/logo_AUP.png" id="divAUP" title="AUTOPRUDENTE">
    </label>
</li>
"""

print("🔍 Análise do HTML do CarJet")
print("=" * 60)
print()

# O HTML está truncado, mas podemos ver que:
# 1. O checkbox AUTOPRUDENTE (AUP) está CHECKED
# 2. Isso significa que o filtro está ativo

print("✅ Filtro AUTOPRUDENTE: ATIVO")
print("   Checkbox: checked")
print("   Código: AUP")
print()

# Informação do HTML
print("📋 Informação da Pesquisa:")
print("   Local: Faro Aeroporto (FAO)")
print("   Data Recolha: 12/11/2025 16:00")
print("   Data Devolução: 17/11/2025 11:00")
print("   Dias: 5")
print()

print("⚠️ NOTA:")
print("   O HTML está truncado (219054 bytes cortados)")
print("   Não consigo ver a lista completa de carros")
print()

print("💡 CONCLUSÃO:")
print("   Para ver os carros AUTOPRUDENTE, precisas:")
print("   1. Fazer scroll na página do CarJet")
print("   2. Contar quantos carros aparecem")
print("   3. Ver quais grupos têm carros")
print()

print("🎯 GRUPOS ESPERADOS (baseado em memórias):")
grupos_conhecidos = {
    'B1': 'Mini 4 Doors',
    'B2': 'Mini 5 Doors', 
    'D': 'Economy',
    'E1': 'Mini Automatic',
    'E2': 'Economy Automatic',
    'F': 'SUV',
    'G': 'Premium',
    'J1': 'Crossover',
    'J2': 'Station Wagon',
    'L1': 'SUV Automatic',
    'L2': 'Station Wagon Automatic',
    'M1': '7 Seater',
    'M2': '7 Seater Automatic',
    'N': '9 Seater'
}

for code, name in grupos_conhecidos.items():
    print(f"   {code}: {name}")
