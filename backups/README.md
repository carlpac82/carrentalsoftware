# 🔒 Backups - CarRental API

Este diretório contém backups completos do sistema CarRental API.

## 📋 Conteúdo dos Backups

Cada backup inclui:

- ✅ **Base de dados** (`carrental.db` + SQL dump)
- ✅ **Uploads** (fotos de perfil, veículos)
- ✅ **Configurações** (`.env`, `requirements.txt`)
- ✅ **Código fonte** (`main.py`, `templates/`, `static/`)
- ✅ **Logs e cache**
- ✅ **Informações do sistema** (`BACKUP_INFO.txt`)

## 🚀 Como Criar um Backup

### Backup Completo (Recomendado)

```bash
./backup_full.sh
```

Este script cria um backup completo e comprimido em `backups/backup_YYYYMMDD_HHMMSS.tar.gz`

## 📦 Como Restaurar um Backup

### 1. Extrair o backup

```bash
cd backups
tar -xzf backup_20251030_011542.tar.gz
cd backup_20251030_011542
```

### 2. Restaurar arquivos

```bash
# Base de dados
cp carrental.db ../../

# Uploads (fotos)
cp -r uploads ../../

# Configurações
cp .env ../../

# Código fonte (se necessário)
cp main.py ../../
cp -r templates ../../
cp -r static ../../
```

### 3. Reinstalar dependências

```bash
cd ../..
pip install -r requirements.txt
```

### 4. Iniciar servidor

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 📅 Política de Backups

### Recomendações

- **Diário**: Antes de grandes alterações
- **Semanal**: Backup de rotina
- **Antes de deploy**: Sempre criar backup

### Automação (Opcional)

Adicionar ao crontab para backup automático diário às 3h:

```bash
0 3 * * * cd /path/to/carrental_api && ./backup_full.sh
```

## 🗑️ Limpeza de Backups Antigos

Manter apenas os últimos 30 dias:

```bash
find backups/ -name "backup_*.tar.gz" -mtime +30 -delete
```

## 🔐 Segurança

### Backups Locais

- Armazenados em `backups/`
- Comprimidos com tar.gz
- **NÃO commitados no Git** (ver `.gitignore`)

### Backups Remotos

Para maior segurança, copiar backups para:

1. **Google Drive / Dropbox**
2. **Servidor remoto via rsync**
3. **AWS S3 / Azure Blob Storage**

### Exemplo: Backup para servidor remoto

```bash
rsync -avz backups/ user@servidor:/backup/carrental_api/
```

## 📊 Verificar Backup

Após criar backup, verificar:

```bash
# Listar conteúdo
tar -tzf backups/backup_20251030_011542.tar.gz

# Ver informações
tar -xzf backups/backup_20251030_011542.tar.gz backup_20251030_011542/BACKUP_INFO.txt -O
```

## 🆘 Recuperação de Emergência

### Cenário 1: Base de dados corrompida

```bash
cd backups/backup_20251030_011542
cp carrental.db ../../
```

### Cenário 2: Fotos perdidas

```bash
cd backups/backup_20251030_011542
cp -r uploads ../../
```

### Cenário 3: Restauração completa

```bash
# Extrair backup
tar -xzf backups/backup_20251030_011542.tar.gz

# Mover para diretório do projeto
cd backup_20251030_011542
cp -r * ../../

# Reinstalar e reiniciar
cd ../..
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 📝 Histórico de Backups

| Data | Tamanho | Descrição |
|------|---------|-----------|
| 2025-10-30 01:15 | 3.8M | Backup completo com sistema de validação de preços |

## 🔗 Links Úteis

- [Documentação SQLite Backup](https://www.sqlite.org/backup.html)
- [Git Workflow](../WORKFLOW_CASA_TRABALHO.md)
- [Render Deploy](https://dashboard.render.com/)

---

**⚠️ IMPORTANTE:** Nunca commitar arquivos `.env` ou backups com dados sensíveis no Git público!
