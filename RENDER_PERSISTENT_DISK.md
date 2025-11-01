# 🔧 CONFIGURAR DISCO PERSISTENTE NO RENDER

## ❌ PROBLEMA
Quando fazes **redeploy** no Render, a base de dados SQLite é **APAGADA** e perdes:
- ✅ Users e passwords
- ✅ Car Groups (Vehicles)
- ✅ Activity Log
- ✅ Todas as configurações

**Tens que criar users novamente em cada deploy!**

---

## ✅ SOLUÇÃO: RENDER DISK (Persistent Storage)

O Render oferece **discos persistentes** que mantêm os dados entre deploys.

---

## 📋 PASSO A PASSO (5 MINUTOS)

### **1️⃣ Render Dashboard**
```
https://dashboard.render.com/
```

### **2️⃣ Selecionar Service**
Clicar em: **carrental-final**

### **3️⃣ Menu Lateral → "Disks"**
No menu lateral esquerdo, clicar em: **"Disks"**

### **4️⃣ Add Disk**
Clicar no botão: **"+ Add Disk"**

### **5️⃣ Configurar Disk**

Preencher os campos:

#### **Name:**
```
rental-tracker-data
```

#### **Mount Path:**
```
/app/data
```

#### **Size:**
```
1 GB
```
*(É gratuito até 1GB no plano Free)*

### **6️⃣ Save Changes**
Clicar em: **"Add Disk"** ou **"Save"**

⚠️ **O Render vai fazer REDEPLOY automático!**

---

## 🔍 VERIFICAR CONFIGURAÇÃO

### **Logs Esperados:**
```
📊 Initializing database tables...
   ✅ app_settings table ready
   ✅ users table ready
   ✅ car_groups table ready
   ✅ activity_log table ready
✅ All database tables initialized!
✅ Database location: /app/data/data.db
```

### **Testar:**
1. Criar users em `/setup-users`
2. Fazer login
3. **Fazer novo Manual Deploy**
4. Fazer login novamente com **mesma password**
5. ✅ **Deve funcionar!** (users não foram apagados)

---

## 📊 COMO FUNCIONA

### **Antes (SEM Disk Persistente):**
```
Deploy 1:
- Criar users
- Login OK ✅

Deploy 2 (redeploy):
- Base de dados APAGADA ❌
- Users desaparecem ❌
- Tens que criar novamente ❌
```

### **Depois (COM Disk Persistente):**
```
Deploy 1:
- Criar users
- Login OK ✅
- Data guardada em /app/data/data.db (disco persistente)

Deploy 2 (redeploy):
- /app apagado (código novo)
- /app/data MANTIDO ✅ (disco persistente)
- Base de dados INTACTA ✅
- Login OK com mesma password ✅

Deploy 3, 4, 5... (redeплoys):
- Users SEMPRE mantidos ✅
- Passwords SEMPRE mantidas ✅
- Nada é apagado ✅
```

---

## ⚠️ IMPORTANTE

### **Primeira Configuração:**
Quando adicionares o disco pela primeira vez:
1. Render faz redeploy
2. Base de dados vai estar **vazia** (normal)
3. Criar users em `/setup-users`
4. **A partir daí, users são mantidos em TODOS os deploys!**

### **Backup Manual (Opcional):**
Se quiseres fazer backup da base de dados:

```bash
# No Render Shell
cd /app/data
ls -lh data.db
# Download via Render Shell ou SFTP
```

---

## 🎯 RESULTADO FINAL

| Ação | Antes | Depois |
|------|-------|--------|
| **Redeploy** | ❌ Perde users | ✅ Mantém users |
| **Manual Deploy** | ❌ Perde passwords | ✅ Mantém passwords |
| **Clear Cache** | ❌ Apaga tudo | ✅ Mantém base de dados |
| **Novo código** | ❌ Reset completo | ✅ Atualiza código, mantém dados |

---

## 💰 CUSTO

- **1 GB**: **GRÁTIS** (incluído no plano Free)
- **Mais de 1 GB**: Pago (não precisas)

A base de dados SQLite com users, car groups e logs ocupa **menos de 10 MB**.
**1 GB é mais que suficiente!**

---

## 🆘 TROUBLESHOOTING

### **Disk não aparece nas opções:**
- Certificar que estás no service correto
- Render Free tier suporta disks (verificado)

### **Erro "Mount path already exists":**
- Mudar mount path para `/app/persistent-data`
- Atualizar variável `DATA_DIR` para o mesmo path

### **Base de dados continua a ser apagada:**
- Verificar que `DATA_DIR=/app/data` está nas Environment Variables
- Verificar que disk está montado em `/app/data`
- Ver logs para confirmar path da base de dados

---

## ✅ CHECKLIST

```
[ ] Dashboard Render → Service carrental-final
[ ] Menu lateral → Disks
[ ] Add Disk
[ ] Name: rental-tracker-data
[ ] Mount Path: /app/data
[ ] Size: 1 GB
[ ] Save → Aguardar redeploy
[ ] Criar users em /setup-users
[ ] Login OK
[ ] Fazer novo Manual Deploy (testar)
[ ] Login novamente com mesma password
[ ] ✅ SUCESSO - Users mantidos!
```

---

## 📝 NOTAS

- O disco é **específico deste service**
- Não é partilhado entre services
- Persiste entre deploys mas **não entre services diferentes**
- Se apagares o service, o disco também é apagado

---

**🎯 CONFIGURA O DISK AGORA E NUNCA MAIS VAIS TER QUE CRIAR USERS EM CADA DEPLOY!** 🚀
