# 🔗 GERAR URLs DO CARJET MANUALMENTE

## ❌ PROBLEMA
Selenium não consegue gerar URLs válidas do CarJet:
- `war=0` → Erro genérico
- `war=11` → Parâmetros inválidos
- Resultado: 0 carros retornados

## ✅ SOLUÇÃO RÁPIDA
Gerar URLs manualmente no browser e configurar no Render.

---

## 📋 PASSO A PASSO

### **1️⃣ Abrir CarJet:**
```
https://www.carjet.com/pt
```

### **2️⃣ Preencher Formulário:**

**Para FARO (7 dias):**
- Local recolha: `Faro Aeroporto (FAO)`
- Data recolha: **HOJE + 2 dias** (ex: se hoje é 29 Jan, usar 31 Jan)
- Hora recolha: `15:00`
- Data entrega: **recolha + 7 dias**
- Hora entrega: `10:00`

**Para ALBUFEIRA (7 dias):**
- Local recolha: `Albufeira Cidade`
- Data recolha: **HOJE + 2 dias**
- Hora recolha: `15:00`
- Data entrega: **recolha + 7 dias**
- Hora entrega: `10:00`

### **3️⃣ Clicar "Pesquisar"**

### **4️⃣ Aguardar Resultados**

Deve carregar página com carros. Vai ver URL tipo:
```
https://www.carjet.com/do/list/pt?s=XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX&b=YYYYYYYY-YYYY-YYYY-YYYY-YYYYYYYYYYYY
```

### **5️⃣ Copiar URL Completa**

Copiar a URL da barra de endereços (toda!)

### **6️⃣ Configurar no Render**

**Dashboard → carrental-final → Environment:**

**Para Faro 7 dias:**
```
Key: TEST_FARO_URL
Value: https://www.carjet.com/do/list/pt?s=...&b=...
```

**Para Albufeira 7 dias:**
```
Key: TEST_ALBUFEIRA_URL  
Value: https://www.carjet.com/do/list/pt?s=...&b=...
```

### **7️⃣ Save Changes**

Render vai fazer redeploy (3-5 min)

### **8️⃣ Testar no App**

Pesquisar:
- Faro, 7 dias → Usa TEST_FARO_URL
- Albufeira, 7 dias → Usa TEST_ALBUFEIRA_URL

**Deve retornar 60+ carros!** ✅

---

## ⏰ IMPORTANTE - VALIDADE

**URLs do CarJet expiram em ~24h!**

Tens que:
1. Gerar novas URLs cada dia
2. Atualizar ENV vars no Render
3. Ou usar para testes rápidos apenas

---

## 🎯 SOLUÇÃO PERMANENTE (TODO)

Para resolver permanentemente, preciso de:
1. Corrigir código Selenium (horários/datas)
2. Ou ativar Playwright com retry
3. Ou usar API paga (ScraperAPI já configurado)

**Mas para AGORA, URLs manuais funcionam!**

---

## 💡 DICA RÁPIDA

Se quiseres testar **SEM gerar URLs**:

**Opção A - Desativar scraping temporariamente:**
Comentar código Selenium e retornar lista vazia (app funciona, só não mostra preços)

**Opção B - Mock data:**
Retornar dados fake para testar UI

**Opção C - Aguardar correção Selenium:**
Posso debuggar e corrigir o código Selenium (mais demorado)

---

## ❓ PERGUNTAS

**P: Porque Selenium falha?**
R: CarJet detecta automação ou rejeita datas/horários inválidos

**P: Playwright resolve?**
R: Pode ajudar mas também pode ser detectado

**P: ScraperAPI resolve?**
R: Sim! Mas é pago (~$50/mês para 100k requests)

**P: Qual a melhor solução?**
R: 
- **Curto prazo:** URLs manuais (funciona já!)
- **Médio prazo:** Corrigir Selenium
- **Longo prazo:** ScraperAPI ou Bright Data

---

## ✅ AÇÃO IMEDIATA

**Opção 1 - Gerar URLs agora (5 min):**
1. Abrir CarJet
2. Pesquisar Faro 7 dias
3. Copiar URL
4. Pesquisar Albufeira 7 dias
5. Copiar URL
6. Adicionar no Render (TEST_FARO_URL, TEST_ALBUFEIRA_URL)
7. Testar!

**Opção 2 - Corrigir Selenium (eu faço):**
1. Debuggar código
2. Corrigir horários/datas
3. Adicionar retry logic
4. Testar
5. Deploy

**Qual preferes?** 🚀
