#!/bin/bash

# Script para fazer push para o novo repositório carrental-Final

echo "=========================================="
echo "🚀 PUSH TO NEW REPO: carrental-Final"
echo "=========================================="
echo ""

# Verificar se estamos no diretório correto
if [ ! -f "main.py" ]; then
    echo "❌ ERRO: main.py não encontrado!"
    echo "Execute este script no diretório do projeto."
    exit 1
fi

echo "📋 Verificando status do Git..."
git status

echo ""
echo "=========================================="
echo "⚠️  ANTES DE CONTINUAR:"
echo "=========================================="
echo "1. ✅ Criaste o repo no GitHub?"
echo "   URL: https://github.com/carlpac82/carrental-Final"
echo ""
echo "2. ✅ O repo está VAZIO? (sem README, .gitignore, etc.)"
echo ""
read -p "Continuar? (y/n): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Cancelado. Cria o repo primeiro!"
    exit 1
fi

echo ""
echo "📦 Adicionando novo remote..."
git remote add new-repo https://github.com/carlpac82/carrental-Final.git

echo ""
echo "🚀 Fazendo push para o novo repositório..."
git push new-repo main

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ PUSH BEM-SUCEDIDO!"
    echo "=========================================="
    echo ""
    echo "📋 PRÓXIMOS PASSOS:"
    echo ""
    echo "1. Aceder a Render Dashboard:"
    echo "   https://dashboard.render.com/"
    echo ""
    echo "2. OPÇÃO A - Criar Novo Service (RECOMENDADO):"
    echo "   - Clicar 'New +' → 'Web Service'"
    echo "   - Conectar: carlpac82/carrental-Final"
    echo "   - Branch: main"
    echo "   - Environment: Docker"
    echo ""
    echo "3. OPÇÃO B - Atualizar Service Existente:"
    echo "   - Settings → GitHub → Disconnect"
    echo "   - Connect: carlpac82/carrental-Final"
    echo "   - Manual Deploy → Clear build cache"
    echo ""
    echo "=========================================="
    echo ""
    
    read -p "Queres mudar o remote origin para o novo repo? (y/n): " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🔧 Atualizando remote origin..."
        git remote remove origin
        git remote rename new-repo origin
        echo "✅ Remote origin atualizado para carrental-Final"
    else
        echo "ℹ️  Remote 'new-repo' mantido. Para atualizar depois:"
        echo "   git remote remove origin"
        echo "   git remote rename new-repo origin"
    fi
else
    echo ""
    echo "=========================================="
    echo "❌ ERRO NO PUSH!"
    echo "=========================================="
    echo ""
    echo "Possíveis causas:"
    echo "1. Repo não existe no GitHub"
    echo "2. Repo não está vazio"
    echo "3. Falta autenticação (token)"
    echo ""
    echo "Para resolver autenticação:"
    echo "1. GitHub → Settings → Developer settings"
    echo "2. Personal access tokens → Generate new token"
    echo "3. Scopes: repo (full control)"
    echo "4. Usar token como password no git push"
    echo ""
    
    # Remover remote se falhou
    git remote remove new-repo 2>/dev/null
fi

echo ""
echo "=========================================="
echo "📝 Detalhes do repositório:"
echo "=========================================="
git remote -v
