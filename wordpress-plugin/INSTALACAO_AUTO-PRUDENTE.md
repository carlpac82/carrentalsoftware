# 🔒 Instalação no auto-prudente.com - Página Privada

## 🎯 Objetivo
Integrar Car Rental API no **https://auto-prudente.com** numa **página escondida** que:
- ✅ **NÃO apareça no Google**
- ✅ **NÃO afete a estrutura atual do website**
- ✅ **Seja apenas para uso interno/administração**
- ✅ **Não apareça nos menus ou pesquisas**

---

## 📦 Método 1: Página Protegida por Password (MAIS SIMPLES)

### Passo 1: Instalar Plugin
1. WordPress Admin → **Plugins** → **Adicionar Novo**
2. Upload: `car-rental-integration.zip`
3. Ativar plugin
4. **Definições** → **Car Rental API**
5. Configurar API URL: `https://sua-api.onrender.com`

### Passo 2: Criar Página Escondida

1. **Páginas** → **Adicionar Nova**

2. **Título da Página:**
   ```
   Gestão Interna - Preços
   ```

3. **URL Slug (importante!):**
   Escolher URL difícil de adivinhar:
   - ✅ `admin-car-prices-2024`
   - ✅ `internal-pricing-management`
   - ✅ `gestao-precos-interno`
   
   **Resultado:** `https://auto-prudente.com/admin-car-prices-2024`

4. **Conteúdo da Página (Editor HTML):**
   ```html
   <!-- NOINDEX - NÃO INDEXAR NO GOOGLE -->
   <meta name="robots" content="noindex, nofollow">
   <meta name="googlebot" content="noindex, nofollow">
   
   <div style="background: #fef3cd; border: 2px solid #ffc107; padding: 20px; border-radius: 8px; margin-bottom: 30px;">
       <strong>⚠️ PÁGINA PRIVADA - USO INTERNO</strong>
       <p>Esta página não está indexada no Google e é protegida por senha.</p>
   </div>
   
   <h2>🔍 Pesquisa de Preços</h2>
   [car_rental_search location="Albufeira" default_days="7"]
   
   <h2 style="margin-top: 50px;">🏆 Melhores Ofertas</h2>
   [car_rental_cheapest location="Albufeira" days="7" limit="5"]
   ```

5. **Configurar Visibilidade:**
   
   **Sidebar Direita → Visibilidade:**
   - Clicar em **"Editar"**
   - Selecionar: **"Protegida por senha"**
   - Definir senha: `AutoPrudente2024` (ou outra à sua escolha)
   - Clicar **"OK"**

6. **Publicar**

7. **Testar:**
   - Abrir: `https://auto-prudente.com/admin-car-prices-2024`
   - Deve pedir senha
   - Após inserir senha, mostra a página

### Passo 3: Garantir que NÃO Aparece no Google

**Opção A: Se usa Yoast SEO ou Rank Math**

1. Na página criada, scroll down até secção do SEO plugin
2. Configurar:
   - **Allow search engines to show in search results:** `No`
   - **Meta Robots:** `noindex, nofollow`
   - **Canonical URL:** Deixar vazio
   - **Include in sitemap:** `No`

**Opção B: Adicionar ao robots.txt**

1. **SEO** → **Tools** → **File Editor** (Yoast)
2. Ou criar/editar `robots.txt` na raiz do WordPress
3. Adicionar:
   ```
   User-agent: *
   Disallow: /admin-car-prices-2024
   Disallow: /gestao-precos-interno
   ```

**Opção C: Header Manual**

Adicionar no `functions.php` do tema child:
```php
// Bloquear indexação da página privada
add_action('wp_head', function() {
    if (is_page('admin-car-prices-2024')) {
        echo '<meta name="robots" content="noindex, nofollow">' . "\n";
        echo '<meta name="googlebot" content="noindex, nofollow">' . "\n";
    }
});
```

### Passo 4: Esconder dos Menus

**Garantir que página não aparece em:**
- ✅ Menus de navegação (não adicionar)
- ✅ Pesquisa interna do site
- ✅ Listagens de páginas
- ✅ Sitemap XML

**Para esconder da pesquisa interna:**

Adicionar ao `functions.php`:
```php
// Esconder página da pesquisa interna
add_filter('pre_get_posts', function($query) {
    if (!is_admin() && $query->is_search) {
        $query->set('post__not_in', array(123)); // ID da página
    }
    return $query;
});
```

*(Substituir `123` pelo ID real da página)*

---

## 🔐 Método 2: Página Apenas para Admins (MAIS SEGURO)

### Template Personalizado

1. **Copiar ficheiro:**
   - Copiar `page-admin-prices.php` para pasta do tema:
   - Localização: `/wp-content/themes/SEU-TEMA/page-admin-prices.php`

2. **Criar Nova Página:**
   - **Páginas** → **Adicionar Nova**
   - **Título:** `Admin - Gestão de Preços`
   - **URL:** `admin-prices-internal`
   
3. **Selecionar Template:**
   - **Atributos da Página** → **Template**
   - Escolher: **"Admin Car Prices (Hidden)"**

4. **Publicar**

5. **Acesso:**
   - Página só acessível se **logged in como admin**
   - Redirect automático para login se não autenticado
   - NÃO indexada pelo Google
   - URL: `https://auto-prudente.com/admin-prices-internal`

---

## 🚫 Método 3: Subdomain Separado (ISOLADO TOTAL)

Se quiser **isolamento completo** do site principal:

### Criar Subdomain

1. **No cPanel ou Hosting:**
   - Criar subdomain: `admin.auto-prudente.com`
   - Apontar para pasta separada

2. **Instalar WordPress Fresh:**
   - Instalação limpa só para administração
   - Instalar plugin Car Rental
   - Usar credenciais diferentes

3. **Bloquear Acesso Público:**
   
   Adicionar `.htaccess` no subdomain:
   ```apache
   # Bloquear acesso público
   AuthType Basic
   AuthName "Área Restrita"
   AuthUserFile /caminho/.htpasswd
   Require valid-user
   
   # Bloquear bots
   <IfModule mod_rewrite.c>
       RewriteEngine On
       RewriteCond %{HTTP_USER_AGENT} (google|bing|yahoo) [NC]
       RewriteRule .* - [F,L]
   </IfModule>
   ```

4. **Criar .htpasswd:**
   ```bash
   htpasswd -c .htpasswd admin
   # Criar senha
   ```

**Vantagens:**
- ✅ Totalmente separado do site principal
- ✅ Zero impacto no site público
- ✅ Pode ter design diferente
- ✅ Credenciais separadas

---

## 🎨 Personalização (Sem Afetar Site Principal)

### CSS Específico da Página

Adicionar no **Customizer** → **CSS Adicional**:

```css
/* APENAS para página admin de preços */
.page-id-123 .site-header,
.page-id-123 .site-footer {
    display: none !important; /* Esconder header/footer */
}

.page-id-123 .entry-content {
    max-width: 100%;
    padding: 0;
}

/* Estilos do plugin */
.page-id-123 .cri-search-form {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 30px;
}
```

*(Substituir `123` pelo ID real da página)*

---

## ✅ Checklist de Segurança

Verificar antes de finalizar:

- [ ] Página protegida por senha OU requer login admin
- [ ] Meta tag `noindex, nofollow` presente
- [ ] Não aparece em menus de navegação
- [ ] Não aparece em pesquisa interna
- [ ] URL não é óbvio (não usar `/admin` sozinho)
- [ ] Adicionado ao `robots.txt` (Disallow)
- [ ] Removido do sitemap XML
- [ ] Testado em navegação anónima
- [ ] Testado no Google Search Console (verificar não indexado)

---

## 🔍 Como Verificar se Está Escondido

### Teste 1: Google Search
```
site:auto-prudente.com "gestão de preços"
```
Deve retornar: **0 resultados**

### Teste 2: Navegação Anónima
1. Abrir browser em modo anónimo
2. Ir para site principal
3. Usar pesquisa interna
4. Procurar por "preços" ou "admin"
5. Página NÃO deve aparecer

### Teste 3: Sitemap
1. Verificar: `https://auto-prudente.com/sitemap.xml`
2. Procurar pelo URL da página
3. NÃO deve estar listado

---

## 📱 Acesso Rápido (Para Admins)

### Criar Bookmark Privado

1. **No Browser:**
   - Adicionar bookmark/favorito
   - Nome: `🔒 Admin Prices`
   - URL: `https://auto-prudente.com/admin-car-prices-2024`

2. **Ou criar QR Code:**
   - Gerar em: https://www.qr-code-generator.com/
   - Imprimir e guardar
   - Scan rápido no telemóvel

### Criar Atalho no WordPress Dashboard

Adicionar ao `functions.php`:
```php
// Adicionar link rápido no admin bar
add_action('admin_bar_menu', function($wp_admin_bar) {
    if (current_user_can('manage_options')) {
        $wp_admin_bar->add_node(array(
            'id' => 'admin_prices',
            'title' => '🔒 Gestão Preços',
            'href' => home_url('/admin-car-prices-2024'),
            'meta' => array('target' => '_blank')
        ));
    }
}, 100);
```

---

## 🎯 Resumo - Configuração Ideal

**Para auto-prudente.com (uso interno):**

1. ✅ **Plugin:** Instalar `car-rental-integration.zip`
2. ✅ **Página:** URL difícil + protegida por senha
3. ✅ **SEO:** Meta noindex + robots.txt + sem sitemap
4. ✅ **Acesso:** Bookmark privado + atalho admin bar
5. ✅ **Segurança:** Password forte + só admins sabem URL

**Zero impacto no site público!**

---

## 🚀 URLs Sugeridos (Escolher 1)

Difíceis de adivinhar:
- `https://auto-prudente.com/gestao-interna-2024`
- `https://auto-prudente.com/admin-pricing-mgmt`
- `https://auto-prudente.com/internal-car-prices`
- `https://auto-prudente.com/backoffice-precos`
- `https://auto-prudente.com/private-admin-tools`

**Evitar:**
- ❌ `/admin` (muito óbvio)
- ❌ `/precos` (pode confundir)
- ❌ `/api` (reservado)

---

## 📞 Suporte

Se tiver dúvidas durante instalação:
1. Seguir checklist passo-a-passo
2. Verificar que API está configurada corretamente
3. Testar com senha/login
4. Verificar que não aparece em pesquisas

**Está pronto para implementar!** 🎉
