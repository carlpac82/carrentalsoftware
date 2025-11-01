# 🔒 GUIA DE PERSISTÊNCIA - NUNCA PERDER DADOS

## 📋 RESUMO

**PROBLEMA RENDER:**
- Filesystem efêmero (perde ao sleep)
- localStorage do browser não sincroniza entre sessões
- Configurações perdidas após deploy

**SOLUÇÃO IMPLEMENTADA:**
- ✅ **Tudo salvo na base de dados SQLite**
- ✅ **Sincronização automática localStorage ↔ Database**
- ✅ **Backup automático via Git**
- ✅ **Recovery automático após sleep**

---

## 🗄️ DADOS PROTEGIDOS

### 1. **AI Learning Data**
**Tabela:** `ai_learning_data`
**Conteúdo:**
- Ajustes manuais de preços (sliders)
- Histórico de decisões do utilizador
- Padrões aprendidos por grupo/dias/localização

**Endpoints:**
- `POST /api/ai/learning/save` - Salvar novo ajuste
- `GET /api/ai/learning/load` - Carregar histórico

**localStorage:** `priceAIData`

---

### 2. **Automated Price Rules**
**Tabela:** `automated_price_rules`
**Conteúdo:**
- Regras por localização (Faro/Albufeira)
- Estratégias por grupo (B1-N)
- Configuração de dias e meses

**Endpoints:**
- `POST /api/price-automation/rules/save`
- `GET /api/price-automation/rules/load`

**localStorage:** `automatedPriceRules`

---

### 3. **Price Automation Settings**
**Tabela:** `price_automation_settings`
**Conteúdo:**
- Comissão broker
- Dias máximos alternativos
- Suppliers excluídos
- Configurações globais

**Endpoints:**
- `POST /api/price-automation/settings/save`
- `GET /api/price-automation/settings/load`

**localStorage:** `priceAutomationSettings`

---

### 4. **Custom Days**
**Tabela:** `user_settings`
**Conteúdo:**
- Dias personalizados selecionados
- Outras preferências do utilizador

**Endpoints:**
- `POST /api/user-settings/save`
- `GET /api/user-settings/load`

**localStorage:** `customDias`

---

### 5. **User Data**
**Tabela:** `users`
**Conteúdo:**
- Username, password_hash
- Profile pictures (Base64)
- Admin flags

**Endpoints:**
- `/api/user/update-profile`
- Profile pictures salvos como BLOB na DB

---

### 6. **Vehicle Photos & Mappings**
**Tabelas:**
- `vehicle_photos` - Fotos em Base64
- `vehicle_name_overrides` - Mapeamentos de nomes
- `vehicle_images` - Imagens BLOB
- `car_images` - URLs de fotos

**Endpoint:** `/api/vehicles/*`

---

### 7. **Supplier Logos**
**Localização:** `/static/logos/` (150+ ficheiros)
**Backup:** Git repository
**Formato:** PNG, AVIF

**Mapeamento:** Hardcoded em `supplierLogoMap` (index.html, price_automation.html)

---

## 🔄 SINCRONIZAÇÃO AUTOMÁTICA

### Script: `static/js/db-sync.js`

**Funcionamento:**

1. **Page Load:**
   ```javascript
   DOMContentLoaded → loadFromDatabase()
   ```
   - Carrega tudo da DB
   - Aplica ao localStorage
   - Pronto para usar

2. **Alterações:**
   ```javascript
   Cada mudança → localStorage.setItem()
   AI adjustment → saveAIAdjustment()
   ```
   - Imediato no localStorage
   - API call para DB (async)

3. **Auto-Save (30s):**
   ```javascript
   setInterval(saveToDatabase, 30000)
   ```
   - Sincroniza tudo automaticamente
   - Sem intervenção do utilizador

4. **Before Unload:**
   ```javascript
   beforeunload → navigator.sendBeacon()
   ```
   - Garante salvamento final
   - Mesmo ao fechar navegador

---

## 📊 FLUXO DE DADOS

```
┌─────────────────┐
│   USER ACTION   │
└────────┬────────┘
         │
         v
┌─────────────────┐
│  localStorage   │ ← Imediato
└────────┬────────┘
         │
         v (30s ou manual)
┌─────────────────┐
│  DATABASE (DB)  │ ← Persistente
└────────┬────────┘
         │
         v (auto)
┌─────────────────┐
│  GIT BACKUP     │ ← Segurança extra
└─────────────────┘
```

---

## 🚀 DEPLOYMENT NO RENDER

### O que acontece:

1. **Deploy novo código:**
   - Git push → Render rebuild
   - DB é copiada (persiste)
   - localStorage é carregado da DB

2. **Sleep Mode:**
   - Filesystem limpo
   - DB persiste (PostgreSQL ou volume)
   - Ao acordar: tudo volta do DB

3. **Recovery:**
   ```
   Abrir app → db-sync.js carrega → tudo de volta!
   ```

---

## ⚙️ CONFIGURAÇÃO

### Variáveis de Ambiente (.env)

```bash
# Database
DB_PATH=data/carrental.db

# Render (opcional)
DATABASE_URL=postgresql://... # Se usar Postgres

# Session
SECRET_KEY=xxx

# CarJet URLs (28 variáveis)
FARO_1D=...
ALBUFEIRA_1D=...
```

### Arquivo: `main.py`

**Tabelas criadas em `init_db()`:**
- Line 1513-1539: `ai_learning_data`, `user_settings`
- Line 1397-1507: Outras tabelas

**Endpoints:**
- Line 8525-8676: AI & User Settings APIs
- Line 8177-8519: Price Automation APIs

---

## 🧪 TESTES

### Teste de Persistência:

1. **Configurar regras:**
   ```
   /admin/price-automation-settings
   → Configurar grupo B1
   → Salvar
   ```

2. **Verificar salvamento:**
   ```javascript
   // Console do browser
   localStorage.getItem('automatedPriceRules')
   ```

3. **Simular perda:**
   ```javascript
   localStorage.clear()
   ```

4. **Recarregar página:**
   ```
   F5 → db-sync carrega da DB → TUDO DE VOLTA!
   ```

### Teste AI Learning:

1. **Ajustar preço manualmente:**
   ```
   Slider em B1/7d → 25€ → 27€
   ```

2. **Verificar DB:**
   ```sql
   SELECT * FROM ai_learning_data 
   ORDER BY timestamp DESC LIMIT 10;
   ```

3. **Resultado esperado:**
   ```
   group=B1, days=7, new_price=27.00
   ```

---

## 📈 MONITORIZAÇÃO

### Console Logs:

```javascript
[DB-SYNC 1.0.0] Inicializando sincronização automática...
[DB-SYNC] 🔄 Auto-loading from database...
[DB-SYNC] ✓ Loaded customDias from database
[DB-SYNC] ✓ Loaded 15 AI adjustments from database
[DB-SYNC] ✅ Dados carregados da database com sucesso!
[DB-SYNC] 🔄 Auto-saving to database...
[DB-SYNC] ✓ Saved 3 settings to database
[DB-SYNC] ✅ Dados salvos na database com sucesso!
```

### Python Logs:

```python
✅ AI Learning saved: B1/7d = 27.00€
✅ User settings saved: 3 keys for default
❌ Error saving AI learning: [erro]
```

---

## 🔐 SEGURANÇA

### Camadas de Proteção:

1. **Primeira Camada: localStorage**
   - Rápido, imediato
   - Perde ao limpar browser

2. **Segunda Camada: Database**
   - Persistente
   - Sobrevive a sleep/restart

3. **Terceira Camada: Git**
   - Backup completo
   - Histórico de mudanças
   - Recovery total

### Autenticação:

```python
@app.post("/api/ai/learning/save")
async def save_ai_learning(request: Request):
    require_auth(request)  # ✅ Protegido
```

Todos os endpoints requerem autenticação exceto `/api/vehicles/*`.

---

## 📝 MANUTENÇÃO

### Adicionar Novo Dado Persistente:

1. **Adicionar à lista de sync:**
   ```javascript
   // db-sync.js
   const KEYS_TO_SYNC = ['customDias', 'priceAIData', 'NOVO_DADO'];
   ```

2. **Criar endpoint (se específico):**
   ```python
   @app.post("/api/novo-dado/save")
   async def save_novo_dado(request: Request):
       # Implementação
   ```

3. **Usar no frontend:**
   ```javascript
   localStorage.setItem('NOVO_DADO', JSON.stringify(data));
   // db-sync salva automaticamente a cada 30s
   ```

---

## 🎯 CHECKLIST DE DEPLOY

Antes de cada deploy no Render:

- [ ] Commit do código (`git push origin main`)
- [ ] DB incluída no Git (se pequena) ou backup separado
- [ ] Variáveis de ambiente configuradas no Render
- [ ] Testar auto-sync localmente
- [ ] Verificar logs de sincronização
- [ ] Confirmar recovery após restart

---

## 🆘 TROUBLESHOOTING

### Dados não aparecem após reload:

1. **Verificar console:**
   ```
   F12 → Console → procurar "[DB-SYNC]"
   ```

2. **Verificar DB:**
   ```bash
   sqlite3 data/carrental.db
   SELECT COUNT(*) FROM ai_learning_data;
   SELECT COUNT(*) FROM user_settings;
   ```

3. **Forçar reload:**
   ```javascript
   await window.dbSync.load();
   ```

### Sincronização falha:

1. **Verificar autenticação:**
   - Login na aplicação
   - Session cookie válido

2. **Verificar endpoints:**
   ```bash
   curl -X GET http://localhost:8000/api/user-settings/load
   ```

3. **Verificar permissões DB:**
   ```bash
   ls -la data/carrental.db
   ```

---

## 📚 REFERÊNCIAS

**Ficheiros Principais:**
- `main.py` - Backend & APIs
- `static/js/db-sync.js` - Sincronização automática
- `templates/price_automation.html` - Frontend integrado

**Tabelas DB:**
- `ai_learning_data`
- `user_settings`
- `automated_price_rules`
- `price_automation_settings`
- `users`
- `vehicle_photos`
- `vehicle_name_overrides`
- `vehicle_images`
- `car_images`

**Endpoints API:**
- `/api/ai/learning/*`
- `/api/user-settings/*`
- `/api/price-automation/*`
- `/api/vehicles/*`

---

## ✅ CONCLUSÃO

**TUDO ESTÁ PROTEGIDO!**

- ✅ Settings → DB
- ✅ AI Data → DB
- ✅ Custom Days → DB
- ✅ Rules → DB
- ✅ Fotos → DB (Base64)
- ✅ Logos → Git
- ✅ Mapeamentos → Git + DB
- ✅ Users → DB
- ✅ Sincronização → Automática
- ✅ Backup → Git
- ✅ Recovery → Automático

**RENDER READY! 🚀**

Zero perda de dados, mesmo com filesystem efêmero!
