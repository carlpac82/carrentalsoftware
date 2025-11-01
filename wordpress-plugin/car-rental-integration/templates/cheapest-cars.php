<?php
/**
 * Template: Cheapest Cars
 * Displays the cheapest car rental deals
 */

if (!defined('ABSPATH')) {
    exit;
}

$items = isset($results['items']) ? $results['items'] : array();
$layout = isset($atts['layout']) ? $atts['layout'] : 'cards';

if (empty($items)) {
    echo '<div class="cri-no-results">';
    echo '<p>' . __('No deals available at the moment.', 'car-rental-integration') . '</p>';
    echo '</div>';
    return;
}
?>

<div class="cri-cheapest-cars cri-layout-<?php echo esc_attr($layout); ?>">
    <div class="cri-section-header">
        <h3>🏆 <?php _e('Best Deals', 'car-rental-integration'); ?></h3>
        <p class="cri-section-subtitle">
            <?php printf(__('Top %d cheapest rentals', 'car-rental-integration'), count($items)); ?>
        </p>
    </div>
    
    <?php if ($layout === 'table'): ?>
        <!-- Table Layout -->
        <table class="cri-deals-table">
            <thead>
                <tr>
                    <th><?php _e('Rank', 'car-rental-integration'); ?></th>
                    <th><?php _e('Vehicle', 'car-rental-integration'); ?></th>
                    <th><?php _e('Supplier', 'car-rental-integration'); ?></th>
                    <th><?php _e('Price/Day', 'car-rental-integration'); ?></th>
                    <th><?php _e('Total', 'car-rental-integration'); ?></th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($items as $index => $item): ?>
                    <tr class="cri-deal-row">
                        <td class="cri-rank">
                            <?php if ($index === 0): ?>
                                <span class="cri-medal gold">🥇</span>
                            <?php elseif ($index === 1): ?>
                                <span class="cri-medal silver">🥈</span>
                            <?php elseif ($index === 2): ?>
                                <span class="cri-medal bronze">🥉</span>
                            <?php else: ?>
                                <span class="cri-rank-number">#<?php echo $index + 1; ?></span>
                            <?php endif; ?>
                        </td>
                        <td class="cri-vehicle">
                            <strong><?php echo esc_html($item['car']); ?></strong>
                            <?php if (!empty($item['category'])): ?>
                                <br><small class="cri-category"><?php echo esc_html($item['category']); ?></small>
                            <?php endif; ?>
                        </td>
                        <td class="cri-supplier"><?php echo esc_html($item['supplier'] ?? '-'); ?></td>
                        <td class="cri-price-daily">
                            <strong>€<?php echo number_format($item['price_per_day'], 2); ?></strong>
                        </td>
                        <td class="cri-price-total">€<?php echo number_format($item['total_price'] ?? 0, 2); ?></td>
                        <td class="cri-action">
                            <?php if (!empty($item['booking_url'])): ?>
                                <a href="<?php echo esc_url($item['booking_url']); ?>" 
                                   class="cri-btn cri-btn-small" 
                                   target="_blank">
                                    <?php _e('Book', 'car-rental-integration'); ?>
                                </a>
                            <?php endif; ?>
                        </td>
                    </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
        
    <?php else: ?>
        <!-- Cards Layout -->
        <div class="cri-deals-grid">
            <?php foreach ($items as $index => $item): ?>
                <div class="cri-deal-card <?php echo $index === 0 ? 'cri-best-deal' : ''; ?>">
                    
                    <?php if ($index < 3): ?>
                        <div class="cri-deal-badge">
                            <?php if ($index === 0): ?>
                                🥇 <?php _e('Best Deal', 'car-rental-integration'); ?>
                            <?php elseif ($index === 1): ?>
                                🥈 <?php _e('2nd Best', 'car-rental-integration'); ?>
                            <?php elseif ($index === 2): ?>
                                🥉 <?php _e('3rd Best', 'car-rental-integration'); ?>
                            <?php endif; ?>
                        </div>
                    <?php endif; ?>
                    
                    <div class="cri-deal-content">
                        <h4 class="cri-deal-title"><?php echo esc_html($item['car']); ?></h4>
                        
                        <?php if (!empty($item['category'])): ?>
                            <p class="cri-deal-category"><?php echo esc_html($item['category']); ?></p>
                        <?php endif; ?>
                        
                        <div class="cri-deal-details">
                            <?php if (!empty($item['supplier'])): ?>
                                <div class="cri-deal-detail">
                                    <span class="cri-icon">🏢</span>
                                    <?php echo esc_html($item['supplier']); ?>
                                </div>
                            <?php endif; ?>
                            
                            <?php if (!empty($item['group'])): ?>
                                <div class="cri-deal-detail">
                                    <span class="cri-icon">🚗</span>
                                    <?php _e('Group', 'car-rental-integration'); ?>: <?php echo esc_html($item['group']); ?>
                                </div>
                            <?php endif; ?>
                        </div>
                        
                        <div class="cri-deal-pricing">
                            <div class="cri-deal-price-main">
                                <span class="cri-currency">€</span>
                                <span class="cri-amount"><?php echo number_format($item['price_per_day'], 2); ?></span>
                                <span class="cri-period">/<?php _e('day', 'car-rental-integration'); ?></span>
                            </div>
                            
                            <?php if (!empty($item['total_price'])): ?>
                                <div class="cri-deal-price-total">
                                    <?php printf(__('Total: €%s', 'car-rental-integration'), number_format($item['total_price'], 2)); ?>
                                </div>
                            <?php endif; ?>
                        </div>
                        
                        <?php if (!empty($item['booking_url'])): ?>
                            <a href="<?php echo esc_url($item['booking_url']); ?>" 
                               class="cri-btn cri-btn-primary cri-btn-full" 
                               target="_blank" 
                               rel="noopener">
                                <?php _e('Book This Deal', 'car-rental-integration'); ?> →
                            </a>
                        <?php endif; ?>
                    </div>
                </div>
            <?php endforeach; ?>
        </div>
    <?php endif; ?>
</div>
