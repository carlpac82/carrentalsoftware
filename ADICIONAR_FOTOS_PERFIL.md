# 📸 Como Adicionar Fotos de Perfil

## 🎯 Fotos Necessárias:

Precisas de adicionar 2 fotos na pasta `static/profiles/`:

1. **carlpac82.png** - Foto do Filipe Pacheco
2. **dprudente.png** - Foto do Daniell Prudente

---

## 📋 Passo a Passo:

### 1️⃣ **Preparar as Fotos**
- Formato: **PNG**
- Nomes exatos:
  - `carlpac82.png`
  - `dprudente.png`
- Tamanho recomendado: 200x200px (ou maior, será redimensionado automaticamente)

### 2️⃣ **Adicionar ao Projeto**
```bash
# Navegar para a pasta do projeto
cd /Users/filipepacheco/CascadeProjects/RentalPriceTrackerPerDay

# Copiar as fotos para a pasta profiles
cp /caminho/para/carlpac82.png static/profiles/
cp /caminho/para/dprudente.png static/profiles/
```

### 3️⃣ **Commit e Push**
```bash
git add static/profiles/carlpac82.png static/profiles/dprudente.png
git commit -m "feat: Adicionar fotos de perfil dos utilizadores"
git push origin main
```

### 4️⃣ **Aguardar Deploy**
- O Render fará deploy automático (~5-10 min)
- As fotos aparecem nos perfis após o deploy

---

## 👥 Utilizadores Criados:

### **admin** / **carlpac82** (mesma pessoa)
- 👤 Nome: Filipe Pacheco
- 📧 Email: carlpac82@hotmail.com
- 📱 Telemóvel: +351 964 805 750
- 🖼️ Foto: `carlpac82.png`
- 🔑 Admin: **Sim**
- 🔐 Passwords:
  - admin: (usa APP_PASSWORD do .env)
  - carlpac82: `Frederico.2025`

### **dprudente**
- 👤 Nome: Daniell Prudente
- 📧 Email: comercial.autoprudente@gmail.com
- 📱 Telemóvel: +351 911 747 478
- 🖼️ Foto: `dprudente.png`
- 🔑 Admin: Não
- 🔐 Password: `dprudente`

---

## ✅ Verificação:

Depois do deploy, acede a:
- **https://cartracker-6twv.onrender.com/login**

Faz login com qualquer utilizador e verifica se a foto aparece!

---

## 🚨 Troubleshooting:

### Foto não aparece?
1. Verifica se o nome do ficheiro está correto (case-sensitive!)
2. Verifica se está na pasta `static/profiles/`
3. Faz refresh da página (Ctrl+F5)
4. Verifica os logs do Render

### Utilizador não existe?
- Os utilizadores são criados automaticamente no primeiro startup
- Verifica os logs do Render: procura por `[INIT] Created user:`

---

## 📝 Notas:

- Os utilizadores **persistem** entre restarts
- As fotos são servidas de `static/profiles/`
- Se quiseres mudar a foto, basta substituir o ficheiro e fazer push
