# 🚀 Guia de Instalação - Plugin WordPress Car Rental

## 📋 Passo 1: Criar o Ficheiro ZIP

Vou criar o ZIP automaticamente para ti. Execute no terminal:

```bash
cd ~/CascadeProjects/RentalPriceTrackerPerDay/wordpress-plugin
zip -r car-rental-integration.zip car-rental-integration/
```

**Resultado:** Ficheiro `car-rental-integration.zip` criado (pronto para upload)

---

## 📦 Passo 2: Instalar no WordPress

### Opção A: Via Admin do WordPress (RECOMENDADO)

1. **Aceder ao WordPress Admin**
   - URL: `https://seu-site.com/wp-admin`
   - Login com suas credenciais

2. **Navegar para Plugins**
   - No menu lateral: **Plugins** → **Adicionar Novo**

3. **Upload do Plugin**
   - Clicar em **"Enviar Plugin"** (topo da página)
   - Clicar em **"Escolher arquivo"**
   - Selecionar: `car-rental-integration.zip`
   - Clicar em **"Instalar Agora"**

4. **Ativar**
   - Após instalação, clicar em **"Ativar Plugin"**
   - ✅ Plugin está ativo!

### Opção B: Via FTP (Manual)

1. **Aceder via FTP**
   - Usar FileZilla, Cyberduck ou similar
   - Conectar ao servidor WordPress

2. **Navegar para pasta plugins**
   - Ir para: `/wp-content/plugins/`

3. **Upload da pasta**
   - Extrair o ZIP localmente
   - Fazer upload da pasta `car-rental-integration/` completa

4. **Ativar no WordPress**
   - Admin → Plugins → Ativar "Car Rental Price Integration"

---

## ⚙️ Passo 3: Configurar o Plugin

### 3.1 Aceder às Configurações

- WordPress Admin → **Definições** → **Car Rental API**

### 3.2 Configurar API Connection

**Tab "API Connection":**

1. **API URL:**
   ```
   https://sua-api.onrender.com
   ```
   (Substituir pelo URL da sua API no Render)

2. **API Token** (Opcional):
   - Deixar vazio se a API for pública
   - Ou inserir token se configurou autenticação

3. **Testar Conexão:**
   - Clicar em **"Test API Connection"**
   - Deve aparecer: ✅ **"API connection successful!"**

### 3.3 Configurar Defaults

**Tab "Defaults":**

- **Default Location:** `Albufeira` ou `Faro Airport`
- **Default Days:** `7` (ou outro valor preferido)

### 3.4 Configurar Cache

**Tab "Cache":**

- **Cache Duration:** `3600` segundos (1 hora)
  - Para melhor performance: `7200` (2 horas)
  - Para dados sempre frescos: `300` (5 minutos)

### 3.5 Guardar

- Clicar em **"Save Settings"**
- ✅ Configuração completa!

---

## 🎨 Passo 4: Usar no Website

### Opção 1: Criar Página de Pesquisa

1. **Criar Nova Página**
   - WordPress Admin → **Páginas** → **Adicionar Nova**
   - Título: "Alugar Carro" ou "Car Rental"

2. **Adicionar Shortcode**
   
   **Editor Clássico:**
   ```
   [car_rental_search location="Albufeira" default_days="7"]
   ```

   **Editor Gutenberg:**
   - Adicionar bloco "Shortcode"
   - Colar o código acima

3. **Publicar**
   - Clicar em "Publicar"
   - Ver página publicada

### Opção 2: Mostrar Melhores Ofertas

**Criar página "Promoções" ou "Best Deals":**

```
<h2>🏆 Melhores Ofertas do Dia</h2>

[car_rental_cheapest location="Albufeira" days="7" limit="5"]

<h2>Todos os Veículos Disponíveis</h2>

[car_rental_prices location="Albufeira" days="7" limit="20"]
```

### Opção 3: Página por Categoria

**Criar páginas específicas:**

**Página "Carros Económicos":**
```
[car_rental_prices group="D" location="Albufeira" days="7"]
```

**Página "Carros Automáticos":**
```
[car_rental_prices group="E2" location="Albufeira" days="7"]
```

**Página "SUVs":**
```
[car_rental_prices group="F" location="Albufeira" days="7"]
```

---

## 📱 Exemplos Práticos

### Exemplo 1: Homepage - Widget de Pesquisa

```
<div style="background: #f9fafb; padding: 40px 20px; border-radius: 12px; margin: 30px 0;">
    <h2 style="text-align: center;">Encontre o Seu Carro Ideal</h2>
    <p style="text-align: center; color: #666;">Compare preços de várias empresas em segundos</p>
    
    [car_rental_search layout="horizontal"]
</div>
```

### Exemplo 2: Sidebar - Top 3 Ofertas

```
<h3>💰 Promoções</h3>
[car_rental_cheapest limit="3" layout="table"]
```

### Exemplo 3: Página Completa de Reservas

```
<div class="car-rental-page">
    <section>
        <h1>Aluguer de Carros em Portugal</h1>
        <p>Os melhores preços garantidos. Compare e reserve online.</p>
        
        [car_rental_search location="Albufeira"]
    </section>
    
    <section style="margin-top: 50px;">
        <h2>🏆 Ofertas em Destaque</h2>
        [car_rental_cheapest location="Albufeira" days="7" limit="6"]
    </section>
    
    <section style="margin-top: 50px;">
        <h2>📋 Todos os Veículos Disponíveis</h2>
        [car_rental_prices location="Albufeira" days="7" limit="30" columns="3"]
    </section>
</div>
```

---

## 🎨 Personalizar Design (CSS)

### Adicionar no seu tema (Appearance → Customize → Additional CSS):

```css
/* Alterar cor principal */
.cri-btn-primary {
    background: #e74c3c !important; /* Sua cor */
}

.cri-btn-primary:hover {
    background: #c0392b !important;
}

/* Cards com mais espaçamento */
.cri-results-grid {
    gap: 30px;
}

/* Aumentar tamanho dos preços */
.cri-price-amount {
    font-size: 2rem !important;
    color: #27ae60 !important;
}

/* Customizar formulário de pesquisa */
.cri-search-form {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 30px;
}

.cri-search-form label {
    color: white !important;
}
```

---

## 🔧 Resolução de Problemas

### ❌ Problema: "No results showing"

**Solução:**
1. Verificar API Connection (Settings → Test Connection)
2. Confirmar que API está online (Render dashboard)
3. Limpar cache (Settings → Cache → Clear All Cache)
4. Verificar console do browser (F12) para erros

### ❌ Problema: "API connection failed"

**Solução:**
1. Confirmar URL da API está correto
2. Verificar que API está deployed no Render
3. Testar URL diretamente no browser: `https://sua-api.onrender.com/api/health`
4. Se API requer token, configurar em API Token field

### ❌ Problema: "Página carrega lento"

**Solução:**
1. Aumentar cache duration: 7200 segundos (2 horas)
2. Reduzir limit nos shortcodes: `[car_rental_prices limit="10"]`
3. Considerar upgrade do plano Render (API mais rápida)

### ❌ Problema: "Design não fica bem"

**Solução:**
1. Tema pode estar a conflitar com estilos
2. Adicionar CSS custom (ver secção acima)
3. Usar layout diferente: `layout="horizontal"` ou `layout="table"`
4. Ajustar número de colunas: `columns="2"`

---

## 📞 Shortcodes Disponíveis - Resumo

### 1️⃣ Formulário de Pesquisa
```
[car_rental_search location="Albufeira" default_days="7"]
```

### 2️⃣ Lista de Preços
```
[car_rental_prices location="Albufeira" date="2025-11-01" days="7" limit="20"]
```

### 3️⃣ Melhores Ofertas
```
[car_rental_cheapest location="Albufeira" days="7" limit="5"]
```

**Parâmetros Comuns:**
- `location` - "Albufeira" ou "Aeroporto de Faro"
- `days` - 1, 2, 3, 4, 5, 6, 7, 8, 9, 14, 22, 28, 31, 60
- `group` - B1, B2, D, E1, E2, F, G, J1, J2, L1, L2, M1, M2, N
- `limit` - número de resultados a mostrar
- `layout` - "vertical", "horizontal", "cards", "table"
- `columns` - 1, 2, 3, 4

---

## ✅ Checklist Final

- [ ] Plugin instalado e ativado
- [ ] API URL configurado corretamente
- [ ] Teste de conexão bem-sucedido
- [ ] Cache configurado (3600 segundos)
- [ ] Página de pesquisa criada
- [ ] Shortcodes testados e funcionando
- [ ] Design ajustado ao tema (se necessário)

---

## 🎉 Pronto!

O seu website WordPress agora tem integração completa com o Car Rental API!

**Próximos Passos:**
1. Testar todas as funcionalidades
2. Ajustar design ao seu gosto
3. Criar páginas para diferentes categorias
4. Promover nas redes sociais

**Necessita de mais ajuda?** 
- Consultar tab "Usage Guide" nas definições do plugin
- Ver exemplos no README.md
- Contactar suporte técnico
