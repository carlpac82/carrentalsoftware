#!/bin/bash
# Teste direto da API para ver se campo 'group' está presente

echo "==============================================="
echo "TESTE DIRETO DA API - Campo 'group'"
echo "==============================================="
echo ""

# Login
echo "1. Fazendo login..."
COOKIE=$(curl -s -c - -X POST http://localhost:8000/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123" | grep session | awk '{print $7}')

echo "Cookie obtido: $COOKIE"
echo ""

# Fazer pesquisa (modo mock para ser rápido)
echo "2. Fazendo pesquisa..."
START_DATE=$(date -v+7d +%Y-%m-%d 2>/dev/null || date -d "+7 days" +%Y-%m-%d 2>/dev/null || echo "2025-02-05")

RESPONSE=$(curl -s -X POST http://localhost:8000/api/track-by-params \
  -H "Content-Type: application/json" \
  -H "Cookie: session=$COOKIE" \
  -d "{
    \"location\": \"Aeroporto de Faro\",
    \"start_date\": \"$START_DATE\",
    \"days\": 7,
    \"start_time\": \"15:00\",
    \"end_time\": \"10:00\",
    \"quick\": true
  }")

echo "Response completo (primeiros 500 chars):"
echo "$RESPONSE" | head -c 500
echo ""
echo ""

# Extrair primeiro item e mostrar campos
echo "3. Analisando primeiro item..."
echo "$RESPONSE" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    if data.get('ok'):
        items = data.get('items', [])
        print(f'Total items: {len(items)}')
        if items:
            first = items[0]
            print('')
            print('Primeiro item:')
            print(f\"  car: {first.get('car')}\")
            print(f\"  category: {first.get('category')}\")
            print(f\"  group: {first.get('group')}\")
            print(f\"  hasGroup: {'group' in first}\")
            print(f\"  supplier: {first.get('supplier')}\")
            print(f\"  price: {first.get('price')}\")
        else:
            print('Nenhum item retornado')
    else:
        print(f\"Erro: {data.get('error')}\")
except Exception as e:
    print(f'Erro ao parsear JSON: {e}')
"

echo ""
echo "==============================================="
echo "FIM DO TESTE"
echo "==============================================="
