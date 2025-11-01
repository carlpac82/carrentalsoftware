/**
 * Car Rental Integration - Frontend JavaScript
 * Handles AJAX search and dynamic result rendering
 */

(function($) {
    'use strict';
    
    // Initialize on document ready
    $(document).ready(function() {
        initSearchForm();
    });
    
    /**
     * Initialize search form
     */
    function initSearchForm() {
        $('#criSearchForm').on('submit', function(e) {
            e.preventDefault();
            performSearch();
        });
    }
    
    /**
     * Perform AJAX search
     */
    function performSearch() {
        const $form = $('#criSearchForm');
        const $results = $('#criResults');
        const $loading = $('#criLoadingSpinner');
        const $error = $('#criErrorMessage');
        
        // Get form data
        const formData = {
            action: 'cri_search_prices',
            nonce: carRentalAPI.nonce,
            location: $form.find('[name="location"]').val(),
            date: $form.find('[name="date"]').val(),
            days: $form.find('[name="days"]').val(),
            group: $form.find('[name="group"]').val() || '',
            sort: $form.find('[name="sort"]').val() || 'price_asc'
        };
        
        // Show loading
        $loading.show();
        $error.hide();
        $results.html('');
        
        // Make AJAX request
        $.ajax({
            url: carRentalAPI.ajaxurl,
            method: 'POST',
            data: formData,
            timeout: 60000, // 60 seconds
            success: function(response) {
                $loading.hide();
                
                if (response.success && response.data) {
                    renderResults(response.data, formData);
                } else {
                    showError(response.data?.message || carRentalAPI.error);
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                $loading.hide();
                
                if (textStatus === 'timeout') {
                    showError('Request timed out. Please try again.');
                } else {
                    showError(carRentalAPI.error + ' (' + textStatus + ')');
                }
            }
        });
    }
    
    /**
     * Render search results
     */
    function renderResults(data, searchParams) {
        const $results = $('#criResults');
        let items = data.items || [];
        
        if (items.length === 0) {
            $results.html(`
                <div class="cri-no-results">
                    <p>No vehicles found for the selected criteria.</p>
                </div>
            `);
            return;
        }
        
        // Filter by group if specified
        if (searchParams.group) {
            items = items.filter(item => item.group === searchParams.group);
        }
        
        // Sort results
        items = sortItems(items, searchParams.sort);
        
        // Build HTML
        let html = `
            <div class="cri-price-list">
                <div class="cri-results-header">
                    <h3>Found ${items.length} vehicles</h3>
                    <div class="cri-results-info">
                        <span>${escapeHtml(searchParams.location)}</span>
                        <span>•</span>
                        <span>${searchParams.days} day${searchParams.days > 1 ? 's' : ''}</span>
                        <span>•</span>
                        <span>${formatDate(searchParams.date)}</span>
                    </div>
                </div>
                
                <div class="cri-results-grid cri-columns-3">
        `;
        
        items.forEach(item => {
            html += renderPriceCard(item);
        });
        
        html += `
                </div>
            </div>
        `;
        
        $results.html(html);
        
        // Scroll to results
        $('html, body').animate({
            scrollTop: $results.offset().top - 100
        }, 500);
    }
    
    /**
     * Render individual price card
     */
    function renderPriceCard(item) {
        const hasImage = item.image && item.image.length > 0;
        
        return `
            <div class="cri-price-card" data-group="${escapeHtml(item.group || '')}">
                ${hasImage ? `
                    <div class="cri-card-image">
                        <img src="${escapeHtml(item.image)}" 
                             alt="${escapeHtml(item.car)}"
                             loading="lazy">
                    </div>
                ` : ''}
                
                <div class="cri-card-content">
                    <div class="cri-card-header">
                        <h4 class="cri-car-name">${escapeHtml(item.car)}</h4>
                        ${item.group ? `
                            <span class="cri-group-badge">${escapeHtml(item.group)}</span>
                        ` : ''}
                    </div>
                    
                    <div class="cri-card-details">
                        ${item.category ? `
                            <div class="cri-detail">
                                <span class="cri-detail-icon">🚗</span>
                                <span class="cri-detail-text">${escapeHtml(item.category)}</span>
                            </div>
                        ` : ''}
                        
                        ${item.supplier ? `
                            <div class="cri-detail">
                                <span class="cri-detail-icon">🏢</span>
                                <span class="cri-detail-text">${escapeHtml(item.supplier)}</span>
                            </div>
                        ` : ''}
                        
                        ${item.passengers ? `
                            <div class="cri-detail">
                                <span class="cri-detail-icon">👥</span>
                                <span class="cri-detail-text">${item.passengers} passengers</span>
                            </div>
                        ` : ''}
                        
                        ${item.transmission ? `
                            <div class="cri-detail">
                                <span class="cri-detail-icon">⚙️</span>
                                <span class="cri-detail-text">${escapeHtml(item.transmission)}</span>
                            </div>
                        ` : ''}
                    </div>
                    
                    <div class="cri-card-footer">
                        <div class="cri-pricing">
                            <div class="cri-price-daily">
                                <span class="cri-price-label">Per Day:</span>
                                <span class="cri-price-amount">€${formatPrice(item.price_per_day)}</span>
                            </div>
                            
                            ${item.total_price ? `
                                <div class="cri-price-total">
                                    <span class="cri-price-label">Total:</span>
                                    <span class="cri-price-amount">€${formatPrice(item.total_price)}</span>
                                </div>
                            ` : ''}
                        </div>
                        
                        ${item.booking_url ? `
                            <a href="${escapeHtml(item.booking_url)}" 
                               class="cri-btn cri-btn-primary cri-btn-book" 
                               target="_blank" 
                               rel="noopener">
                                Book Now
                            </a>
                        ` : ''}
                    </div>
                </div>
            </div>
        `;
    }
    
    /**
     * Show error message
     */
    function showError(message) {
        const $error = $('#criErrorMessage');
        $error.html(`
            <strong>Error:</strong> ${escapeHtml(message)}
        `).show();
    }
    
    /**
     * Sort items
     */
    function sortItems(items, sortBy) {
        switch (sortBy) {
            case 'price_asc':
                return items.sort((a, b) => {
                    const priceA = parseFloat(a.price_per_day) || 0;
                    const priceB = parseFloat(b.price_per_day) || 0;
                    return priceA - priceB;
                });
                
            case 'price_desc':
                return items.sort((a, b) => {
                    const priceA = parseFloat(a.price_per_day) || 0;
                    const priceB = parseFloat(b.price_per_day) || 0;
                    return priceB - priceA;
                });
                
            case 'car_name':
                return items.sort((a, b) => {
                    const nameA = (a.car || '').toLowerCase();
                    const nameB = (b.car || '').toLowerCase();
                    return nameA.localeCompare(nameB);
                });
                
            default:
                return items;
        }
    }
    
    /**
     * Format price with 2 decimals
     */
    function formatPrice(price) {
        const num = parseFloat(price) || 0;
        return num.toFixed(2);
    }
    
    /**
     * Format date for display
     */
    function formatDate(dateString) {
        const date = new Date(dateString);
        const options = { year: 'numeric', month: 'short', day: 'numeric' };
        return date.toLocaleDateString(undefined, options);
    }
    
    /**
     * Escape HTML to prevent XSS
     */
    function escapeHtml(text) {
        if (!text) return '';
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.toString().replace(/[&<>"']/g, m => map[m]);
    }
    
})(jQuery);
