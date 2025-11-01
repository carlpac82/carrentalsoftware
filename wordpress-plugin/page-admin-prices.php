<?php
/**
 * Template Name: Admin Car Prices (Hidden)
 * 
 * Página escondida para gestão interna de preços
 * NÃO indexada pelo Google
 * Requer autenticação WordPress
 */

// Verificar se user está logado
if (!is_user_logged_in()) {
    auth_redirect(); // Redirect para login
    exit;
}

// Verificar se user é admin
if (!current_user_can('manage_options')) {
    wp_die('Acesso negado. Apenas administradores podem ver esta página.');
}

get_header();
?>

<!-- NOINDEX: Página não deve ser indexada -->
<meta name="robots" content="noindex, nofollow">
<meta name="googlebot" content="noindex, nofollow">

<style>
    .admin-prices-page {
        max-width: 1400px;
        margin: 40px auto;
        padding: 0 20px;
    }
    
    .admin-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 12px;
        margin-bottom: 30px;
        text-align: center;
    }
    
    .admin-notice {
        background: #fef3cd;
        border: 2px solid #ffc107;
        padding: 15px 20px;
        border-radius: 8px;
        margin-bottom: 30px;
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .admin-notice-icon {
        font-size: 24px;
    }
</style>

<div class="admin-prices-page">
    
    <!-- Header -->
    <div class="admin-header">
        <h1>🔒 Gestão Interna de Preços</h1>
        <p>Página de administração - Uso exclusivo interno</p>
        <p><strong>Utilizador:</strong> <?php echo wp_get_current_user()->display_name; ?></p>
    </div>
    
    <!-- Aviso -->
    <div class="admin-notice">
        <span class="admin-notice-icon">⚠️</span>
        <div>
            <strong>PÁGINA PRIVADA</strong>
            <p style="margin: 5px 0 0 0;">Esta página não está indexada no Google e requer autenticação.</p>
        </div>
    </div>
    
    <!-- Search Form -->
    <div style="background: white; padding: 30px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 30px;">
        <h2>🔍 Pesquisa de Preços</h2>
        <?php echo do_shortcode('[car_rental_search location="Albufeira" default_days="7"]'); ?>
    </div>
    
    <!-- Best Deals -->
    <div style="background: white; padding: 30px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 30px;">
        <h2>🏆 Melhores Ofertas Atuais</h2>
        <?php echo do_shortcode('[car_rental_cheapest location="Albufeira" days="7" limit="5"]'); ?>
    </div>
    
    <!-- All Prices -->
    <div style="background: white; padding: 30px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
        <h2>📋 Todos os Preços Disponíveis</h2>
        <?php echo do_shortcode('[car_rental_prices location="Albufeira" days="7" limit="30" columns="3"]'); ?>
    </div>
    
    <!-- Links Úteis -->
    <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin-top: 30px;">
        <h3>🔗 Links Úteis</h3>
        <ul>
            <li><a href="<?php echo admin_url('options-general.php?page=car-rental-integration'); ?>">⚙️ Configurações do Plugin</a></li>
            <li><a href="<?php echo admin_url(); ?>">🏠 WordPress Dashboard</a></li>
            <li><a href="<?php echo get_site_url(); ?>">🌐 Ver Website Principal</a></li>
        </ul>
    </div>
    
</div>

<?php get_footer(); ?>
