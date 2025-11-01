# Guia de Backup e Deploy

## 🔧 Problema Resolvido

Agora você pode **exportar e importar** todas as configurações para não perder dados ao fazer deploy!

## 📤 Antes de Fazer Deploy

### 1. Exportar Configurações

1. Acesse: `http://localhost:8000/admin/car-groups`
2. Faça login: `admin / admin`
3. Clique no botão **📤 Exportar Config** (verde, no header)
4. Ficheiro JSON será baixado automaticamente
5. **Guarde este ficheiro em local seguro!**

### O Que é Exportado

O ficheiro JSON contém:
- ✅ **VEHICLES** - Todos os 124+ veículos categorizados
- ✅ **SUPPLIER_MAP** - Mapeamento de 53 fornecedores
- ✅ **Users** - Todos os utilizadores e passwords
- ✅ **FOTOS** - Todas as fotos dos veículos (em base64)

Exemplo de ficheiro exportado:
```json
{
  "version": "1.1",
  "exported_at": "2025-10-29T17:45:00",
  "vehicles": {
    "fiat 500": "MINI 5 Portas",
    "renault clio": "ECONOMY",
    ...
  },
  "suppliers": {
    "AUP": "Auto Prudente Rent a Car",
    "AVS": "Avis",
    "DOL": "Dollar",
    ...
  },
  "users": [
    {"username": "admin", "password": "hashed_password"}
  ],
  "photos": {
    "peugeot 3008": {
      "data": "/9j/4AAQSkZJRgABAQAA...",
      "content_type": "image/jpeg",
      "url": "https://www.carjet.com/..."
    }
  }
}
```

## 📥 Após Deploy

### 2. Importar Configurações

1. Acesse o servidor novo: `https://seu-servidor.render.com/admin/car-groups`
2. Faça login com credenciais padrão: `admin / admin`
3. Clique no botão **📥 Importar Config** (roxo, no header)
4. Selecione o ficheiro JSON que exportou
5. Aguarde confirmação

### O Que Acontece

- ✅ **Users restaurados** automaticamente na base de dados
- ✅ **Fotos restauradas** automaticamente (base64 → BLOB)
- ✅ **Código gerado** para VEHICLES e SUPPLIER_MAP
- ✅ **Modal aparece** com código pronto para copiar

### 3. Aplicar o Código

1. Copie o código do modal (botão **📋 Copiar Código**)
2. Abra `carjet_direct.py`
3. Substitua o dicionário `VEHICLES` e `SUPPLIER_MAP`
4. Commit e push:
   ```bash
   git add carjet_direct.py
   git commit -m "restore: importar configurações de backup"
   git push origin main
   ```

## 🔄 Workflow Completo

### Desenvolvimento Local → Deploy

```bash
# 1. Exportar configurações
Localhost → 📤 Exportar Config → carrental_config_20251029.json

# 2. Fazer deploy
git push origin main
# Render faz deploy automático

# 3. Importar no servidor
Servidor → 📥 Importar Config → selecionar carrental_config_20251029.json

# 4. Users já restaurados! VEHICLES code gerado
# 5. Copiar e colar código em carjet_direct.py
# 6. Commit e push novamente
```

## 🚨 Importante

### Fazer Backup Regular

- **Antes de cada deploy importante**
- **Após adicionar muitos veículos novos**
- **Antes de mudanças grandes no código**

### Guardar Ficheiros JSON

- Guardar em repositório privado (GitLab, Bitbucket)
- Guardar em Google Drive / Dropbox
- **NÃO** commitar no GitHub público (contém passwords)

### Segurança

Os ficheiros JSON contêm:
- ⚠️ **Passwords de users** (hashed)
- ⚠️ **Todas as configurações**

Trate como **informação sensível**!

## 📋 Checklist de Deploy

- [ ] Exportar configurações (`📤 Exportar Config`)
- [ ] Guardar ficheiro JSON em local seguro
- [ ] Fazer deploy (`git push`)
- [ ] Aguardar deploy completar
- [ ] Importar configurações no servidor (`📥 Importar Config`)
- [ ] Verificar users restaurados (login funciona)
- [ ] Copiar código VEHICLES gerado
- [ ] Colar em `carjet_direct.py`
- [ ] Commit e push novamente
- [ ] Testar funcionalidade completa

## 🎯 Botões na Interface

No header da página `/admin/car-groups`:

```
┌─────────────────────────────────────────────────────┐
│ [📤 Exportar Config] [📥 Importar Config] [💾 ...] │
│     (verde)              (roxo)                      │
└─────────────────────────────────────────────────────┘
```

- **📤 Exportar Config** - Download de ficheiro JSON
- **📥 Importar Config** - Upload de ficheiro JSON
- **💾 Exportar VEHICLES** - Só dicionário VEHICLES (como antes)

## ❓ FAQ

### Perdi as configurações no deploy. E agora?

Se não fez backup antes:
- Users perdidos → recriar manualmente
- VEHICLES perdidos → recriar manualmente (muito trabalho!)

**Solução:** Sempre exportar ANTES de deploy!

### Posso editar o ficheiro JSON manualmente?

Sim! É um ficheiro JSON normal. Pode:
- Adicionar veículos novos
- Corrigir categorias
- Adicionar users

### O ficheiro JSON funciona entre versões diferentes?

Sim, desde que a estrutura seja mantida. O sistema valida na importação.

### Quantos backups devo guardar?

Recomendação:
- **Mínimo:** 1 backup recente
- **Ideal:** 3-5 backups (últimos dias/semanas)
- **Melhor:** Backup automático diário

## 🔗 Links Úteis

- Localhost: http://localhost:8000/admin/car-groups
- Render Deploy: https://dashboard.render.com/
- API Export: http://localhost:8000/api/export/config
- API Import: http://localhost:8000/api/import/config (POST)

---

**Última atualização:** 29 Out 2025
**Versão:** 1.0
