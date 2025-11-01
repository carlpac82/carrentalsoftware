#!/bin/bash

# ============================================================
# BACKUP COMPLETO - CarRental API
# ============================================================
# Este script cria um backup completo de:
# - Base de dados SQLite
# - Uploads (fotos de perfil, veículos)
# - Configurações (.env)
# - Código fonte
# - Histórico de pedidos e logs
# ============================================================

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="backups/backup_${TIMESTAMP}"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "============================================================"
echo "🔒 BACKUP COMPLETO - CarRental API"
echo "============================================================"
echo "📅 Data: $(date)"
echo "📁 Diretório: $PROJECT_DIR"
echo "💾 Backup: $BACKUP_DIR"
echo ""

# Criar diretório de backup
mkdir -p "$BACKUP_DIR"

# ============================================================
# 1. BACKUP DA BASE DE DADOS
# ============================================================
echo "📊 [1/6] Backing up database..."
if [ -f "carrental.db" ]; then
    cp carrental.db "$BACKUP_DIR/carrental.db"
    sqlite3 carrental.db ".dump" > "$BACKUP_DIR/carrental_dump.sql"
    echo "   ✅ Database backed up (SQLite + SQL dump)"
else
    echo "   ⚠️  Database not found"
fi

# ============================================================
# 2. BACKUP DOS UPLOADS (Fotos)
# ============================================================
echo "📸 [2/6] Backing up uploads..."
if [ -d "uploads" ]; then
    cp -r uploads "$BACKUP_DIR/uploads"
    echo "   ✅ Uploads backed up"
else
    echo "   ⚠️  Uploads directory not found"
fi

# ============================================================
# 3. BACKUP DAS CONFIGURAÇÕES
# ============================================================
echo "⚙️  [3/6] Backing up configurations..."
if [ -f ".env" ]; then
    cp .env "$BACKUP_DIR/.env"
    echo "   ✅ .env backed up"
else
    echo "   ⚠️  .env not found"
fi

cp requirements.txt "$BACKUP_DIR/requirements.txt" 2>/dev/null || echo "   ⚠️  requirements.txt not found"

# ============================================================
# 4. BACKUP DO CÓDIGO FONTE
# ============================================================
echo "💻 [4/6] Backing up source code..."
cp main.py "$BACKUP_DIR/main.py" 2>/dev/null
cp carjet_direct.py "$BACKUP_DIR/carjet_direct.py" 2>/dev/null
cp -r templates "$BACKUP_DIR/templates" 2>/dev/null
cp -r static "$BACKUP_DIR/static" 2>/dev/null
echo "   ✅ Source code backed up"

# ============================================================
# 5. BACKUP DE LOGS E CACHE
# ============================================================
echo "📝 [5/6] Backing up logs and cache..."
if [ -d "logs" ]; then
    cp -r logs "$BACKUP_DIR/logs"
    echo "   ✅ Logs backed up"
fi

if [ -d "cache" ]; then
    cp -r cache "$BACKUP_DIR/cache"
    echo "   ✅ Cache backed up"
fi

# ============================================================
# 6. CRIAR ARQUIVO DE INFORMAÇÕES
# ============================================================
echo "📋 [6/6] Creating backup info..."
cat > "$BACKUP_DIR/BACKUP_INFO.txt" << EOF
============================================================
BACKUP COMPLETO - CarRental API
============================================================
Data do Backup: $(date)
Timestamp: $TIMESTAMP
Hostname: $(hostname)
User: $(whoami)
Python Version: $(python3 --version 2>/dev/null || echo "N/A")

============================================================
CONTEÚDO DO BACKUP
============================================================
✅ Base de dados: carrental.db + SQL dump
✅ Uploads: Fotos de perfil e veículos
✅ Configurações: .env, requirements.txt
✅ Código fonte: main.py, templates, static
✅ Logs e cache

============================================================
RESTAURAR BACKUP
============================================================
1. Copiar carrental.db para o diretório do projeto
2. Copiar uploads/ para o diretório do projeto
3. Copiar .env para o diretório do projeto
4. Instalar dependências: pip install -r requirements.txt
5. Iniciar servidor: uvicorn main:app --host 0.0.0.0 --port 8000

============================================================
GIT STATUS
============================================================
$(git log --oneline -5 2>/dev/null || echo "Git not available")

============================================================
DATABASE STATS
============================================================
EOF

# Adicionar estatísticas da base de dados
if [ -f "carrental.db" ]; then
    sqlite3 carrental.db "SELECT 'Users: ' || COUNT(*) FROM users;" >> "$BACKUP_DIR/BACKUP_INFO.txt" 2>/dev/null || echo "Users: N/A" >> "$BACKUP_DIR/BACKUP_INFO.txt"
    sqlite3 carrental.db "SELECT 'Vehicles: ' || COUNT(*) FROM vehicles;" >> "$BACKUP_DIR/BACKUP_INFO.txt" 2>/dev/null || echo "Vehicles: N/A" >> "$BACKUP_DIR/BACKUP_INFO.txt"
fi

echo "   ✅ Backup info created"

# ============================================================
# 7. COMPRIMIR BACKUP
# ============================================================
echo ""
echo "🗜️  Compressing backup..."
cd backups
tar -czf "backup_${TIMESTAMP}.tar.gz" "backup_${TIMESTAMP}"
BACKUP_SIZE=$(du -h "backup_${TIMESTAMP}.tar.gz" | cut -f1)
cd ..

echo "   ✅ Backup compressed: backup_${TIMESTAMP}.tar.gz ($BACKUP_SIZE)"

# ============================================================
# 8. RESUMO
# ============================================================
echo ""
echo "============================================================"
echo "✅ BACKUP CONCLUÍDO COM SUCESSO!"
echo "============================================================"
echo "📦 Arquivo: backups/backup_${TIMESTAMP}.tar.gz"
echo "📏 Tamanho: $BACKUP_SIZE"
echo "📁 Pasta: $BACKUP_DIR"
echo ""
echo "💡 Para restaurar:"
echo "   tar -xzf backups/backup_${TIMESTAMP}.tar.gz"
echo "   cd backup_${TIMESTAMP}"
echo "   cp carrental.db ../"
echo "   cp -r uploads ../"
echo "   cp .env ../"
echo ""
echo "🔒 Backup seguro criado!"
echo "============================================================"
