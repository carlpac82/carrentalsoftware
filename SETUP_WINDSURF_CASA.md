# 🏠 Setup Completo para Windsurf em Casa

## 📦 PASSO 1: Clonar Repositório com TODO o Histórico

### **No seu computador de casa:**

```bash
# 1. Abrir terminal
cd ~/Desktop  # ou qualquer pasta

# 2. Clonar repositório completo
git clone https://github.com/comercial-autoprudente/carrental_api.git

# 3. Entrar na pasta
cd carrental_api

# 4. Verificar histórico (deve ter 100+ commits)
git log --oneline | wc -l
```

---

## 🔧 PASSO 2: Instalar Dependências

### **Python 3.11+ necessário:**

```bash
# Verificar versão Python
python3 --version

# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Instalar Playwright browsers
playwright install
```

---

## 🗄️ PASSO 3: Configurar Base de Dados

### **SQLite já incluído no projeto:**

```bash
# Verificar se ficheiro existe
ls -lh carrental.db

# Se não existir, será criado automaticamente ao iniciar
```

### **Criar utilizador admin:**

```bash
# Executar script de criação
python3 -c "
from main import hash_password, get_db_connection
import secrets

conn = get_db_connection()
c = conn.cursor()

# Criar tabela users se não existir
c.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')

# Inserir admin
username = 'admin'
password = 'admin123'  # MUDE ISTO!
password_hash = hash_password(password)

c.execute('INSERT OR IGNORE INTO users (username, password_hash) VALUES (?, ?)',
          (username, password_hash))
conn.commit()
conn.close()
print(f'✓ User {username} criado!')
"
```

---

## 🚀 PASSO 4: Iniciar Aplicação

```bash
# Ativar ambiente virtual (se não estiver ativo)
source venv/bin/activate  # macOS/Linux
# ou
venv\Scripts\activate  # Windows

# Iniciar servidor
python3 main.py

# Deve aparecer:
# ✓ Running on http://localhost:8000
```

---

## 🌐 PASSO 5: Testar no Browser

### **Abrir no browser:**

```
http://localhost:8000/
```

### **Login:**
```
Username: admin
Password: admin123  (ou a que definiu)
```

### **Páginas principais:**
- **Homepage:** http://localhost:8000/
- **Admin Users:** http://localhost:8000/admin/users
- **Vehicle Editor:** http://localhost:8000/admin/car-groups
- **Settings:** http://localhost:8000/admin/settings

---

## 📂 Estrutura do Projeto

```
carrental_api/
├── main.py                      # Servidor FastAPI principal
├── carjet_direct.py            # Scraping CarJet + VEHICLES
├── requirements.txt            # Dependências Python
├── carrental.db               # Base de dados SQLite
├── templates/
│   └── index.html             # Frontend principal
├── vehicle_editor.html        # Editor de veículos
├── static/
│   ├── logos/                 # Logos suppliers
│   ├── vehicle_photos/        # Fotos veículos
│   └── ap-heather.png        # Logo Auto Prudente
└── venv/                      # Ambiente virtual Python
```

---

## 🔄 Manter Sincronizado

### **Fazer Pull das últimas alterações:**

```bash
# No computador de casa
cd carrental_api
git pull origin main
```

### **Fazer Push das suas alterações:**

```bash
# Adicionar ficheiros modificados
git add .

# Commit com mensagem
git commit -m "feat: descrição da alteração"

# Push para GitHub
git push origin main
```

---

## 🐛 Troubleshooting

### **Problema: "Port 8000 already in use"**

```bash
# Encontrar processo
lsof -i :8000

# Matar processo
kill -9 <PID>

# Ou usar outra porta
python3 main.py --port 8001
```

### **Problema: "Module not found"**

```bash
# Reinstalar dependências
pip install -r requirements.txt
```

### **Problema: "playwright not found"**

```bash
# Instalar browsers
playwright install
```

### **Problema: "Database locked"**

```bash
# Parar servidor
# Verificar se outro processo está a usar
lsof carrental.db

# Reiniciar servidor
```

---

## 📝 Commits Recentes (últimos 20)

```
6504fe2 - feat: mapeamento COMPLETO de 150+ suppliers
f673027 - feat: adicionar códigos de suppliers faltantes
46e5d9c - feat: mapear códigos de imagem para nomes
48d46d8 - fix: corrigir limpeza de nomes sem espaços
9d8b1e2 - feat: aplicar clean names na frontend UI
da5b22b - feat: endpoint para mapear nomes para clean names
1bbc729 - feat: atribuir grupo a categoria ao criar novo grupo
4303e6f - feat: adicionar botões criar categoria/grupo
f29ff4b - feat: BOTÕES DESTACADOS para criar categorias
49d4fbb - feat: capitalizar Clean Name
50e9492 - feat: modais profissionais para criar categorias
c4e443c - feat: adicionar coluna Group nas tabelas
6303531 - feat: adicionar toggle e scroll melhorado
5907fb2 - feat: aplicar cores da UI (azul/amarelo)
41a1b60 - feat: agrupar veículos por marca
62b5b0c - fix: corrigir campo password para password_hash
075e3ff - fix: corrigir erros de export e interface
255dc6a - docs: atualizar guia com fotos
3f638c3 - feat: exportar/importar com fotos + suppliers
0cd6293 - docs: adicionar guia completo de backup
```

---

## ✅ Checklist Final

- [ ] Clone feito com sucesso
- [ ] Ambiente virtual criado
- [ ] Dependências instaladas
- [ ] Playwright instalado
- [ ] Base de dados configurada
- [ ] Utilizador admin criado
- [ ] Servidor iniciado
- [ ] Login funciona
- [ ] Páginas carregam
- [ ] Pesquisa de preços funciona

---

## 🆘 Suporte

Se tiver problemas:

1. **Verificar logs do servidor** no terminal
2. **Abrir Console do browser** (F12) para ver erros
3. **Verificar commits recentes** com `git log`
4. **Fazer pull** para garantir última versão

---

## 📊 Informações do Projeto

- **Repositório:** https://github.com/comercial-autoprudente/carrental_api
- **Última atualização:** Hoje (ver `git log`)
- **Total de commits:** 100+
- **Funcionalidades:**
  - ✅ Scraping CarJet em tempo real
  - ✅ 150+ suppliers mapeados
  - ✅ Clean names automático
  - ✅ Editor de veículos completo
  - ✅ Criar categorias e grupos
  - ✅ Export/Import configuração
  - ✅ Fotos de veículos
  - ✅ Cache de resultados

---

## 🎯 Próximos Passos

Depois de configurar:

1. **Testar funcionalidades** principais
2. **Fazer alterações** necessárias
3. **Commit e push** para GitHub
4. **Pull no trabalho** para sincronizar

**TUDO ESTÁ NO GITHUB - HISTÓRICO COMPLETO INCLUÍDO!** ✨
