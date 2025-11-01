# Car Rental Integration WordPress Plugin

Professional WordPress plugin to integrate Car Rental API with your website. Display live car rental prices, search forms, and best deals directly in your WordPress pages and posts.

## 🚀 Features

- **Live Price Search** - Real-time car rental prices from your API
- **Multiple Shortcodes** - Easy integration with pages and posts
- **Responsive Design** - Mobile-friendly and modern UI
- **Smart Caching** - Improved performance with configurable cache
- **AJAX Search** - Fast search without page reload
- **Group Filtering** - Filter by vehicle groups (B1, B2, D, E1, etc.)
- **Multiple Layouts** - Cards, table, vertical, horizontal
- **Best Deals Widget** - Show cheapest rentals automatically

## 📋 Requirements

- WordPress 5.0 or higher
- PHP 7.4 or higher
- Car Rental API backend deployed and accessible

## 📦 Installation

### Method 1: Upload via WordPress Admin (Recommended)

1. **Create ZIP file:**
   ```bash
   cd wordpress-plugin
   zip -r car-rental-integration.zip car-rental-integration/
   ```

2. **Install in WordPress:**
   - Go to WordPress Admin → Plugins → Add New
   - Click "Upload Plugin"
   - Choose `car-rental-integration.zip`
   - Click "Install Now"
   - Click "Activate Plugin"

### Method 2: Manual Upload via FTP

1. Upload the `car-rental-integration` folder to `/wp-content/plugins/`
2. Activate the plugin through the 'Plugins' menu in WordPress

### Method 3: Direct Server Installation

```bash
# SSH into your server
cd /path/to/wordpress/wp-content/plugins/

# Copy the plugin folder
cp -r /path/to/car-rental-integration .

# Set proper permissions
chown -R www-data:www-data car-rental-integration
chmod -R 755 car-rental-integration
```

## ⚙️ Configuration

After activation, configure the plugin:

1. **Go to Settings → Car Rental API**

2. **API Connection Tab:**
   - **API URL**: Enter your Car Rental API URL
     - Example: `https://your-app.onrender.com`
   - **API Token** (Optional): If your API requires authentication
   - Click "Test API Connection" to verify

3. **Defaults Tab:**
   - **Default Location**: Albufeira or Faro Airport
   - **Default Days**: Default rental period (1-60 days)

4. **Cache Tab:**
   - **Cache Duration**: How long to cache results (seconds)
   - Recommended: 3600 (1 hour)
   - Click "Clear All Cache" to force fresh data

5. **Usage Guide Tab:**
   - View complete shortcode documentation
   - Copy-paste examples

## 🎨 Usage

### Shortcode 1: Search Form

Add a complete search form to any page:

```
[car_rental_search location="Albufeira" default_days="7"]
```

**Parameters:**
- `location` - Pickup location (default: "Albufeira")
- `default_days` - Default rental days (default: "7")
- `show_filters` - Show advanced filters (default: "yes")
- `layout` - Form layout: "vertical" or "horizontal" (default: "vertical")

**Examples:**
```
[car_rental_search]
[car_rental_search location="Aeroporto de Faro" default_days="14"]
[car_rental_search layout="horizontal" show_filters="no"]
```

### Shortcode 2: Price List

Display prices for specific criteria:

```
[car_rental_prices location="Albufeira" date="2025-11-01" days="7"]
```

**Parameters:**
- `location` - Pickup location
- `date` - Start date (Y-m-d format)
- `days` - Rental days
- `group` - Filter by group (optional): B1, B2, D, E1, etc.
- `limit` - Maximum results to show (default: "20")
- `show_images` - Show vehicle images (default: "yes")
- `columns` - Grid columns 1-4 (default: "3")

**Examples:**
```
[car_rental_prices location="Albufeira" days="7" limit="10"]
[car_rental_prices group="B1" columns="2"]
[car_rental_prices location="Faro Airport" days="14" show_images="no"]
```

### Shortcode 3: Best Deals

Show the cheapest rentals (top deals):

```
[car_rental_cheapest location="Albufeira" days="7" limit="5"]
```

**Parameters:**
- `location` - Pickup location
- `date` - Start date (default: tomorrow)
- `days` - Rental days
- `limit` - Number of deals to show (default: "5")
- `layout` - Display style: "cards" or "table" (default: "cards")

**Examples:**
```
[car_rental_cheapest limit="3"]
[car_rental_cheapest location="Faro Airport" days="14" layout="table"]
```

## 🎯 Complete Page Examples

### Example 1: Search Page

Create a new page "Car Rental Search":

```
<h2>Find Your Perfect Rental Car</h2>
[car_rental_search layout="horizontal"]
```

### Example 2: Deals Page

Create a page "Best Car Rental Deals":

```
<h2>Today's Best Deals</h2>
[car_rental_cheapest limit="10" layout="table"]

<h2>All Available Cars</h2>
[car_rental_prices days="7" limit="50"]
```

### Example 3: Category Pages

Create separate pages for each vehicle category:

**Economy Cars:**
```
[car_rental_prices group="D" location="Albufeira" days="7"]
```

**Automatic Cars:**
```
[car_rental_prices group="E2" location="Albufeira" days="7"]
```

**SUVs:**
```
[car_rental_prices group="F" location="Albufeira" days="7"]
```

## 🎨 Customization

### Custom CSS

Add custom styles in your theme's CSS:

```css
/* Change primary color */
.cri-btn-primary {
    background: #your-color !important;
}

/* Adjust card spacing */
.cri-results-grid {
    gap: 2rem;
}

/* Custom card styling */
.cri-price-card {
    border: 2px solid #your-color;
}
```

### PHP Filters

Developers can use filters to customize behavior:

```php
// Modify API request parameters
add_filter('cri_api_request_params', function($params) {
    $params['custom_field'] = 'value';
    return $params;
});

// Customize cache duration per request
add_filter('cri_cache_duration', function($duration, $location, $days) {
    if ($days >= 30) {
        return 7200; // 2 hours for long rentals
    }
    return $duration;
}, 10, 3);
```

## 🐛 Troubleshooting

### No Results Showing

1. **Check API Connection:**
   - Go to Settings → Car Rental API
   - Click "Test API Connection"
   - Verify URL is correct

2. **Clear Cache:**
   - Go to Cache tab
   - Click "Clear All Cache"
   - Try search again

3. **Check Browser Console:**
   - Press F12 in browser
   - Look for JavaScript errors
   - Check Network tab for failed requests

### Slow Loading

1. **Increase Cache Duration:**
   - Settings → Cache tab
   - Increase to 7200 (2 hours) or more

2. **Reduce Result Limit:**
   ```
   [car_rental_prices limit="10"]
   ```

3. **Check API Response Time:**
   - API may be slow or in sleep mode (Render free tier)
   - Consider upgrading API hosting

### Styling Issues

1. **Theme Conflicts:**
   - Some themes override plugin styles
   - Use browser inspector to identify conflicts
   - Add custom CSS with `!important`

2. **Mobile Issues:**
   - Plugin is responsive by default
   - Check theme's mobile CSS isn't conflicting

## 📊 Vehicle Groups Reference

- **B1** - Mini 4 Doors (e.g., Fiat 500 4p)
- **B2** - Mini (e.g., Fiat Panda, Toyota Aygo)
- **D** - Economy (e.g., Renault Clio, Peugeot 208)
- **E1** - Mini Automatic (e.g., Fiat 500 Auto)
- **E2** - Economy Automatic (e.g., Opel Corsa Auto)
- **F** - SUV (e.g., Nissan Juke, Peugeot 2008)
- **G** - Premium (e.g., Mini Cooper Countryman)
- **J1** - Crossover (e.g., Citroen C3 Aircross)
- **J2** - Station Wagon (e.g., Seat Leon SW)
- **L1** - SUV Automatic (e.g., Peugeot 3008 Auto)
- **L2** - Station Wagon Automatic (e.g., Toyota Corolla SW Auto)
- **M1** - 7 Seater (e.g., Dacia Lodgy, Peugeot Rifter)
- **M2** - 7 Seater Automatic (e.g., Renault Grand Scenic Auto)
- **N** - 9 Seater (e.g., Ford Tourneo, Mercedes Vito)

## 🔒 Security

- All user inputs are sanitized
- AJAX requests use WordPress nonces
- API credentials stored securely in WordPress options
- XSS protection on all outputs
- SQL injection protection via WordPress database API

## 🆘 Support

For issues or questions:

1. Check this README and Usage Guide in WordPress admin
2. Review browser console for errors (F12)
3. Test API connection in settings
4. Clear cache and try again

## 📝 Changelog

### Version 1.0.0 (2025-10-31)
- Initial release
- Search form shortcode
- Price list shortcode
- Best deals shortcode
- Admin settings page
- Caching system
- Responsive design
- AJAX search functionality

## 👨‍💻 Developer Info

**Author:** Autoprudente  
**License:** GPL v2 or later  
**Repository:** https://github.com/comercial-autoprudente/carrental_api

## 📄 License

This plugin is licensed under the GPL v2 or later.

```
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
```
