# 🔐 COMO FAZER O PRIMEIRO LOGIN

## ❌ PROBLEMA: "Não deixa fazer o login"

**Causa:** A base de dados SQLite está vazia (sem users criados).

---

## ✅ SOLUÇÃO: Criar Primeiro Admin User

### **PASSO 1: Aceder ao Setup**

```
https://carrental-final.onrender.com/setup-admin
```

### **PASSO 2: Preencher o Formulário**

- **Username:** `admin` (ou outro nome)
- **Password:** `<tua password forte>`
- **Email:** `admin@example.com` (ou teu email)

### **PASSO 3: Criar Admin**

Clicar no botão: **"Create Admin User"**

### **PASSO 4: Login**

Depois de criar, vais ver:
```
✅ Admin User Created!
Username: admin
```

Clicar em **"Go to Login"** e fazer login com:
- Username: `admin`
- Password: `<a password que definiste>`

---

## 🔒 SEGURANÇA

- Este endpoint **só funciona UMA VEZ**
- Depois de criar o primeiro user, fica desativado
- Se tentares aceder outra vez, vais ver:
  ```
  ❌ Setup Already Complete
  Admin user already exists.
  ```

---

## 📋 DEPOIS DE CRIAR O ADMIN

### **1. Aceder à aplicação:**
```
https://carrental-final.onrender.com/
```

### **2. Fazer login:**
- Username: `admin`
- Password: `<tua password>`

### **3. Verificar features:**
- ✅ `/admin/users` → Link "Vehicles"
- ✅ `/admin/car-groups` → Tabela completa
- ✅ `/admin/settings` → Price adjustments

### **4. Criar mais users:**
- Ir para `/admin/users`
- Clicar **"+ New User"**
- Preencher formulário
- Marcar **"Is Admin"** se necessário

---

## 🆘 TROUBLESHOOTING

### **Problema: "Setup Already Complete" mas não sei a password**

**Solução 1: Criar novo deployment**
1. Render Dashboard → Manual Deploy → Clear build cache
2. Isto cria nova base de dados vazia
3. Voltar a `/setup-admin`

**Solução 2: Aceder à base de dados**
1. Render Dashboard → Shell
2. `sqlite3 app.db`
3. `DELETE FROM users;`
4. Voltar a `/setup-admin`

### **Problema: Login falha mesmo com password correta**

Verificar:
1. **SECRET_KEY** está configurado nas Environment Variables
2. Browser não está a bloquear cookies
3. Hard refresh (Cmd+Shift+R)

---

## ✅ RESUMO RÁPIDO

```bash
1. https://carrental-final.onrender.com/setup-admin
2. Username: admin
3. Password: <tua password forte>
4. Create Admin User
5. Go to Login
6. Login com admin + password
7. ✅ Pronto!
```

---

**🎯 Depois de fazer isto, podes começar a usar a aplicação normalmente!**
