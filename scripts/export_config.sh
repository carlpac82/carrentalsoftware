#!/bin/bash
# Export configuração completa (veículos + imagens + nomes editados)

# Configuração
HOST="http://localhost:8000"
OUTPUT_DIR="./backups"
DATE=$(date +%Y%m%d_%H%M%S)
OUTPUT_FILE="$OUTPUT_DIR/carrental_config_$DATE.json"

# Criar diretório se não existir
mkdir -p "$OUTPUT_DIR"

# Login (ajustar credenciais conforme necessário)
echo "🔐 Fazendo login..."
COOKIE=$(curl -s -c - -X POST "$HOST/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123" | grep session | awk '{print $7}')

if [ -z "$COOKIE" ]; then
    echo "❌ Erro: Login falhou"
    exit 1
fi

echo "✅ Login bem-sucedido"
echo ""

# Export
echo "💾 Exportando configuração..."
HTTP_CODE=$(curl -s -w "%{http_code}" -o "$OUTPUT_FILE" \
  "$HOST/api/export/config" \
  -H "Cookie: session=$COOKIE")

if [ "$HTTP_CODE" = "200" ]; then
    # Verificar tamanho
    SIZE=$(wc -c < "$OUTPUT_FILE" | tr -d ' ')
    SIZE_MB=$(echo "scale=2; $SIZE/1024/1024" | bc)
    
    echo "✅ Export concluído!"
    echo "   Ficheiro: $OUTPUT_FILE"
    echo "   Tamanho: ${SIZE_MB}MB"
    echo ""
    
    # Mostrar resumo
    echo "📊 Resumo do export:"
    cat "$OUTPUT_FILE" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    print(f'   Versão: {data.get(\"version\", \"N/A\")}')
    print(f'   Data: {data.get(\"exported_at\", \"N/A\")[:19]}')
    print(f'   Veículos: {len(data.get(\"vehicles\", {}))}')
    print(f'   Name overrides: {len(data.get(\"name_overrides\", []))}')
    print(f'   Imagens: {len(data.get(\"images\", {}))}')
except:
    print('   ⚠️  Erro ao ler resumo')
"
    echo ""
    
    # Perguntar se quer comprimir
    read -p "Comprimir ficheiro? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        gzip "$OUTPUT_FILE"
        echo "✅ Ficheiro comprimido: ${OUTPUT_FILE}.gz"
    fi
else
    echo "❌ Erro ao exportar (HTTP $HTTP_CODE)"
    cat "$OUTPUT_FILE"
    rm "$OUTPUT_FILE"
    exit 1
fi
