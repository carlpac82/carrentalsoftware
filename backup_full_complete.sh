#!/bin/bash

# Script de Backup Completo - CarRental API
# Inclui: código, base de dados, imagens, configurações, commits Git

set -e  # Exit on error

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  BACKUP COMPLETO - CarRental API${NC}"
echo -e "${GREEN}========================================${NC}"

# Timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_NAME="backup_full_${TIMESTAMP}"
BACKUP_DIR="../backups_full/${BACKUP_NAME}"

echo -e "\n${YELLOW}📦 Timestamp: ${TIMESTAMP}${NC}"
echo -e "${YELLOW}📁 Diretório: ${BACKUP_DIR}${NC}\n"

# Criar diretório de backup
mkdir -p "${BACKUP_DIR}"

echo -e "${GREEN}[1/10]${NC} Criando estrutura de diretórios..."
mkdir -p "${BACKUP_DIR}/code"
mkdir -p "${BACKUP_DIR}/database"
mkdir -p "${BACKUP_DIR}/images"
mkdir -p "${BACKUP_DIR}/config"
mkdir -p "${BACKUP_DIR}/git"
mkdir -p "${BACKUP_DIR}/docs"

# Backup do código fonte completo
echo -e "${GREEN}[2/10]${NC} Copiando código fonte..."
rsync -av --exclude='.git' \
          --exclude='.venv' \
          --exclude='__pycache__' \
          --exclude='*.pyc' \
          --exclude='node_modules' \
          --exclude='backups' \
          --exclude='backups_full' \
          ./ "${BACKUP_DIR}/code/"

# Backup das bases de dados
echo -e "${GREEN}[3/10]${NC} Backup das bases de dados..."
if [ -f "carrental.db" ]; then
    sqlite3 carrental.db ".backup '${BACKUP_DIR}/database/carrental_${TIMESTAMP}.db'"
    echo "  ✓ carrental.db"
fi

if [ -f "car_images.db" ]; then
    sqlite3 car_images.db ".backup '${BACKUP_DIR}/database/car_images_${TIMESTAMP}.db'"
    echo "  ✓ car_images.db"
fi

if [ -f "data.db" ]; then
    sqlite3 data.db ".backup '${BACKUP_DIR}/database/data_${TIMESTAMP}.db'"
    echo "  ✓ data.db"
fi

if [ -f "rental_tracker.db" ]; then
    cp rental_tracker.db "${BACKUP_DIR}/database/rental_tracker_${TIMESTAMP}.db"
    echo "  ✓ rental_tracker.db"
fi

# Backup do banco de imagens
echo -e "${GREEN}[4/10]${NC} Backup do banco de imagens..."
if [ -d "cars" ]; then
    cp -r cars "${BACKUP_DIR}/images/"
    echo "  ✓ Pasta cars/ ($(ls -1 cars 2>/dev/null | wc -l) ficheiros)"
fi

if [ -d "static/images" ]; then
    cp -r static/images "${BACKUP_DIR}/images/static_images"
    echo "  ✓ static/images/"
fi

if [ -d "uploads" ]; then
    cp -r uploads "${BACKUP_DIR}/images/"
    echo "  ✓ uploads/"
fi

# Backup das configurações
echo -e "${GREEN}[5/10]${NC} Backup das configurações..."
if [ -f ".env" ]; then
    cp .env "${BACKUP_DIR}/config/.env_${TIMESTAMP}"
    echo "  ✓ .env"
fi

if [ -f ".env.example" ]; then
    cp .env.example "${BACKUP_DIR}/config/"
    echo "  ✓ .env.example"
fi

if [ -f "requirements.txt" ]; then
    cp requirements.txt "${BACKUP_DIR}/config/"
    echo "  ✓ requirements.txt"
fi

if [ -f "render.yaml" ]; then
    cp render.yaml "${BACKUP_DIR}/config/"
    echo "  ✓ render.yaml"
fi

if [ -f "Dockerfile" ]; then
    cp Dockerfile "${BACKUP_DIR}/config/"
    echo "  ✓ Dockerfile"
fi

# Backup dos ficheiros Excel
echo -e "${GREEN}[6/10]${NC} Backup dos ficheiros de dados..."
if [ -f "Brokers Albufeira.xlsx" ]; then
    cp "Brokers Albufeira.xlsx" "${BACKUP_DIR}/config/"
    echo "  ✓ Brokers Albufeira.xlsx"
fi

# Backup do histórico Git
echo -e "${GREEN}[7/10]${NC} Backup do repositório Git..."
git bundle create "${BACKUP_DIR}/git/repository_${TIMESTAMP}.bundle" --all
echo "  ✓ Git bundle criado"

# Exportar log de commits
git log --all --oneline --graph --decorate > "${BACKUP_DIR}/git/commits_log_${TIMESTAMP}.txt"
echo "  ✓ Log de commits exportado"

# Exportar branches
git branch -a > "${BACKUP_DIR}/git/branches_${TIMESTAMP}.txt"
echo "  ✓ Lista de branches exportada"

# Backup da documentação
echo -e "${GREEN}[8/10]${NC} Backup da documentação..."
cp *.md "${BACKUP_DIR}/docs/" 2>/dev/null || true
echo "  ✓ Ficheiros .md copiados"

# Criar manifesto do backup
echo -e "${GREEN}[9/10]${NC} Criando manifesto do backup..."
cat > "${BACKUP_DIR}/MANIFEST.txt" << EOF
========================================
BACKUP COMPLETO - CarRental API
========================================

Data/Hora: $(date)
Timestamp: ${TIMESTAMP}
Hostname: $(hostname)
User: $(whoami)

CONTEÚDO DO BACKUP:
-------------------

1. CÓDIGO FONTE (code/)
   - Todos os ficheiros .py, .html, .js, .css
   - Templates e static files
   - Scripts de teste e utilitários

2. BASES DE DADOS (database/)
   - carrental.db - Base principal
   - car_images.db - Imagens dos veículos
   - data.db - Dados adicionais
   - rental_tracker.db - Tracking

3. IMAGENS (images/)
   - cars/ - Fotos dos veículos
   - static/images/ - Imagens estáticas
   - uploads/ - Uploads de utilizadores

4. CONFIGURAÇÕES (config/)
   - .env - Variáveis de ambiente
   - requirements.txt - Dependências Python
   - render.yaml - Configuração Render
   - Dockerfile - Container config
   - Brokers Albufeira.xlsx - Dados brokers

5. GIT (git/)
   - repository_${TIMESTAMP}.bundle - Repositório completo
   - commits_log_${TIMESTAMP}.txt - Histórico de commits
   - branches_${TIMESTAMP}.txt - Lista de branches

6. DOCUMENTAÇÃO (docs/)
   - Todos os ficheiros .md

ESTATÍSTICAS:
-------------
Total de ficheiros: $(find "${BACKUP_DIR}" -type f | wc -l)
Tamanho total: $(du -sh "${BACKUP_DIR}" | cut -f1)

RESTAURAR BACKUP:
-----------------
1. Extrair conteúdo para diretório desejado
2. Restaurar Git: git clone repository_${TIMESTAMP}.bundle
3. Copiar .env de config/ para raiz
4. Copiar bases de dados de database/ para raiz
5. Copiar imagens de images/ para estrutura original
6. Instalar dependências: pip install -r requirements.txt

========================================
EOF

echo "  ✓ Manifesto criado"

# Criar arquivo comprimido
echo -e "${GREEN}[10/10]${NC} Comprimindo backup..."
cd ../backups_full
tar -czf "${BACKUP_NAME}.tar.gz" "${BACKUP_NAME}"
BACKUP_SIZE=$(du -sh "${BACKUP_NAME}.tar.gz" | cut -f1)
echo "  ✓ Arquivo criado: ${BACKUP_NAME}.tar.gz (${BACKUP_SIZE})"

# Resumo
echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}  BACKUP CONCLUÍDO COM SUCESSO!${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "\n📦 ${YELLOW}Backup Local:${NC}"
echo -e "   Pasta: ../backups_full/${BACKUP_NAME}/"
echo -e "   Arquivo: ../backups_full/${BACKUP_NAME}.tar.gz"
echo -e "   Tamanho: ${BACKUP_SIZE}"
echo -e "\n📊 ${YELLOW}Conteúdo:${NC}"
echo -e "   ✓ Código fonte completo"
echo -e "   ✓ $(ls -1 ${BACKUP_NAME}/database/*.db 2>/dev/null | wc -l) bases de dados"
echo -e "   ✓ Banco de imagens completo"
echo -e "   ✓ Todas as configurações"
echo -e "   ✓ Histórico Git completo"
echo -e "   ✓ Documentação completa"

echo -e "\n${YELLOW}Próximo passo: Commit e Push para GitHub${NC}"
echo -e "Execute: ${GREEN}git add . && git commit -m \"backup: ${TIMESTAMP}\" && git push${NC}\n"
