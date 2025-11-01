<?php
/**
 * Plugin Name: Car Rental Price Integration
 * Plugin URI: https://github.com/comercial-autoprudente/carrental_api
 * Description: Professional integration with Car Rental API - Display live car rental prices with advanced search and filtering
 * Version: 1.0.0
 * Author: Autoprudente
 * Author URI: https://autoprudente.pt
 * License: GPL v2 or later
 * Text Domain: car-rental-integration
 * Domain Path: /languages
 */

if (!defined('ABSPATH')) {
    exit; // Exit if accessed directly
}

// Define plugin constants
define('CRI_VERSION', '1.0.0');
define('CRI_PLUGIN_DIR', plugin_dir_path(__FILE__));
define('CRI_PLUGIN_URL', plugin_dir_url(__FILE__));
define('CRI_PLUGIN_BASENAME', plugin_basename(__FILE__));

/**
 * Main Plugin Class
 */
class CarRentalIntegration {
    
    private static $instance = null;
    
    public static function get_instance() {
        if (null === self::$instance) {
            self::$instance = new self();
        }
        return self::$instance;
    }
    
    private function __construct() {
        $this->load_dependencies();
        $this->init_hooks();
    }
    
    /**
     * Load required files
     */
    private function load_dependencies() {
        require_once CRI_PLUGIN_DIR . 'includes/class-api-client.php';
        require_once CRI_PLUGIN_DIR . 'includes/class-shortcodes.php';
        require_once CRI_PLUGIN_DIR . 'includes/class-admin-settings.php';
    }
    
    /**
     * Initialize WordPress hooks
     */
    private function init_hooks() {
        add_action('wp_enqueue_scripts', array($this, 'enqueue_frontend_assets'));
        add_action('admin_enqueue_scripts', array($this, 'enqueue_admin_assets'));
        add_action('plugins_loaded', array($this, 'load_textdomain'));
        
        // Initialize components
        CRI_Shortcodes::init();
        CRI_Admin_Settings::init();
    }
    
    /**
     * Load plugin text domain for translations
     */
    public function load_textdomain() {
        load_plugin_textdomain('car-rental-integration', false, 
            dirname(CRI_PLUGIN_BASENAME) . '/languages');
    }
    
    /**
     * Enqueue frontend styles and scripts
     */
    public function enqueue_frontend_assets() {
        // CSS
        wp_enqueue_style(
            'car-rental-styles',
            CRI_PLUGIN_URL . 'assets/css/frontend.css',
            array(),
            CRI_VERSION
        );
        
        // JavaScript
        wp_enqueue_script(
            'car-rental-script',
            CRI_PLUGIN_URL . 'assets/js/frontend.js',
            array('jquery'),
            CRI_VERSION,
            true
        );
        
        // Localize script with AJAX URL and nonce
        wp_localize_script('car-rental-script', 'carRentalAPI', array(
            'ajaxurl' => admin_url('admin-ajax.php'),
            'nonce' => wp_create_nonce('car_rental_nonce'),
            'apiUrl' => get_option('cri_api_url', ''),
            'loading' => __('Loading prices...', 'car-rental-integration'),
            'error' => __('Error loading prices. Please try again.', 'car-rental-integration'),
        ));
    }
    
    /**
     * Enqueue admin styles and scripts
     */
    public function enqueue_admin_assets($hook) {
        // Only load on our settings page
        if ('settings_page_car-rental-integration' !== $hook) {
            return;
        }
        
        wp_enqueue_style(
            'car-rental-admin-styles',
            CRI_PLUGIN_URL . 'assets/css/admin.css',
            array(),
            CRI_VERSION
        );
    }
}

/**
 * Initialize the plugin
 */
function car_rental_integration_init() {
    return CarRentalIntegration::get_instance();
}

// Start the plugin
car_rental_integration_init();

/**
 * Activation hook
 */
register_activation_hook(__FILE__, 'car_rental_integration_activate');
function car_rental_integration_activate() {
    // Set default options
    add_option('cri_api_url', '');
    add_option('cri_api_token', '');
    add_option('cri_default_location', 'Albufeira');
    add_option('cri_default_days', '7');
    add_option('cri_cache_duration', '3600'); // 1 hour
    
    // Flush rewrite rules
    flush_rewrite_rules();
}

/**
 * Deactivation hook
 */
register_deactivation_hook(__FILE__, 'car_rental_integration_deactivate');
function car_rental_integration_deactivate() {
    // Flush rewrite rules
    flush_rewrite_rules();
}
