# 📦 Sistema de Backup Completo - Car Rental API

## 🎯 O que é guardado no backup?

Este sistema cria backups **COMPLETOS** de TUDO:

### ✅ Código Fonte
- `main.py` e todos os ficheiros Python
- Templates HTML (todas as páginas)
- Ficheiros estáticos (CSS, JS, imagens)
- Scripts e utilitários

### ✅ Git Repository
- **Histórico completo** de todos os commits
- Todas as branches
- Tags e releases
- **Permite restaurar qualquer versão anterior**

### ✅ Bases de Dados
- `carrental.db` - Utilizadores, settings, automation_settings, logs
- `car_images.db` - Fotos de veículos em blob
- `data.db` - Dados de scraping
- **SQL dumps** de todas as DBs (para restauro fácil)

### ✅ Fotos e Imagens
- Todas as fotos de veículos (`static/vehicle_photos/`)
- Logos (Auto Prudente)
- Favicons
- Profile pictures

### ✅ Configurações
- `.env` - Credenciais e API keys
- `render.yaml` - Configuração de deploy
- `Dockerfile` - Container config
- `requirements.txt` - Dependências Python

### ✅ Documentação
- Todos os ficheiros `.md`
- Guias de deploy (DEPLOY_RENDER.md, etc)
- Workflows e checklists
- Notas e instruções

---

## 🚀 Como Criar um Backup

### Método 1: Script Automático (Recomendado)

```bash
cd ~/CascadeProjects/RentalPriceTrackerPerDay
./create_full_backup.sh
```

O script irá:
1. ✅ Copiar todo o código fonte
2. ✅ Clonar o repositório Git completo
3. ✅ Copiar todas as bases de dados + criar SQL dumps
4. ✅ Copiar todas as fotos
5. ✅ Copiar configurações
6. ✅ Copiar documentação
7. ✅ Criar metadata com informações do backup
8. ✅ Comprimir tudo num arquivo `.tar.gz`

**Resultado:**
- 📁 **LOCAL**: Pasta `backups/FULL_BACKUP_YYYYMMDD_HHMMSS/`
- 📦 **LOCAL**: Arquivo `backups/FULL_BACKUP_YYYYMMDD_HHMMSS.tar.gz`
- ☁️ **GITHUB**: Push automático para `comercial-autoprudente/carrental_api`

### Método 2: Manual

Se preferires fazer manualmente:

```bash
cd ~/CascadeProjects/RentalPriceTrackerPerDay
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
mkdir -p backups/FULL_BACKUP_$TIMESTAMP
cp -r . backups/FULL_BACKUP_$TIMESTAMP/
cd backups
tar -czf FULL_BACKUP_$TIMESTAMP.tar.gz FULL_BACKUP_$TIMESTAMP
```

---

## 📂 Estrutura do Backup

```
FULL_BACKUP_20251031_020000/
├── source/                    # Código fonte completo
│   ├── main.py
│   ├── templates/
│   ├── static/
│   └── ...
├── git_mirror.git/            # Git repository completo
├── databases/                 # Bases de dados
│   ├── carrental.db
│   ├── carrental_dump.sql
│   ├── car_images.db
│   ├── car_images_dump.sql
│   ├── data.db
│   └── data_dump.sql
├── vehicle_photos/            # Fotos de veículos
├── static/                    # Ficheiros estáticos
├── templates/                 # Templates HTML
├── config/                    # Configurações
│   ├── .env
│   ├── render.yaml
│   ├── Dockerfile
│   └── requirements.txt
├── logs/                      # Logs (se existirem)
├── docs/                      # Documentação
└── BACKUP_INFO.txt           # Metadata do backup
```

---

## 🔄 Como Restaurar um Backup

### Restauro Completo

```bash
cd ~/CascadeProjects/RentalPriceTrackerPerDay/backups

# Extrair o backup
tar -xzf FULL_BACKUP_20251031_020000.tar.gz
cd FULL_BACKUP_20251031_020000

# Restaurar código fonte
cp -r source/* ~/CascadeProjects/RentalPriceTrackerPerDay/

# Restaurar bases de dados
cp databases/*.db ~/CascadeProjects/RentalPriceTrackerPerDay/

# Restaurar fotos
cp -r vehicle_photos/* ~/CascadeProjects/RentalPriceTrackerPerDay/static/vehicle_photos/

# Restaurar configurações
cp config/.env ~/CascadeProjects/RentalPriceTrackerPerDay/
```

### Restauro Parcial (apenas BD)

```bash
cd ~/CascadeProjects/RentalPriceTrackerPerDay/backups
tar -xzf FULL_BACKUP_20251031_020000.tar.gz
cp FULL_BACKUP_20251031_020000/databases/carrental.db ~/CascadeProjects/RentalPriceTrackerPerDay/
```

### Restauro de Git History

```bash
cd ~/CascadeProjects/RentalPriceTrackerPerDay/backups
tar -xzf FULL_BACKUP_20251031_020000.tar.gz
cd ~/CascadeProjects/RentalPriceTrackerPerDay
git clone backups/FULL_BACKUP_20251031_020000/git_mirror.git .git
```

---

## ⏰ Quando Fazer Backups?

### 🔴 Obrigatório (SEMPRE)
- ✅ Antes de fazer deploy para produção
- ✅ Antes de alterações grandes no código
- ✅ Antes de modificar bases de dados
- ✅ Antes de fechar o Windsurf/IDE
- ✅ No fim de cada dia de trabalho

### 🟡 Recomendado
- ✅ Depois de adicionar features importantes
- ✅ Depois de corrigir bugs críticos
- ✅ Antes de atualizar dependências
- ✅ Semanalmente (mínimo)

### 🟢 Opcional
- ✅ Antes de experimentar código novo
- ✅ Antes de fazer refactoring
- ✅ Mensalmente (para arquivo)

---

## 💾 Onde Guardar os Backups?

### Local (Atual)
```
~/CascadeProjects/RentalPriceTrackerPerDay/backups/
```
✅ Rápido
❌ Só no Mac (se o disco falhar, perdes tudo)

### GitHub (Recomendado)
```bash
# Já configurado!
git push backup main
```
✅ Seguro (cloud)
✅ Versionado
✅ Acessível de qualquer lugar

### Cloud Storage (Extra)
- **Google Drive**: Copiar `.tar.gz` para Drive
- **Dropbox**: Sincronizar pasta `backups/`
- **iCloud**: Mover backups para iCloud Drive

**Recomendação:** Usa os 3! (Local + GitHub + Cloud)

---

## 📊 Gestão de Backups Antigos

### Limpar Backups Antigos

```bash
cd ~/CascadeProjects/RentalPriceTrackerPerDay/backups

# Ver backups ordenados por data
ls -lth

# Apagar backups com mais de 30 dias
find . -name "FULL_BACKUP_*.tar.gz" -mtime +30 -delete

# Manter apenas os últimos 10 backups
ls -t FULL_BACKUP_*.tar.gz | tail -n +11 | xargs rm
```

### Política de Retenção Sugerida

- **Últimos 7 dias**: Todos os backups
- **Último mês**: 1 backup por semana
- **Último ano**: 1 backup por mês
- **Mais de 1 ano**: Apagar (ou mover para arquivo)

---

## 🔍 Verificar Integridade do Backup

```bash
cd ~/CascadeProjects/RentalPriceTrackerPerDay/backups

# Testar arquivo comprimido
tar -tzf FULL_BACKUP_20251031_020000.tar.gz > /dev/null
echo $?  # Se retornar 0, está OK

# Ver conteúdo sem extrair
tar -tzf FULL_BACKUP_20251031_020000.tar.gz | less

# Ver informações do backup
tar -xzf FULL_BACKUP_20251031_020000.tar.gz FULL_BACKUP_20251031_020000/BACKUP_INFO.txt -O
```

---

## 🚨 Troubleshooting

### Backup muito grande

**Problema**: Arquivo `.tar.gz` > 1GB

**Solução**:
```bash
# Excluir fotos grandes (fazer backup separado)
# Editar create_full_backup.sh e adicionar:
# --exclude='*.jpg' --exclude='*.png'
```

### Sem espaço em disco

**Problema**: `No space left on device`

**Solução**:
```bash
# Limpar backups antigos
cd ~/CascadeProjects/RentalPriceTrackerPerDay/backups
rm -rf FULL_BACKUP_2024*  # Apagar backups de 2024

# Verificar espaço
df -h
```

### Backup corrompido

**Problema**: Erro ao extrair `.tar.gz`

**Solução**:
```bash
# Usar backup anterior
ls -lt backups/*.tar.gz | head -5

# Ou restaurar do GitHub
git clone https://github.com/comercial-autoprudente/carrental_api.git
```

---

## 📝 Checklist de Backup

Antes de fechar o Windsurf:

- [ ] Fazer commit de todas as alterações
- [ ] Push para GitHub (`git push backup main`)
- [ ] Executar `./create_full_backup.sh`
- [ ] Verificar que backup foi criado (`.tar.gz` existe)
- [ ] (Opcional) Copiar `.tar.gz` para Google Drive

---

## 🎯 Resumo

**Para criar backup:**
```bash
./create_full_backup.sh
```

**Para restaurar:**
```bash
tar -xzf backups/FULL_BACKUP_*.tar.gz
# Copiar ficheiros necessários
```

**Frequência:** Diariamente (mínimo) ou antes de mudanças importantes

**Localização:** Local + GitHub + Cloud (tripla segurança)

---

**Última atualização:** 31 de Outubro de 2025  
**Autor:** Cascade AI Assistant  
**Status:** ✅ Pronto para uso
