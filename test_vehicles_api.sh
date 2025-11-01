#!/bin/bash
# Testar API de veículos com autenticação

echo "🧪 TESTE API VEHICLES"
echo "======================================================================"
echo ""

# Fazer login primeiro para obter cookie de sessão
echo "1️⃣ Fazendo login..."
COOKIE=$(curl -s -c - -X POST http://localhost:8000/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123" \
  | grep session | awk '{print $7}')

if [ -z "$COOKIE" ]; then
    echo "❌ Erro: Não foi possível fazer login"
    echo ""
    echo "💡 Verifica:"
    echo "   - Servidor está a correr?"
    echo "   - Credenciais corretas? (admin/admin123)"
    exit 1
fi

echo "✅ Login OK! Cookie: ${COOKIE:0:20}..."
echo ""

# Testar endpoint /api/vehicles/with-originals
echo "2️⃣ Testando /api/vehicles/with-originals..."
RESPONSE=$(curl -s -b "session=$COOKIE" http://localhost:8000/api/vehicles/with-originals)

# Verificar se retornou JSON válido
if echo "$RESPONSE" | jq . > /dev/null 2>&1; then
    echo "✅ JSON válido recebido"
    echo ""
    
    # Extrair informações
    OK=$(echo "$RESPONSE" | jq -r '.ok')
    TOTAL=$(echo "$RESPONSE" | jq -r '.total')
    
    if [ "$OK" = "true" ]; then
        echo "✅ API retornou sucesso!"
        echo "📊 Total de veículos: $TOTAL"
        echo ""
        
        if [ "$TOTAL" -gt 0 ]; then
            echo "📋 Primeiros 5 veículos:"
            echo "$RESPONSE" | jq -r '.vehicles | to_entries | .[0:5] | .[] | "  - \(.key) → \(.value.category)"'
        else
            echo "⚠️  PROBLEMA: Total = 0"
            echo ""
            echo "Resposta completa:"
            echo "$RESPONSE" | jq .
        fi
    else
        echo "❌ API retornou erro!"
        echo ""
        echo "Erro:"
        echo "$RESPONSE" | jq -r '.error'
        echo ""
        echo "Traceback:"
        echo "$RESPONSE" | jq -r '.traceback'
    fi
else
    echo "❌ Resposta não é JSON válido!"
    echo ""
    echo "Resposta recebida:"
    echo "$RESPONSE" | head -50
fi

echo ""
echo "======================================================================"
