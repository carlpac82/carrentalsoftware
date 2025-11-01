# 🔍 DEBUG - Problema de Replicação de Regras

## ❌ Problema Reportado
Quando configuro uma regra para Nov + 1 dia, ela aparece replicada em TODOS os dias e meses.

## 🛠️ Alterações Implementadas

### 1. Reset Agressivo
- FORÇA a limpeza de TODOS os inputs
- Loga cada input que está a ser limpo
- Garante que não fica nenhum valor residual

### 2. Logs Extremamente Detalhados
- Mostra TODO o processo de load
- Mostra passo-a-passo a navegação da estrutura de dados
- Indica claramente SE há ou NÃO há configuração

### 3. Auto-Save por Grupo/Mês/Dia
- Cada campo guarda APENAS para o mês/dia específico
- Usa dataset para guardar contexto atual
- Impossível guardar para o grupo errado

## 📝 TESTE DEFINITIVO

### PASSO 1: Limpar Tudo
1. Abrir http://localhost:8000/admin/price-automation-settings
2. Pressionar F12 (abrir console)
3. Executar no console:
   ```javascript
   localStorage.removeItem('automatedPriceRules');
   location.reload();
   ```

### PASSO 2: Configurar Nov + 1 dia
1. Tab "Albufeira" → Grupo B1
2. Clicar "Nov" (mês)
3. Clicar "1d" (dia)

**Verificar no Console:**
```
═══════════════════════════════════════════════════════════
📂 Loading config for: Albufeira/B1/11/1
═══════════════════════════════════════════════════════════
🧹🧹🧹 AGGRESSIVE RESET for Albufeira/B1
  → Strategy FORCED to: follow_lowest
  → Input diffValue_Albufeira_B1 cleared: 
  → Input minPriceDay_Albufeira_B1 cleared: 
  ...
✅✅✅ AGGRESSIVE RESET COMPLETE
❌ No saved rules in localStorage
═══════════════════════════════════════════════════════════
```

4. Configurar: Follow Lowest + 0.50€
5. Colocar Min Price/Day: 25

**Verificar no Console após alterar campo:**
```
📝 Field diffValue_Albufeira_B1 changed - auto-saving Albufeira/B1/11/1
💾 Saving config for Albufeira/B1/11/1: {...}
✅ Config saved for Albufeira/B1/11/1
✅ Configuration saved!
```

### PASSO 3: Mudar para Nov + 2 dias
1. Clicar "2d"

**Verificar no Console:**
```
═══════════════════════════════════════════════════════════
📂 Loading config for: Albufeira/B1/11/2
═══════════════════════════════════════════════════════════
🧹🧹🧹 AGGRESSIVE RESET for Albufeira/B1
  → Strategy FORCED to: follow_lowest
  → Input diffValue_Albufeira_B1 cleared: 
  ...
✅✅✅ AGGRESSIVE RESET COMPLETE
📦 Full rules object: {
  "Albufeira": {
    "B1": {
      "months": {
        "11": {
          "days": {
            "1": {
              "strategy": "follow_lowest",
              "diffValue": 0.5,
              "minPriceDay": 25
            }
          }
        }
      }
    }
  }
}
  → Available days in month 11: ["1"]
📭 NO CONFIGURATION for Albufeira/B1/11/2
   Fields should be empty/default
═══════════════════════════════════════════════════════════
```

**VERIFICAR VISUALMENTE:**
- ❓ Os campos mostram valores (0.50€, 25€)?
- ❓ OU os campos estão VAZIOS?

### PASSO 4: Verificar o HTML
Se os campos ainda mostram valores, executar no console:
```javascript
const input = document.getElementById('diffValue_Albufeira_B1');
console.log('Input value:', input.value);
console.log('Input element:', input);
```

### PASSO 5: Voltar para Nov + 1 dia
1. Clicar "1d" novamente

**Verificar no Console:**
```
═══════════════════════════════════════════════════════════
📂 Loading config for: Albufeira/B1/11/1
═══════════════════════════════════════════════════════════
🧹🧹🧹 AGGRESSIVE RESET for Albufeira/B1
  ...
✅✅✅ AGGRESSIVE RESET COMPLETE
📦 Full rules object: {...}
✅✅✅ CONFIGURATION FOUND for Albufeira/B1/11/1
   Config: {
     "strategy": "follow_lowest",
     "diffValue": 0.5,
     "minPriceDay": 25,
     ...
   }
   → Loading strategy: follow_lowest
   → Loading diffValue: 0.5
   → Loading minPriceDay: 25
```

**VERIFICAR:** Campos devem mostrar 0.50€ e 25€

## 🔍 Análise de Resultados

### Se os campos ficam VAZIOS em Nov+2d ✅
**PROBLEMA RESOLVIDO!** 
- A lógica está correta
- Cada mês/dia é independente
- Funciona conforme esperado

### Se os campos AINDA mostram valores em Nov+2d ❌
**PROBLEMA IDENTIFICADO:**

O problema NÃO está no JavaScript! Está em uma destas 3 possibilidades:

1. **Browser Cache:**
   - O navegador está a usar ficheiro antigo em cache
   - Solução: Ctrl+Shift+R (hard refresh)

2. **Valores Default no HTML:**
   - Os campos têm valores default no HTML
   - Solução: Verificar o HTML dos inputs

3. **Outro Script:**
   - Existe outro script a preencher os campos
   - Solução: Verificar todos os scripts na página

## 📋 Checklist de Debug

- [ ] Console aberto durante todo o teste
- [ ] localStorage limpo antes de começar
- [ ] Logs mostram "AGGRESSIVE RESET" a cada mudança de dia
- [ ] Logs mostram "NO CONFIGURATION" para Nov+2d
- [ ] Logs mostram "CONFIGURATION FOUND" para Nov+1d
- [ ] Verificado valor do input via JavaScript console
- [ ] Hard refresh feito (Ctrl+Shift+R)

## 📤 O Que Partilhar

Se o problema persistir, partilhar:

1. **Screenshot** dos campos mostrando valores em Nov+2d
2. **Console logs completos** (copiar tudo)
3. **Resultado do comando:**
   ```javascript
   JSON.stringify(localStorage.getItem('automatedPriceRules'), null, 2)
   ```
4. **Valor do input:**
   ```javascript
   document.getElementById('diffValue_Albufeira_B1').value
   ```

## 🎯 Próximos Passos

Se após TODOS estes logs e testes ainda houver problema, significa que:

1. O reset NÃO está a funcionar (mas os logs mostrarão isso)
2. O load ESTÁ a carregar quando não devia (mas os logs mostrarão isso)
3. Há algum outro código a interferir (precisaremos procurar)

Com todos estes logs, será IMPOSSÍVEL o problema passar despercebido! 🔍✨
