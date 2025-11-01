<?php
/**
 * Snippets de Código para functions.php
 * Copiar e colar no functions.php do tema child
 * 
 * IMPORTANTE: Ajustar IDs e slugs conforme necessário
 */

// ============================================
// 1. BLOQUEAR INDEXAÇÃO DA PÁGINA PRIVADA
// ============================================
add_action('wp_head', 'autoprudente_noindex_admin_pages');
function autoprudente_noindex_admin_pages() {
    // Adicionar slugs das páginas privadas aqui
    $private_pages = array(
        'admin-car-prices-2024',
        'gestao-interna-2024',
        'internal-pricing-management'
    );
    
    if (is_page($private_pages)) {
        echo '<meta name="robots" content="noindex, nofollow">' . "\n";
        echo '<meta name="googlebot" content="noindex, nofollow">' . "\n";
        echo '<meta name="googlebot-news" content="noindex, nofollow">' . "\n";
    }
}

// ============================================
// 2. ESCONDER DA PESQUISA INTERNA DO SITE
// ============================================
add_filter('pre_get_posts', 'autoprudente_exclude_pages_search');
function autoprudente_exclude_pages_search($query) {
    if (!is_admin() && $query->is_search) {
        // IDs das páginas a esconder (substituir pelos IDs reais)
        $exclude_pages = array(123, 456); // Exemplo: páginas 123 e 456
        $query->set('post__not_in', $exclude_pages);
    }
    return $query;
}

// ============================================
// 3. REMOVER DO SITEMAP XML
// ============================================
add_filter('wp_sitemaps_posts_query_args', 'autoprudente_exclude_from_sitemap');
function autoprudente_exclude_from_sitemap($args) {
    // IDs das páginas a excluir do sitemap
    $args['post__not_in'] = isset($args['post__not_in']) 
        ? array_merge($args['post__not_in'], array(123, 456))
        : array(123, 456);
    return $args;
}

// Se usa Yoast SEO
add_filter('wpseo_sitemap_exclude_post_type', 'autoprudente_yoast_exclude_pages', 10, 2);
function autoprudente_yoast_exclude_pages($excluded, $post_type) {
    if ($post_type === 'page') {
        // Adicionar IDs aqui
        global $post;
        if (in_array($post->ID, array(123, 456))) {
            return true;
        }
    }
    return $excluded;
}

// ============================================
// 4. ATALHO NO ADMIN BAR (SÓ PARA ADMINS)
// ============================================
add_action('admin_bar_menu', 'autoprudente_admin_bar_link', 100);
function autoprudente_admin_bar_link($wp_admin_bar) {
    // Só mostrar para administradores
    if (!current_user_can('manage_options')) {
        return;
    }
    
    $wp_admin_bar->add_node(array(
        'id'     => 'admin_prices',
        'title'  => '🔒 Gestão Preços',
        'href'   => home_url('/admin-car-prices-2024'), // Ajustar URL
        'meta'   => array(
            'target' => '_blank',
            'title'  => 'Abrir Gestão de Preços'
        )
    ));
}

// ============================================
// 5. ESCONDER HEADER/FOOTER NA PÁGINA ADMIN
// ============================================
add_action('wp_head', 'autoprudente_admin_page_styles');
function autoprudente_admin_page_styles() {
    // Adicionar slugs das páginas aqui
    if (is_page(array('admin-car-prices-2024', 'gestao-interna-2024'))) {
        ?>
        <style>
            /* Esconder elementos desnecessários */
            .site-header,
            .site-footer,
            .breadcrumbs,
            .social-share,
            .related-posts,
            .comments-area {
                display: none !important;
            }
            
            /* Página full width */
            .entry-content,
            .site-content {
                max-width: 100% !important;
                padding: 20px !important;
            }
            
            /* Estilo clean para administração */
            body.page {
                background: #f5f5f5;
            }
        </style>
        <?php
    }
}

// ============================================
// 6. REDIRECT AUTOMÁTICO SE NÃO AUTENTICADO
// ============================================
add_action('template_redirect', 'autoprudente_protect_admin_pages');
function autoprudente_protect_admin_pages() {
    // Páginas que requerem login
    $protected_pages = array('admin-car-prices-2024', 'gestao-interna-2024');
    
    if (is_page($protected_pages) && !is_user_logged_in()) {
        // Redirect para login
        auth_redirect();
        exit;
    }
}

// ============================================
// 7. VERIFICAR SE USER É ADMIN
// ============================================
add_action('template_redirect', 'autoprudente_admin_only_pages');
function autoprudente_admin_only_pages() {
    // Páginas só para admins
    $admin_only_pages = array('admin-car-prices-2024');
    
    if (is_page($admin_only_pages)) {
        if (!current_user_can('manage_options')) {
            wp_die('Acesso Negado. Esta página é apenas para administradores.', 'Acesso Restrito', array('response' => 403));
        }
    }
}

// ============================================
// 8. LOG DE ACESSO À PÁGINA (OPCIONAL)
// ============================================
add_action('wp', 'autoprudente_log_admin_access');
function autoprudente_log_admin_access() {
    if (is_page(array('admin-car-prices-2024', 'gestao-interna-2024'))) {
        $user = wp_get_current_user();
        $log_entry = sprintf(
            "[%s] User: %s (ID: %d) accessed admin page\n",
            date('Y-m-d H:i:s'),
            $user->user_login,
            $user->ID
        );
        
        // Log para ficheiro (criar pasta 'logs' no tema)
        $log_file = get_stylesheet_directory() . '/logs/admin-access.log';
        if (is_writable(dirname($log_file))) {
            error_log($log_entry, 3, $log_file);
        }
    }
}

// ============================================
// 9. ADICIONAR AVISO DE PÁGINA PRIVADA
// ============================================
add_filter('the_content', 'autoprudente_admin_page_notice');
function autoprudente_admin_page_notice($content) {
    if (is_page(array('admin-car-prices-2024', 'gestao-interna-2024'))) {
        $notice = '
        <div style="background: #fff3cd; border: 2px solid #ffc107; padding: 20px; border-radius: 8px; margin-bottom: 30px;">
            <div style="display: flex; align-items: center; gap: 15px;">
                <span style="font-size: 32px;">⚠️</span>
                <div>
                    <strong style="font-size: 18px; color: #856404;">PÁGINA PRIVADA - USO INTERNO</strong>
                    <p style="margin: 5px 0 0 0; color: #856404;">
                        Esta página não está indexada no Google e é apenas para administração interna.<br>
                        <strong>Utilizador atual:</strong> ' . wp_get_current_user()->display_name . '
                    </p>
                </div>
            </div>
        </div>';
        
        return $notice . $content;
    }
    return $content;
}

// ============================================
// 10. BLOQUEAR ACESSO VIA USER AGENT (BOTS)
// ============================================
add_action('init', 'autoprudente_block_bots_admin_pages');
function autoprudente_block_bots_admin_pages() {
    if (is_page(array('admin-car-prices-2024', 'gestao-interna-2024'))) {
        $user_agent = isset($_SERVER['HTTP_USER_AGENT']) ? $_SERVER['HTTP_USER_AGENT'] : '';
        
        // Lista de bots a bloquear
        $blocked_bots = array('googlebot', 'bingbot', 'yahoo', 'baiduspider', 'yandex');
        
        foreach ($blocked_bots as $bot) {
            if (stripos($user_agent, $bot) !== false) {
                header('HTTP/1.0 403 Forbidden');
                exit('Access Denied');
            }
        }
    }
}

// ============================================
// INSTRUÇÕES DE USO
// ============================================
/*

PASSO 1: Identificar ID da página
---------------------------------
1. Criar a página no WordPress
2. Editar a página
3. Ver URL no browser: ?post=123 <- este é o ID
4. Substituir '123' nos códigos acima

PASSO 2: Escolher funções necessárias
-------------------------------------
Copiar apenas as funções que precisa para o functions.php do tema child

ESSENCIAIS:
- Função 1: Bloquear indexação (OBRIGATÓRIO)
- Função 2: Esconder de pesquisas (RECOMENDADO)
- Função 3: Remover do sitemap (RECOMENDADO)

OPCIONAIS:
- Função 4: Atalho no admin bar (ÚTIL)
- Função 5: Esconder header/footer (DESIGN)
- Função 6: Redirect se não autenticado (SEGURANÇA)
- Função 7: Só admins (SEGURANÇA EXTRA)
- Função 8: Log de acessos (AUDITORIA)
- Função 9: Aviso na página (VISUAL)
- Função 10: Bloquear bots (EXTRA SEGURANÇA)

PASSO 3: Ajustar valores
------------------------
- Substituir IDs: 123, 456 → IDs reais das páginas
- Substituir slugs: 'admin-car-prices-2024' → seu slug real
- Ajustar URLs: home_url('/seu-url') → seu URL real

PASSO 4: Testar
---------------
1. Visitar página em navegação anónima
2. Verificar se pede login/senha
3. Pesquisar no Google: site:auto-prudente.com "página"
4. Verificar sitemap.xml

*/
