#!/bin/bash
# Testar o que a API retorna para a URL problemática

echo "==================================="
echo "TESTE API - Preço Fiat 500 Cabrio"
echo "==================================="

# Login
COOKIE=$(curl -s -c - -X POST http://localhost:8000/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123" | grep session | awk '{print $7}')

echo "✓ Login OK"
echo ""

# Testar com a URL problemática
URL="https://www.carjet.com/do/list/pt?s=9cd340ac-f710-4a33-aa26-3622ea8b171a&b=ca0dd8d7-db7e-415c-8f76-0440d17ca196"

echo "📍 URL: ${URL:0:80}..."
echo ""

# Chamar API
RESPONSE=$(curl -s -X POST http://localhost:8000/api/track-by-url \
  -H "Content-Type: application/json" \
  -H "Cookie: session=$COOKIE" \
  -d "{\"url\": \"$URL\"}")

echo "RESULTADO:"
echo "$RESPONSE" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    if data.get('ok'):
        items = data.get('items', [])
        print(f'Total items: {len(items)}\n')
        
        # Procurar Fiat 500 Cabrio
        for item in items:
            car = item.get('car', '').lower()
            if 'fiat 500' in car and 'cabrio' in car:
                print('🚗 FIAT 500 CABRIO ENCONTRADO!')
                print(f'  Supplier: {item.get(\"supplier\", \"N/A\")}')
                print(f'  Car: {item.get(\"car\", \"N/A\")}')
                print(f'  Price: {item.get(\"price\", \"N/A\")}')
                print(f'  Category: {item.get(\"category\", \"N/A\")}')
                print(f'  Group: {item.get(\"group\", \"N/A\")}')
                print(f'  Currency: {item.get(\"currency\", \"N/A\")}')
                print(f'  Transmission: {item.get(\"transmission\", \"N/A\")}')
                print()
                break
        else:
            print('⚠️  Fiat 500 Cabrio NÃO encontrado!')
            print('\nPrimeiros 3 carros:')
            for i, item in enumerate(items[:3], 1):
                print(f'{i}. {item.get(\"car\", \"N/A\")} - {item.get(\"price\", \"N/A\")} ({item.get(\"supplier\", \"N/A\")})')
    else:
        print(f'❌ Erro: {data.get(\"error\")}')
except Exception as e:
    print(f'❌ Erro ao parsear: {e}')
    import traceback
    traceback.print_exc()
"

echo ""
echo "==================================="
