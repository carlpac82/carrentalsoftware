#!/bin/bash
# Ver quais carros estão na categoria MINI

echo "=========================================="
echo "CARROS NA CATEGORIA 'MINI 5 Portas'"
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
        
        # Filtrar MINI 5 Portas
        mini_5 = [item for item in items if 'MINI 5 Portas' in item.get('category', '')]
        
        print(f'Total MINI 5 Portas: {len(mini_5)}\n')
        print('Carro → Grupo Atual')
        print('-' * 60)
        
        # Mostrar carros únicos
        cars_seen = set()
        for item in mini_5:
            car = item.get('car', 'N/A')
            # Limpar nome
            car_clean = car.split('ou similar')[0].strip()
            if car_clean not in cars_seen:
                cars_seen.add(car_clean)
                group = item.get('group', 'NULL')
                print(f'{car_clean:40} → {group}')
        
        print('\n' + '='*60)
        print('CARROS COM \"4\" NO NOME (possível B1):')
        print('='*60)
        for item in items:
            car = item.get('car', '')
            if '500' in car or '4' in car.lower():
                car_clean = car.split('ou similar')[0].strip()
                cat = item.get('category', 'N/A')
                group = item.get('group', 'NULL')
                print(f'{car_clean:40} → {cat:20} → {group}')
                
    else:
        print(f\"Erro: {data.get('error')}\")
except Exception as e:
    print(f'Erro: {e}')
    import traceback
    traceback.print_exc()
"
