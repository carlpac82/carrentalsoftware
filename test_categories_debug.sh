#!/bin/bash
# Teste detalhado para debug de categorias

echo "=========================================="
echo "DEBUG CATEGORIAS - Ver TODAS as categorias únicas"
echo "=========================================="
echo ""

# Login
COOKIE=$(curl -s -c - -X POST http://localhost:8000/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123" | grep session | awk '{print $7}')

echo "Cookie: ${COOKIE:0:50}..."
echo ""

# Fazer pesquisa
START_DATE=$(date -v+7d +%Y-%m-%d 2>/dev/null || date -d "+7 days" +%Y-%m-%d 2>/dev/null || echo "2025-02-05")

echo "Fazendo pesquisa..."
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

echo ""
echo "=========================================="
echo "CATEGORIAS ÚNICAS (primeiras 20):"
echo "=========================================="
echo "$RESPONSE" | python3 -c "
import json, sys
from collections import Counter

try:
    data = json.load(sys.stdin)
    if data.get('ok'):
        items = data.get('items', [])
        print(f'Total items: {len(items)}\n')
        
        # Contar categorias
        categories = [item.get('category', 'N/A') for item in items]
        cat_counts = Counter(categories)
        
        print('Categoria → Contagem → Grupo')
        print('-' * 60)
        for cat, count in cat_counts.most_common(20):
            # Buscar grupo do primeiro item com essa categoria
            group = next((item.get('group', 'NULL') for item in items if item.get('category') == cat), 'NULL')
            print(f'{cat:30} → {count:3} items → group: {group}')
        
        print('\n' + '='*60)
        print('GRUPOS ÚNICOS:')
        print('='*60)
        groups = [item.get('group', 'NULL') for item in items]
        group_counts = Counter(groups)
        for grp, count in group_counts.most_common():
            print(f'  {grp:10} → {count:3} items')
            
    else:
        print(f\"Erro: {data.get('error')}\")
except Exception as e:
    print(f'Erro ao parsear JSON: {e}')
    import traceback
    traceback.print_exc()
"

echo ""
echo "=========================================="
echo "FIM DO DEBUG"
echo "=========================================="
