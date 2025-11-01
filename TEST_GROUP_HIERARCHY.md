# 🧪 INSTRUÇÕES DE TESTE - GROUP HIERARCHY

## ✅ Alterações Implementadas

### 1. **3 Operadores de Comparação**
- **≥** (maior ou igual) - Grupo deve ser maior ou igual ao outro
- **≤** (menor ou igual) - Grupo deve ser menor ou igual ao outro  
- **>** (estritamente maior) - Grupo deve ser maior (não pode ser igual)

### 2. **Seleção Múltipla de Grupos**
Agora pode selecionar múltiplos grupos com operadores diferentes:
- **Exemplo:** Grupo B1 pode ser ≤ D E ≤ G simultaneamente
- **Exemplo:** Grupo D pode ser ≥ B1 E ≥ B2 simultaneamente

### 3. **Mensagens de Erro Melhoradas**
- Console do browser mostra erros detalhados
- Logs do servidor mostram o que está a ser guardado
- Notificações mostram erro específico se falhar

---

## 🎯 COMO TESTAR (PASSO A PASSO)

### Passo 1: Aceder à Página
```
URL: http://localhost:8000/admin/price-automation-settings
Login: admin / admin123
```

### Passo 2: Ativar Group Hierarchy
1. Scroll até "Group Hierarchy & Price Validation"
2. ✅ Marcar checkbox "Enable Group Hierarchy Validation"
3. A secção deve expandir

### Passo 3: Configurar Regra Simples
**Teste A: D ≥ B1 (D deve ser maior ou igual a B1)**

1. Clicar em "Configure Dependencies"
2. No dropdown, selecionar **"D - Economy"**
3. Marcar checkbox **"B1 - Mini 4 Doors"**
4. Verificar que o select mostra **"≥ (greater or equal)"**
5. Clicar "Apply Rules"
6. **Resultado esperado:** Lista mostra "D ≥ B1"

### Passo 4: Configurar Múltiplas Dependências
**Teste B: D ≥ B1 AND D ≥ B2**

1. Clicar em "Configure Dependencies"
2. Selecionar **"D - Economy"** (já tem B1 configurado)
3. Marcar checkbox **"B2 - Mini"**
4. O select de B2 deve mostrar **"≥ (greater or equal)"**
5. Clicar "Apply Rules"
6. **Resultado esperado:** Lista mostra "D ≥ B1, ≥ B2"

### Passo 5: Testar Operador Diferente
**Teste C: B1 ≤ D (B1 deve ser menor ou igual a D)**

1. Clicar em "Configure Dependencies"
2. Selecionar **"B1 - Mini 4 Doors"**
3. Marcar checkbox **"D - Economy"**
4. **ALTERAR** o select para **"≤ (less or equal)"**
5. Clicar "Apply Rules"
6. **Resultado esperado:** Lista mostra "B1 ≤ D"

### Passo 6: Testar Operador ">" (estritamente maior)
**Teste D: N > M1 (N deve ser estritamente maior que M1)**

1. Clicar em "Configure Dependencies"
2. Selecionar **"N - 9 Seater"**
3. Marcar checkbox **"M1 - 7 Seater"**
4. Alterar select para **"> (greater than)"**
5. Clicar "Apply Rules"
6. **Resultado esperado:** Lista mostra "N > M1"

### Passo 7: Guardar Configurações
1. Clicar botão **"Save Settings"** (no final da página)
2. **Verificar Console do Browser (F12):**
   - Deve ver: `💾 Saving settings to database...`
   - Deve ver: `📥 Server response: {ok: true, ...}`
3. **Verificar Notificação:**
   - Verde: "✅ Settings saved to database!"
   - Amarelo: "⚠️ Saved locally only..." (se houver erro)

### Passo 8: Verificar Persistência
1. **Recarregar a página (F5)**
2. Expandir "Group Hierarchy & Price Validation"
3. **Verificar que todas as regras estão visíveis**

---

## 🔍 VERIFICAÇÃO DA BASE DE DADOS

### Opção 1: Via Console do Browser
```javascript
// Abrir console (F12) e executar:
fetch('/api/price-automation/settings/load')
  .then(r => r.json())
  .then(data => console.log('Settings from DB:', data))
```

**Resultado esperado:**
```json
{
  "ok": true,
  "settings": {
    "groupHierarchyRules": {
      "D": [
        {"group": "B1", "operator": ">="},
        {"group": "B2", "operator": ">="}
      ],
      "B1": [
        {"group": "D", "operator": "<="}
      ]
    }
  }
}
```

### Opção 2: Via SQLite direto
```bash
cd /Users/filipepacheco/CascadeProjects/RentalPriceTrackerPerDay

sqlite3 carrental.db "SELECT key, value FROM price_automation_settings WHERE key='groupHierarchyRules';"
```

---

## ❌ TESTE DE ERROS ESPERADOS

### Erro 1: Tentar selecionar o próprio grupo
1. Selecionar "D - Economy"
2. Tentar marcar checkbox "D - Economy"
3. **Esperado:** Checkbox está desabilitado e opaco

### Erro 2: Não selecionar nenhum grupo
1. Selecionar "D - Economy"
2. NÃO marcar nenhum checkbox
3. Clicar "Apply Rules"
4. **Esperado:** Regra é removida (se existia)

---

## 📊 LOGS DO SERVIDOR

Ao guardar, deve ver no terminal do servidor:
```
INFO:     💾 Saving price automation settings: 9 keys
DEBUG:      - comissaoBroker: 13.66
DEBUG:      - groupHierarchyRules: {"D":[{"group":"B1","operator":">="},...
INFO:     ✅ Price automation settings saved successfully to database
```

---

## 🐛 TROUBLESHOOTING

### Problema: "Saved locally only (database error)"

**Verificar:**
1. Console do browser - ver mensagem de erro detalhada
2. Logs do servidor - procurar por "❌ Database error"
3. Permissões do ficheiro `carrental.db`

**Solução rápida:**
```bash
# Verificar se DB existe
ls -la carrental.db

# Testar acesso direto
sqlite3 carrental.db "SELECT COUNT(*) FROM price_automation_settings;"
```

### Problema: Regras desaparecem ao recarregar

**Verificar:**
1. Se viu mensagem verde "✅ Settings saved to database!"
2. Se clicar em "Save Settings" após configurar regras
3. Console para erros de JavaScript

---

## ✨ EXEMPLOS PRÁTICOS DE USO

### Exemplo 1: Hierarquia de Minis
```
B1 (Mini 4 Doors) ≤ D (Economy)
B2 (Mini) ≤ D (Economy)
```
**Resultado:** Minis nunca podem custar mais que Economy

### Exemplo 2: Automáticos > Manuais
```
E1 (Mini Auto) > B2 (Mini manual)
E2 (Economy Auto) > D (Economy manual)
L1 (SUV Auto) > F (SUV manual)
```
**Resultado:** Automáticos sempre mais caros que manuais

### Exemplo 3: Hierarquia de Tamanho
```
N (9 Seater) ≥ M1, M2 (7 Seaters)
M1 (7 Seater) ≥ L1, L2 (SUVs)
```
**Resultado:** Veículos maiores têm preços crescentes

---

## 📝 CHECKLIST FINAL

- [ ] Servidor a correr em http://localhost:8000
- [ ] Login com admin/admin123
- [ ] Página /admin/price-automation-settings carrega
- [ ] Checkbox "Enable Group Hierarchy Validation" funciona
- [ ] Botão "Configure Dependencies" abre modal
- [ ] Consegue selecionar múltiplos grupos
- [ ] Consegue alterar operadores (≥, ≤, >)
- [ ] Botão "Apply Rules" adiciona regra à lista
- [ ] Regras aparecem no formato correto (ex: "D ≥ B1, ≥ B2")
- [ ] Botão "Save Settings" guarda na base de dados
- [ ] Notificação verde aparece após guardar
- [ ] Após F5, regras ainda estão presentes
- [ ] Console não mostra erros JavaScript
- [ ] Logs do servidor mostram salvamento bem-sucedido

---

## 🎓 DOCUMENTAÇÃO COMPLETA

Ver: `GROUP_HIERARCHY_IMPROVEMENTS.md` para:
- Detalhes técnicos da implementação
- Estrutura de dados completa
- Exemplos de código
- Troubleshooting avançado
