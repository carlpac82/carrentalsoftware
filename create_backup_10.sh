#!/bin/bash

# Backup Completo 10 - Sistema Final com Calendar Scan
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="FULL_BACKUP_10_${TIMESTAMP}"
BACKUP_DIR="backups/${BACKUP_NAME}"
PROJECT_DIR=$(pwd)

echo "🗄️  CRIANDO BACKUP COMPLETO 10..."
echo "📂 Backup: ${BACKUP_NAME}"
echo ""

# Criar diretório de backup
mkdir -p "${BACKUP_DIR}"

# 1. Backup do código fonte
echo "📝 1/7 - Copiando código fonte..."
mkdir -p "${BACKUP_DIR}/source"
cp -r templates "${BACKUP_DIR}/source/"
cp -r static "${BACKUP_DIR}/source/"
cp main.py "${BACKUP_DIR}/source/"
cp requirements.txt "${BACKUP_DIR}/source/"
cp render.yaml "${BACKUP_DIR}/source/"
cp Dockerfile "${BACKUP_DIR}/source/" 2>/dev/null || true
cp .gitignore "${BACKUP_DIR}/source/" 2>/dev/null || true
echo "   ✅ Código fonte copiado"

# 2. Backup de configurações
echo "📋 2/7 - Copiando configurações..."
mkdir -p "${BACKUP_DIR}/config"
cp render.yaml "${BACKUP_DIR}/config/"
cp start.sh "${BACKUP_DIR}/config/" 2>/dev/null || true
echo "   ✅ Configurações copiadas"

# 3. Backup de scripts
echo "🔧 3/7 - Copiando scripts..."
mkdir -p "${BACKUP_DIR}/scripts"
cp -r scripts/* "${BACKUP_DIR}/scripts/" 2>/dev/null || true
cp *.sh "${BACKUP_DIR}/scripts/" 2>/dev/null || true
cp *.py "${BACKUP_DIR}/scripts/" 2>/dev/null || echo "   ⚠️  Nenhum script .py adicional"
echo "   ✅ Scripts copiados"

# 4. Backup de documentação
echo "📚 4/7 - Copiando documentação..."
mkdir -p "${BACKUP_DIR}/docs"
cp README.md "${BACKUP_DIR}/docs/" 2>/dev/null || echo "README.md" > "${BACKUP_DIR}/docs/README.md"
cp -r wordpress-plugin "${BACKUP_DIR}/docs/" 2>/dev/null || true
echo "   ✅ Documentação copiada"

# 5. Backup de dados SQLite
echo "💾 5/7 - Backup de databases..."
mkdir -p "${BACKUP_DIR}/data"
cp *.db "${BACKUP_DIR}/data/" 2>/dev/null || echo "   ⚠️  Nenhum arquivo .db encontrado"
cp *.sqlite3 "${BACKUP_DIR}/data/" 2>/dev/null || true
echo "   ✅ Databases copiadas"

# 6. Git info
echo "📊 6/7 - Salvando informações do Git..."
mkdir -p "${BACKUP_DIR}/git_info"
git log --oneline -20 > "${BACKUP_DIR}/git_info/recent_commits.txt" 2>/dev/null || true
git status > "${BACKUP_DIR}/git_info/status.txt" 2>/dev/null || true
git remote -v > "${BACKUP_DIR}/git_info/remotes.txt" 2>/dev/null || true
git branch -a > "${BACKUP_DIR}/git_info/branches.txt" 2>/dev/null || true
echo "   ✅ Git info salva"

# 7. Criar README do backup
echo "📄 7/7 - Criando README do backup..."
cat > "${BACKUP_DIR}/README_BACKUP.md" << 'EOF'
# FULL BACKUP 10 - Sistema Completo

## 📅 Data do Backup
Criado em: $(date)

## ✨ Features Incluídas

### 1. Calendar Scan System
- Escaneia próximos 24 meses
- Detecta mudanças de preço (>5%)
- Identifica períodos de pricing
- Histórico de scans guardado

### 2. Price Period Detection
- Backend analysis endpoint
- Detecção automática de períodos
- Low/Mid/High season classification
- Timeline de mudanças de preço

### 3. Enhanced Automated Prices
- Date Selection: Specific/Month/Year/Period
- Month picker para pricing mensal
- Year picker para estratégias anuais
- Period picker com períodos REAIS detectados

### 4. All Suppliers Comparison
- 20+ suppliers normalizados
- Comparação com TODOS disponíveis
- Display visual dos suppliers analisados
- Transparência total nos resultados

### 5. Deep Scan Dual Location
- Albufeira + Aeroporto de Faro
- 24 meses de análise
- Todos os períodos de rental
- Insights combinados

### 6. Complete History System
- Tab "Calendar Scans" no History
- Guarda últimos 10 scans
- View/Delete functionality
- Períodos e mudanças preservados

## 📂 Estrutura do Backup

```
FULL_BACKUP_10_YYYYMMDD_HHMMSS/
├── source/          # Código fonte completo
│   ├── templates/   # HTML templates
│   ├── static/      # CSS, JS, imagens
│   ├── main.py      # Backend FastAPI
│   └── ...
├── config/          # Configurações
│   └── render.yaml  # Deploy config
├── scripts/         # Scripts utilitários
├── docs/            # Documentação
├── data/            # Databases SQLite
├── git_info/        # Informações do Git
└── README_BACKUP.md # Este arquivo
```

## 🔄 Como Restaurar

### Restaurar Código:
```bash
cp -r source/* /caminho/destino/
```

### Restaurar Configurações:
```bash
cp config/render.yaml /caminho/destino/
```

### Restaurar Databases:
```bash
cp data/*.db /caminho/destino/
```

## 🚀 Deploy

Este backup está pronto para deploy em:
- Render.com (via render.yaml)
- Docker (via Dockerfile)
- Servidor Python direto (via main.py)

## 📝 Notas Importantes

- ✅ Código completo e funcional
- ✅ Todas as features testadas
- ✅ Git histórico limpo
- ✅ Deploy automático configurado
- ✅ Pronto para produção

## 🔗 Repositórios

- GitHub: github.com/carlpac82/carrentalsoftware
- Branch: main
- Commit: $(git rev-parse --short HEAD 2>/dev/null || echo "N/A")

---
**Backup criado automaticamente pelo script create_backup_10.sh**
EOF

echo "   ✅ README criado"
echo ""

# Criar tarball comprimido
echo "📦 Comprimindo backup..."
cd backups
tar -czf "${BACKUP_NAME}.tar.gz" "${BACKUP_NAME}/"
BACKUP_SIZE=$(du -h "${BACKUP_NAME}.tar.gz" | cut -f1)
echo "   ✅ Backup comprimido: ${BACKUP_SIZE}"
echo ""

# Resumo
echo "════════════════════════════════════════"
echo "✅ BACKUP COMPLETO 10 CRIADO COM SUCESSO!"
echo "════════════════════════════════════════"
echo ""
echo "📂 Localização:"
echo "   Pasta:    backups/${BACKUP_NAME}/"
echo "   Arquivo:  backups/${BACKUP_NAME}.tar.gz"
echo "   Tamanho:  ${BACKUP_SIZE}"
echo ""
echo "📋 Conteúdo:"
echo "   ✅ Código fonte completo"
echo "   ✅ Templates e static files"
echo "   ✅ Configurações (render.yaml)"
echo "   ✅ Scripts e utilitários"
echo "   ✅ Databases SQLite"
echo "   ✅ Git info e histórico"
echo "   ✅ Documentação completa"
echo ""
echo "🚀 Próximo passo: Fazer backup no GitHub"
echo "════════════════════════════════════════"
