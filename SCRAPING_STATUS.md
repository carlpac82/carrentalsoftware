# ⚠️ Status Atual do Scraping - Preços Reais

**Última atualização**: 28 de Outubro de 2025

## 🎯 Configuração Atual

A aplicação está configurada para usar **APENAS PREÇOS REAIS** via scraping do CarJet.

```bash
TEST_MODE_LOCAL=0  # Scraping real ao vivo
```

**Modo mock removido** - apenas dados reais do CarJet.

---

## ⚠️ Problemas Conhecidos

### Status dos Métodos de Scraping

| Método | Status | Resultado Atual | Tempo |
|--------|--------|-----------------|-------|
| **ScraperAPI** | ❌ FALHA | HTTP 404 | ~5s |
| **Selenium** | ❌ BLOQUEADO | Redireciona para erro (war=11) | ~15s |
| **Playwright** | ❌ BLOQUEADO | Anti-bot detecta automação | ~20s |

### Resultados dos Testes

**Faro**: 0 carros (scraping bloqueado)
**Albufeira**: 0 carros (scraping bloqueado)

---

## 🔍 Detalhes dos Problemas

### 1. ScraperAPI/ScraperOps - HTTP 404

```
[SCRAPERAPI] Fazendo request via ScraperOps...
[SCRAPERAPI] ❌ HTTP 404
```

**Causas possíveis**:
- API key pode estar inválida/expirada
- Serviço ScraperOps pode estar com problemas
- URL do CarJet mudou

**Solução**: Verificar/renovar API key em https://scrapeops.io/

---

### 2. Selenium - Bloqueado pelo CarJet

```
[SELENIUM] Submetendo formulário...
[SELENIUM] URL final: https://www.carjet.com/aluguel-carros/index.htm?war=11
[SELENIUM] ⚠️ URL s/b NÃO obtida!
```

**Problema**: O CarJet detecta o Selenium e redireciona para página de erro com parâmetro `war=11`.

**Causas**:
- Anti-bot detection (detecta `navigator.webdriver`)
- Falta de user-agent realista
- Comportamento não-humano (velocidade, padrões)

---

### 3. Playwright - Anti-bot

**Problema**: Mesmo com Playwright, o website detecta automação.

**Causas**:
- Fingerprinting do browser
- Headers incompletos
- Falta de cookies/session
- Tempo de carregamento muito rápido

---

## 🔧 Soluções Possíveis

### Curto Prazo (1-2 dias)

#### 1. Atualizar ScraperOps API Key
```bash
# Em .env
SCRAPER_API_KEY=nova_key_aqui

# Testar: https://scrapeops.io/
```

#### 2. Usar URLs Pré-Geradas (Temporário)
```bash
TEST_MODE_LOCAL=1
TEST_FARO_URL=https://www.carjet.com/do/list/pt?s=...&b=...
TEST_ALBUFEIRA_URL=https://www.carjet.com/do/list/pt?s=...&b=...
```

**Limitação**: URLs expiram em ~24h

---

### Médio Prazo (1 semana)

#### 1. Implementar Playwright Stealth Mode

```python
from playwright_stealth import stealth_sync

# Aplicar patches anti-detection
stealth_sync(page)
```

**Pacotes necessários**:
- `playwright-stealth`
- User-agent rotation
- Cookie persistence

#### 2. Usar Proxies Residenciais

Serviços recomendados:
- **Bright Data** (formerly Luminati)
- **SmartProxy**
- **Oxylabs**

**Custos**: $75-300/mês

#### 3. ScrapingBee/Apify

Alternativas ao ScraperOps com melhor anti-bot:
- **ScrapingBee**: $49/mês (100k requests)
- **Apify**: Pay-as-you-go

---

### Longo Prazo (1 mês)

#### 1. Browser Automation Service

Usar serviço especializado:
- **Browserless.io**: $25-100/mês
- **Selenium Grid** em cloud
- **Puppeteer Cluster** self-hosted

#### 2. API Oficial (Se Existir)

Contactar CarJet para acesso API oficial:
- Pode ter custos
- Mais confiável
- Sem anti-bot

#### 3. Alternativas ao CarJet

Outras agregadoras de aluguer:
- **RentalCars.com** API
- **Kayak** API (mais difícil)
- **Auto Europe**

---

## 🚀 Próximos Passos Recomendados

### Passo 1: Verificar ScraperOps (Hoje)
```bash
# Testar API key
curl "https://proxy.scrapeops.io/v1/?api_key=SUA_KEY&url=https://httpbin.org/ip"
```

Se retornar 200 OK, a key está válida.

### Passo 2: Gerar URLs de Teste (Hoje)
Use o script `gerar_url_faro.py` para obter URLs s/b válidas:

```bash
python gerar_url_faro.py
# Copiar URL para TEST_FARO_URL
```

Fazer o mesmo para Albufeira.

### Passo 3: Implementar Stealth Mode (Esta Semana)

Adicionar ao `requirements.txt`:
```
playwright-stealth==1.0.5
```

Modificar código Playwright para usar stealth.

### Passo 4: Considerar Serviço Pago (Próximas Semanas)

Avaliar custo vs benefício de serviços profissionais.

---

## 💡 Solução Temporária: URLs Manuais

Enquanto o scraping automático não funciona:

1. **Manualmente**, aceder ao CarJet
2. Fazer pesquisa para Faro e Albufeira
3. Copiar URLs geradas (formato: `?s=...&b=...`)
4. Colocar em `.env`:

```bash
TEST_MODE_LOCAL=1
TEST_FARO_URL=url_copiada_faro
TEST_ALBUFEIRA_URL=url_copiada_albufeira
```

**Duração**: ~1-3 dias até URLs expirarem

---

## 📊 Estimativa de Tempo/Custo

| Solução | Tempo Dev | Custo Mensal | Confiabilidade |
|---------|-----------|--------------|----------------|
| Renovar ScraperOps | 30min | €0 (free tier) | ⚠️ Baixa |
| URLs Manuais | 5min/dia | €0 | ⚠️ Muito Baixa |
| Playwright Stealth | 2-3 dias | €0 | 🟡 Média |
| ScrapingBee | 1 dia | €45/mês | ✅ Alta |
| Proxies Residenciais | 2-3 dias | €100-300/mês | ✅ Muito Alta |
| API Oficial CarJet | Variável | Desconhecido | ✅✅ Máxima |

---

## 🆘 Contacto de Suporte

### ScraperOps
- Website: https://scrapeops.io/
- Support: support@scrapeops.io
- Docs: https://scrapeops.io/docs/

### CarJet
- Website: https://www.carjet.com/
- Email: info@carjet.com
- Perguntar sobre: API access para agregadores

---

## 📝 Log de Tentativas

| Data | Método | Resultado | Notas |
|------|--------|-----------|-------|
| 2025-10-28 | ScraperOps | ❌ HTTP 404 | API key expirada? |
| 2025-10-28 | Selenium | ❌ war=11 | Anti-bot forte |
| 2025-10-28 | Playwright | ❌ Bloqueado | Detectado |

---

## ✅ Ações Imediatas

- [ ] Verificar ScraperOps API key
- [ ] Testar com nova key se expirou
- [ ] Gerar URLs manuais para teste
- [ ] Pesquisar alternativas (ScrapingBee, etc)
- [ ] Considerar implementar Playwright Stealth

---

**Status Geral**: ⚠️ SCRAPING REAL BLOQUEADO - Necessita intervenção manual ou serviço pago
