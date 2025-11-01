#!/bin/bash
# Import configuração completa de um ficheiro JSON

# Verificar argumentos
if [ $# -eq 0 ]; then
    echo "Uso: $0 <ficheiro_config.json>"
    echo ""
    echo "Exemplo:"
    echo "  $0 backups/carrental_config_20250129_224047.json"
    exit 1
fi

CONFIG_FILE="$1"
HOST="http://localhost:8000"

# Verificar se ficheiro existe
if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ Ficheiro não encontrado: $CONFIG_FILE"
    exit 1
fi

echo "📄 Ficheiro: $CONFIG_FILE"
echo ""

# Descomprimir se necessário
if [[ "$CONFIG_FILE" == *.gz ]]; then
    echo "📦 Descomprimindo..."
    gunzip -k "$CONFIG_FILE"
    CONFIG_FILE="${CONFIG_FILE%.gz}"
fi

# Verificar se é JSON válido
echo "🔍 Verificando JSON..."
if ! python3 -c "import json; json.load(open('$CONFIG_FILE'))" 2>/dev/null; then
    echo "❌ JSON inválido"
    exit 1
fi

echo "✅ JSON válido"
echo ""

# Mostrar resumo
echo "📊 Resumo do import:"
cat "$CONFIG_FILE" | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(f'   Versão: {data.get(\"version\", \"N/A\")}')
print(f'   Data export: {data.get(\"exported_at\", \"N/A\")[:19]}')
print(f'   Veículos: {len(data.get(\"vehicles\", {}))}')
print(f'   Name overrides: {len(data.get(\"name_overrides\", []))}')
print(f'   Imagens: {len(data.get(\"images\", {}))}')
"
echo ""

# Confirmar
read -p "⚠️  Confirma import? Isto vai SOBRESCREVER dados existentes! (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Import cancelado"
    exit 0
fi

# Login
echo ""
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

# Import
echo "📤 Importando configuração..."
RESPONSE=$(curl -s -X POST "$HOST/api/import/config" \
  -H "Content-Type: application/json" \
  -H "Cookie: session=$COOKIE" \
  -d @"$CONFIG_FILE")

# Verificar resultado
echo "$RESPONSE" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    if data.get('ok'):
        print('✅ Import concluído com sucesso!')
        print(f'   Mensagem: {data.get(\"message\", \"N/A\")}')
        imported = data.get('imported', {})
        print(f'   Name overrides: {imported.get(\"name_overrides\", 0)} importados')
        print(f'   Imagens: {imported.get(\"images\", 0)} importadas')
    else:
        print(f'❌ Erro: {data.get(\"error\", \"Desconhecido\")}')
        sys.exit(1)
except Exception as e:
    print(f'❌ Erro ao processar resposta: {e}')
    print('Resposta bruta:')
    print(sys.stdin.read())
    sys.exit(1)
"

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Configuração importada! Recarregar página para ver mudanças."
else
    exit 1
fi
