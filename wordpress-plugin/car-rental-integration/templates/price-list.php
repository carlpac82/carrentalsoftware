<?php
/**
 * Template: Price List
 * Displays list of car rental prices
 */

if (!defined('ABSPATH')) {
    exit;
}

$items = isset($results['items']) ? $results['items'] : array();
$columns = isset($atts['columns']) ? (int) $atts['columns'] : 3;
$show_images = isset($atts['show_images']) && $atts['show_images'] === 'yes';

if (empty($items)) {
    echo '<div class="cri-no-results">';
    echo '<p>' . __('No vehicles found for the selected criteria.', 'car-rental-integration') . '</p>';
    echo '</div>';
    return;
}
?>

<div class="cri-price-list">
    <div class="cri-results-header">
        <h3><?php printf(__('Found %d vehicles', 'car-rental-integration'), count($items)); ?></h3>
        <div class="cri-results-info">
            <span><?php echo esc_html($atts['location']); ?></span>
            <span>•</span>
            <span><?php echo esc_html($atts['days']); ?> <?php echo _n('day', 'days', $atts['days'], 'car-rental-integration'); ?></span>
            <span>•</span>
            <span><?php echo date_i18n(get_option('date_format'), strtotime($atts['date'])); ?></span>
        </div>
    </div>
    
    <div class="cri-results-grid cri-columns-<?php echo $columns; ?>">
        <?php foreach ($items as $item): ?>
            <div class="cri-price-card" data-group="<?php echo esc_attr($item['group'] ?? ''); ?>">
                
                <?php if ($show_images && !empty($item['image'])): ?>
                <div class="cri-card-image">
                    <img src="<?php echo esc_url($item['image']); ?>" 
                         alt="<?php echo esc_attr($item['car']); ?>"
                         loading="lazy">
                </div>
                <?php endif; ?>
                
                <div class="cri-card-content">
                    <div class="cri-card-header">
                        <h4 class="cri-car-name"><?php echo esc_html($item['car']); ?></h4>
                        
                        <?php if (!empty($item['group'])): ?>
                            <span class="cri-group-badge">
                                <?php echo esc_html($item['group']); ?>
                            </span>
                        <?php endif; ?>
                    </div>
                    
                    <div class="cri-card-details">
                        <?php if (!empty($item['category'])): ?>
                            <div class="cri-detail">
                                <span class="cri-detail-icon">🚗</span>
                                <span class="cri-detail-text"><?php echo esc_html($item['category']); ?></span>
                            </div>
                        <?php endif; ?>
                        
                        <?php if (!empty($item['supplier'])): ?>
                            <div class="cri-detail">
                                <span class="cri-detail-icon">🏢</span>
                                <span class="cri-detail-text"><?php echo esc_html($item['supplier']); ?></span>
                            </div>
                        <?php endif; ?>
                        
                        <?php if (!empty($item['passengers'])): ?>
                            <div class="cri-detail">
                                <span class="cri-detail-icon">👥</span>
                                <span class="cri-detail-text">
                                    <?php printf(__('%d passengers', 'car-rental-integration'), $item['passengers']); ?>
                                </span>
                            </div>
                        <?php endif; ?>
                        
                        <?php if (!empty($item['transmission'])): ?>
                            <div class="cri-detail">
                                <span class="cri-detail-icon">⚙️</span>
                                <span class="cri-detail-text"><?php echo esc_html($item['transmission']); ?></span>
                            </div>
                        <?php endif; ?>
                    </div>
                    
                    <div class="cri-card-footer">
                        <div class="cri-pricing">
                            <div class="cri-price-daily">
                                <span class="cri-price-label"><?php _e('Per Day:', 'car-rental-integration'); ?></span>
                                <span class="cri-price-amount">€<?php echo number_format($item['price_per_day'], 2); ?></span>
                            </div>
                            
                            <?php if (!empty($item['total_price'])): ?>
                                <div class="cri-price-total">
                                    <span class="cri-price-label"><?php _e('Total:', 'car-rental-integration'); ?></span>
                                    <span class="cri-price-amount">€<?php echo number_format($item['total_price'], 2); ?></span>
                                </div>
                            <?php endif; ?>
                        </div>
                        
                        <?php if (!empty($item['booking_url'])): ?>
                            <a href="<?php echo esc_url($item['booking_url']); ?>" 
                               class="cri-btn cri-btn-book" 
                               target="_blank" 
                               rel="noopener">
                                <?php _e('Book Now', 'car-rental-integration'); ?>
                            </a>
                        <?php endif; ?>
                    </div>
                </div>
            </div>
        <?php endforeach; ?>
    </div>
</div>
