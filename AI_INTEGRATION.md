# 🤖 AI Integration Guide

## Overview

AutoPrudente agora integra com AI externa (Claude Sonnet 3.5 ou GPT-4) para fornecer análises e sugestões inteligentes de pricing baseadas em contexto de mercado completo.

---

## 🌟 Features

### **Análise Inteligente de Mercado**
- Avalia posicionamento competitivo atual
- Considera tipo de booking (weekend, semanal, long-term)
- Analisa psicologia do cliente por duração
- Identifica oportunidades e riscos
- Recomenda preço ótimo com confiança (%)

### **Context-Aware Recommendations**
- **Short-term (1-3d):** Mercado competitivo, último minuto
- **Week rental (4-7d):** Bookings padrão, abordagem equilibrada
- **Extended (8-14d):** Viagens de férias, value positioning
- **Long-term (15+d):** Reservas antecipadas, confiabilidade > preço

---

## 📦 Installation

### **1. Install Required Libraries**

```bash
# Choose ONE:

# Option A: Claude (Recommended)
pip install anthropic

# Option B: OpenAI
pip install openai

# Or install both for flexibility
pip install anthropic openai
```

### **2. Get API Key**

#### **Claude (Recommended)**
1. Go to https://console.anthropic.com/
2. Sign up / Log in
3. Navigate to API Keys
4. Create new key
5. Copy the key (starts with `sk-ant-`)

#### **OpenAI (Alternative)**
1. Go to https://platform.openai.com/
2. Sign up / Log in
3. Navigate to API Keys
4. Create new secret key
5. Copy the key (starts with `sk-`)

### **3. Configure Environment**

Add to your `.env` file:

```bash
# For Claude (Recommended)
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here

# OR for OpenAI
OPENAI_API_KEY=sk-your-openai-key-here
```

---

## 🚀 Usage

### **API Endpoint: External AI Analysis**

```http
POST /api/ai/external-analysis
Content-Type: application/json

{
  "group": "B1",
  "days": 7,
  "location": "Albufeira",
  "current_price": 28.50,
  "competitors": [
    {
      "supplier": "Hertz",
      "price": 25.00,
      "car": "Fiat 500"
    },
    {
      "supplier": "Europcar",
      "price": 30.00,
      "car": "Renault Clio"
    }
  ],
  "provider": "claude"  // or "openai"
}
```

### **Response Example**

```json
{
  "ok": true,
  "analysis": {
    "analysis": "Current pricing is slightly above market average...",
    "current_position": "optimal",
    "recommended_price": 27.50,
    "price_change": -1.00,
    "price_change_percentage": -3.5,
    "confidence": 85,
    "strategy": "DECREASE_SLIGHTLY",
    "reasoning": "For 7-day rentals, positioning at 45th percentile...",
    "risk_factors": [
      "High competition in mid-range segment",
      "Weekend overlap may increase demand"
    ],
    "opportunities": [
      "Slightly below average captures price-sensitive customers",
      "Good value proposition for week rentals"
    ],
    "target_percentile": 45,
    "ai_provider": "claude-sonnet-3.5"
  },
  "provider": "claude",
  "status": {
    "provider": "claude",
    "available": true,
    "client_initialized": true
  }
}
```

### **Check AI Status**

```http
GET /api/ai/status
```

Response:
```json
{
  "ok": true,
  "claude": {
    "provider": "claude",
    "available": true,
    "has_anthropic": true,
    "client_initialized": true
  },
  "openai": {
    "provider": "openai",
    "available": false,
    "has_openai": true,
    "client_initialized": false
  },
  "recommended": "claude",
  "env_keys": {
    "anthropic": true,
    "openai": false
  }
}
```

---

## 💡 Integration in Smart AI

O Smart AI button já está preparado para usar AI externa quando disponível. O sistema funciona em modo híbrido:

1. **AI Externa Disponível:** Usa Claude/GPT para análise profunda
2. **Fallback:** Usa lógica local baseada em percentis

### **Como Funciona:**

```javascript
// Frontend chama o backend
const response = await fetch('/api/ai/external-analysis', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    group: 'B1',
    days: 7,
    location: 'Albufeira',
    current_price: 28.50,
    competitors: competitorData,
    provider: 'claude'
  })
});

const result = await response.json();

if (result.ok) {
  // Mostrar sugestão AI
  displayAISuggestion(result.analysis);
}
```

---

## 🔍 What AI Analyzes

### **Market Data Sent to AI:**
- Vehicle group and category
- Rental duration (booking type classification)
- Location and market
- Current AutoPrudente price
- All competitor prices (up to 10 shown in detail)
- Market statistics (lowest, average, median, highest, range)
- Current market position and percentile

### **AI Provides:**
1. **Analysis:** Overall market assessment
2. **Position Evaluation:** too_cheap | optimal | too_expensive
3. **Recommended Price:** Specific € amount
4. **Confidence Score:** 0-100%
5. **Strategy:** INCREASE_TO_VALUE, DECREASE_TO_COMPETITIVE, MAINTAIN, etc.
6. **Detailed Reasoning:** Why this recommendation
7. **Risk Factors:** What could go wrong
8. **Opportunities:** What you gain
9. **Target Percentile:** Where to position in market

---

## 💰 Costs

### **Claude (Anthropic)**
- Model: Claude Sonnet 3.5 (claude-3-5-sonnet-20241022)
- Input: ~$3.00 per million tokens
- Output: ~$15.00 per million tokens
- **Typical request:** ~$0.001-0.003 per analysis
- **1000 analyses:** ~$1-3

### **OpenAI**
- Model: GPT-4 Turbo
- Similar pricing structure
- **Typical request:** ~$0.002-0.005 per analysis

### **Recommendations:**
- Use for important decisions only
- Cache results for same group/days/location
- Consider batching multiple analyses
- Start with Claude (better reasoning for business)

---

## 🔧 Troubleshooting

### **"AI provider not available"**
✅ Check `.env` file has correct API key
✅ Restart application after adding key
✅ Verify library installed: `pip list | grep anthropic`

### **"Module not found: anthropic"**
```bash
pip install anthropic
```

### **"Invalid API key"**
✅ Key format: `sk-ant-api03-...` (Claude) or `sk-...` (OpenAI)
✅ Check for extra spaces/quotes in .env
✅ Verify key is active at provider console

### **"Rate limit exceeded"**
✅ Slow down requests
✅ Implement caching
✅ Consider upgrading API tier

---

## 🎯 Best Practices

1. **Cache Results:**
   - Same group/days/location = same analysis for 1 hour
   - Avoid redundant API calls

2. **Fallback Strategy:**
   - System works without AI (local logic)
   - AI enhances but isn't required

3. **Monitor Costs:**
   - Log each API call
   - Set monthly budget alerts
   - Review usage regularly

4. **Security:**
   - Never commit .env with real keys
   - Use environment variables in production
   - Rotate keys periodically

5. **Testing:**
   - Use local fallback first
   - Test with small dataset
   - Verify responses make business sense

---

## 📚 Further Reading

- [Anthropic Claude Docs](https://docs.anthropic.com/)
- [OpenAI API Docs](https://platform.openai.com/docs/)
- [Demand Pricing Theory](https://en.wikipedia.org/wiki/Dynamic_pricing)
- [Car Rental Pricing Strategies](https://www.researchgate.net/publication/car_rental_pricing)

---

## 🆘 Support

For issues or questions:
1. Check this guide first
2. Review API logs in console
3. Test `/api/ai/status` endpoint
4. Verify `.env` configuration
5. Check provider console for errors

---

**Last Updated:** 2024-11-01
**Version:** 1.0.0
