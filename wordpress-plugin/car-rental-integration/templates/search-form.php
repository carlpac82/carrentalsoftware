<?php
/**
 * Template: Search Form
 * Displays car rental search form
 */

if (!defined('ABSPATH')) {
    exit;
}

$layout_class = isset($atts['layout']) && $atts['layout'] === 'horizontal' ? 'cri-layout-horizontal' : 'cri-layout-vertical';
?>

<div class="cri-search-wrapper <?php echo esc_attr($layout_class); ?>">
    <div class="cri-search-form">
        <form id="criSearchForm" class="cri-form">
            
            <div class="cri-form-row">
                <div class="cri-form-group">
                    <label for="cri_location">
                        <span class="cri-label-icon">📍</span>
                        <?php _e('Pickup Location', 'car-rental-integration'); ?>
                    </label>
                    <select id="cri_location" name="location" required class="cri-select">
                        <option value="Albufeira" <?php selected($atts['location'], 'Albufeira'); ?>>
                            Albufeira
                        </option>
                        <option value="Aeroporto de Faro" <?php selected($atts['location'], 'Aeroporto de Faro'); ?>>
                            Faro Airport
                        </option>
                    </select>
                </div>
                
                <div class="cri-form-group">
                    <label for="cri_date">
                        <span class="cri-label-icon">📅</span>
                        <?php _e('Pickup Date', 'car-rental-integration'); ?>
                    </label>
                    <input type="date" 
                           id="cri_date" 
                           name="date" 
                           required 
                           class="cri-input"
                           min="<?php echo date('Y-m-d'); ?>"
                           value="<?php echo date('Y-m-d', strtotime('+1 day')); ?>">
                </div>
                
                <div class="cri-form-group">
                    <label for="cri_days">
                        <span class="cri-label-icon">🕒</span>
                        <?php _e('Rental Days', 'car-rental-integration'); ?>
                    </label>
                    <select id="cri_days" name="days" required class="cri-select">
                        <?php
                        $available_days = [1, 2, 3, 4, 5, 6, 7, 8, 9, 14, 22, 28, 31, 60];
                        foreach ($available_days as $day):
                        ?>
                            <option value="<?php echo $day; ?>" <?php selected($atts['default_days'], $day); ?>>
                                <?php echo $day; ?> <?php echo _n('day', 'days', $day, 'car-rental-integration'); ?>
                            </option>
                        <?php endforeach; ?>
                    </select>
                </div>
                
                <div class="cri-form-group cri-form-submit">
                    <button type="submit" class="cri-btn cri-btn-primary">
                        <span class="cri-btn-icon">🔍</span>
                        <?php _e('Search Prices', 'car-rental-integration'); ?>
                    </button>
                </div>
            </div>
            
            <?php if (isset($atts['show_filters']) && $atts['show_filters'] === 'yes'): ?>
            <div class="cri-filters-row" id="criFilters" style="display: none;">
                <div class="cri-form-group">
                    <label><?php _e('Vehicle Group', 'car-rental-integration'); ?></label>
                    <select name="group" class="cri-select">
                        <option value=""><?php _e('All Groups', 'car-rental-integration'); ?></option>
                        <option value="B1">B1 - Mini 4 Doors</option>
                        <option value="B2">B2 - Mini</option>
                        <option value="D">D - Economy</option>
                        <option value="E1">E1 - Mini Automatic</option>
                        <option value="E2">E2 - Economy Automatic</option>
                        <option value="F">F - SUV</option>
                        <option value="G">G - Premium</option>
                        <option value="J1">J1 - Crossover</option>
                        <option value="J2">J2 - Station Wagon</option>
                        <option value="L1">L1 - SUV Automatic</option>
                        <option value="L2">L2 - SW Automatic</option>
                        <option value="M1">M1 - 7 Seater</option>
                        <option value="M2">M2 - 7 Seater Automatic</option>
                        <option value="N">N - 9 Seater</option>
                    </select>
                </div>
                
                <div class="cri-form-group">
                    <label><?php _e('Sort By', 'car-rental-integration'); ?></label>
                    <select name="sort" class="cri-select">
                        <option value="price_asc"><?php _e('Price: Low to High', 'car-rental-integration'); ?></option>
                        <option value="price_desc"><?php _e('Price: High to Low', 'car-rental-integration'); ?></option>
                        <option value="car_name"><?php _e('Car Name A-Z', 'car-rental-integration'); ?></option>
                    </select>
                </div>
            </div>
            
            <button type="button" class="cri-toggle-filters" onclick="document.getElementById('criFilters').style.display = document.getElementById('criFilters').style.display === 'none' ? 'block' : 'none';">
                <?php _e('Advanced Filters', 'car-rental-integration'); ?> ▼
            </button>
            <?php endif; ?>
            
        </form>
    </div>
    
    <div class="cri-results-container">
        <div id="criLoadingSpinner" class="cri-loading" style="display: none;">
            <div class="cri-spinner"></div>
            <p><?php _e('Loading prices...', 'car-rental-integration'); ?></p>
        </div>
        
        <div id="criErrorMessage" class="cri-error-message" style="display: none;"></div>
        
        <div id="criResults" class="cri-results"></div>
    </div>
</div>
