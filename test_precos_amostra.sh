#!/bin/bash
# Verificar amostra de preços para confirmar que estão corretos

echo "=========================================="
echo "AMOSTRA DE PREÇOS - Verificação"
echo "=========================================="

COOKIE=$(curl -s -c - -X POST http://localhost:8000/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123" | grep session | awk '{print $7}')

START_DATE=$(date -v+7d +%Y-%m-%d 2>/dev/null || date -d "+7 days" +%Y-%m-%d 2>/dev/null || echo "2025-02-05")

RESPONSE=$(curl -s -X POST http://localhost:8000/api/track-by-params \
  -H "Content-Type: application/json" \
  -H "Cookie: session=$COOKIE" \
  -d "{
    \"location\": \"Aeroporto de Faro\",
    \"start_date\": \"$START_DATE\",
    \"days\": 7,
    \"start_time\": \"15:00\",
    \"quick\": true
  }")

echo "$RESPONSE" | python3 -c "
import json, sys

try:
    data = json.load(sys.stdin)
    if data.get('ok'):
        items = data.get('items', [])
        
        print(f'Total items: {len(items)}\n')
        print('AMOSTRA DE 10 PREÇOS:')
        print('='*70)
        print(f'{\"Carro\":<35} {\"Grupo\":<6} {\"Preço\":>15}')
        print('-'*70)
        
        for i, item in enumerate(items[:10]):
            car = item.get('car', 'N/A').split('ou similar')[0][:35]
            group = item.get('group', 'N/A')
            price = item.get('price', 'N/A')
            print(f'{car:<35} {group:<6} {price:>15}')
        
        print('='*70)
        print('\nNOTA: Estes preços são para 7 dias em Faro')
        print('Se parecem diferentes do que esperavas, verifica:')
        print('  1. Estás a comparar o mesmo número de dias?')
        print('  2. Mesma localização (Faro/Albufeira)?')
        print('  3. Mesma data?')
        
    else:
        print(f\"Erro: {data.get('error')}\")
except Exception as e:
    print(f'Erro: {e}')
"
