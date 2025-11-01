<?php
/**
 * Shortcodes for Car Rental Integration
 * Provides shortcodes to embed car rental functionality in WordPress pages
 */

if (!defined('ABSPATH')) {
    exit;
}

class CRI_Shortcodes {
    
    public static function init() {
        add_shortcode('car_rental_search', array(__CLASS__, 'render_search_form'));
        add_shortcode('car_rental_prices', array(__CLASS__, 'render_price_list'));
        add_shortcode('car_rental_cheapest', array(__CLASS__, 'render_cheapest_cars'));
        
        // AJAX handlers
        add_action('wp_ajax_cri_search_prices', array(__CLASS__, 'ajax_search_prices'));
        add_action('wp_ajax_nopriv_cri_search_prices', array(__CLASS__, 'ajax_search_prices'));
    }
    
    /**
     * Render search form
     * 
     * Usage: [car_rental_search location="Albufeira" default_days="7"]
     */
    public static function render_search_form($atts) {
        $atts = shortcode_atts(array(
            'location' => get_option('cri_default_location', 'Albufeira'),
            'default_days' => get_option('cri_default_days', '7'),
            'show_filters' => 'yes',
            'layout' => 'vertical' // vertical or horizontal
        ), $atts);
        
        ob_start();
        include CRI_PLUGIN_DIR . 'templates/search-form.php';
        return ob_get_clean();
    }
    
    /**
     * Render price list for specific criteria
     * 
     * Usage: [car_rental_prices location="Albufeira" date="2025-11-01" days="7"]
     */
    public static function render_price_list($atts) {
        $atts = shortcode_atts(array(
            'location' => get_option('cri_default_location', 'Albufeira'),
            'date' => date('Y-m-d', strtotime('+1 day')),
            'days' => get_option('cri_default_days', '7'),
            'group' => '', // Optional: filter by group (B1, B2, D, etc)
            'limit' => '20',
            'show_images' => 'yes',
            'columns' => '3' // Grid columns (1-4)
        ), $atts);
        
        $api_client = new CRI_API_Client();
        $results = $api_client->search_prices(
            $atts['location'],
            $atts['date'],
            (int) $atts['days']
        );
        
        if (is_wp_error($results)) {
            return '<div class="cri-error">' . esc_html($results->get_error_message()) . '</div>';
        }
        
        // Filter by group if specified
        if (!empty($atts['group']) && isset($results['items'])) {
            $results['items'] = array_filter($results['items'], function($item) use ($atts) {
                return isset($item['group']) && $item['group'] === $atts['group'];
            });
        }
        
        // Limit results
        if (isset($results['items']) && !empty($atts['limit'])) {
            $results['items'] = array_slice($results['items'], 0, (int) $atts['limit']);
        }
        
        ob_start();
        include CRI_PLUGIN_DIR . 'templates/price-list.php';
        return ob_get_clean();
    }
    
    /**
     * Render cheapest cars (top deals)
     * 
     * Usage: [car_rental_cheapest location="Albufeira" days="7" limit="5"]
     */
    public static function render_cheapest_cars($atts) {
        $atts = shortcode_atts(array(
            'location' => get_option('cri_default_location', 'Albufeira'),
            'date' => date('Y-m-d', strtotime('+1 day')),
            'days' => get_option('cri_default_days', '7'),
            'limit' => '5',
            'layout' => 'cards' // cards or table
        ), $atts);
        
        $api_client = new CRI_API_Client();
        $results = $api_client->search_prices(
            $atts['location'],
            $atts['date'],
            (int) $atts['days']
        );
        
        if (is_wp_error($results)) {
            return '<div class="cri-error">' . esc_html($results->get_error_message()) . '</div>';
        }
        
        // Sort by price and get cheapest
        if (isset($results['items']) && is_array($results['items'])) {
            usort($results['items'], function($a, $b) {
                $price_a = isset($a['price_per_day']) ? (float) $a['price_per_day'] : PHP_INT_MAX;
                $price_b = isset($b['price_per_day']) ? (float) $b['price_per_day'] : PHP_INT_MAX;
                return $price_a <=> $price_b;
            });
            
            $results['items'] = array_slice($results['items'], 0, (int) $atts['limit']);
        }
        
        ob_start();
        include CRI_PLUGIN_DIR . 'templates/cheapest-cars.php';
        return ob_get_clean();
    }
    
    /**
     * AJAX handler for price search
     */
    public static function ajax_search_prices() {
        check_ajax_referer('car_rental_nonce', 'nonce');
        
        $location = isset($_POST['location']) ? sanitize_text_field($_POST['location']) : '';
        $date = isset($_POST['date']) ? sanitize_text_field($_POST['date']) : '';
        $days = isset($_POST['days']) ? (int) $_POST['days'] : 0;
        
        if (empty($location) || empty($date) || empty($days)) {
            wp_send_json_error(array(
                'message' => __('Missing required parameters', 'car-rental-integration')
            ));
        }
        
        $api_client = new CRI_API_Client();
        $results = $api_client->search_prices($location, $date, $days);
        
        if (is_wp_error($results)) {
            wp_send_json_error(array(
                'message' => $results->get_error_message()
            ));
        }
        
        wp_send_json_success($results);
    }
}
