# 🔧 RENDER ENVIRONMENT VARIABLES

## 📋 VARIÁVEIS OBRIGATÓRIAS

### **1. SECRET_KEY** (OBRIGATÓRIO)
```
SECRET_KEY=<gerar novo token seguro>
```
**Como gerar:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### **2. APP_PASSWORD** (OBRIGATÓRIO)
```
APP_PASSWORD=<tua password forte>
```
**Exemplo:** `MySecureP@ssw0rd2025`

---

## ⚙️ VARIÁVEIS DE CONFIGURAÇÃO

### **3. CARJET_PRICE_ADJUSTMENT_PCT**
```
CARJET_PRICE_ADJUSTMENT_PCT=3.12
```
Ajuste de preço do CarJet em percentagem.

### **4. CARJET_PRICE_OFFSET_EUR**
```
CARJET_PRICE_OFFSET_EUR=0
```
Offset de preço do CarJet em euros.

---

## 🔧 VARIÁVEIS OPCIONAIS (SCRAPING)

### **5. USE_PLAYWRIGHT**
```
USE_PLAYWRIGHT=1
```
Ativar Playwright para scraping (recomendado).

### **6. TEST_MODE_LOCAL**
```
TEST_MODE_LOCAL=0
```
**IMPORTANTE:** Manter em `0` para usar scraping real (não mock).

---

## 🌐 URLs DE TESTE (OPCIONAL)

Se quiseres usar URLs pré-geradas do CarJet (expiram em 24h):

### **FARO:**
```
FARO_1D=<url carjet para 1 dia>
FARO_2D=<url carjet para 2 dias>
FARO_3D=<url carjet para 3 dias>
FARO_4D=<url carjet para 4 dias>
FARO_5D=<url carjet para 5 dias>
FARO_6D=<url carjet para 6 dias>
FARO_7D=<url carjet para 7 dias>
FARO_8D=<url carjet para 8 dias>
FARO_9D=<url carjet para 9 dias>
FARO_14D=<url carjet para 14 dias>
FARO_22D=<url carjet para 22 dias>
FARO_28D=<url carjet para 28 dias>
FARO_31D=<url carjet para 31 dias>
FARO_60D=<url carjet para 60 dias>
```

### **ALBUFEIRA:**
```
ALBUFEIRA_1D=<url carjet para 1 dia>
ALBUFEIRA_2D=<url carjet para 2 dias>
ALBUFEIRA_3D=<url carjet para 3 dias>
ALBUFEIRA_4D=<url carjet para 4 dias>
ALBUFEIRA_5D=<url carjet para 5 dias>
ALBUFEIRA_6D=<url carjet para 6 dias>
ALBUFEIRA_7D=<url carjet para 7 dias>
ALBUFEIRA_8D=<url carjet para 8 dias>
ALBUFEIRA_9D=<url carjet para 9 dias>
ALBUFEIRA_14D=<url carjet para 14 dias>
ALBUFEIRA_22D=<url carjet para 22 dias>
ALBUFEIRA_28D=<url carjet para 28 dias>
ALBUFEIRA_31D=<url carjet para 31 dias>
ALBUFEIRA_60D=<url carjet para 60 dias>
```

**⚠️ NOTA:** Estas URLs expiram em ~24h. Se não configurares, o sistema usa Selenium automaticamente.

---

## 📧 EMAIL (OPCIONAL)

Para funcionalidade de reset de password por email:

```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=<teu email>
SMTP_PASSWORD=<app password do gmail>
SMTP_FROM=<email remetente>
```

---

## 🔐 SCRAPER API (OPCIONAL)

Se estiveres a usar ScraperAPI:

```
SCRAPER_SERVICE=scraperapi
SCRAPER_API_KEY=<tua api key>
SCRAPER_COUNTRY=pt
```

---

## 📊 OUTRAS CONFIGURAÇÕES (OPCIONAL)

```
AUDIT_RETENTION_DAYS=90
IMAGE_CACHE_DAYS=365
PRICES_CACHE_TTL_SECONDS=300
BULK_CONCURRENCY=6
```

---

## ✅ MÍNIMO PARA FUNCIONAR

Se quiseres configurar APENAS o essencial:

```env
SECRET_KEY=<gerar com: python3 -c "import secrets; print(secrets.token_urlsafe(32))">
APP_PASSWORD=<tua password>
CARJET_PRICE_ADJUSTMENT_PCT=3.12
CARJET_PRICE_OFFSET_EUR=0
USE_PLAYWRIGHT=1
TEST_MODE_LOCAL=0
```

**Estas 6 variáveis são suficientes para a aplicação funcionar!**

---

## 🚀 COMO CONFIGURAR NO RENDER

### **Método 1: Durante a criação do Service**

1. Criar novo Web Service
2. Conectar ao repo `carrental-Final`
3. Na secção **Environment Variables**, clicar "Add Environment Variable"
4. Adicionar cada variável (Key + Value)

### **Método 2: Depois de criar o Service**

1. Render Dashboard → Service `carrental-final`
2. **Settings** → **Environment**
3. Clicar **"Add Environment Variable"**
4. Adicionar Key + Value
5. **Save Changes**

**⚠️ IMPORTANTE:** Depois de adicionar/modificar variáveis, fazer **Manual Deploy**.

---

## 📋 TEMPLATE COPY-PASTE

```env
# === OBRIGATÓRIAS ===
SECRET_KEY=GERAR_TOKEN_AQUI
APP_PASSWORD=TUA_PASSWORD_AQUI

# === CONFIGURAÇÃO ===
CARJET_PRICE_ADJUSTMENT_PCT=3.12
CARJET_PRICE_OFFSET_EUR=0

# === SCRAPING ===
USE_PLAYWRIGHT=1
TEST_MODE_LOCAL=0

# === OPCIONAL - CACHE ===
AUDIT_RETENTION_DAYS=90
IMAGE_CACHE_DAYS=365
PRICES_CACHE_TTL_SECONDS=300
BULK_CONCURRENCY=6
```

---

## 🔐 GERAR SECRET_KEY

**Local (Mac/Linux):**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Online:**
https://generate-secret.now.sh/32

**Exemplo de output:**
```
Xk7pQ9mR2nL5wT8vY3zA1bN6cH4dJ0eK
```

---

## ⚠️ SEGURANÇA

- ✅ **SECRET_KEY** deve ser único por deployment
- ✅ **APP_PASSWORD** deve ser forte (min 12 caracteres)
- ❌ **NÃO** partilhar estas variáveis publicamente
- ❌ **NÃO** fazer commit no GitHub
- ✅ Usar "Secret" option no Render para passwords

---

## 🔄 COPIAR DO SERVICE ANTIGO

Se já tens um service no Render:

1. Service antigo → **Settings** → **Environment**
2. Copiar todas as variáveis
3. Service novo → **Settings** → **Environment**
4. Colar uma por uma

**Atenção:** O `SECRET_KEY` pode ser diferente, mas o resto pode ser igual.

---

## ✅ VERIFICAR CONFIGURAÇÃO

Depois de configurar, verificar nos logs se não há erros:

```
# Deve aparecer:
🔥 LOADING main.py - VERSION: 2025-01-29-00:02-FORCE
📦 FEATURES: Vehicles + Car Groups + 60+ Cars
========================================
🚀 APP STARTUP - VERSION: 2025-01-29-00:02-FORCE
📦 Features: Vehicles Management, Automatic Field, Blocklist Removed
========================================
INFO: Uvicorn running on http://0.0.0.0:10000

# NÃO deve aparecer:
ERROR: Environment variable not set
KeyError: 'SECRET_KEY'
```

---

**🎯 Configura as variáveis e faz Manual Deploy depois!**
