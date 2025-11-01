# 🔧 VARIÁVEIS DE AMBIENTE NECESSÁRIAS NO RENDER

## ⚠️ PROBLEMA ATUAL:
Render NÃO tem as URLs pré-geradas nem o SCRAPER_API_KEY configurado!
Por isso só tenta Selenium e sempre dá `war=0`.

## ✅ SOLUÇÃO: Adicionar estas variáveis no Dashboard do Render

### 1. Dashboard Render:
```
https://dashboard.render.com/
→ carrental-final
→ Environment
→ Add Environment Variable
```

### 2. Variáveis CRÍTICAS (copiar e colar):

```bash
# ScraperAPI (tenta primeiro, mais confiável)
SCRAPER_SERVICE=scrapeops
SCRAPER_API_KEY=80bba4c6-e162-4796-bada-5f6d1646051f
SCRAPER_COUNTRY=pt

# URLs Faro (válidas ~24h, geradas 2025-11-01)
FARO_1D=https://www.carjet.com/do/list/pt?s=bfe7dfb7-3285-4ff7-a519-20af8bd07fb8&b=6477f981-b30a-4fb2-ba2a-ccf43238ba06
FARO_2D=https://www.carjet.com/do/list/pt?s=a615769e-4809-4c6f-a6b9-f9722e0f4282&b=c390a1bf-41af-402d-a699-0e3216e1cc7f
FARO_3D=https://www.carjet.com/do/list/pt?s=4d8cdb54-369b-45e7-8aae-ea724530c732&b=abb8a58d-4f7c-45bb-8bd0-9feaa6a1b2f5
FARO_4D=https://www.carjet.com/do/list/pt?s=4ca4f2e2-16e4-4793-b177-1350dc86d9ea&b=06534536-15f1-4a25-9515-74d625d9ca89
FARO_5D=https://www.carjet.com/do/list/pt?s=67a77525-14b0-46cc-8ad2-fca08b647a30&b=649d7e98-8bc3-4944-9f76-4d1dce716f21
FARO_6D=https://www.carjet.com/do/list/pt?s=ea0f1d29-e37e-4eed-9c23-680329dc2c4c&b=60a7a51d-d79f-4531-905e-c5d0ee7a7aa9
FARO_7D=https://www.carjet.com/do/list/pt?s=8cb70642-ba28-40a4-bfee-52e6b4d8eef1&b=6a5e62a8-ef46-4ff0-8386-a1f93fc03c1b
FARO_8D=https://www.carjet.com/do/list/pt?s=47022592-88fc-4868-b660-32a1a0b06380&b=bb9e4130-f310-4a72-b468-d97c83f5089b
FARO_9D=https://www.carjet.com/do/list/pt?s=cf692205-6335-4690-a5e5-673c5bb6524d&b=f96c54de-f263-47a1-9870-d2eac77c748a
FARO_14D=https://www.carjet.com/do/list/pt?s=d0fae63e-14f4-4abc-99ff-fe09476f2d50&b=cfe2538a-f0bf-4024-a58c-8700f28ed2dd
FARO_22D=https://www.carjet.com/do/list/pt?s=a80caa06-0cc5-4a82-99cd-d8d427027a15&b=693da1ce-e7cd-49c6-b9af-59477095fa53
FARO_28D=https://www.carjet.com/do/list/pt?s=dc32d0cb-1558-4adc-a37a-1f03351cf330&b=947525dd-afa4-4ec1-a65e-a9451d7965e5
FARO_31D=https://www.carjet.com/do/list/pt?s=5ec479dd-5fcb-4eee-990b-90d8682df806&b=28134386-2b59-41bc-aa19-1bae18e92dfa
FARO_60D=https://www.carjet.com/do/list/pt?s=bcca77e3-c272-4a37-83a1-b6844e3679cf&b=8faa8434-ffb7-4a1a-af8a-82baebefd0ea

# URLs Albufeira (válidas ~24h, geradas 2025-11-01)
ALBUFEIRA_1D=https://www.carjet.com/do/list/pt?s=e8d6b135-4a1d-4e16-97b8-78c8dd6efeb0&b=65588dc1-6c8e-4495-aa5a-d9f9eca4937e
ALBUFEIRA_2D=https://www.carjet.com/do/list/pt?s=71899e60-0407-437f-a9e1-0790332e67cf&b=445c911f-0f48-440b-960c-9d7b2fbded79
ALBUFEIRA_3D=https://www.carjet.com/do/list/pt?s=00a32904-d9cc-428f-b843-5374391c1046&b=95c2c57b-d449-44dc-b4cf-d4ef0d61ebc3
ALBUFEIRA_4D=https://www.carjet.com/do/list/pt?s=5fe26f0f-b6ad-46ae-a481-0099bc24a3d5&b=9d8f8081-d8fa-415d-bed3-e55bcdc92f26
ALBUFEIRA_5D=https://www.carjet.com/do/list/pt?s=515430ae-4d41-40c7-a80b-2252f1aa91b7&b=044f1f53-e49f-4568-91e6-f53b74f0b293
ALBUFEIRA_6D=https://www.carjet.com/do/list/pt?s=72d0621c-d391-4815-9ea3-ab20ebb57001&b=19d9c816-4d86-41c7-9db0-fba76c00fd18
ALBUFEIRA_7D=https://www.carjet.com/do/list/pt?s=f9ddd8b3-0256-4d1e-95ce-a7733bc4425f&b=49ac64da-9cea-45ef-99e0-4dd14ae0cacc
ALBUFEIRA_8D=https://www.carjet.com/do/list/pt?s=f9ddd8b3-0256-4d1e-95ce-a7733bc4425f&b=49ac64da-9cea-45ef-99e0-4dd14ae0cacc
ALBUFEIRA_9D=https://www.carjet.com/do/list/pt?s=f9ddd8b3-0256-4d1e-95ce-a7733bc4425f&b=95be8602-5ab4-422a-9e58-65c2b168bc1c
ALBUFEIRA_14D=https://www.carjet.com/do/list/pt?s=e4632759-2151-4c66-8211-3714f47de618&b=61a9601f-e31e-4d3a-819d-ae0348692e95
ALBUFEIRA_22D=https://www.carjet.com/do/list/pt?s=302f9f60-8976-43dc-91b5-1a87d13afa33&b=fbfe4225-7cfd-4ecb-b7d7-e71dc9627319
ALBUFEIRA_28D=https://www.carjet.com/do/list/pt?s=4d595b00-6eed-4efa-822b-2327f09c0d14&b=1129f359-7e3a-47f9-a7d0-006eaa566f43
ALBUFEIRA_31D=https://www.carjet.com/do/list/pt?s=cc40aac7-347e-456e-b9dc-d9e440679347&b=232248c6-39ec-4202-80a3-287df1cbede9
ALBUFEIRA_60D=https://www.carjet.com/do/list/pt?s=1227a4bd-be23-4b84-86b3-df1d1f704ba7&b=f12b3891-cf3a-498a-b48a-62b4af1f60cd
```

### 3. Ordem de tentativas DEPOIS de configurar:

1. **ScraperAPI** (mais confiável) ✅
2. **Selenium** (fallback)
3. **Playwright** (último recurso)

### 4. Como adicionar no Render:

#### Método Rápido (um por um):
```
1. Abrir: https://dashboard.render.com/
2. Clicar: carrental-final
3. Tab: Environment
4. Botão: Add Environment Variable
5. Copiar nome (ex: SCRAPER_API_KEY)
6. Copiar valor (ex: 80bba4c6-e162-4796-bada-5f6d1646051f)
7. Clicar: Add
8. Repetir para todas as 31 variáveis
9. Clicar: Save Changes
10. Aguardar redeploy automático
```

### 5. Variáveis que JÁ DEVEM ESTAR no Render:
```
APP_PASSWORD=admin
SECRET_KEY=(gerado automaticamente)
TEST_MODE_LOCAL=0
USE_PLAYWRIGHT=1
```

### 6. Logs esperados DEPOIS de configurar:

```
[SCRAPERAPI] Iniciando scraping para Albufeira
[SCRAPERAPI] Fazendo request via ScraperOps...
[SCRAPERAPI] ✅ HTML recebido: 250000 bytes
[SCRAPERAPI] Parsed 65 items
[SCRAPERAPI] ✅ 60+ carros encontrados!
```

### 7. URLs expiram em ~24h:
Estas URLs foram geradas em 2025-11-01.
Quando expirarem, precisas gerar novas usando Selenium localmente.

### 8. Alternativa (se não quiser adicionar URLs):
Só adicionar:
```
SCRAPER_API_KEY=80bba4c6-e162-4796-bada-5f6d1646051f
SCRAPER_SERVICE=scrapeops
SCRAPER_COUNTRY=pt
```

E deixar usar Selenium como fallback (mas pode dar war=0).

## ⚠️ NOTA IMPORTANTE:
Sem estas variáveis, o Render SEMPRE vai usar só Selenium,
que tem taxa de falha alta (war=0) e requer 2 cliques!
