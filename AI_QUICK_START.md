# 🚀 AI Quick Start (5 minutes)

## ⚡ Fastest Setup - Claude

```bash
# 1. Install library
pip install anthropic

# 2. Get API key (free tier available)
# Visit: https://console.anthropic.com/
# Copy your key (starts with sk-ant-...)

# 3. Add to .env file
echo "ANTHROPIC_API_KEY=sk-ant-api03-YOUR-KEY-HERE" >> .env

# 4. Restart app
# Kill server (Ctrl+C) and restart

# 5. Test it!
# Go to: http://localhost:8000/admin/price-automation
# Click AI icon → Click "Smart" button
# AI will now provide intelligent analysis! 🧠
```

## ✅ Verify It's Working

```bash
# Check status endpoint
curl http://localhost:8000/api/ai/status

# Should return:
# {
#   "ok": true,
#   "claude": {
#     "provider": "claude",
#     "available": true
#   },
#   "recommended": "claude"
# }
```

## 🎯 What You Get

**BEFORE (Local Logic):**
- Simple percentile calculation
- Basic positioning

**NOW (Claude AI):**
- Context-aware analysis
- Booking type consideration (weekend vs long-term)
- Customer psychology insights
- Risk & opportunity identification
- Confidence scoring
- Detailed reasoning
- Smart recommendations

## 💡 Example Analysis

**Input:**
- Group B1, 7 days, Albufeira
- Current: 28.50€
- Market: 25-35€ range

**Claude Output:**
```
Analysis: "Week-long rental in competitive segment. 
Currently positioned at 55th percentile. For 7-day 
bookings, customers prioritize value over lowest price..."

Recommended: 27.50€ (-1.00€)
Confidence: 85%
Strategy: DECREASE_SLIGHTLY

Reasoning: "Positioning at 45th percentile captures 
price-sensitive customers while maintaining margin..."

Risks: ["High competition", "Weekend overlap"]
Opportunities: ["Good value proposition", "Week rental sweet spot"]
```

## 🆓 Free Tier

**Claude (Anthropic):**
- $5 free credit on signup
- ~1,500-5,000 analyses free
- No credit card required initially

## 📊 Cost Calculator

| Analyses | Cost (Approx) |
|----------|---------------|
| 100      | $0.10 - $0.30 |
| 1,000    | $1.00 - $3.00 |
| 10,000   | $10 - $30     |

💡 **Tip:** Cache results for same group/days/location to reduce costs!

## ❓ Troubleshooting

**"AI not available"**
→ Check .env has `ANTHROPIC_API_KEY=...`
→ Restart server

**"Module not found"**
→ Run: `pip install anthropic`

**"Invalid API key"**
→ Verify format: `sk-ant-api03-...`
→ Check no extra spaces in .env

## 🔄 Fallback

Sistema funciona SEMPRE, mesmo sem AI:
- ✅ Com AI: Análise profunda inteligente
- ✅ Sem AI: Lógica local de percentis

**You can't break it!** 💪

---

**Full docs:** See `AI_INTEGRATION.md`
