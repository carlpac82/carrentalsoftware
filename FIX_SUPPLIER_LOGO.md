# FIX: Correção de Logos de Suppliers Incorretos

## 🐛 Problema Identificado

Veículos que aparecem como **Autoprudente (AUP)** no CarJet estavam a ser apresentados com o logo da **Centauro (CEN)** no website da API.

### Veículos Afetados (Exemplo)
- **Renault Grand Scenic Auto** - 352,26 € (3 dias, Albufeira)
- **Renault Grand Scenic** - 172,74 € (3 dias, Albufeira)

### URL de Referência
```
https://www.carjet.com/do/list/pt?s=af5264f8-30cc-4bfe-9e6b-7898c4dbda3a&b=b9b9ea42-1d73-4e65-b10b-4a422ece975a
```

---

## 🔍 Causa Raiz

O HTML do CarJet contém **múltiplos elementos `<img>` com logos de suppliers** dentro de cada card de veículo. O código anterior usava `query_selector()` que retorna apenas o **primeiro elemento** encontrado.

**Estrutura HTML do CarJet:**
```html
<article class="all-areas" data-prv="AUP" data-order="90">
    <div class="cl--footer">
        <div class="cl--car-rent">
            <!-- Primeiro logo (pode ser de outro supplier) -->
            <img src="/cdn/img/prv/flat/mid/logo_CEN.png" alt="CENTAURO">
            
            <!-- Logo correto (mais abaixo no HTML) -->
            <img src="/cdn/img/prv/flat/mid/logo_AUP.png" alt="AUTO PRUDENTE">
        </div>
    </div>
</article>
```

O atributo **`data-prv="AUP"`** no elemento `<article>` é a fonte mais confiável, mas estava a ser ignorado.

---

## ✅ Solução Implementada

### Alterações no Código

#### 1. Função `scrape_with_playwright()` (linhas 282-308)

**ANTES:**
```python
# Prioridade 1: Logo do supplier
im = h.query_selector("img[src*='/prv/'], img[src*='logo_']")
if im:
    src = im.get_attribute("src") or ""
    match = re.search(r'logo_([A-Z0-9]+)', src)
    if match:
        supplier = match.group(1)
```

**DEPOIS:**
```python
# Prioridade 1: Atributo data-prv do article (mais confiável)
prv_code = h.get_attribute("data-prv")
if prv_code:
    supplier = prv_code.strip()
    print(f"[PLAYWRIGHT] Supplier extraído de data-prv: {supplier}", file=sys.stderr, flush=True)

# Prioridade 2: Logo do supplier (fallback)
if not supplier:
    im = h.query_selector("img[src*='/prv/'], img[src*='logo_']")
    if im:
        src = im.get_attribute("src") or ""
        match = re.search(r'logo_([A-Z0-9]+)', src)
        if match:
            supplier = match.group(1)
```

#### 2. Função `parse_prices()` (linhas 4268-4284)

**ANTES:**
```python
code = ""
for im in card.select("img[src]"):
    src = im.get("src") or ""
    mcode = LOGO_CODE_RX.search(src)
    if mcode:
        code = (mcode.group(1) or "").upper()
        break
```

**DEPOIS:**
```python
# Prioridade 1: Atributo data-prv do card (mais confiável)
code = (card.get("data-prv") or "").strip().upper()

# Prioridade 2: Logo do supplier (fallback)
if not code:
    for im in card.select("img[src]"):
        src = im.get("src") or ""
        mcode = LOGO_CODE_RX.search(src)
        if mcode:
            code = (mcode.group(1) or "").upper()
            break
```

---

## 🎯 Hierarquia de Extração de Supplier

### Nova Ordem de Prioridade:
1. ✅ **Atributo `data-prv`** do elemento `<article>` ou card (MAIS CONFIÁVEL)
2. ✅ **Logo do supplier** extraído do `src` da imagem (`logo_AUP.png` → `AUP`)
3. ✅ **Texto do supplier** em elementos `.supplier`, `.vendor`, etc. (fallback final)

---

## 📊 Mapeamento de Códigos para Nomes

O código do supplier (ex: `AUP`, `CEN`) é mapeado para o nome completo:

```python
supplier_alias = {
    "AUP": "Auto Prudente Rent a Car",  # ✅ CORRETO
    "CEN": "Centauro",                   # ❌ ERRADO (era capturado antes)
    "SXT": "Sixt",
    "ECR": "Europcar",
    # ... 150+ suppliers
}
```

---

## 🧪 Como Testar

### 1. Fazer Nova Pesquisa
```bash
# Iniciar servidor
cd ~/CascadeProjects/RentalPriceTrackerPerDay
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 2. Pesquisar no Website
- **Local:** Albufeira
- **Data recolha:** 04/11/2025
- **Dias:** 3
- **Hora:** 14:30

### 3. Verificar Resultados
Os veículos **Renault Grand Scenic** e **Renault Grand Scenic Auto** devem aparecer com:
- ✅ Logo: **Auto Prudente** (logo_AUP.png)
- ❌ NÃO: Centauro (logo_CEN.png)

### 4. Verificar Logs
```bash
tail -f nohup.out | grep "data-prv"
```

Deve aparecer:
```
[PLAYWRIGHT] Supplier extraído de data-prv: AUP
```

---

## 📝 Commit

```bash
git log -1 --oneline
# bb4022b fix: priorizar data-prv para extrair supplier correto
```

**Mensagem completa:**
```
fix: priorizar data-prv para extrair supplier correto

- Problema: Veículos da Autoprudente (AUP) apareciam com logo da Centauro (CEN)
- Causa: HTML do CarJet tem múltiplos logos, scraper capturava o primeiro
- Solução: Priorizar atributo data-prv do elemento article/card
- Aplicado em scrape_with_playwright() e parse_prices()
- Fallback mantido para logo e texto se data-prv não existir
```

---

## 🔄 Próximos Passos

1. ✅ **Testar com pesquisa real** (3 dias, Albufeira, 04/11/2025)
2. ✅ **Verificar logs** para confirmar extração de `data-prv`
3. ✅ **Validar no website** que logos estão corretos
4. ✅ **Fazer backup** antes de fechar Windsurf

---

## 📚 Ficheiros Modificados

- **main.py** (linhas 282-308, 4268-4284)
  - `scrape_with_playwright()` - extração de supplier com Playwright
  - `parse_prices()` - extração de supplier com BeautifulSoup

---

## ⚠️ Notas Importantes

- O atributo `data-prv` é **sempre confiável** no HTML do CarJet
- Mantido **fallback** para casos onde `data-prv` não existe
- Logs adicionados para **debug** (apenas quando `data-prv` é usado)
- **Não afeta** extração de suppliers de JSON (já estava correto)

---

**Data:** 31 de Outubro de 2025  
**Autor:** Cascade AI  
**Versão:** 1.0
