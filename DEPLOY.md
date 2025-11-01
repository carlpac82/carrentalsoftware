# 🚀 Deploy no Render (RECOMENDADO)

Este guia mostra como fazer deploy da aplicação no Render, onde o Playwright **FUNCIONA** perfeitamente em Linux!

## ✅ Preparação (já está pronto!)

- ✅ `Dockerfile` configurado com Playwright
- ✅ `render.yaml` configurado
- ✅ `requirements.txt` atualizado
- ✅ `.env.example` documentado

---

## 📋 PASSO 1: Criar Repositório no GitHub

### 1.1. Ir para GitHub
```
https://github.com/new
```

### 1.2. Criar novo repositório:
- **Nome:** `RentalPriceTrackerPerDay` (ou outro nome)
- **Visibilidade:** Private (recomendado) ou Public
- **NÃO** marcar "Add README" (já temos ficheiros)
- Clicar **"Create repository"**

### 1.3. Copiar a URL do repositório:
Exemplo: `https://github.com/SEU_USERNAME/RentalPriceTrackerPerDay.git`

---

## 📋 PASSO 2: Push para GitHub

Abre o terminal na pasta do projeto e executa:

```bash
# 1. Configurar remote (substitui pela TUA URL do GitHub!)
git remote add origin https://github.com/SEU_USERNAME/RentalPriceTrackerPerDay.git

# 2. Verificar status
git status

# 3. Add todos os ficheiros modificados
git add .

# 4. Commit
git commit -m "Deploy ready: Playwright configured for Render"

# 5. Push para GitHub
git push -u origin main
```

**IMPORTANTE:** Substitui `SEU_USERNAME` pela tua conta do GitHub!

---

## 📋 PASSO 3: Deploy no Render

### 3.1. Criar conta no Render
```
https://render.com/
```
- Sign up com GitHub (grátis!)

### 3.2. Criar novo Web Service
1. No dashboard do Render, clicar **"New +"**
2. Escolher **"Web Service"**
3. Conectar com GitHub
4. Selecionar o repositório **RentalPriceTrackerPerDay**
5. Clicar **"Connect"**

### 3.3. Configurar o Web Service

**Configurações básicas:**
- **Name:** `rental-price-tracker` (ou outro nome)
- **Region:** Frankfurt (mais perto da Europa)
- **Branch:** `main`
- **Root Directory:** (deixar vazio)
- **Environment:** `Docker`
- **Plan:** `Free` ✅

### 3.4. Adicionar Variáveis de Ambiente

Clicar em **"Advanced"** e adicionar:

```env
APP_USERNAME=admin
APP_PASSWORD=SEU_PASSWORD_FORTE_AQUI
SECRET_KEY=GERA_UMA_CHAVE_SECRETA_ALEATÓRIA_AQUI
TEST_MODE_LOCAL=0
SCRAPER_API_KEY=80bba4c6-e162-4796-bada-5f6d1646051f
```

**IMPORTANTE:**
- ✅ `TEST_MODE_LOCAL=0` → Usa Playwright (scraping real)
- ✅ `APP_PASSWORD` → Escolhe uma password forte!
- ✅ `SECRET_KEY` → Gera uma chave aleatória (ex: `python -c "import secrets; print(secrets.token_hex(32))"`)

### 3.5. Deploy!
1. Clicar **"Create Web Service"**
2. Aguardar o build (5-10 minutos na primeira vez)
3. ✅ Quando ficar **"Live"**, está pronto!

---

## 🧪 TESTAR

### 1. Aceder à URL do Render
Exemplo: `https://rental-price-tracker.onrender.com`

### 2. Login
- Username: `admin`
- Password: (a que definiste no `.env`)

### 3. Fazer Pesquisa
- Selecionar **Aeroporto de Faro**
- Escolher data futura
- Selecionar **1 dia**, depois **3 dias**, depois **7 dias**
- Ver que **OS PREÇOS MUDAM!** ✅

---

## ✅ VANTAGENS NO RENDER

- ✅ **Playwright FUNCIONA** (Linux)
- ✅ **Preços reais** para cada número de dias
- ✅ **Scraping dinâmico** do CarJet
- ✅ **Grátis** (plano Free)
- ✅ **HTTPS** automático
- ✅ **Auto-deploy** quando fizer push

---

## 🔧 TROUBLESHOOTING

### Build falha?
- Verifica logs no Render dashboard
- Confirma que `Dockerfile` tem instalação do Playwright

### Login não funciona?
- Verifica variáveis de ambiente no Render
- `APP_USERNAME` e `APP_PASSWORD` corretos?

### Scraping falha?
- Verifica logs: pode ser timeout (aumentar timeout no código)
- Tenta adicionar `SCRAPER_API_KEY` se CarJet bloquear

---

## 📝 NOTAS

- **Free tier:** Render hiberna app após 15 min inativo (demora ~1 min a acordar)
- **Upgrade:** Se precisar de mais performance, upgrade para Starter ($7/mês)
- **Logs:** Acessa logs em tempo real no Render dashboard

---

## 🎉 PRONTO!

Agora tens scraping **REAL** com preços **DIFERENTES** para cada número de dias!

Qualquer problema, verifica os logs no Render dashboard.
