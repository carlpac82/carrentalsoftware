# Deploy to Render - Car Rental Price Tracker

## 📋 Pré-requisitos

1. Conta no [Render](https://render.com/) (grátis)
2. Repositório Git com o código
3. Credenciais e API keys prontas

## 🚀 Passos para Deploy

### 1. Push do Código para Git

```bash
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

### 2. Criar Novo Web Service no Render

1. Acesse [Render Dashboard](https://dashboard.render.com/)
2. Clique em **"New +"** → **"Web Service"**
3. Conecte seu repositório Git
4. Selecione o repositório `RentalPriceTrackerPerDay`

### 3. Configurar o Service

O Render irá detectar automaticamente o `render.yaml`. Confirme as seguintes configurações:

- **Name**: `rental-price-tracker`
- **Environment**: `Docker`
- **Plan**: `Free`
- **Auto Deploy**: `Yes`

### 4. Configurar Environment Variables

No dashboard do Render, configure as seguintes variáveis de ambiente:

#### ✅ Obrigatórias

| Variable | Value | Descrição |
|----------|-------|-----------|
| `APP_USERNAME` | `admin` | Username para login |
| `APP_PASSWORD` | `sua_senha_segura` | Password para login (mude!) |
| `SECRET_KEY` | (auto-gerado) | Chave para sessions |

#### ⚙️ Configuração de Scraping

| Variable | Value | Descrição |
|----------|-------|-----------|
| `USE_PLAYWRIGHT` | `1` | Ativar Playwright |
| `TEST_MODE_LOCAL` | `2` | **2**=Mock, **1**=Test URLs, **0**=Real scraping |
| `SCRAPER_SERVICE` | `scrapeops` | Serviço de proxy |
| `SCRAPER_API_KEY` | `sua_api_key` | API key do ScraperOps |
| `SCRAPER_COUNTRY` | `pt` | País do proxy |

#### 🧪 URLs de Teste (Opcional)

| Variable | Value | Descrição |
|----------|-------|-----------|
| `TEST_FARO_URL` | URL do CarJet | Para TEST_MODE_LOCAL=1 |
| `TEST_ALBUFEIRA_URL` | URL do CarJet | Para TEST_MODE_LOCAL=1 |

### 5. Deploy

1. Clique em **"Create Web Service"**
2. Aguarde o build (~5-10 minutos na primeira vez)
3. O Render irá:
   - Build do Docker image
   - Instalar dependências Python
   - Instalar Playwright e Chromium
   - Iniciar a aplicação

### 6. Verificar Deploy

Quando o deploy estiver completo:

1. Acesse a URL fornecida pelo Render: `https://rental-price-tracker.onrender.com`
2. Teste o health check: `https://rental-price-tracker.onrender.com/healthz`
   - Deve retornar: `{"ok": true}`
3. Faça login com suas credenciais
4. Teste a API com ambos os locais (Faro e Albufeira)

## 🔧 Modos de Operação

### Mock Mode (Recomendado para Produção)

```
TEST_MODE_LOCAL=2
```

✅ **Vantagens**:
- Rápido (sem scraping)
- Sempre funciona
- Grátis (sem custos de API)
- Bom para testes

❌ **Desvantagens**:
- Dados simulados
- Preços não são reais

### Test URL Mode

```
TEST_MODE_LOCAL=1
TEST_FARO_URL=https://www.carjet.com/do/list/pt?s=...
TEST_ALBUFEIRA_URL=https://www.carjet.com/do/list/pt?s=...
```

✅ **Vantagens**:
- Preços reais
- Mais rápido que scraping dinâmico

❌ **Desvantagens**:
- URLs expiram
- Precisa atualizar manualmente

### Real Scraping Mode

```
TEST_MODE_LOCAL=0
SCRAPER_API_KEY=sua_key_scrapeops
```

✅ **Vantagens**:
- Dados 100% reais e atualizados
- Totalmente automático

❌ **Desvantagens**:
- Lento (15-30 seg por consulta)
- Pode ser bloqueado (anti-bot)
- Custos de API (ScraperOps)
- **Atualmente com problemas** (ver TEST_RESULTS.md)

## 🐛 Troubleshooting

### Build Falha

**Problema**: Erro durante `pip install` ou `playwright install`

**Solução**:
```bash
# Verifique requirements.txt está correto
# Certifique-se que todas as deps estão listadas
```

### Health Check Falha

**Problema**: `/healthz` retorna erro ou timeout

**Solução**:
1. Verifique logs no Render Dashboard
2. Confirme que a porta está correta (8000)
3. Verifique se o servidor iniciou corretamente

### Login Não Funciona

**Problema**: Credenciais não aceitas

**Solução**:
1. Verifique `APP_USERNAME` e `APP_PASSWORD` nas env vars
2. Confirme que `SECRET_KEY` foi gerado
3. Teste com credenciais corretas

### Scraping Retorna 0 Resultados

**Problema**: API responde mas sem carros

**Solução**:
1. Mude `TEST_MODE_LOCAL=2` para usar mock data
2. Verifique logs para erros de scraping
3. Confirme se `SCRAPER_API_KEY` é válida
4. Consulte `TEST_RESULTS.md` para status atual

## 📊 Monitoramento

### Logs

Acesse logs em tempo real:
1. Dashboard do Render → Seu service
2. Tab **"Logs"**
3. Procure por:
   - `[API] REQUEST:` - Chamadas da API
   - `[SELENIUM]` - Status do scraping
   - `ERROR` - Erros

### Métricas

No Free Plan do Render:
- ✅ Health checks automáticos
- ✅ Auto-restart em caso de crash
- ⚠️ Sleep após 15 min de inatividade
- ⚠️ 750h grátis/mês

## 🔒 Segurança

### Passwords

**IMPORTANTE**: Mude as senhas padrão!

```
APP_USERNAME=seu_username_unico
APP_PASSWORD=senha_muito_forte_123!@#
```

### API Keys

- Nunca comite API keys no Git
- Use environment variables do Render
- Marque como `sync: false` no render.yaml

### HTTPS

O Render fornece HTTPS automático:
- ✅ Certificado SSL grátis
- ✅ Renovação automática
- ✅ Força HTTPS

## 💰 Custos

### Render Free Plan

- **Web Service**: Grátis (750h/mês)
- **Bandwidth**: 100 GB/mês grátis
- **Build Time**: Ilimitado

### ScraperOps (se usar scraping real)

- **Free Tier**: 1,000 requests/mês
- **Paid Plans**: A partir de $29/mês
- **Alternativas**: ScrapingBee, Apify, Bright Data

## 📚 Recursos

- [Render Docs](https://render.com/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/docker/)
- [Playwright in Docker](https://playwright.dev/python/docs/docker)
- [ScraperOps](https://scrapeops.io/)

## 🎯 Próximos Passos

1. ✅ Deploy inicial com Mock Mode
2. ✅ Testar health check e login
3. ✅ Verificar que ambos os locais funcionam
4. 🔄 Configurar scraping real (quando fixado)
5. 🔄 Adicionar domínio custom (opcional)
6. 🔄 Configurar alertas/monitoring

---

**Última atualização**: 28 de Outubro de 2025
**Status**: ✅ Pronto para deploy com Mock Mode
