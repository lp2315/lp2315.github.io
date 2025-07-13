// Universal Language Toggle System

class LanguageToggle {
    constructor() {
        this.currentLanguage = 'en';
        this.translations = {
            en: {
                // Page headers
                'page-title': 'APK Calculator',
                'page-subtitle': 'Systembolaget drinks ranked by alcohol per krona value',
                'products-heading': 'All Products',

                // Form controls
                'search-placeholder': 'Search products...',
                'filter-all-types': 'All Types',
                'page-25': '25 per page',
                'page-50': '50 per page',
                'page-100': '100 per page',
                'page-all': 'Show all',

                // Table headers
                'th-rank': 'Rank',
                'th-product': 'Product',
                'th-type': 'Type',
                'th-apk': 'APK',
                'th-price': 'Price',
                'th-volume': 'Volume',
                'th-alcohol': 'Alcohol',

                // Status messages
                'loading': 'Loading data...',
                'showing-simple': 'Showing {count} of {total} products',
                'showing-paged': 'Showing {start}-{end} of {count} products (Page {page}/{totalPages})',
                'load-error': 'Failed to load data: {error}',

                // Units
                'currency': 'kr',
                'volume-unit': 'ml',
                'alcohol-unit': '%'
            },
            sv: {
                // Page headers
                'page-title': 'APK Kalkylator',
                'page-subtitle': 'Systembolagets drycker rankade efter alkohol per krona värde',
                'products-heading': 'Alla Produkter',

                // Form controls
                'search-placeholder': 'Sök produkter...',
                'filter-all-types': 'Alla Typer',
                'page-25': '25 per sida',
                'page-50': '50 per sida',
                'page-100': '100 per sida',
                'page-all': 'Visa alla',

                // Table headers
                'th-rank': 'Rang',
                'th-product': 'Produkt',
                'th-type': 'Typ',
                'th-apk': 'APK',
                'th-price': 'Pris',
                'th-volume': 'Volym',
                'th-alcohol': 'Alkohol',

                // Status messages
                'loading': 'Laddar data...',
                'showing-simple': 'Visar {count} av {total} produkter',
                'showing-paged': 'Visar {start}-{end} av {count} produkter (Sida {page}/{totalPages})',
                'load-error': 'Misslyckades att ladda data: {error}',

                // Units
                'currency': 'kr',
                'volume-unit': 'ml',
                'alcohol-unit': '%'
            }
        };

        this.elementMap = {
            // Direct text content
            'h1': 'page-title',
            'header p': 'page-subtitle',
            '.products-section h2': 'products-heading',
            '#loading': 'loading',

            // Placeholder attributes
            '#search-input': { attr: 'placeholder', key: 'search-placeholder' },

            // Table headers (by position)
            '.products-table th:nth-child(1)': 'th-rank',
            '.products-table th:nth-child(2)': 'th-product',
            '.products-table th:nth-child(3)': 'th-type',
            '.products-table th:nth-child(4)': 'th-apk',
            '.products-table th:nth-child(5)': 'th-price',
            '.products-table th:nth-child(6)': 'th-volume',
            '.products-table th:nth-child(7)': 'th-alcohol'
        };
    }

    init() {
        this.createToggleButton();
        this.updateLanguage();
    }

    createToggleButton() {
        const button = document.createElement('button');
        button.id = 'language-toggle';
        button.className = 'language-toggle';
        button.innerHTML = '🇬🇧'; // Start with English flag
        button.addEventListener('click', () => this.toggleLanguage());

        // Add to controls area
        const controls = document.querySelector('.controls');
        if (controls) {
            controls.appendChild(button);
        }
    }

    toggleLanguage() {
        this.currentLanguage = this.currentLanguage === 'en' ? 'sv' : 'en';
        this.updateLanguage();

        // Update button flag
        const button = document.getElementById('language-toggle');
        button.innerHTML = this.currentLanguage === 'en' ? '🇬🇧' : '🇸🇪';
    }

    updateLanguage() {
        const texts = this.translations[this.currentLanguage];

        // Update direct text elements
        Object.entries(this.elementMap).forEach(([selector, config]) => {
            const elements = document.querySelectorAll(selector);

            elements.forEach(element => {
                if (typeof config === 'string') {
                    // Direct text replacement
                    element.textContent = texts[config];
                } else if (config.attr) {
                    // Attribute replacement
                    element.setAttribute(config.attr, texts[config.key]);
                }
            });
        });

        // Update dropdown options
        this.updateDropdownOptions();

        // Store language preference
        localStorage.setItem('apk-language', this.currentLanguage);
    }

    updateDropdownOptions() {
        const texts = this.translations[this.currentLanguage];

        // Update type filter first option
        const typeFilter = document.getElementById('type-filter');
        if (typeFilter && typeFilter.options[0]) {
            typeFilter.options[0].textContent = texts['filter-all-types'];
        }

        // Update page size options
        const pageSize = document.getElementById('page-size');
        if (pageSize) {
            pageSize.options[0].textContent = texts['page-25'];
            pageSize.options[1].textContent = texts['page-50'];
            pageSize.options[2].textContent = texts['page-100'];
            pageSize.options[3].textContent = texts['page-all'];
        }
    }

    // Method to get translated text (for dynamic content)
    getText(key, params = {}) {
        let text = this.translations[this.currentLanguage][key] || key;

        // Replace parameters like {count}, {total}, etc.
        Object.entries(params).forEach(([param, value]) => {
            text = text.replace(`{${param}}`, value);
        });

        return text;
    }

    // Load saved language preference
    loadSavedLanguage() {
        const saved = localStorage.getItem('apk-language');
        if (saved && this.translations[saved]) {
            this.currentLanguage = saved;
        }
    }
}

// Global instance
let languageToggle;

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    languageToggle = new LanguageToggle();
    languageToggle.loadSavedLanguage();
    languageToggle.init();
});
