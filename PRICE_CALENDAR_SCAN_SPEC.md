# 📅 PRICE CALENDAR SCAN - ESPECIFICAÇÃO COMPLETA

## 🎯 OBJETIVO

Detectar QUANDO os preços mudam ao longo do tempo e identificar padrões de mudança de tarifas dos competitors para otimizar o calendário de pricing.

---

## 📊 FUNCIONALIDADE

### **1. Scan Diário de Preços**
- Buscar preços para TODOS os dias de múltiplos meses
- Não apenas 1,7,14,30 dias - mas TODOS os dias do calendário
- Exemplo: 1 Jan, 2 Jan, 3 Jan... 31 Jan

### **2. Detecção de Mudanças**
- Comparar preço de hoje vs ontem
- Identificar quando houve mudança
- Calcular magnitude da mudança
- Categorizar tipo de mudança (aumento/diminuição/%)

### **3. Identificação de Períodos**
```
Exemplo:
Jan 1-5:   25.00€ (período estável)
Jan 6-12:  28.00€ (↑ +12% alta temporada início)
Jan 13-20: 32.00€ (↑ +14% pico)
Jan 21-31: 26.00€ (↓ -19% fim período)
```

### **4. Comparação Competitiva**
- Ver QUANDO cada competitor muda preços
- Identificar padrões comuns
- Detectar líderes vs seguidores
- Calcular lag time (quanto tempo depois mudamos)

### **5. Padrões Temporais**
```
Descobertas:
- Europcar muda preços toda 2ª feira
- Hertz ajusta 1º dia do mês
- AutoPrudente está 3-5 dias atrás
- Média indústria: mudança a cada 7 dias
```

---

## 🔧 IMPLEMENTAÇÃO

### **Fase 1: Data Collection**
```javascript
// Buscar preços diários
for each month (last 12 months) {
  for each day in month {
    fetch prices for:
      - 7 days rental
      - Start date = this day
      - All suppliers
  }
}

Total: ~365 searches × 2 locations = ~730 API calls
```

### **Fase 2: Change Detection**
```javascript
prices_by_day = {
  '2024-01-01': { AutoPrudente: 25.00, Hertz: 27.00, ... },
  '2024-01-02': { AutoPrudente: 25.00, Hertz: 27.00, ... },
  '2024-01-03': { AutoPrudente: 26.00, Hertz: 28.00, ... }, // MUDANÇA!
}

// Detectar onde mudou
changes = detectChanges(prices_by_day)
```

### **Fase 3: Period Identification**
```javascript
// Agrupar dias consecutivos com mesmo preço
periods = groupByStablePrice(prices_by_day)

// Exemplo result:
[
  { start: '2024-01-01', end: '2024-01-05', price: 25.00, days: 5 },
  { start: '2024-01-06', end: '2024-01-12', price: 28.00, days: 7 },
  ...
]
```

### **Fase 4: Pattern Analysis**
```javascript
// Calcular frequência média de mudança
avg_change_frequency = calculateAverage(all_periods)

// Identificar gatilhos (que dia da semana/mês)
triggers = detectTriggers(changes)

// Comparar vs competitors
competitive_lag = compareTimings(changes_by_supplier)
```

### **Fase 5: AI Recommendations**
```python
# Backend AI analysis
patterns = analyze_price_calendar(data)

recommendations = {
  "optimal_change_days": ["Monday", "1st of month"],
  "suggested_periods": [...],
  "competitive_timing": "Move 2 days earlier",
  "average_cycle": "7 days"
}
```

---

## 📈 OUTPUT

### **Price Calendar Heatmap**
```
         Jan  Feb  Mar  Apr  May  Jun
AutoP   🟢🟢🟡🟡🔴🔴  ...
Hertz   🟢🟡🟡🔴🔴🔴  ...
Europcar 🟢🟢🟢🟡🔴🔴  ...

Legend:
🟢 Low price period
🟡 Medium price period  
🔴 High price period
```

### **Change Detection Timeline**
```
Jan 2024:
  Day 1  ➤ No change
  Day 5  ➤ AutoP +10% ⬆️ (Hertz já tinha mudado dia 3)
  Day 12 ➤ All +15% ⬆️ (Synchronized increase)
  Day 20 ➤ AutoP -8% ⬇️
```

### **Pattern Insights**
```
📊 Findings for AutoPrudente:

Frequency: Changes every 8.3 days on average
Timing: Usually 2-3 days AFTER competitors
Best Days: Mondays (32% of changes)
Seasonality: +25% Dec-Feb, -15% Mar-May

🎯 Recommendations:
1. Move changes to Fridays (get ahead of weekend demand)
2. Reduce lag to 1 day after competitors
3. Increase prices 5 days earlier in high season
4. Expected revenue impact: +8-12%
```

---

## 💾 DATA STRUCTURE

```javascript
priceCalendarData = {
  location: "Albufeira",
  period: { start: "2024-01-01", end: "2024-12-31" },
  suppliers: ["AutoPrudente", "Hertz", "Europcar", ...],
  
  daily_prices: {
    "2024-01-01": {
      "AutoPrudente": { B1: 25.00, D: 30.00, ... },
      "Hertz": { B1: 27.00, D: 32.00, ... },
      ...
    },
    ...
  },
  
  changes: [
    {
      date: "2024-01-05",
      supplier: "AutoPrudente",
      group: "B1",
      old_price: 25.00,
      new_price: 27.50,
      change_pct: 10.0,
      trigger: "weekend_demand"
    },
    ...
  ],
  
  periods: [
    {
      supplier: "AutoPrudente",
      group: "B1",
      start: "2024-01-01",
      end: "2024-01-04",
      price: 25.00,
      duration_days: 4,
      season: "low"
    },
    ...
  ],
  
  patterns: {
    avg_change_frequency: 8.3,
    most_common_day: "Monday",
    typical_increase: 12.5,
    typical_decrease: -8.2,
    competitive_lag: 2.7
  }
}
```

---

## 🚀 USER FLOW

```
1. User: Clicks "Calendar" button
2. Modal: "Analyze pricing calendar?"
   "This will scan daily prices for 12 months"
   "Estimated time: 10-15 minutes"
3. Progress: Shows date being scanned
   "Scanning: Jan 15, 2024..."
4. Analysis: AI processes data
5. Display: Visual calendar + insights
6. Actions: Apply recommended timing
```

---

## ⚡ OPTIMIZATIONS

1. **Caching**: Store daily prices in database
2. **Incremental**: Only scan new days since last scan
3. **Parallel**: Batch requests (10 at a time)
4. **Smart Sampling**: Focus on high-value periods
5. **Background**: Run overnight as scheduled task

---

## 🎯 SUCCESS METRICS

- Detect 95%+ of price changes
- Identify patterns within 5% accuracy
- Reduce competitive lag by 50%
- Increase revenue by 8-12%
- Save 10+ hours/month manual analysis
