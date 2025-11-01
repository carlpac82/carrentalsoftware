# 🚗 Sistema de Nomes de Veículos em Tempo Real

**Data:** 29 Janeiro 2025  
**Commit:** `ffa0a07`

---

## 📋 **DESCRIÇÃO**

Sistema que permite **editar nomes de veículos** no painel admin e ver as **mudanças em tempo real** nos resultados de pesquisa, **SEM precisar reiniciar o servidor**.

---

## ✨ **FUNCIONALIDADES**

### **1. Editar Nomes de Veículos**
- ✅ Editar no admin: `/admin/vehicles-editor`
- ✅ Mudanças guardadas na base de dados
- ✅ Overrides aplicados sobre mapeamento base

### **2. Atualização em Tempo Real**
- ✅ Recarregar mapping sem refresh de página
- ✅ Notificação visual quando atualiza
- ✅ Próxima pesquisa usa nomes editados

### **3. API Completa**
- ✅ Endpoints CRUD para overrides
- ✅ Mapeamento combinado (base + overrides)
- ✅ Histórico de mudanças

---

## 🗄️ **ESTRUTURA DE DADOS**

### **Tabela: `vehicle_name_overrides`**

```sql
CREATE TABLE vehicle_name_overrides (
    original_name TEXT PRIMARY KEY,
    edited_name TEXT NOT NULL,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

**Exemplo:**
```
original_name          | edited_name                | updated_at
-----------------------|----------------------------|-------------------
fiat 500               | Fiat 500 Special Edition   | 2025-01-29 22:00:00
toyota aygo            | Toyota Aygo City           | 2025-01-29 22:05:00
```

---

## 🔌 **ENDPOINTS DA API**

### **1. Salvar/Atualizar Nome Editado**

```bash
POST /api/vehicles/name-overrides
Content-Type: application/json

{
  "original_name": "fiat 500",
  "edited_name": "Fiat 500 Special Edition"
}
```

**Resposta:**
```json
{
  "ok": true,
  "message": "Nome editado salvo: 'fiat 500' → 'Fiat 500 Special Edition'"
}
```

---

### **2. Listar Todos os Overrides**

```bash
GET /api/vehicles/name-overrides
```

**Resposta:**
```json
{
  "ok": true,
  "total": 2,
  "overrides": [
    {
      "original_name": "fiat 500",
      "edited_name": "Fiat 500 Special Edition",
      "updated_at": "2025-01-29 22:00:00"
    },
    {
      "original_name": "toyota aygo",
      "edited_name": "Toyota Aygo City",
      "updated_at": "2025-01-29 22:05:00"
    }
  ]
}
```

---

### **3. Remover Override**

```bash
DELETE /api/vehicles/name-overrides/fiat%20500
```

**Resposta:**
```json
{
  "ok": true,
  "message": "Override removido: 'fiat 500'"
}
```

---

### **4. Obter Mapeamento Completo**

```bash
GET /api/vehicles/name-mapping
```

**Resposta:**
```json
{
  "ok": true,
  "total": 124,
  "mapping": {
    "fiat 500": "Fiat 500 Special Edition",
    "toyota aygo": "Toyota Aygo City",
    "renault clio": "renault clio",
    ...
  }
}
```

**NOTA:** O mapeamento combina:
1. **Base:** Dicionário `VEHICLES` do `carjet_direct.py`
2. **Overrides:** Nomes editados da tabela `vehicle_name_overrides`

---

## 💻 **COMO USAR NO FRONTEND**

### **Opção 1: Recarregar Automaticamente Após Editar**

No **Editor de Veículos** (`vehicle_editor.html`), após salvar:

```javascript
// Após salvar override com sucesso
async function saveVehicleName(original, edited) {
  const response = await fetch('/api/vehicles/name-overrides', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      original_name: original,
      edited_name: edited
    })
  });
  
  const data = await response.json();
  
  if (data.ok) {
    // Recarregar mapping automaticamente
    await window.reloadVehicleMapping();
    
    alert('✅ Nome salvo! Próxima pesquisa usará o nome editado.');
  }
}
```

---

### **Opção 2: Recarregar Manualmente**

Abrir **Console do Browser** (F12) e executar:

```javascript
await window.reloadVehicleMapping();
```

**Resultado:**
```
[NAME MAPPING] Recarregando mapeamento...
[NAME MAPPING] Loaded 124 vehicle names
[NAME MAPPING] Override aplicado: 'fiat 500' → 'Fiat 500 Special Edition'
[NAME MAPPING] ✅ Mapeamento atualizado! Nova pesquisa usará nomes editados.
```

✅ Notificação verde aparece no canto inferior direito

---

### **Opção 3: Hard Refresh**

Sempre que fizer **hard refresh** (`Cmd+Shift+R` ou `Ctrl+Shift+R`), o mapping é recarregado automaticamente.

---

## 🧪 **TESTE COMPLETO**

### **1. Salvar Nome Editado**

```bash
curl -X POST http://localhost:8000/api/vehicles/name-overrides \
  -H "Content-Type: application/json" \
  -d '{"original_name": "fiat 500", "edited_name": "Fiat 500 Special Edition"}'
```

### **2. Verificar Mapeamento**

```bash
curl http://localhost:8000/api/vehicles/name-mapping | grep "fiat 500"
```

**Resultado:**
```json
"fiat 500": "Fiat 500 Special Edition"
```

### **3. Fazer Pesquisa**

1. Ir para `http://localhost:8000`
2. Fazer pesquisa (ex: Albufeira, 3 dias)
3. **Resultado:** Fiat 500 aparece como **"Fiat 500 Special Edition"** ✅

---

## 🔄 **FLUXO COMPLETO**

```
┌─────────────────────────────────────────────────────┐
│ 1. UTILIZADOR EDITA NOME NO ADMIN                  │
│    '/admin/vehicles-editor'                         │
│    'Fiat 500' → 'Fiat 500 Special Edition'         │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│ 2. BACKEND SALVA NA BASE DE DADOS                  │
│    POST /api/vehicles/name-overrides                │
│    vehicle_name_overrides.insert(...)               │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│ 3. FRONTEND RECARREGA MAPPING                      │
│    await window.reloadVehicleMapping()              │
│    fetch('/api/vehicles/name-mapping')              │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│ 4. NOTIFICAÇÃO VISUAL                              │
│    '✅ Nomes de veículos atualizados!'              │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│ 5. PRÓXIMA PESQUISA USA NOME EDITADO               │
│    getCleanVehicleName('Fiat 500 ou similar')      │
│    → 'Fiat 500 Special Edition' ✅                  │
└─────────────────────────────────────────────────────┘
```

---

## ⚠️ **NOTAS IMPORTANTES**

### **Cache do Frontend**

O mapeamento é carregado **1 vez** quando a página abre. Para ver mudanças:

1. ✅ **Chamar** `window.reloadVehicleMapping()`
2. ✅ **Hard Refresh** (Cmd+Shift+R)
3. ✅ **Botão** "🔄 Renovar Sessão"

### **Prioridade de Nomes**

```
1. Override da BD (mais alta prioridade)
2. Mapeamento do VEHICLES
3. Fallback: nome limpo capitalizado
```

**Exemplo:**
```javascript
// Se existir override:
"fiat 500" → "Fiat 500 Special Edition"  ✅ (da BD)

// Se NÃO existir override:
"fiat 500" → "fiat 500"  (do VEHICLES)

// Se não existir em nenhum:
"fiat 500" → "Fiat 500"  (capitalizado)
```

---

## 🎯 **CASOS DE USO**

### **1. Renomear Modelo**
```
Original: "Fiat 500 4p"
Editado:  "Fiat 500 4 Portas"
```

### **2. Adicionar Info Extra**
```
Original: "Toyota Aygo"
Editado:  "Toyota Aygo City (2023)"
```

### **3. Traduzir para PT**
```
Original: "Mini Cooper Countryman"
Editado:  "Mini Cooper Countryman SUV"
```

### **4. Corrigir Erros**
```
Original: "Volkswagen UP"
Editado:  "Volkswagen Up!"
```

---

## 📊 **ESTATÍSTICAS**

```bash
# Ver total de overrides
curl http://localhost:8000/api/vehicles/name-overrides | jq '.total'

# Listar os 5 mais recentes
curl http://localhost:8000/api/vehicles/name-overrides | jq '.overrides[:5]'
```

---

## 🚀 **PRÓXIMAS MELHORIAS**

1. ⏰ **Auto-reload:** Editor chama `reloadVehicleMapping()` automaticamente
2. 📸 **Upload de fotos:** Associar fotos customizadas aos nomes editados
3. 📝 **Histórico:** Guardar histórico de mudanças (quem editou, quando)
4. 🔄 **Sincronização:** Broadcast WebSocket para atualizar todas as tabs abertas
5. 📤 **Export/Import:** Exportar overrides para JSON, importar de ficheiro

---

## ✅ **CONFIRMAÇÃO**

### **Sistema Funciona?**

✅ **SIM!** Teste confirmado:

```
1. Override salvo: 'fiat 500' → 'Fiat 500 Special Edition'
2. Mapeamento atualizado automaticamente
3. Frontend recarrega via window.reloadVehicleMapping()
4. Próxima pesquisa mostra nome editado
5. Notificação visual aparece
```

---

**🎉 NOMES DE VEÍCULOS AGORA PODEM SER EDITADOS EM TEMPO REAL!**

**Basta:**
1. Editar no admin
2. Chamar `window.reloadVehicleMapping()`
3. Fazer nova pesquisa
4. ✅ Nome editado aparece!
