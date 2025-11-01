# Resultados dos Testes da API - Car Rental Software

**Data**: 28 de Outubro de 2025
**Locais Testados**: Faro e Albufeira

## ✅ Modo Mock (TEST_MODE_LOCAL=2)

API funcionando perfeitamente com dados simulados para ambos os locais.

### Faro (Aeroporto)
- **Status**: ✅ SUCCESS
- **Carros Encontrados**: 34
- **Preço Inicial**: €38.70/dia
- **Fornecedores**: Greenmotion, Goldcar, Surprice, Centauro, OK Mobility
- **Exemplo**: Fiat 500 - Group B1 - Greenmotion - €38.70/dia

### Albufeira (Cidade)
- **Status**: ✅ SUCCESS
- **Carros Encontrados**: 34
- **Preço Inicial**: €53.70/dia (15€ mais caro que Faro)
- **Fornecedores**: Centauro, Goldcar, Surprice, OK Mobility
- **Exemplo**: Fiat 500 - Group B1 - Centauro - €53.70/dia

**Conclusão**: A lógica da API está a funcionar corretamente. Os preços variam conforme esperado entre as localizações.

---

## ⚠️ Modo Real/Scraping (TEST_MODE_LOCAL=0)

API responde mas falha ao obter dados reais do CarJet.

### Faro (Aeroporto)
- **Status**: ⚠️ FALHA NO SCRAPING
- **Carros Encontrados**: 0
- **Tentativas**:
  1. ScraperAPI/ScraperOps: HTTP 404 ❌
  2. Selenium: Redirecionado para página de erro (?war=11) ❌

### Albufeira (Cidade)
- **Status**: ⚠️ FALHA NO SCRAPING
- **Carros Encontrados**: 0
- **Tentativas**:
  1. ScraperAPI/ScraperOps: HTTP 404 ❌
  2. Selenium: Redirecionado para página de erro (?war=11) ❌

### Logs do Selenium
```
[SELENIUM] Preenchendo formulário: Faro Aeroporto (FAO)
[SELENIUM] Submetendo formulário...
[SELENIUM] URL final: https://www.carjet.com/aluguel-carros/index.htm?war=11
[SELENIUM] ⚠️ URL s/b NÃO obtida!
```

**Problemas Identificados**:
1. ❌ ScraperOps retorna HTTP 404 (serviço pode estar inativo ou API key inválida)
2. ❌ CarJet está a redirecionar para página de erro (`war=11`)
3. ❌ Possíveis medidas anti-bot do website

---

## 🔧 Correções Aplicadas

Durante os testes, foram identificadas e corrigidas as seguintes dependências em falta:

1. **httpx** - Necessário para ScraperAPI
2. **selenium** - Necessário para scraping direto
3. **webdriver-manager** - Necessário para gestão automática do ChromeDriver

Estas dependências foram:
- ✅ Instaladas no ambiente virtual
- ✅ Adicionadas ao `requirements.txt`

---

## 📊 Resumo

| Local | Mock Mode | Real Scraping | Comentários |
|-------|-----------|---------------|-------------|
| **Faro** | ✅ 34 carros | ❌ 0 carros | API OK, scraping falha |
| **Albufeira** | ✅ 34 carros | ❌ 0 carros | API OK, scraping falha |

---

## 🎯 Recomendações

### Curto Prazo
1. **Usar Mock Mode** (`TEST_MODE_LOCAL=2`) para desenvolvimento e testes
2. **Verificar API Key** do ScraperOps (pode estar expirada)
3. **Investigar parâmetro `war=11`** do CarJet (Warning/Error code)

### Médio Prazo
1. **Atualizar estratégia de scraping**:
   - Playwright com stealth mode
   - User-agent rotation
   - Proxy rotation
2. **Analisar mudanças no website do CarJet**:
   - Estrutura HTML pode ter mudado
   - Novos campos obrigatórios
   - Validações JavaScript
3. **Implementar retry logic** com backoff exponencial

### Longo Prazo
1. **Considerar alternativas ao scraping**:
   - API oficial do CarJet (se existir)
   - Parceria com agregadores de dados
   - Web scraping as a service (Apify, ScrapingBee)

---

## 🧪 Como Reproduzir os Testes

```bash
# 1. Ativar ambiente virtual
source .venv/bin/activate

# 2. Iniciar servidor
uvicorn main:app --host 0.0.0.0 --port 8000

# 3. Em outro terminal, executar testes
python test_both_locations.py
```

## 🔄 Alternar entre Modos

Editar `.env`:
```bash
# Mock mode (dados simulados)
TEST_MODE_LOCAL=2

# Real scraping (scraping ao vivo)
TEST_MODE_LOCAL=0

# Test URLs (URLs pré-configuradas)
TEST_MODE_LOCAL=1
```
