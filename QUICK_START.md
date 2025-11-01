# ⚡ Quick Start - Windsurf Casa

## 🏠 NO COMPUTADOR DE CASA (Primeira Vez)

```bash
# 1. Clonar repositório
git clone https://github.com/comercial-autoprudente/carrental_api.git
cd carrental_api

# 2. Verificar setup
bash verify_setup.sh

# 3. Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# ou: venv\Scripts\activate  # Windows

# 4. Instalar dependências
pip install -r requirements.txt
playwright install

# 5. Iniciar servidor
python3 main.py

# 6. Abrir browser
# http://localhost:8000
# Login: admin / admin123
```

---

## 🔄 TODOS OS DIAS (Sincronizar)

```bash
# 1. Entrar na pasta
cd carrental_api

# 2. Buscar últimas alterações
git pull origin main

# 3. Ativar ambiente
source venv/bin/activate

# 4. Iniciar servidor
python3 main.py
```

---

## 💾 GUARDAR ALTERAÇÕES

```bash
# 1. Ver o que mudou
git status

# 2. Adicionar ficheiros
git add .

# 3. Commit
git commit -m "feat: descrição da alteração"

# 4. Push para GitHub
git push origin main
```

---

## 🚀 Comandos Rápidos

| Comando | Descrição |
|---------|-----------|
| `git status` | Ver alterações |
| `git log --oneline -10` | Ver últimos 10 commits |
| `git pull origin main` | Buscar alterações |
| `git push origin main` | Enviar alterações |
| `bash verify_setup.sh` | Verificar setup |
| `source venv/bin/activate` | Ativar ambiente |
| `python3 main.py` | Iniciar servidor |

---

## 🌐 URLs Importantes

- **Homepage:** http://localhost:8000/
- **Admin:** http://localhost:8000/admin/users
- **Vehicle Editor:** http://localhost:8000/admin/car-groups
- **GitHub:** https://github.com/comercial-autoprudente/carrental_api

---

## 🐛 Problemas Comuns

### Porta ocupada
```bash
lsof -i :8000
kill -9 <PID>
```

### Dependências
```bash
pip install -r requirements.txt
```

### Git conflitos
```bash
git stash
git pull
git stash pop
```

---

## ✅ TODO Está no GitHub!

- ✓ **Histórico completo** de todos os commits
- ✓ **Todas as funcionalidades** implementadas
- ✓ **Ficheiros e fotos** incluídos
- ✓ **Configurações** preservadas

**Repositório:** https://github.com/comercial-autoprudente/carrental_api
