# 🔍 TESTE DE SCRAPING REAL

## ✅ CONFIGURAÇÃO ATUAL:

```env
TEST_MODE_LOCAL=0  ← SCRAPING REAL ATIVADO!
USE_PLAYWRIGHT=1
```

---

## 🚀 COMO TESTAR LOCALHOST:

### **1. Abrir Browser:**
http://localhost:8000

### **2. Fazer Login:**
- **Username:** `admin`
- **Password:** `admin`

### **3. Fazer Pesquisa:**
- **Localização:** Aeroporto de Faro
- **Data:** Qualquer data futura (ex: 30 dias à frente)
- **Dias:** 5d (clicar no chip)
- **Clicar:** "Pesquisar"

### **4. Aguardar:**
- ⏳ **30-90 segundos** (Playwright está a trabalhar!)
- Ver loading modal com carro animado

### **5. LOGS ESPERADOS:**

Ver logs em `/tmp/uvicorn_scraping.log`:
```bash
tail -f /tmp/uvicorn_scraping.log
```

**Logs de SUCESSO:**
```
[API] REQUEST: location=Aeroporto de Faro, start_date=2025-XX-XX, days=5
[SCRAPERAPI] Iniciando scraping para Aeroporto de Faro
[SCRAPERAPI] ❌ HTTP 404                          ← Normal! ScraperAPI falha
[SCRAPERAPI] Tentando fallback para Playwright...
[PLAYWRIGHT] Iniciando scraping direto para Aeroporto de Faro
[PLAYWRIGHT] Acessando CarJet homepage PT...
[PLAYWRIGHT] Preenchendo formulário via JS: Faro Aeroporto (FAO)
[PLAYWRIGHT] Submetendo formulário...
[PLAYWRIGHT] Aguardando navegação...
[PLAYWRIGHT] Aguardando carros carregarem...
[PLAYWRIGHT] URL final: https://www.carjet.com/do/list/pt?s=XXXX&b=YYYY
[PLAYWRIGHT] ✅ HTML capturado: 500000+ bytes
[PLAYWRIGHT] Parsed 200+ items antes conversão
[PLAYWRIGHT] 200+ items após GBP→EUR
[PLAYWRIGHT] ✅ 200+ carros encontrados!
[PLAYWRIGHT] Primeiro: Fiat 500 - €XX,XX
[API] ✅ RESPONSE: 200+ items for 5 days
```

**Se der erro:**
```
[PLAYWRIGHT ERROR] Page.wait_for_url: Timeout 90000ms exceeded
```
→ CarJet está lento ou mudou. Ver TROUBLESHOOTING abaixo.

---

## 📊 RESULTADO ESPERADO:

### **✅ SUCESSO:**
- ~200 carros aparecem
- Agrupados por categoria (B1, B2, D, E1, E2, F, G, J1, J2, L1, L2, M1, M2, N)
- **PREÇOS REAIS** do CarJet
- **Preços DIFERENTES** para 1d, 3d, 7d, etc.

### **❌ FALHA:**
- "Nenhum resultado encontrado"
- Ver logs para debug

---

## 🐛 TROUBLESHOOTING:

### **1. Timeout após 90 segundos:**
```python
# Em main.py linha 2048, aumentar timeout:
await page.wait_for_url('**/do/list/**', timeout=120000)  # 2 minutos
```

### **2. Formulário não submete:**
Ver logs para identificar qual campo falhou:
```
[PLAYWRIGHT] Preenchendo formulário via JS: ...
```

Pode ser que o CarJet mudou os nomes dos campos.

### **3. Parse retorna 0 items:**
```
[PLAYWRIGHT] Parsed 0 items antes conversão
```

Significa que o HTML mudou. Precisa atualizar `parse_prices()` em `main.py`.

### **4. ScraperAPI sempre HTTP 404:**
Normal! ScraperAPI tem problemas. Por isso há fallback para Playwright.

---

## 🔧 MELHORIAS FUTURAS:

### **Se Playwright falhar consistentemente:**

**Opção 1:** Usar ScraperAPI diferente (mais confiável)
```env
SCRAPER_API_KEY=nova_key_aqui
```

**Opção 2:** Aumentar timeouts
```python
# main.py
timeout=120000  # 2 minutos
await page.wait_for_timeout(10000)  # 10 seg
```

**Opção 3:** Screenshot para debug
```python
await page.screenshot(path="debug_carjet.png")
```

---

## 📝 TESTAR DIFERENTES CENÁRIOS:

### **Teste 1: Faro, 5 dias**
- ✅ Deve funcionar
- ✅ ~200 carros

### **Teste 2: Albufeira, 7 dias**
- ✅ Deve funcionar
- ✅ Preços DIFERENTES de Faro

### **Teste 3: Fetch All**
- ⏳ **MUITO LENTO!** (10-15 minutos)
- Faz scraping para 1d, 2d, 3d, 4d, 5d, 6d, 7d, 8d, 9d, 14d, 22d, 31d, 60d
- Cada um demora ~60-90 seg
- **NÃO RECOMENDADO** para teste inicial

---

## ⚡ COMPARAÇÃO DE PERFORMANCE:

| Modo | Velocidade | Confiabilidade | Preços Reais |
|------|------------|----------------|--------------|
| MODE=2 (Mock) | ⚡ <1 seg | ✅ 100% | ❌ Não |
| MODE=0 (Playwright) | 🐢 60-90 seg | ⚠️ 70-80% | ✅ Sim |
| MODE=1 (URLs fixas) | ⚡ 2-3 seg | ❌ 0% (expiram) | ✅ Sim (quando funcionam) |

---

## 🎯 RECOMENDAÇÃO:

### **DESENVOLVIMENTO:**
```env
TEST_MODE_LOCAL=2  # Mock - rápido e confiável
```

### **PRODUÇÃO (Render):**
```env
TEST_MODE_LOCAL=0  # Scraping real - lento mas preços reais
```

### **DEMOS:**
```env
TEST_MODE_LOCAL=2  # Mock - instantâneo, sempre funciona
```

---

## 📋 CHECKLIST DE TESTE:

- [ ] Servidor iniciado (`uvicorn main:app --reload --port 8000`)
- [ ] `.env` tem `TEST_MODE_LOCAL=0`
- [ ] Login funciona (admin/admin)
- [ ] Escolher: Faro + data futura + 5d
- [ ] Clicar "Pesquisar"
- [ ] Aguardar 60-90 segundos
- [ ] Ver logs em `/tmp/uvicorn_scraping.log`
- [ ] Verificar "[PLAYWRIGHT] ✅ X carros encontrados!"
- [ ] Ver ~200 carros no frontend
- [ ] Verificar preços em EUR (€)
- [ ] Testar 1d, 3d, 7d → Preços DIFERENTES

---

## ✅ STATUS:

**LOCALHOST:** Servidor ativo em http://localhost:8000  
**CONFIGURAÇÃO:** Scraping REAL ativado (MODE=0)  
**PRÓXIMO PASSO:** Fazer pesquisa e aguardar 60-90 seg!  

**BOA SORTE! 🍀**
