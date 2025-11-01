# 🚀 MIGRAR PARA NOVO REPOSITÓRIO

## 📋 PASSO 1: CRIAR REPOSITÓRIO NO GITHUB

1. Aceder a: https://github.com/new
2. **Repository name:** `carrental-Final`
3. **Description:** `Car Rental Price Tracker - Production Version`
4. **Visibility:** Private ou Public (à tua escolha)
5. ⚠️ **IMPORTANTE:** NÃO selecionar:
   - ❌ Add a README file
   - ❌ Add .gitignore
   - ❌ Choose a license
6. Clicar **"Create repository"**

---

## 📋 PASSO 2: FAZER PUSH DO CÓDIGO ATUAL

Depois de criar o repo no GitHub, executar estes comandos:

```bash
cd /Users/filipepacheco/CascadeProjects/RentalPriceTrackerPerDay

# Adicionar novo remote
git remote add new-repo https://github.com/carlpac82/carrental-Final.git

# Fazer push de TUDO para o novo repo
git push new-repo main

# (Opcional) Remover remote antigo e renomear
git remote remove origin
git remote rename new-repo origin
```

---

## 📋 PASSO 3: ATUALIZAR RENDER

### **Opção A: Criar Novo Service (RECOMENDADO)**

1. Render Dashboard → **"New +"** → **"Web Service"**
2. **Connect Repository:** `carlpac82/carrental-Final`
3. **Name:** `cartracker-final` (ou outro nome)
4. **Environment:** `Docker`
5. **Branch:** `main`
6. **Plan:** Free ou Paid

#### **Environment Variables (COPIAR DO SERVICE ANTIGO):**

No service antigo:
1. Settings → Environment → Copy all variables

No service novo:
1. Settings → Environment → Add variables

**Variáveis críticas:**
- `SECRET_KEY`
- `APP_PASSWORD`
- `CARJET_PRICE_ADJUSTMENT_PCT`
- `CARJET_PRICE_OFFSET_EUR`
- Todas as URLs de Faro/Albufeira (FARO_7D, etc.)

#### **Advantages:**
✅ Fresh start - sem cache
✅ Mantém service antigo como backup
✅ Pode testar antes de desativar antigo

---

### **Opção B: Atualizar Service Existente**

1. Render Dashboard → Service `cartracker-6twv`
2. **Settings** → **Build & Deploy**
3. Secção **"GitHub"**
4. Clicar **"Disconnect"**
5. Clicar **"Connect Repository"**
6. Escolher: `carlpac82/carrental-Final`
7. Branch: `main`
8. **Save Changes**
9. Ir para **"Manual Deploy"** → **"Clear build cache & deploy"**

#### **Advantages:**
✅ Mantém mesmo URL
✅ Não precisa reconfigurar environment variables

---

## ✅ PASSO 4: VERIFICAR DEPLOY

Depois do deploy terminar, verificar nos logs:

```
========================================
🚀 APP STARTUP - VERSION: 2025-01-28-23-31-MANUAL-DEPLOY-REQUIRED
📦 Features: Vehicles Management, Automatic Field, Blocklist Removed
========================================
```

### **Se a mensagem aparecer:**
✅ Deploy bem-sucedido!

1. Aceder à aplicação
2. Login como admin
3. Verificar `/admin/users` → Link "Vehicles"
4. Verificar `/admin/car-groups` → Tabela completa
5. Pesquisar Faro 7 dias → 60+ carros

---

## 🔧 TROUBLESHOOTING

### **Erro: Permission Denied**
```bash
git push new-repo main
# Se pedir password:
# 1. Ir a GitHub → Settings → Developer settings → Personal access tokens
# 2. Generate new token (classic)
# 3. Scopes: repo (full control)
# 4. Usar token como password
```

### **Render não conecta ao repo:**
- Verificar se o repo é Private → Render precisa de permissão
- Render Settings → GitHub → Re-authorize

---

## 📊 COMPARAÇÃO DE OPÇÕES

| Aspecto | Novo Service | Atualizar Existente |
|---------|--------------|---------------------|
| **Cache limpo** | ✅ Garantido | ⚠️ Depende de "Clear cache" |
| **URL** | ❌ Novo URL | ✅ Mantém URL atual |
| **Env Variables** | ❌ Reconfigurar | ✅ Mantém configuração |
| **Backup** | ✅ Service antigo fica | ❌ Sobrescreve |
| **Tempo** | ~10 min | ~5 min |

---

## 🎯 RECOMENDAÇÃO

**Para esta situação (cache problemático):**
→ **OPÇÃO A: CRIAR NOVO SERVICE**

Razões:
1. ✅ Garante cache limpo 100%
2. ✅ Service antigo fica como backup
3. ✅ Podes testar antes de desativar o antigo
4. ✅ Fresh start resolve problemas de deploy

Depois de confirmar que funciona:
- Desativar service antigo
- Ou apagar se não for necessário

---

## 📝 NOTAS

- Toda a base de dados SQLite será criada de novo
- Precisas criar utilizadores admin novamente
- Car groups serão criados automaticamente quando fizerem scraping
- Price adjustments precisam ser configurados novamente

---

**🚀 BOA SORTE COM O NOVO DEPLOY!**
