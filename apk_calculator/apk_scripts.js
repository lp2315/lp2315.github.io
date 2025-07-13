// APK Calculator JavaScript - Clean Version

let allProducts = [];
let filteredProducts = [];
let currentPage = 1;

// Load data on page load
document.addEventListener('DOMContentLoaded', async function() {
    await loadProductData();

    // Set up event listeners after DOM is ready
    document.getElementById('search-input').addEventListener('input', filterProducts);
    document.getElementById('type-filter').addEventListener('change', filterProducts);
    document.getElementById('page-size').addEventListener('change', function() {
        currentPage = 1;
        displayProducts();
        updateResultsCount();
    });

    // Pagination event listeners
    document.getElementById('prev-page').addEventListener('click', () => changePage('prev'));
    document.getElementById('next-page').addEventListener('click', () => changePage('next'));

    // Initialize smooth scrolling
    initSmoothScrolling();
});

async function loadProductData() {
    try {
        const response = await fetch('processed_systembolaget_data.json');
        if (!response.ok) throw new Error('Failed to load product data');
        allProducts = await response.json();

        // Initialize display
        populateTypeFilter();
        filteredProducts = [...allProducts];
        displayProducts();
        updateResultsCount();

        // Show table and hide loading
        document.getElementById('loading').style.display = 'none';
        document.getElementById('products-table').style.display = 'table';

    } catch (error) {
        showError('Failed to load data: ' + error.message);
    }
}

// Formatting functions
function formatPrice(price) {
    return price.toFixed(2).replace('.', ':');
}

function formatAlcohol(alcohol) {
    return alcohol.toString().replace('.', ',') + '%';
}

function formatAPK(apk) {
    return apk.toFixed(2);
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
    const pageSizeElement = document.getElementById('page-size');

    if (!tbody || !pageSizeElement) {
        return; // DOM not ready
    }

    tbody.innerHTML = '';

    // Calculate pagination
    const pageSizeValue = pageSizeElement.value;
    let productsToShow;

    if (pageSizeValue === 'all') {
        productsToShow = filteredProducts;
    } else {
        const pageSize = parseInt(pageSizeValue);
        const startIndex = (currentPage - 1) * pageSize;
        const endIndex = startIndex + pageSize;
        productsToShow = filteredProducts.slice(startIndex, endIndex);
    }

    productsToShow.forEach(product => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><span class="rank-badge">${product.rank}</span></td>
            <td>
                <div class="product-name">
                    <a href="${product.url}" target="_blank" class="product-link">${product.name}</a>
                </div>
            </td>
            <td><span class="product-type">${product.type}</span></td>
            <td><span class="apk-value">${formatAPK(product.apk)}</span></td>
            <td>${formatPrice(product.price)} kr</td>
            <td>${product.volume} ml</td>
            <td>${formatAlcohol(product.alcohol_content)}</td>
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

    currentPage = 1; // Reset to first page
    displayProducts();
    updateResultsCount();
}

function updateResultsCount() {
    const count = filteredProducts.length;
    const total = allProducts.length;
    const pageSizeElement = document.getElementById('page-size');
    const paginationControls = document.getElementById('pagination-controls');

    if (!pageSizeElement) return;

    const pageSizeValue = pageSizeElement.value;

    if (pageSizeValue === 'all') {
        document.getElementById('results-count').textContent =
            languageToggle.getText('showing-simple', { count, total });
        paginationControls.style.display = 'none';
    } else {
        const pageSize = parseInt(pageSizeValue);
        const totalPages = Math.ceil(count / pageSize);
        const startIndex = (currentPage - 1) * pageSize + 1;
        const endIndex = Math.min(currentPage * pageSize, count);

        document.getElementById('results-count').textContent =
            languageToggle.getText('showing-paged', {
                start: startIndex,
                end: endIndex,
                count,
                page: currentPage,
                totalPages
            });

        if (totalPages > 1) {
            paginationControls.style.display = 'flex';
            updatePaginationButtons(totalPages);
        } else {
            paginationControls.style.display = 'none';
        }
    }
}

function showError(message) {
    document.getElementById('loading').style.display = 'none';
    const errorText = languageToggle.getText('load-error', { error: message });
    document.getElementById('error-message').textContent = errorText;
    document.getElementById('error-message').style.display = 'block';
}

function updatePaginationButtons(totalPages) {
    const prevButton = document.getElementById('prev-page');
    const nextButton = document.getElementById('next-page');

    prevButton.disabled = currentPage === 1;
    nextButton.disabled = currentPage === totalPages;
}

function changePage(direction) {
    const pageSizeValue = document.getElementById('page-size').value;
    if (pageSizeValue === 'all') return;

    const pageSize = parseInt(pageSizeValue);
    const totalPages = Math.ceil(filteredProducts.length / pageSize);

    if (direction === 'prev' && currentPage > 1) {
        currentPage--;
    } else if (direction === 'next' && currentPage < totalPages) {
        currentPage++;
    }

    displayProducts();
    updateResultsCount();
}

// Smooth scrolling with acceleration
function initSmoothScrolling() {
    let lastScrollTime = 0;
    let scrollVelocity = 0;
    let lastScrollTop = 0;
    let scrollTimeout;

    window.addEventListener('scroll', function() {
        const currentTime = Date.now();
        const currentScrollTop = window.pageYOffset;
        const scrollDistance = Math.abs(currentScrollTop - lastScrollTop);
        const timeDiff = currentTime - lastScrollTime;

        if (timeDiff > 0) {
            scrollVelocity = scrollDistance / timeDiff;
        }

        clearTimeout(scrollTimeout);

        // Add momentum for fast scrolling
        if (scrollVelocity > 2) {
            document.body.style.scrollBehavior = 'auto';
            scrollTimeout = setTimeout(() => {
                document.body.style.scrollBehavior = 'smooth';
            }, 150);
        }

        lastScrollTop = currentScrollTop;
        lastScrollTime = currentTime;
    });
}
