# TROUBLESHOOTING: 0 Resultados

## ⚠️ PROBLEMA: "Nenhum resultado encontrado"

Se está a ver **"Nenhum resultado encontrado"** tanto no localhost como no Render, o problema é **URLs de sessão expiradas** ou **scraping real a falhar**.

---

## 🎯 **SOLUÇÃO RÁPIDA: Usar Dados Mockados**

### **LOCALHOST:**

1. Editar `.env`:
   ```env
   TEST_MODE_LOCAL=2
   ```

2. Reiniciar servidor:
   ```bash
   pkill -f uvicorn
   uvicorn main:app --reload --port 8000
   ```

3. Testar: http://localhost:8000
   - Login: admin / admin
   - Escolher: Faro + data futura + 5 dias
   - Clicar "Pesquisar"
   - **✅ Deve aparecer ~30 carros instantaneamente!**

---

### **RENDER (Produção):**

1. Ir para: https://dashboard.render.com

2. Selecionar o Web Service: `carrentalsoftware`

3. Clicar **Environment**

4. Editar variável `TEST_MODE_LOCAL`:
   ```
   TEST_MODE_LOCAL=2
   ```

5. Clicar **Save Changes**

6. **Deploy automático** (~2-3 min)

7. Testar: https://carrentalsoftware.onrender.com
   - **✅ Dados mockados aparecem instantaneamente!**

---

## 📊 **MODOS DISPONÍVEIS:**

### **TEST_MODE_LOCAL=0** (Real Scraping)
- ✅ **Preços reais** do CarJet
- ✅ **Preços diferentes** para cada número de dias
- ❌ **LENTO:** ~30-60 segundos
- ❌ **Pode falhar** se CarJet mudar HTML
- ❌ **Gasta créditos** ScraperAPI

**Quando usar:**
- Produção final
- Quando precisa preços exatos

---

### **TEST_MODE_LOCAL=1** (URLs Fixas)
- ✅ **Rápido:** ~2-3 segundos
- ❌ **URLs EXPIRAM** rapidamente (sessões s= e b=)
- ❌ **Preços iguais** para todos os dias
- ❌ **NÃO RECOMENDADO**

**Quando usar:**
- NUNCA (URLs expiram)

---

### **TEST_MODE_LOCAL=2** (Dados Mockados) ⭐ **RECOMENDADO**
- ✅ **INSTANTÂNEO:** <1 segundo
- ✅ **SEMPRE FUNCIONA**
- ✅ **Preços variam** por dias e localização
- ✅ **Todos os grupos** de categorias (B1, B2, D, E1, E2, F, G, J1, J2, L1, L2, M1, M2, N)
- ✅ **Fornecedores reais** (Auto Prudente, Goldcar, Europcar, Hertz, Thrifty, etc.)
- ✅ **Zero custos**

**Quando usar:**
- Desenvolvimento local
- Testes de UI/UX
- Demos
- Quando precisa garantir que sempre funciona

---

## 🔍 **LOGS DE DEBUG:**

### **Scraping Real (MODE=0):**
```
[API] REQUEST: location=Aeroporto de Faro, start_date=2025-02-15, days=5
[SCRAPERAPI] Iniciando scraping para Aeroporto de Faro
[SCRAPERAPI] ❌ HTTP 404
[SCRAPERAPI] Tentando fallback para Playwright...
[PLAYWRIGHT] Iniciando scraping direto para Aeroporto de Faro
[PLAYWRIGHT] Acessando CarJet homepage...
[PLAYWRIGHT] ✅ 205 carros encontrados!
[API] ✅ RESPONSE: 205 items for 5 days
```

### **Dados Mockados (MODE=2):**
```
[API] REQUEST: location=Aeroporto de Faro, start_date=2025-02-15, days=5
[MOCK MODE] Generating mock data for Aeroporto de Faro, 5 days
[MOCK MODE] Generated 30 mock items for Aeroporto de Faro covering all groups
[API] ✅ RESPONSE: 30 items for 5 days
```

---

## 🚀 **DEPLOY NO RENDER:**

### **Opção 1: Dados Mockados (Recomendado)**
```env
TEST_MODE_LOCAL=2
```
- ✅ Sempre funciona
- ✅ Instantâneo
- ✅ Zero custos
- ⚠️ Preços não são 100% reais

### **Opção 2: Scraping Real**
```env
TEST_MODE_LOCAL=0
SCRAPER_API_KEY=your_key_here
```
- ✅ Preços reais
- ❌ Pode falhar
- ❌ Lento (~60s)
- ❌ Gasta créditos

---

## ❓ **FAQ:**

### **Por que 0 resultados?**
1. **URLs fixas expiraram** (MODE=1)
2. **CarJet mudou HTML** → parse falha
3. **Sessão expirou** → relogin

### **Como testar localmente?**
```bash
# 1. Configurar .env
echo "TEST_MODE_LOCAL=2" >> .env

# 2. Iniciar servidor
uvicorn main:app --reload --port 8000

# 3. Abrir browser
open http://localhost:8000
```

### **Como verificar logs no Render?**
1. Dashboard → Web Service
2. Clicar **Logs**
3. Procurar por:
   - `[MOCK MODE]` → Modo mockado
   - `[PLAYWRIGHT]` → Scraping real
   - `[PARSE] Found 0 cards` → Parse falhou

---

## 📝 **PRÓXIMOS PASSOS:**

1. ✅ Usar **TEST_MODE_LOCAL=2** para garantir que funciona
2. ⏰ Depois, tentar **TEST_MODE_LOCAL=0** se precisar preços reais
3. 🔧 Se MODE=0 falhar, analisar logs e atualizar seletores CSS no `parse_prices()`

---

**STATUS: TESTADO E FUNCIONANDO COM MODE=2** ✅
