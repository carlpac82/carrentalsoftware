<?php
/**
 * API Client for Car Rental Integration
 * Handles all communication with the Car Rental API
 */

if (!defined('ABSPATH')) {
    exit;
}

class CRI_API_Client {
    
    private $api_url;
    private $api_token;
    private $cache_duration;
    
    public function __construct() {
        $this->api_url = get_option('cri_api_url', '');
        $this->api_token = get_option('cri_api_token', '');
        $this->cache_duration = (int) get_option('cri_cache_duration', 3600);
    }
    
    /**
     * Search car rental prices
     * 
     * @param string $location Location name (Albufeira or Aeroporto de Faro)
     * @param string $date Start date (Y-m-d format)
     * @param int $days Number of rental days
     * @return array|WP_Error
     */
    public function search_prices($location, $date, $days) {
        // Validate inputs
        if (empty($location) || empty($date) || empty($days)) {
            return new WP_Error('invalid_params', __('Invalid search parameters', 'car-rental-integration'));
        }
        
        // Check cache first
        $cache_key = $this->get_cache_key($location, $date, $days);
        $cached_data = get_transient($cache_key);
        
        if (false !== $cached_data) {
            return $cached_data;
        }
        
        // Make API request
        $response = $this->make_request('/api/scrape', array(
            'location' => $location,
            'start_date' => $date,
            'days' => (int) $days
        ));
        
        if (is_wp_error($response)) {
            return $response;
        }
        
        // Cache the results
        set_transient($cache_key, $response, $this->cache_duration);
        
        return $response;
    }
    
    /**
     * Get current prices for a specific group
     * 
     * @param string $location Location name
     * @param string $group Group code (B1, B2, D, etc)
     * @param string $date Date (Y-m-d format)
     * @param int $days Number of days
     * @return array|WP_Error
     */
    public function get_group_prices($location, $group, $date, $days) {
        $cache_key = "cri_group_{$location}_{$group}_{$date}_{$days}";
        $cached_data = get_transient($cache_key);
        
        if (false !== $cached_data) {
            return $cached_data;
        }
        
        $response = $this->make_request('/api/group-prices', array(
            'location' => $location,
            'group' => $group,
            'date' => $date,
            'days' => (int) $days
        ));
        
        if (!is_wp_error($response)) {
            set_transient($cache_key, $response, $this->cache_duration);
        }
        
        return $response;
    }
    
    /**
     * Get available suppliers
     * 
     * @return array|WP_Error
     */
    public function get_suppliers() {
        $cache_key = 'cri_suppliers_list';
        $cached_data = get_transient($cache_key);
        
        if (false !== $cached_data) {
            return $cached_data;
        }
        
        $response = $this->make_request('/api/suppliers', array(), 'GET');
        
        if (!is_wp_error($response)) {
            set_transient($cache_key, $response, DAY_IN_SECONDS); // Cache for 24 hours
        }
        
        return $response;
    }
    
    /**
     * Make HTTP request to API
     * 
     * @param string $endpoint API endpoint
     * @param array $data Request data
     * @param string $method HTTP method (GET or POST)
     * @return array|WP_Error
     */
    private function make_request($endpoint, $data = array(), $method = 'POST') {
        if (empty($this->api_url)) {
            return new WP_Error('no_api_url', __('API URL not configured', 'car-rental-integration'));
        }
        
        $url = trailingslashit($this->api_url) . ltrim($endpoint, '/');
        
        $args = array(
            'method' => $method,
            'timeout' => 60,
            'headers' => array(
                'Content-Type' => 'application/json',
            ),
        );
        
        // Add authorization if token is set
        if (!empty($this->api_token)) {
            $args['headers']['Authorization'] = 'Bearer ' . $this->api_token;
        }
        
        // Add body for POST requests
        if ('POST' === $method && !empty($data)) {
            $args['body'] = json_encode($data);
        }
        
        // Add query string for GET requests
        if ('GET' === $method && !empty($data)) {
            $url = add_query_arg($data, $url);
        }
        
        // Make request
        $response = wp_remote_request($url, $args);
        
        // Check for errors
        if (is_wp_error($response)) {
            return $response;
        }
        
        $response_code = wp_remote_retrieve_response_code($response);
        $body = wp_remote_retrieve_body($response);
        
        if ($response_code < 200 || $response_code >= 300) {
            return new WP_Error(
                'api_error',
                sprintf(__('API returned error code: %d', 'car-rental-integration'), $response_code)
            );
        }
        
        $data = json_decode($body, true);
        
        if (json_last_error() !== JSON_ERROR_NONE) {
            return new WP_Error('json_decode_error', __('Invalid JSON response from API', 'car-rental-integration'));
        }
        
        return $data;
    }
    
    /**
     * Generate cache key
     */
    private function get_cache_key($location, $date, $days) {
        return 'cri_prices_' . md5($location . $date . $days);
    }
    
    /**
     * Clear all cached data
     */
    public static function clear_cache() {
        global $wpdb;
        
        $wpdb->query(
            "DELETE FROM {$wpdb->options} 
             WHERE option_name LIKE '_transient_cri_%' 
             OR option_name LIKE '_transient_timeout_cri_%'"
        );
        
        return true;
    }
    
    /**
     * Test API connection
     * 
     * @return bool|WP_Error
     */
    public function test_connection() {
        $response = $this->make_request('/api/health', array(), 'GET');
        
        if (is_wp_error($response)) {
            return $response;
        }
        
        return true;
    }
}
