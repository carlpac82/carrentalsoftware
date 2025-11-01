# 🔒 Guia de Backup Completo - CarRental API

## 📋 Visão Geral

Este documento descreve o procedimento completo de backup do projeto CarRental API, incluindo todos os componentes críticos.

## 🎯 O que é incluído no Backup Full

### 1. **Código Fonte Completo**
- Todos os ficheiros `.py`, `.html`, `.js`, `.css`
- Templates e static files
- Scripts de teste e utilitários
- Configurações do projeto

### 2. **Bases de Dados SQLite**
- `carrental.db` - Base de dados principal
- `car_images.db` - Imagens dos veículos
- `data.db` - Dados adicionais
- `rental_tracker.db` - Sistema de tracking

### 3. **Banco de Imagens**
- `cars/` - Fotos dos veículos (14 ficheiros)
- `static/images/` - Imagens estáticas da UI
- `static/logos/` - Logos das empresas
- `uploads/` - Uploads de utilizadores

### 4. **Configurações e Parametrizações**
- `.env` - Variáveis de ambiente (URLs CarJet, credenciais)
- `requirements.txt` - Dependências Python
- `render.yaml` - Configuração Render.com
- `Dockerfile` - Configuração Docker
- `Brokers Albufeira.xlsx` - Dados dos brokers

### 5. **Histórico Git Completo**
- Repository bundle (todos os commits)
- Log de commits
- Lista de branches
- Tags de versão

### 6. **Documentação**
- Todos os ficheiros `.md`
- Guias de deployment
- Troubleshooting
- Workflows

### 7. **Parametrizações de Veículos e Grupos**
- Mapeamento de categorias para grupos (B1, B2, D, E1, E2, F, G, J1, J2, L1, L2, M1, M2, N, Others)
- Configurações de nomes limpos dos veículos
- Imagens associadas a cada veículo

## 🚀 Como Executar o Backup

### Método Automático (Recomendado)

```bash
cd ~/CascadeProjects/RentalPriceTrackerPerDay
./backup_full_complete.sh
```

O script irá:
1. ✅ Criar diretório com timestamp
2. ✅ Copiar todo o código fonte
3. ✅ Fazer backup de todas as bases de dados
4. ✅ Copiar banco de imagens completo
5. ✅ Backup de todas as configurações
6. ✅ Criar Git bundle com histórico completo
7. ✅ Copiar documentação
8. ✅ Criar manifesto detalhado
9. ✅ Comprimir tudo em arquivo `.tar.gz`
10. ✅ Mostrar resumo completo

### Localização dos Backups

**Backup Local:**
```
~/CascadeProjects/backups_full/
├── backup_full_YYYYMMDD_HHMMSS/
│   ├── code/           # Código fonte
│   ├── database/       # Bases de dados
│   ├── images/         # Banco de imagens
│   ├── config/         # Configurações
│   ├── git/            # Histórico Git
│   ├── docs/           # Documentação
│   └── MANIFEST.txt    # Manifesto do backup
└── backup_full_YYYYMMDD_HHMMSS.tar.gz  # Arquivo comprimido
```

**Backup GitHub:**
- Repositório: https://github.com/carlpac82/carrentalsoftware
- Tag: `backup-YYYYMMDD_HHMMSS`
- Commit: "backup: script completo de backup full"

## 📦 Exemplo de Backup Realizado

**Data:** 30 de Outubro de 2025, 19:37:55  
**Timestamp:** 20251030_193755  
**Tamanho:** 80 MB comprimido  
**Localização Local:** `../backups_full/backup_full_20251030_193755.tar.gz`  
**Tag GitHub:** `backup-20251030_193755`

### Conteúdo Verificado:
- ✅ 4 bases de dados SQLite
- ✅ 14 imagens de veículos
- ✅ Código fonte completo (801 MB antes compressão)
- ✅ Todas as configurações (.env, requirements.txt, etc.)
- ✅ Histórico Git completo (1135 objetos)
- ✅ 30+ ficheiros de documentação

## 🔄 Como Restaurar um Backup

### 1. Restaurar do Arquivo Local

```bash
# Extrair backup
cd ~/CascadeProjects
tar -xzf backups_full/backup_full_YYYYMMDD_HHMMSS.tar.gz

# Entrar no diretório
cd backup_full_YYYYMMDD_HHMMSS

# Copiar código
cp -r code/* ~/CascadeProjects/RentalPriceTrackerPerDay/

# Restaurar bases de dados
cp database/*.db ~/CascadeProjects/RentalPriceTrackerPerDay/

# Restaurar imagens
cp -r images/cars ~/CascadeProjects/RentalPriceTrackerPerDay/
cp -r images/uploads ~/CascadeProjects/RentalPriceTrackerPerDay/

# Restaurar configurações
cp config/.env_* ~/CascadeProjects/RentalPriceTrackerPerDay/.env
cp config/requirements.txt ~/CascadeProjects/RentalPriceTrackerPerDay/

# Reinstalar dependências
cd ~/CascadeProjects/RentalPriceTrackerPerDay
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Restaurar do Git Bundle

```bash
# Clonar do bundle
git clone git/repository_YYYYMMDD_HHMMSS.bundle novo_projeto
cd novo_projeto

# Verificar branches
git branch -a

# Checkout para main
git checkout main
```

### 3. Restaurar do GitHub

```bash
# Clonar repositório
git clone https://github.com/carlpac82/carrentalsoftware.git

# Checkout para tag específica
cd carrentalsoftware
git checkout tags/backup-YYYYMMDD_HHMMSS
```

## 🔐 Segurança

### Ficheiros Sensíveis Incluídos:
- ⚠️ `.env` - Contém credenciais e URLs do CarJet
- ⚠️ `carrental.db` - Dados de utilizadores (passwords hash)
- ⚠️ `SECRET_KEY` - Chave de encriptação

### Recomendações:
1. **Manter backups locais em local seguro**
2. **Não partilhar arquivos `.tar.gz` publicamente**
3. **GitHub privado** - Repositório deve ser privado
4. **Encriptar backups** para armazenamento externo

## 📅 Frequência Recomendada

- **Backup Automático:** Antes de cada deploy
- **Backup Manual:** Após alterações críticas
- **Backup Completo:** Semanalmente
- **Backup de Emergência:** Antes de updates major

## 🆘 Troubleshooting

### Erro: "Permission denied"
```bash
chmod +x backup_full_complete.sh
```

### Erro: "No space left on device"
```bash
# Limpar backups antigos
cd ~/CascadeProjects/backups_full
rm -rf backup_full_202410*  # Cuidado!
```

### Erro: "Git push rejected"
```bash
# Fazer pull primeiro
git pull origin main
# Resolver conflitos se necessário
git push origin main
git push origin backup-YYYYMMDD_HHMMSS
```

## 📊 Checklist de Backup Completo

Quando pedir "cópia de segurança", verificar:

- [ ] Código fonte completo
- [ ] Todas as bases de dados SQLite
- [ ] Banco de imagens (cars/, uploads/, static/)
- [ ] Ficheiro .env com URLs CarJet
- [ ] requirements.txt e dependências
- [ ] Histórico Git completo (bundle)
- [ ] Documentação (.md files)
- [ ] Parametrizações de veículos
- [ ] Mapeamento de grupos (B1-N, Others)
- [ ] Configurações Render/Docker
- [ ] Dados Excel (Brokers)
- [ ] Commit no Git local
- [ ] Tag de backup criada
- [ ] Push para GitHub
- [ ] Arquivo .tar.gz criado
- [ ] Manifesto gerado

## 🔗 Links Úteis

- **Repositório GitHub:** https://github.com/carlpac82/carrentalsoftware
- **Render Deploy:** https://dashboard.render.com
- **Documentação Completa:** Ver ficheiros `.md` no projeto

## 📝 Notas Importantes

1. **Backups locais** são mais rápidos para restaurar
2. **Git bundle** preserva todo o histórico
3. **GitHub** serve como backup remoto seguro
4. **Arquivo .tar.gz** facilita transferência
5. **Manifesto** documenta exatamente o que foi incluído

---

**Última Atualização:** 30 de Outubro de 2025  
**Versão do Script:** backup_full_complete.sh  
**Autor:** Filipe Pacheco
