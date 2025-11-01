# 📋 DEFINIÇÕES LOCALSTORAGE QUE PRECISAM SER SINCRONIZADAS

**Data:** 2025-11-01
**Status:** ⚠️ PENDENTE - Dados em localStorage (perdidos em deploy/sleep)

---

## 🔴 CRÍTICO - MOVER PARA DATABASE

### 1. **vansPricing** ⚠️ NOVO
```javascript
localStorage.getItem('vansPricing')
```
**Conteúdo:**
- c3_1day, c3_2days, c3_3days
- c4_1day, c4_2days, c4_3days
- c5_1day, c5_2days, c5_3days

**Ação:** Criar tabela `vans_pricing` na database

---

### 2. **automatedPriceRules** ⚠️ CRÍTICO
```javascript
localStorage.getItem('automatedPriceRules')
```
**Conteúdo:**
- Regras de pricing por localização
- Estratégias por grupo/mês/dia
- Configurações de margem, diferença, etc.

**Ação:** Criar tabela `automated_price_rules` na database

---

### 3. **priceAutomationSettings** ⚠️ CRÍTICO
```javascript
localStorage.getItem('priceAutomationSettings')
```
**Conteúdo:**
- excludeSuppliers (default: ['autoprudente'])
- maxAlternativeDays
- comissao (13.66%)
- rounding settings

**Ação:** Criar tabela `price_automation_settings` na database

---

### 4. **pricingStrategies** ⚠️ CRÍTICO
```javascript
localStorage.getItem('pricingStrategies')
```
**Conteúdo:**
- Estratégias configuradas por localização/grupo/dia

**Ação:** Mover para database (pode ser merged com automatedPriceRules)

---

### 5. **customDias** ⚠️ IMPORTANTE
```javascript
localStorage.getItem('customDias')
```
**Conteúdo:**
- Array de dias personalizados: [1, 2, 3, 4, 5, 6, 7, 8, 9, 14, 22, 28, 31, 60]

**Ação:** Criar tabela `custom_settings` ou adicionar a `app_settings`

---

### 6. **priceAIData** ⚠️ IMPORTANTE
```javascript
localStorage.getItem('priceAIData')
```
**Conteúdo:**
- adjustments: histórico de ajustes manuais
- patterns: padrões detectados
- suggestions: sugestões AI

**Ação:** Criar tabela `ai_learning_data` na database

---

### 7. **priceHistory_YYYYMM** ⚠️ IMPORTANTE
```javascript
localStorage.getItem('priceHistory_202411')
```
**Conteúdo:**
- Histórico de preços Current por mês
- Últimas 3 versões salvas

**Ação:** Criar tabela `price_history` na database

---

### 8. **automatedPriceHistory_YYYYMM** ⚠️ IMPORTANTE
```javascript
localStorage.getItem('automatedPriceHistory_202411')
```
**Conteúdo:**
- Histórico de preços Automated por mês
- Últimas 3 versões salvas

**Ação:** Adicionar à tabela `price_history` com campo `type`

---

### 9. **AI Settings** ⚠️ MENOR PRIORIDADE
```javascript
localStorage.getItem('aiLocation')
localStorage.getItem('aiReferenceSupplier')
localStorage.getItem('aiAnalysisPeriod')
```
**Conteúdo:**
- Configurações da interface AI

**Ação:** Adicionar a `app_settings` ou criar `user_preferences`

---

## ✅ JÁ NA DATABASE

### 1. **export_history** ✅
- Histórico de exports CSV (Way2Rentals, Abbycar)
- Últimos 12 meses
- Implementado recentemente

---

## 📊 PRIORIDADE DE IMPLEMENTAÇÃO

### **ALTA (Perda de dados crítica):**
1. ✅ vansPricing (C3, C4, C5 preços fixos)
2. ✅ automatedPriceRules (regras de pricing)
3. ✅ priceAutomationSettings (configurações gerais)

### **MÉDIA (Perda de configurações):**
4. ⚠️ customDias (dias personalizados)
5. ⚠️ pricingStrategies (estratégias)

### **BAIXA (Pode ser reconstruído):**
6. ⚠️ priceAIData (learning data)
7. ⚠️ priceHistory_* (histórico de versões)
8. ⚠️ AI Settings (preferências UI)

---

## 🚀 PRÓXIMOS PASSOS

1. **Criar tabelas na database:**
   - `vans_pricing`
   - `automated_price_rules`
   - `price_automation_settings`
   - `custom_days`
   - `ai_learning_data`
   - `price_history`

2. **Criar API endpoints:**
   - GET/POST `/api/vans-pricing`
   - GET/POST `/api/automated-rules`
   - GET/POST `/api/automation-settings`
   - GET/POST `/api/custom-days`
   - GET/POST `/api/ai-data`
   - GET/POST `/api/price-history`

3. **Migrar dados existentes:**
   - Script de migração localStorage → Database
   - Executar antes de deploy

4. **Atualizar frontend:**
   - Substituir localStorage por API calls
   - Manter fallback para compatibilidade

---

## ⚠️ AVISO

**RENDER FREE PLAN:**
- Disco efêmero (perde ao sleep/restart)
- localStorage perdido em cada deploy
- **URGENTE:** Mover para database antes de produção

**SOLUÇÃO TEMPORÁRIA:**
- Exportar configurações manualmente
- Backup regular do localStorage
- Documentar configurações importantes

**SOLUÇÃO PERMANENTE:**
- Implementar todas as tabelas acima
- Migrar 100% para database
- Remover dependência de localStorage
