# 🚀 CRIAR STRATEGIES AUTOMÁTICAS PARA TODOS OS GRUPOS

## Problema
Apenas o grupo B1 tem strategies configuradas, por isso o slider interativo só aparece no B1.

## Solução: Método 1 - Script JavaScript (RECOMENDADO)

### Passo a Passo:

1. **Abrir Settings:**
   - Ir para: `http://localhost:8000/admin/price-automation-settings`

2. **Abrir Console do Browser:**
   - Pressionar `F12` (Windows/Linux) ou `Cmd+Option+I` (Mac)
   - Clicar no tab **Console**

3. **Executar Script:**
   - Abrir o ficheiro: `create_default_strategies.js`
   - **Copiar TODO o conteúdo** do ficheiro
   - **Colar no Console** do browser
   - Pressionar **Enter**

4. **Verificar Resultado:**
   ```
   ✅ DEFAULT STRATEGIES CREATED SUCCESSFULLY!
   📊 Total configurations created: 336
   ```

5. **Refresh a Página:**
   - Pressionar `F5` ou `Cmd+R`

---

## O Que Foi Criado?

### Configuração Automática:

**Localizações:**
- ✅ Albufeira
- ✅ Aeroporto de Faro

**Grupos:**
- ✅ B1, B2, D, E1, E2, F, G, J1, J2, L1, L2, M1, M2, N (todos!)

**Meses:**
- ✅ Novembro (11)
- ✅ Dezembro (12)

**Dias:**
- ✅ 1, 2, 3, 4, 5, 6, 7, 14, 21, 30, 60, 90

**Strategy Padrão:**
- **Tipo:** Follow Lowest Price
- **Diferença:** +0.50€
- **Min Price/Day:** Não definido (pode configurar depois)
- **Min Price/Month:** Não definido (pode configurar depois)

**Total:** 336 configurações (2 localizações × 14 grupos × 2 meses × 12 dias)

---

## Verificar se Funcionou

1. **Ir para:** `/price-automation`
2. **Selecionar data** (ex: 4 Nov 2025)
3. **Clicar em ⚡** (Generate Automated Prices)
4. **Aguardar pesquisa**
5. **Clicar em 📊** (View Cards)
6. **Verificar:**
   - ✅ Todos os grupos (B1, B2, D, etc.) têm AUTOMATED PRICE
   - ✅ Todos têm slider interativo
   - ✅ Todos mostram carro da AutoPrudente

---

## Solução: Método 2 - Manual (Se preferir)

1. **Ir para:** `/admin/price-automation-settings`
2. **Manual Settings** → **Albufeira**
3. **Expandir cada grupo** (B2, D, E1, etc.)
4. **Para cada grupo:**
   - Selecionar mês: **Novembro**
   - Selecionar dia: **1**
   - **Add Strategy:**
     - Type: **Follow Lowest Price**
     - Difference Type: **Euros**
     - Difference Value: **0.50**
   - Clicar **Save**
5. **Repetir para todos os grupos**

---

## Customizar Strategies Depois

Depois de criar as strategies padrão, pode customizar cada grupo:

**Exemplos:**

### Grupo B1 (Mini 4 Doors):
```
- Follow Lowest Price + 0.30€
- Min Price/Day: 22.00€
```

### Grupo D (Economy):
```
- Follow Lowest Price + 0.50€
- Min Price/Day: 25.00€
```

### Grupo F (Intermediate):
```
- Follow Lowest Price + 1.00€
- Min Price/Day: 30.00€
```

### Grupo M1 (7 Seater):
```
- Follow Lowest Price + 2.00€
- Min Price/Day: 50.00€
```

---

## Troubleshooting

### ❌ "Slider ainda não aparece"
**Causa:** Console mostra `Found 0 strategies`
**Solução:** Script não foi executado corretamente. Repetir Método 1.

### ❌ "Automated price não é calculado"
**Causa:** Sem carros no Carjet para aquele grupo/dia
**Solução:** Normal. Alguns grupos podem não ter preços disponíveis.

### ❌ "Erro ao executar script"
**Causa:** Sintaxe incorreta ao copiar
**Solução:** Copiar TODO o conteúdo do ficheiro `create_default_strategies.js`

---

## Notas Importantes

⚠️ **LocalStorage vs Database:**
- Strategies são salvas em `localStorage` (browser)
- Para persistência permanente, usar backend API (futuro)

💡 **Copy Strategies:**
- Use a feature "Copy Strategies to Days" para copiar para mais dias

🔄 **Backup:**
- Fazer export das settings antes de mudanças grandes
- Botão "Export All Settings" no topo da página

---

## Resultado Final

Depois de executar o script, terá:
- ✅ Sliders interativos em TODOS os grupos
- ✅ Carros AutoPrudente em todos os cards
- ✅ Automated prices calculados automaticamente
- ✅ Reordenação dinâmica da lista de preços
- ✅ AI Learning registrando ajustes manuais

**PRONTO PARA USAR EM PRODUÇÃO!** 🚀✨
