# 🔄 Workflow Bidirecional Casa ↔️ Trabalho

## ✅ Setup Completo em Casa

**Repositório GitHub:** https://github.com/comercial-autoprudente/carrental_api

### Configuração Inicial (FEITO ✓)
- ✅ Repositório clonado
- ✅ Virtual environment criado
- ✅ Dependências instaladas
- ✅ Playwright browsers instalados
- ✅ Base de dados criada
- ✅ Utilizador admin configurado
- ✅ Servidor a correr em http://localhost:8000

### 🔑 Credenciais
```
Username: admin
Password: admin123
```

---

## 🔄 Sincronização Bidirecional

### 📥 Antes de Trabalhar (Pull)
```bash
cd ~/CascadeProjects/RentalPriceTrackerPerDay/carrental_api

# 1. Ver estado atual
git status

# 2. Puxar últimas alterações do trabalho
git pull origin main

# 3. Ativar ambiente virtual
source venv/bin/activate

# 4. Atualizar dependências (se necessário)
pip install -r requirements.txt

# 5. Iniciar servidor
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 📤 Depois de Trabalhar (Push)
```bash
# 1. Ver ficheiros modificados
git status

# 2. Adicionar alterações
git add .

# 3. Commit com mensagem descritiva
git commit -m "feat: descrição das alterações feitas em casa"

# 4. Push para GitHub
git push origin main

# 5. Verificar
git log --oneline -5
```

---

## 📋 Comandos Rápidos

### Iniciar Servidor
```bash
cd ~/CascadeProjects/RentalPriceTrackerPerDay/carrental_api
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Ver Logs do Servidor
```bash
tail -f server.log
tail -f server_errors.log
```

### Reiniciar Servidor
```bash
# Matar processo na porta 8000
lsof -ti :8000 | xargs kill -9

# Iniciar novamente
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Atualizar Base de Dados
```bash
python3 init_db.py
```

---

## 🎯 Workflow Recomendado

### Trabalho → Casa
1. **No Trabalho:** Fazer commit e push das alterações
   ```bash
   git add .
   git commit -m "feat: alteração X"
   git push origin main
   ```

2. **Em Casa:** Pull das alterações
   ```bash
   git pull origin main
   ```

3. **Continuar trabalho em casa**

### Casa → Trabalho
1. **Em Casa:** Fazer commit e push
   ```bash
   git add .
   git commit -m "feat: alteração Y"
   git push origin main
   ```

2. **No Trabalho:** Pull das alterações
   ```bash
   git pull origin main
   ```

3. **Continuar trabalho no escritório**

---

## 🔍 Verificar Estado

### Ver Histórico
```bash
# Últimos 10 commits
git log --oneline -10

# Ver diferenças
git diff

# Ver branches
git branch -a
```

### Verificar Setup
```bash
bash verify_setup.sh
```

---

## 🐛 Resolução de Problemas

### Conflitos no Git
```bash
# Se houver conflitos ao fazer pull
git status  # ver ficheiros em conflito
# Editar ficheiros manualmente
git add .
git commit -m "fix: resolver conflitos"
git push origin main
```

### Porta 8000 Ocupada
```bash
# Ver processo
lsof -i :8000

# Matar processo
lsof -ti :8000 | xargs kill -9

# Ou usar outra porta
uvicorn main:app --host 0.0.0.0 --port 8001
```

### Dependências em Falta
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Base de Dados Corrompida
```bash
# Backup
cp carrental.db carrental.db.backup

# Reinicializar
rm carrental.db
python3 init_db.py
```

---

## 📁 Estrutura do Projeto

```
carrental_api/
├── main.py                      # Servidor FastAPI principal (6831 linhas)
├── carjet_direct.py            # Scraping CarJet + 316 veículos
├── init_db.py                  # Script de inicialização DB
├── requirements.txt            # 17 dependências Python
├── .env                        # Configuração (não no Git)
├── carrental.db               # Base de dados SQLite
├── venv/                      # Ambiente virtual
├── templates/                 # 11 templates HTML
├── static/                    # Assets (logos, fotos, CSS)
└── WORKFLOW_CASA_TRABALHO.md  # Este ficheiro
```

---

## ✅ Checklist Diário

### Antes de Começar
- [ ] `cd carrental_api`
- [ ] `git pull origin main`
- [ ] `source venv/bin/activate`
- [ ] `uvicorn main:app --host 0.0.0.0 --port 8000`
- [ ] Testar http://localhost:8000

### Antes de Terminar
- [ ] Parar servidor (Ctrl+C)
- [ ] `git status` (ver alterações)
- [ ] `git add .`
- [ ] `git commit -m "descrição"`
- [ ] `git push origin main`
- [ ] Verificar no GitHub que push foi bem sucedido

---

## 🎓 Boas Práticas Git

### Mensagens de Commit
```bash
# Boa
git commit -m "feat: adicionar filtro por categoria"
git commit -m "fix: corrigir bug de preços em libras"
git commit -m "docs: atualizar README com instruções"

# Má
git commit -m "update"
git commit -m "fix stuff"
git commit -m "changes"
```

### Tipos de Commit
- `feat:` - Nova funcionalidade
- `fix:` - Correção de bug
- `docs:` - Documentação
- `refactor:` - Refactoring sem mudar funcionalidade
- `style:` - Formatação, espaços, etc
- `test:` - Adicionar testes
- `chore:` - Manutenção geral

---

## 📊 Estado Atual do Projeto

### Funcionalidades Implementadas
- ✅ Scraping CarJet em tempo real (Playwright)
- ✅ 150+ suppliers mapeados
- ✅ Clean names automático (ex: Fiat 500)
- ✅ Vehicle Editor completo
- ✅ Criar categorias (B1, D, E2, etc)
- ✅ Criar grupos por marca
- ✅ Export/Import configuração com fotos
- ✅ Fotos de veículos automáticas
- ✅ Cache de resultados inteligente
- ✅ Gestão de utilizadores
- ✅ Sistema de autenticação
- ✅ Interface responsiva
- ✅ Cores da marca (azul + amarelo)

### Histórico
- 90+ commits
- Desenvolvimento desde início do projeto
- Totalmente sincronizado entre casa e trabalho

---

## 🆘 Suporte

### Se algo correr mal:
1. Verificar `git status`
2. Ver logs: `tail -f server.log`
3. Consultar `SETUP_WINDSURF_CASA.md`
4. Consultar `TROUBLESHOOTING.md`
5. Fazer `git pull` para garantir última versão
6. Executar `bash verify_setup.sh`

### Contactos
- GitHub: https://github.com/comercial-autoprudente/carrental_api
- Issues: https://github.com/comercial-autoprudente/carrental_api/issues

---

**TUDO PRONTO PARA TRABALHO BIDIRECIONAL! 🚀**
