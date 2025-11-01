#!/bin/bash

# ============================================================================
# BACKUP COMPLETO - Car Rental API
# ============================================================================
# Cria backup TOTAL de:
# - Código fonte completo
# - Todas as bases de dados (.db)
# - Todas as fotos (static/vehicle_photos/)
# - Profiles de utilizadores
# - Logs
# - Git history completo
# - Configurações (.env)
# - Tudo!
# ============================================================================

set -e  # Exit on error

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Diretório base
PROJECT_DIR="/Users/filipepacheco/CascadeProjects/RentalPriceTrackerPerDay"
cd "$PROJECT_DIR"

# Data e hora para nome do backup
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_NAME="FULL_BACKUP_${TIMESTAMP}"
BACKUP_DIR="$PROJECT_DIR/backups/$BACKUP_NAME"

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║         BACKUP COMPLETO - Car Rental API                   ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}📦 Backup:${NC} $BACKUP_NAME"
echo -e "${YELLOW}📁 Destino:${NC} $BACKUP_DIR"
echo ""

# Criar diretório de backup
mkdir -p "$BACKUP_DIR"

# ============================================================================
# 1. CÓDIGO FONTE COMPLETO
# ============================================================================
echo -e "${GREEN}[1/10]${NC} Copiando código fonte..."
rsync -av --exclude='backups' \
          --exclude='venv' \
          --exclude='__pycache__' \
          --exclude='*.pyc' \
          --exclude='.git' \
          --exclude='node_modules' \
          "$PROJECT_DIR/" "$BACKUP_DIR/source/" > /dev/null
echo -e "       ✅ Código fonte copiado"

# ============================================================================
# 2. GIT REPOSITORY COMPLETO
# ============================================================================
echo -e "${GREEN}[2/10]${NC} Clonando repositório Git completo..."
git clone --mirror "$PROJECT_DIR/.git" "$BACKUP_DIR/git_mirror.git" > /dev/null 2>&1
echo -e "       ✅ Git repository clonado (todos os commits preservados)"

# ============================================================================
# 3. BASES DE DADOS
# ============================================================================
echo -e "${GREEN}[3/10]${NC} Copiando bases de dados..."
mkdir -p "$BACKUP_DIR/databases"
for db in carrental.db car_images.db data.db; do
    if [ -f "$PROJECT_DIR/$db" ]; then
        cp "$PROJECT_DIR/$db" "$BACKUP_DIR/databases/"
        # Criar dump SQL também
        sqlite3 "$PROJECT_DIR/$db" .dump > "$BACKUP_DIR/databases/${db%.db}_dump.sql"
        echo -e "       ✅ $db (binário + SQL dump)"
    fi
done

# ============================================================================
# 4. FOTOS DE VEÍCULOS
# ============================================================================
echo -e "${GREEN}[4/10]${NC} Copiando fotos de veículos..."
if [ -d "$PROJECT_DIR/static/vehicle_photos" ]; then
    mkdir -p "$BACKUP_DIR/vehicle_photos"
    rsync -av "$PROJECT_DIR/static/vehicle_photos/" "$BACKUP_DIR/vehicle_photos/" > /dev/null
    PHOTO_COUNT=$(find "$BACKUP_DIR/vehicle_photos" -type f | wc -l)
    echo -e "       ✅ $PHOTO_COUNT fotos copiadas"
else
    echo -e "       ⚠️  Pasta de fotos não encontrada"
fi

# ============================================================================
# 5. STATIC FILES (logos, favicons, etc)
# ============================================================================
echo -e "${GREEN}[5/10]${NC} Copiando ficheiros estáticos..."
if [ -d "$PROJECT_DIR/static" ]; then
    mkdir -p "$BACKUP_DIR/static"
    rsync -av "$PROJECT_DIR/static/" "$BACKUP_DIR/static/" > /dev/null
    echo -e "       ✅ Ficheiros estáticos copiados"
fi

# ============================================================================
# 6. TEMPLATES
# ============================================================================
echo -e "${GREEN}[6/10]${NC} Copiando templates HTML..."
if [ -d "$PROJECT_DIR/templates" ]; then
    mkdir -p "$BACKUP_DIR/templates"
    rsync -av "$PROJECT_DIR/templates/" "$BACKUP_DIR/templates/" > /dev/null
    TEMPLATE_COUNT=$(find "$BACKUP_DIR/templates" -name "*.html" | wc -l)
    echo -e "       ✅ $TEMPLATE_COUNT templates copiados"
fi

# ============================================================================
# 7. CONFIGURAÇÕES E ENVIRONMENT
# ============================================================================
echo -e "${GREEN}[7/10]${NC} Copiando configurações..."
mkdir -p "$BACKUP_DIR/config"
for file in .env render.yaml Dockerfile requirements.txt; do
    if [ -f "$PROJECT_DIR/$file" ]; then
        cp "$PROJECT_DIR/$file" "$BACKUP_DIR/config/"
        echo -e "       ✅ $file"
    fi
done

# ============================================================================
# 8. LOGS (se existirem)
# ============================================================================
echo -e "${GREEN}[8/10]${NC} Copiando logs..."
mkdir -p "$BACKUP_DIR/logs"
if [ -d "$PROJECT_DIR/logs" ]; then
    rsync -av "$PROJECT_DIR/logs/" "$BACKUP_DIR/logs/" > /dev/null
    echo -e "       ✅ Logs copiados"
else
    echo -e "       ℹ️  Sem logs para copiar"
fi

# ============================================================================
# 9. DOCUMENTAÇÃO
# ============================================================================
echo -e "${GREEN}[9/10]${NC} Copiando documentação..."
mkdir -p "$BACKUP_DIR/docs"
find "$PROJECT_DIR" -maxdepth 1 -name "*.md" -exec cp {} "$BACKUP_DIR/docs/" \;
find "$PROJECT_DIR" -maxdepth 1 -name "*.txt" -exec cp {} "$BACKUP_DIR/docs/" \;
DOC_COUNT=$(find "$BACKUP_DIR/docs" -type f | wc -l)
echo -e "       ✅ $DOC_COUNT documentos copiados"

# ============================================================================
# 10. METADATA E INFORMAÇÕES DO BACKUP
# ============================================================================
echo -e "${GREEN}[10/10]${NC} Criando metadata do backup..."

cat > "$BACKUP_DIR/BACKUP_INFO.txt" << EOF
╔════════════════════════════════════════════════════════════╗
║         BACKUP COMPLETO - Car Rental API                   ║
╚════════════════════════════════════════════════════════════╝

📅 Data: $(date +"%d/%m/%Y às %H:%M:%S")
💻 Hostname: $(hostname)
👤 User: $(whoami)
📦 Backup: $BACKUP_NAME

════════════════════════════════════════════════════════════

📊 CONTEÚDO DO BACKUP:

✅ Código Fonte Completo
   - Python (main.py, etc)
   - Templates HTML
   - Static files (CSS, JS, imagens)
   
✅ Git Repository
   - Histórico completo de commits
   - Todas as branches
   - Tags
   
✅ Bases de Dados
   - carrental.db (utilizadores, settings, logs)
   - car_images.db (fotos de veículos)
   - data.db (dados de scraping)
   - SQL dumps de todas as DBs
   
✅ Fotos
   - Todas as fotos de veículos
   - Logos e favicons
   - Profile pictures
   
✅ Configurações
   - .env (credenciais)
   - render.yaml (deploy config)
   - Dockerfile
   - requirements.txt
   
✅ Documentação
   - Todos os ficheiros .md
   - Guias de deploy
   - Workflows

════════════════════════════════════════════════════════════

📈 ESTATÍSTICAS:

EOF

# Adicionar estatísticas
echo "Tamanho total: $(du -sh "$BACKUP_DIR" | cut -f1)" >> "$BACKUP_DIR/BACKUP_INFO.txt"
echo "Ficheiros: $(find "$BACKUP_DIR" -type f | wc -l)" >> "$BACKUP_DIR/BACKUP_INFO.txt"
echo "Pastas: $(find "$BACKUP_DIR" -type d | wc -l)" >> "$BACKUP_DIR/BACKUP_INFO.txt"
echo "" >> "$BACKUP_DIR/BACKUP_INFO.txt"

# Git info
if [ -d "$PROJECT_DIR/.git" ]; then
    echo "Git:" >> "$BACKUP_DIR/BACKUP_INFO.txt"
    echo "  - Branch atual: $(git branch --show-current)" >> "$BACKUP_DIR/BACKUP_INFO.txt"
    echo "  - Último commit: $(git log -1 --format='%h - %s (%ci)')" >> "$BACKUP_DIR/BACKUP_INFO.txt"
    echo "  - Total commits: $(git rev-list --count HEAD)" >> "$BACKUP_DIR/BACKUP_INFO.txt"
fi

echo -e "       ✅ Metadata criada"

# ============================================================================
# CRIAR ARQUIVO COMPRIMIDO
# ============================================================================
echo ""
echo -e "${YELLOW}📦 Comprimindo backup...${NC}"
cd "$PROJECT_DIR/backups"
tar -czf "${BACKUP_NAME}.tar.gz" "$BACKUP_NAME" 2>/dev/null
BACKUP_SIZE=$(du -sh "${BACKUP_NAME}.tar.gz" | cut -f1)
echo -e "   ✅ Arquivo criado: ${BACKUP_NAME}.tar.gz ($BACKUP_SIZE)"

# ============================================================================
# RESUMO FINAL
# ============================================================================
echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                  BACKUP CONCLUÍDO! ✅                       ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}📁 Backup criado em:${NC}"
echo -e "   Pasta: $BACKUP_DIR"
echo -e "   Arquivo: ${BACKUP_NAME}.tar.gz ($BACKUP_SIZE)"
echo ""
echo -e "${GREEN}📊 Conteúdo:${NC}"
cat "$BACKUP_DIR/BACKUP_INFO.txt" | tail -n 15
echo ""
echo -e "${YELLOW}💡 Para restaurar este backup:${NC}"
echo -e "   cd $PROJECT_DIR/backups"
echo -e "   tar -xzf ${BACKUP_NAME}.tar.gz"
echo -e "   cd ${BACKUP_NAME}"
echo -e "   # Copiar ficheiros necessários de volta"
echo ""

# ============================================================================
# PUSH PARA GITHUB
# ============================================================================
echo -e "${YELLOW}🔄 Enviando para GitHub...${NC}"
cd "$PROJECT_DIR"

# Commit do código atual (se houver alterações)
if ! git diff-index --quiet HEAD --; then
    echo -e "   📝 Fazendo commit das alterações..."
    git add .
    git commit -m "backup: ${BACKUP_NAME}" > /dev/null 2>&1
    echo -e "   ✅ Commit criado"
else
    echo -e "   ℹ️  Sem alterações para commit"
fi

# Push para GitHub
echo -e "   📤 Enviando para GitHub..."
if git push backup main > /dev/null 2>&1; then
    echo -e "   ✅ Push para GitHub concluído"
    echo -e "   🔗 https://github.com/comercial-autoprudente/carrental_api"
else
    echo -e "   ⚠️  Erro no push (verificar manualmente)"
fi

echo ""
echo -e "${GREEN}✅ Backup completo guardado com sucesso!${NC}"
echo -e "${GREEN}   📁 Local: $BACKUP_DIR${NC}"
echo -e "${GREEN}   ☁️  GitHub: comercial-autoprudente/carrental_api${NC}"
echo ""
