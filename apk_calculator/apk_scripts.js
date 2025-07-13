// APK Calculator JavaScript

let allProducts = [];
let filteredProducts = [];
let summaryData = {};

// Load data on page load
document.addEventListener('DOMContentLoaded', async function() {
    await loadData();
});

async function loadData() {
    try {
        // Load products data
        const productsResponse = await fetch('current_data.json');
        if (!productsResponse.ok) throw new Error('Failed to load products data');
        allProducts = await productsResponse.json();

        // Load summary data
        try {
            const summaryResponse = await fetch('scan_summary.json');
            if (summaryResponse.ok) {
                summaryData = await summaryResponse.json();
                displaySummary();
            }
        } catch (e) {
            console.log('Summary data not available');
        }

        // Initialize display
        populateTypeFilter();
        filteredProducts = [...allProducts];
        displayProducts();
        updateResultsCount();

        document.getElementById('loading').style.display = 'none';
        document.getElementById('products-table').style.display = 'table';

    } catch (error) {
        showError('Failed to load data: ' + error.message);
    }
}

function displaySummary() {
    if (!summaryData) return;

    document.getElementById('total-products').textContent = summaryData.total_processed || '-';
    document.getElementById('scan-date').textContent = summaryData.scan_date || '-';
    document.getElementById('avg-apk').textContent = summaryData.average_apk || '-';
    document.getElementById('faulty-count').textContent = summaryData.faulty_entries || '-';

    // Display top 3 products
    const topProductsContainer = document.getElementById('top-products');
    if (summaryData.top_3_products) {
        topProductsContainer.innerHTML = summaryData.top_3_products.map((product, index) => `
            <div class="top-product-card">
                <strong>#${index + 1} Best Value</strong>
                <div style="margin-top: 5px;">${product}</div>
            </div>
        `).join('');
    }

    document.getElementById('summary-section').style.display = 'block';
}

function populateTypeFilter() {
    const types = [...new Set(allProducts.map(p => p.type))].sort();
    const typeFilter = document.getElementById('type-filter');

    types.forEach(type => {
        const option = document.createElement('option');
        option.value = type;
        option.textContent = type;
        typeFilter.appendChild(option);
    });
}

function displayProducts() {
    const tbody = document.getElementById('products-tbody');
    tbody.innerHTML = '';

    filteredProducts.forEach(product => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><span class="rank-badge">${product.rank}</span></td>
            <td>
                <div class="product-name">${product.name}</div>
            </td>
            <td><span class="product-type">${product.type}</span></td>
            <td><span class="apk-value">${product.apk}</span></td>
            <td>${product.price} kr</td>
            <td>${product.volume} ml</td>
            <td>${product.alcohol_content}%</td>
        `;
        tbody.appendChild(row);
    });
}

function filterProducts() {
    const searchTerm = document.getElementById('search-input').value.toLowerCase();
    const typeFilter = document.getElementById('type-filter').value;

    filteredProducts = allProducts.filter(product => {
        const matchesSearch = product.name.toLowerCase().includes(searchTerm);
        const matchesType = !typeFilter || product.type === typeFilter;
        return matchesSearch && matchesType;
    });

    displayProducts();
    updateResultsCount();
}

function updateResultsCount() {
    const count = filteredProducts.length;
    const total = allProducts.length;
    document.getElementById('results-count').textContent =
        `Showing ${count} of ${total} products`;
}

function showError(message) {
    document.getElementById('loading').style.display = 'none';
    document.getElementById('error-message').textContent = message;
    document.getElementById('error-message').style.display = 'block';
}

// Event listeners
document.getElementById('search-input').addEventListener('input', filterProducts);
document.getElementById('type-filter').addEventListener('change', filterProducts);
