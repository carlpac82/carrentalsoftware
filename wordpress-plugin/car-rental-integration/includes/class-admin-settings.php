<?php
/**
 * Admin Settings for Car Rental Integration
 * Creates settings page in WordPress admin
 */

if (!defined('ABSPATH')) {
    exit;
}

class CRI_Admin_Settings {
    
    public static function init() {
        add_action('admin_menu', array(__CLASS__, 'add_settings_page'));
        add_action('admin_init', array(__CLASS__, 'register_settings'));
        add_action('admin_post_cri_test_connection', array(__CLASS__, 'test_api_connection'));
        add_action('admin_post_cri_clear_cache', array(__CLASS__, 'clear_cache'));
    }
    
    /**
     * Add settings page to WordPress admin menu
     */
    public static function add_settings_page() {
        add_options_page(
            __('Car Rental Integration Settings', 'car-rental-integration'),
            __('Car Rental API', 'car-rental-integration'),
            'manage_options',
            'car-rental-integration',
            array(__CLASS__, 'render_settings_page')
        );
    }
    
    /**
     * Register plugin settings
     */
    public static function register_settings() {
        // API Settings
        register_setting('cri_api_settings', 'cri_api_url', array(
            'type' => 'string',
            'sanitize_callback' => 'esc_url_raw',
            'default' => ''
        ));
        
        register_setting('cri_api_settings', 'cri_api_token', array(
            'type' => 'string',
            'sanitize_callback' => 'sanitize_text_field',
            'default' => ''
        ));
        
        // Default Settings
        register_setting('cri_default_settings', 'cri_default_location', array(
            'type' => 'string',
            'sanitize_callback' => 'sanitize_text_field',
            'default' => 'Albufeira'
        ));
        
        register_setting('cri_default_settings', 'cri_default_days', array(
            'type' => 'integer',
            'sanitize_callback' => 'absint',
            'default' => 7
        ));
        
        register_setting('cri_cache_settings', 'cri_cache_duration', array(
            'type' => 'integer',
            'sanitize_callback' => 'absint',
            'default' => 3600
        ));
        
        // Add settings sections
        add_settings_section(
            'cri_api_section',
            __('API Connection', 'car-rental-integration'),
            array(__CLASS__, 'render_api_section'),
            'cri_api_settings'
        );
        
        add_settings_section(
            'cri_defaults_section',
            __('Default Settings', 'car-rental-integration'),
            array(__CLASS__, 'render_defaults_section'),
            'cri_default_settings'
        );
        
        add_settings_section(
            'cri_cache_section',
            __('Cache Settings', 'car-rental-integration'),
            array(__CLASS__, 'render_cache_section'),
            'cri_cache_settings'
        );
        
        // Add settings fields
        add_settings_field(
            'cri_api_url',
            __('API URL', 'car-rental-integration'),
            array(__CLASS__, 'render_api_url_field'),
            'cri_api_settings',
            'cri_api_section'
        );
        
        add_settings_field(
            'cri_api_token',
            __('API Token (Optional)', 'car-rental-integration'),
            array(__CLASS__, 'render_api_token_field'),
            'cri_api_settings',
            'cri_api_section'
        );
        
        add_settings_field(
            'cri_default_location',
            __('Default Location', 'car-rental-integration'),
            array(__CLASS__, 'render_default_location_field'),
            'cri_default_settings',
            'cri_defaults_section'
        );
        
        add_settings_field(
            'cri_default_days',
            __('Default Days', 'car-rental-integration'),
            array(__CLASS__, 'render_default_days_field'),
            'cri_default_settings',
            'cri_defaults_section'
        );
        
        add_settings_field(
            'cri_cache_duration',
            __('Cache Duration (seconds)', 'car-rental-integration'),
            array(__CLASS__, 'render_cache_duration_field'),
            'cri_cache_settings',
            'cri_cache_section'
        );
    }
    
    /**
     * Render settings page
     */
    public static function render_settings_page() {
        if (!current_user_can('manage_options')) {
            return;
        }
        
        // Check if settings were saved
        if (isset($_GET['settings-updated'])) {
            add_settings_error(
                'cri_messages',
                'cri_message',
                __('Settings saved successfully', 'car-rental-integration'),
                'success'
            );
        }
        
        settings_errors('cri_messages');
        ?>
        <div class="wrap">
            <h1><?php echo esc_html(get_admin_page_title()); ?></h1>
            
            <h2 class="nav-tab-wrapper">
                <a href="?page=car-rental-integration&tab=api" class="nav-tab <?php echo (!isset($_GET['tab']) || $_GET['tab'] === 'api') ? 'nav-tab-active' : ''; ?>">
                    <?php _e('API Connection', 'car-rental-integration'); ?>
                </a>
                <a href="?page=car-rental-integration&tab=defaults" class="nav-tab <?php echo (isset($_GET['tab']) && $_GET['tab'] === 'defaults') ? 'nav-tab-active' : ''; ?>">
                    <?php _e('Defaults', 'car-rental-integration'); ?>
                </a>
                <a href="?page=car-rental-integration&tab=cache" class="nav-tab <?php echo (isset($_GET['tab']) && $_GET['tab'] === 'cache') ? 'nav-tab-active' : ''; ?>">
                    <?php _e('Cache', 'car-rental-integration'); ?>
                </a>
                <a href="?page=car-rental-integration&tab=usage" class="nav-tab <?php echo (isset($_GET['tab']) && $_GET['tab'] === 'usage') ? 'nav-tab-active' : ''; ?>">
                    <?php _e('Usage Guide', 'car-rental-integration'); ?>
                </a>
            </h2>
            
            <?php
            $active_tab = isset($_GET['tab']) ? $_GET['tab'] : 'api';
            
            if ($active_tab === 'usage') {
                self::render_usage_guide();
            } else {
                ?>
                <form action="options.php" method="post">
                    <?php
                    if ($active_tab === 'api') {
                        settings_fields('cri_api_settings');
                        do_settings_sections('cri_api_settings');
                    } elseif ($active_tab === 'defaults') {
                        settings_fields('cri_default_settings');
                        do_settings_sections('cri_default_settings');
                    } elseif ($active_tab === 'cache') {
                        settings_fields('cri_cache_settings');
                        do_settings_sections('cri_cache_settings');
                    }
                    
                    submit_button(__('Save Settings', 'car-rental-integration'));
                    ?>
                </form>
                
                <?php if ($active_tab === 'api'): ?>
                <div class="cri-test-connection" style="margin-top: 20px;">
                    <form method="post" action="<?php echo admin_url('admin-post.php'); ?>">
                        <input type="hidden" name="action" value="cri_test_connection">
                        <?php wp_nonce_field('cri_test_connection'); ?>
                        <?php submit_button(__('Test API Connection', 'car-rental-integration'), 'secondary', 'test_connection', false); ?>
                    </form>
                </div>
                <?php endif; ?>
                
                <?php if ($active_tab === 'cache'): ?>
                <div class="cri-clear-cache" style="margin-top: 20px;">
                    <form method="post" action="<?php echo admin_url('admin-post.php'); ?>">
                        <input type="hidden" name="action" value="cri_clear_cache">
                        <?php wp_nonce_field('cri_clear_cache'); ?>
                        <?php submit_button(__('Clear All Cache', 'car-rental-integration'), 'secondary', 'clear_cache', false); ?>
                    </form>
                </div>
                <?php endif; ?>
                <?php
            }
            ?>
        </div>
        <?php
    }
    
    // Section callbacks
    public static function render_api_section() {
        echo '<p>' . __('Configure the connection to your Car Rental API backend.', 'car-rental-integration') . '</p>';
    }
    
    public static function render_defaults_section() {
        echo '<p>' . __('Set default values for search forms and shortcodes.', 'car-rental-integration') . '</p>';
    }
    
    public static function render_cache_section() {
        echo '<p>' . __('Control how long search results are cached to improve performance.', 'car-rental-integration') . '</p>';
    }
    
    // Field callbacks
    public static function render_api_url_field() {
        $value = get_option('cri_api_url', '');
        ?>
        <input type="url" name="cri_api_url" value="<?php echo esc_attr($value); ?>" class="regular-text" placeholder="https://your-api.render.com">
        <p class="description"><?php _e('The base URL of your Car Rental API (e.g., https://your-app.onrender.com)', 'car-rental-integration'); ?></p>
        <?php
    }
    
    public static function render_api_token_field() {
        $value = get_option('cri_api_token', '');
        ?>
        <input type="password" name="cri_api_token" value="<?php echo esc_attr($value); ?>" class="regular-text">
        <p class="description"><?php _e('Optional: API authentication token if your API requires it', 'car-rental-integration'); ?></p>
        <?php
    }
    
    public static function render_default_location_field() {
        $value = get_option('cri_default_location', 'Albufeira');
        ?>
        <select name="cri_default_location">
            <option value="Albufeira" <?php selected($value, 'Albufeira'); ?>>Albufeira</option>
            <option value="Aeroporto de Faro" <?php selected($value, 'Aeroporto de Faro'); ?>>Faro Airport</option>
        </select>
        <p class="description"><?php _e('Default pickup location for search forms', 'car-rental-integration'); ?></p>
        <?php
    }
    
    public static function render_default_days_field() {
        $value = get_option('cri_default_days', 7);
        ?>
        <select name="cri_default_days">
            <?php foreach ([1, 2, 3, 4, 5, 6, 7, 8, 9, 14, 22, 28, 31, 60] as $days): ?>
                <option value="<?php echo $days; ?>" <?php selected($value, $days); ?>><?php echo $days; ?> days</option>
            <?php endforeach; ?>
        </select>
        <p class="description"><?php _e('Default number of rental days', 'car-rental-integration'); ?></p>
        <?php
    }
    
    public static function render_cache_duration_field() {
        $value = get_option('cri_cache_duration', 3600);
        ?>
        <input type="number" name="cri_cache_duration" value="<?php echo esc_attr($value); ?>" min="0" step="60">
        <p class="description">
            <?php _e('How long to cache search results (in seconds). Recommended: 3600 (1 hour)', 'car-rental-integration'); ?><br>
            <?php _e('Set to 0 to disable caching', 'car-rental-integration'); ?>
        </p>
        <?php
    }
    
    /**
     * Test API connection
     */
    public static function test_api_connection() {
        check_admin_referer('cri_test_connection');
        
        if (!current_user_can('manage_options')) {
            wp_die(__('Unauthorized', 'car-rental-integration'));
        }
        
        $api_client = new CRI_API_Client();
        $result = $api_client->test_connection();
        
        if (is_wp_error($result)) {
            add_settings_error(
                'cri_messages',
                'cri_message',
                __('Connection failed: ', 'car-rental-integration') . $result->get_error_message(),
                'error'
            );
        } else {
            add_settings_error(
                'cri_messages',
                'cri_message',
                __('✅ API connection successful!', 'car-rental-integration'),
                'success'
            );
        }
        
        set_transient('settings_errors', get_settings_errors(), 30);
        wp_redirect(add_query_arg('settings-updated', 'true', wp_get_referer()));
        exit;
    }
    
    /**
     * Clear cache
     */
    public static function clear_cache() {
        check_admin_referer('cri_clear_cache');
        
        if (!current_user_can('manage_options')) {
            wp_die(__('Unauthorized', 'car-rental-integration'));
        }
        
        CRI_API_Client::clear_cache();
        
        add_settings_error(
            'cri_messages',
            'cri_message',
            __('✅ Cache cleared successfully!', 'car-rental-integration'),
            'success'
        );
        
        set_transient('settings_errors', get_settings_errors(), 30);
        wp_redirect(add_query_arg('settings-updated', 'true', wp_get_referer()));
        exit;
    }
    
    /**
     * Render usage guide
     */
    private static function render_usage_guide() {
        ?>
        <div class="cri-usage-guide">
            <h2><?php _e('How to Use Car Rental Integration', 'car-rental-integration'); ?></h2>
            
            <div class="card">
                <h3>📋 <?php _e('Available Shortcodes', 'car-rental-integration'); ?></h3>
                
                <h4>1. Search Form</h4>
                <p><?php _e('Add a complete search form to any page:', 'car-rental-integration'); ?></p>
                <code>[car_rental_search location="Albufeira" default_days="7"]</code>
                
                <h4>2. Price List</h4>
                <p><?php _e('Display prices for specific criteria:', 'car-rental-integration'); ?></p>
                <code>[car_rental_prices location="Albufeira" date="2025-11-01" days="7" limit="20"]</code>
                
                <h4>3. Cheapest Cars (Top Deals)</h4>
                <p><?php _e('Show the best deals:', 'car-rental-integration'); ?></p>
                <code>[car_rental_cheapest location="Faro Airport" days="7" limit="5"]</code>
                
                <h4>4. Filter by Group</h4>
                <p><?php _e('Show only specific vehicle groups:', 'car-rental-integration'); ?></p>
                <code>[car_rental_prices group="B1" location="Albufeira" days="7"]</code>
                
                <hr>
                
                <h3>🎨 <?php _e('Customization', 'car-rental-integration'); ?></h3>
                <p><?php _e('You can customize the appearance using CSS in your theme:', 'car-rental-integration'); ?></p>
                <code>
                    .cri-search-form { /* Your styles */ }<br>
                    .cri-price-card { /* Your styles */ }<br>
                    .cri-results-grid { /* Your styles */ }
                </code>
            </div>
        </div>
        <?php
    }
}
