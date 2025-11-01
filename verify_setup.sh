#!/bin/bash

# 🔍 Script de Verificação - Windsurf Casa
# Execute: bash verify_setup.sh

echo "🔍 Verificando setup do projeto..."
echo ""

# Cores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Contador
ERRORS=0

# 1. Verificar Python
echo -n "1. Python 3.11+: "
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo -e "${GREEN}✓ $PYTHON_VERSION${NC}"
else
    echo -e "${RED}✗ Não encontrado${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 2. Verificar Git
echo -n "2. Git: "
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version | cut -d' ' -f3)
    echo -e "${GREEN}✓ $GIT_VERSION${NC}"
else
    echo -e "${RED}✗ Não encontrado${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 3. Verificar repositório
echo -n "3. Repositório clonado: "
if [ -d ".git" ]; then
    COMMITS=$(git log --oneline | wc -l | tr -d ' ')
    echo -e "${GREEN}✓ $COMMITS commits${NC}"
else
    echo -e "${RED}✗ Não é um repositório Git${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 4. Verificar remote
echo -n "4. GitHub remote: "
if git remote get-url origin &> /dev/null; then
    REMOTE=$(git remote get-url origin)
    echo -e "${GREEN}✓ $REMOTE${NC}"
else
    echo -e "${RED}✗ Remote não configurado${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 5. Verificar branch
echo -n "5. Branch atual: "
if git branch &> /dev/null; then
    BRANCH=$(git branch --show-current)
    echo -e "${GREEN}✓ $BRANCH${NC}"
else
    echo -e "${YELLOW}⚠ Não detectado${NC}"
fi

# 6. Verificar virtual environment
echo -n "6. Virtual environment: "
if [ -d "venv" ]; then
    echo -e "${GREEN}✓ Existe${NC}"
else
    echo -e "${YELLOW}⚠ Não encontrado - execute: python3 -m venv venv${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 7. Verificar requirements.txt
echo -n "7. requirements.txt: "
if [ -f "requirements.txt" ]; then
    DEPS=$(wc -l < requirements.txt | tr -d ' ')
    echo -e "${GREEN}✓ $DEPS dependências${NC}"
else
    echo -e "${RED}✗ Não encontrado${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 8. Verificar main.py
echo -n "8. main.py: "
if [ -f "main.py" ]; then
    LINES=$(wc -l < main.py | tr -d ' ')
    echo -e "${GREEN}✓ $LINES linhas${NC}"
else
    echo -e "${RED}✗ Não encontrado${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 9. Verificar carjet_direct.py
echo -n "9. carjet_direct.py: "
if [ -f "carjet_direct.py" ]; then
    VEHICLES=$(grep -c "'" carjet_direct.py)
    echo -e "${GREEN}✓ ~$VEHICLES veículos${NC}"
else
    echo -e "${RED}✗ Não encontrado${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 10. Verificar templates
echo -n "10. templates/: "
if [ -d "templates" ]; then
    TEMPLATES=$(find templates -name "*.html" | wc -l | tr -d ' ')
    echo -e "${GREEN}✓ $TEMPLATES templates${NC}"
else
    echo -e "${RED}✗ Pasta não encontrada${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 11. Verificar static
echo -n "11. static/: "
if [ -d "static" ]; then
    STATIC=$(find static -type f | wc -l | tr -d ' ')
    echo -e "${GREEN}✓ $STATIC ficheiros${NC}"
else
    echo -e "${YELLOW}⚠ Pasta não encontrada${NC}"
fi

# 12. Verificar vehicle_editor.html
echo -n "12. vehicle_editor.html: "
if [ -f "vehicle_editor.html" ]; then
    echo -e "${GREEN}✓ Existe${NC}"
else
    echo -e "${RED}✗ Não encontrado${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 13. Verificar database
echo -n "13. carrental.db: "
if [ -f "carrental.db" ]; then
    SIZE=$(du -h carrental.db | cut -f1)
    echo -e "${GREEN}✓ $SIZE${NC}"
else
    echo -e "${YELLOW}⚠ Será criado ao iniciar${NC}"
fi

# 14. Verificar se está atualizado
echo -n "14. Sincronizado com GitHub: "
git fetch origin main 2>/dev/null
LOCAL=$(git rev-parse main 2>/dev/null)
REMOTE=$(git rev-parse origin/main 2>/dev/null)
if [ "$LOCAL" = "$REMOTE" ]; then
    echo -e "${GREEN}✓ Atualizado${NC}"
else
    echo -e "${YELLOW}⚠ Execute: git pull origin main${NC}"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Resumo
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ TUDO OK! Pronto para iniciar!${NC}"
    echo ""
    echo "Próximos passos:"
    echo "  1. source venv/bin/activate"
    echo "  2. pip install -r requirements.txt"
    echo "  3. python3 main.py"
    echo "  4. Abrir: http://localhost:8000"
else
    echo -e "${RED}❌ $ERRORS erro(s) encontrado(s)${NC}"
    echo ""
    echo "Consulte: SETUP_WINDSURF_CASA.md"
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
