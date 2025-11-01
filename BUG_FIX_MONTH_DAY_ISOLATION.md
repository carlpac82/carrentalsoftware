# 🐛 BUG FIX - Month/Day Configuration Isolation

## 📋 Problema Reportado

**Descrição:** Quando o utilizador configura uma regra para um mês e dia específico (ex: Novembro + 2 dias), essa regra aparece ativa em todos os outros meses e dias.

**Exemplo do Bug:**
1. Selecionar **Novembro + 2 dias**
2. Configurar regra: Follow Lowest Price + 0.50€
3. Guardar
4. Selecionar **Dezembro + 7 dias**
5. ❌ **BUG**: Os campos mostram a mesma configuração de Novembro

---

## 🔍 Causa Raiz

### Problema 1: IDs dos Campos HTML Não São Únicos
Os campos de configuração usam IDs no formato:
```javascript
`strategy_${location}_${grupo}`
`diffType_${location}_${grupo}`
`minPriceDay_${location}_${grupo}`
```

**NÃO incluem mês nem dia!**

Isto significa que:
- Todos os meses e dias **partilham os mesmos campos HTML**
- Quando mudamos de mês/dia, os campos ainda mostram os valores anteriores
- Visualmente, parece que a configuração está ativa em todos os meses/dias

### Problema 2: Campos Não Eram Limpos ao Mudar de Mês/Dia
A função `loadDayConfiguration()` só chamava `resetDayConfiguration()` se **não houvesse** configuração para aquele dia:

```javascript
if (dayRule) {
    // Carregar configuração
} else {
    resetDayConfiguration(); // ❌ Só limpa se não houver config!
}
```

**Resultado:** Se mudássemos de um dia COM config para outro dia COM config, os campos nunca eram limpos entre as mudanças.

### Problema 3: Dias Permaneciam Selecionados ao Mudar de Mês
Ao selecionar um novo mês, os chips de dias do mês anterior continuavam visualmente selecionados (amarelos).

---

## ✅ Solução Implementada

### Fix 1: Sempre Limpar Campos ANTES de Carregar Config
```javascript
function loadDayConfiguration(location, grupo, month, day) {
    // ✅ SEMPRE reset campos primeiro
    resetDayConfiguration(location, grupo);
    
    const saved = localStorage.getItem('automatedPriceRules');
    if (!saved) return;
    
    const dayRule = rules[location]?.[grupo]?.months?.[month]?.days?.[day];
    if (dayRule) {
        // Carregar configuração específica
    }
    // ✅ Se não houver config, os campos já estão limpos!
}
```

### Fix 2: Limpar Seleção de Dias ao Mudar de Mês
```javascript
function selectMonth(location, grupo, monthNumber, monthName, chipElement) {
    // Selecionar novo mês
    chipElement.dataset.selected = 'true';
    
    // ✅ Limpar seleção de TODOS os dias
    const allDayChips = document.querySelectorAll(
        `button[data-location="${location}"][data-grupo="${grupo}"][data-day]`
    );
    allDayChips.forEach(chip => {
        chip.dataset.selected = 'false';
        chip.className = 'px-2 py-0.5 text-xs border border-gray-300 ...';
    });
    
    // ✅ Esconder conteúdo de configuração
    const ruleContent = document.getElementById(`ruleContent_${location}_${grupo}`);
    ruleContent.classList.add('hidden');
}
```

### Fix 3: Logs de Debug
Adicionados logs para facilitar troubleshooting:
```javascript
console.log(`✅ Loading configuration for ${location}/${grupo}/${month}/${day}`);
console.log(`📭 No configuration saved for ${location}/${grupo}/${month}/${day}`);
console.log(`📅 Month changed to ${monthName} - day selection cleared`);
```

### Fix 4: Verificações Robustas para Valores
Melhorada a verificação de valores null/undefined:
```javascript
// ❌ Antes
if (dayRule.minPriceDay) input.value = dayRule.minPriceDay;

// ✅ Depois
if (dayRule.minPriceDay !== undefined && dayRule.minPriceDay !== null) {
    input.value = dayRule.minPriceDay;
}
```

---

## 🧪 Como Testar a Correção

### Teste 1: Configurações Isoladas por Mês/Dia
1. **Abrir** grupo B1 em Albufeira
2. **Selecionar** Janeiro + 2 dias
3. **Configurar** Follow Lowest Price + 0.50€
4. **Clicar** "Save Settings"
5. **Selecionar** Janeiro + 7 dias
6. ✅ **Verificar**: Campos devem estar vazios (sem config)
7. **Selecionar** Janeiro + 2 dias novamente
8. ✅ **Verificar**: Campos mostram 0.50€ (config guardada)

### Teste 2: Mudança de Mês Limpa Seleção
1. **Selecionar** Janeiro + 2 dias
2. **Configurar** alguma regra
3. **Selecionar** Fevereiro (novo mês)
4. ✅ **Verificar**: 
   - Nenhum dia está selecionado (amarelo)
   - Campos de configuração estão escondidos
   - Console mostra: "📅 Month changed to February..."

### Teste 3: Verificar No Console
Abrir console do browser (F12) e ver logs:
```
✅ Loading configuration for Albufeira/B1/1/2
📭 No configuration saved for Albufeira/B1/1/7
📅 Month changed to February for Albufeira/B1 - day selection cleared
```

### Teste 4: Persistência na Base de Dados
1. Configurar regra para Janeiro + 2 dias
2. Guardar
3. **Recarregar página** (F5)
4. Selecionar Janeiro + 2 dias
5. ✅ **Verificar**: Configuração foi carregada corretamente

---

## 📊 Estrutura de Dados (Correta)

As configurações são guardadas com esta estrutura:
```javascript
{
  "Albufeira": {
    "B1": {
      "months": {
        "1": {  // Janeiro
          "days": {
            "2": {  // 2 dias
              "strategy": "follow_lowest",
              "diffValue": 0.50,
              "minPriceDay": 25.00
            },
            "7": {  // 7 dias
              "strategy": "fixed_margin",
              "margin": 15
            }
          }
        },
        "2": {  // Fevereiro
          "days": {
            "2": { ... }
          }
        }
      }
    }
  }
}
```

**✅ Cada combinação mês+dia tem a sua própria configuração isolada!**

---

## 🎯 Resultado Final

### Antes (❌)
- Regras apareciam em todos os meses/dias
- Campos mostravam última configuração feita
- Confusão sobre qual regra estava ativa onde

### Depois (✅)
- Cada mês+dia é completamente independente
- Campos sempre limpos ao mudar de mês/dia
- Apenas carrega config se existir para aquele mês+dia específico
- Visual claro: campos vazios = sem config, campos preenchidos = tem config

---

## 📝 Ficheiros Modificados

**File:** `templates/price_automation_settings.html`

**Funções alteradas:**
1. `loadDayConfiguration()` - Linhas 1161-1225
   - Sempre chama reset primeiro
   - Logs de debug
   - Verificações robustas

2. `selectMonth()` - Linhas 1068-1098
   - Limpa seleção de dias
   - Esconde conteúdo de config
   - Log de mudança de mês

---

## 🔧 Manutenção Futura

### Se Adicionar Novos Campos
Sempre adicionar no `resetDayConfiguration()`:
```javascript
function resetDayConfiguration(location, grupo) {
    // Adicionar aqui qualquer novo campo!
    document.getElementById(`novocampo_${location}_${grupo}`).value = '';
}
```

### Se Mudar Estrutura de Dados
Atualizar a verificação em `loadDayConfiguration()`:
```javascript
const dayRule = rules[location]?.[grupo]?.months?.[month]?.days?.[day];
```

---

## ✨ Melhorias Adicionais Possíveis

1. **Visual Indicator:** Mostrar badge nos meses que têm configurações
   ```
   [Jan ●] [Feb] [Mar ●] [Apr]
   ```

2. **Copy Config Between Days:** Botão para copiar config de um dia para outro
   (Já existe: botão "Copy from another day")

3. **Batch Configuration:** Permitir configurar múltiplos dias de uma vez
   ```
   Aplicar esta config aos dias: [1] [2] [3] [7]
   ```

4. **Template System:** Guardar configs como templates reutilizáveis
   ```
   Template: "Weekend Pricing"
   - Follow Lowest + 1€
   - Min 30€/day
   ```

---

## 📞 Suporte

Se o bug persistir:
1. ✅ Verificar logs no console do browser (F12)
2. ✅ Verificar localStorage: `localStorage.getItem('automatedPriceRules')`
3. ✅ Verificar base de dados: `SELECT * FROM automated_price_rules;`
4. ✅ Limpar cache e recarregar (Ctrl+Shift+R)
