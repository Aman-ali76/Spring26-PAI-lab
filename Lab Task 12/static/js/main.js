// DOM Elements
const searchForm = document.getElementById('searchForm');
const queryInput = document.getElementById('queryInput');
const resultsCount = document.getElementById('resultsCount');
const loadingDiv = document.getElementById('loading');
const resultsSection = document.getElementById('resultsSection');
const resultsContainer = document.getElementById('resultsContainer');
const errorMessage = document.getElementById('errorMessage');
const statsSection = document.getElementById('statsSection');
const statsContent = document.getElementById('statsContent');

// Load stats on page load
document.addEventListener('DOMContentLoaded', loadStats);

// Handle form submission
searchForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const query = queryInput.value.trim();
    
    if (!query) {
        showError('Please enter a search query');
        return;
    }
    
    await searchReviews(query);
});

async function searchReviews(query) {
    hideError();
    loadingDiv.style.display = 'block';
    resultsSection.style.display = 'none';
    
    try {
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: query,
                results: resultsCount.value
            })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Search failed');
        }
        
        const data = await response.json();
        displayResults(data);
    } catch (error) {
        showError(`Error: ${error.message}`);
    } finally {
        loadingDiv.style.display = 'none';
    }
}

function displayResults(data) {
    resultsContainer.innerHTML = '';
    
    if (!data.results || data.results.length === 0) {
        showError('No results found');
        return;
    }
    
    data.results.forEach((result, index) => {
        const stars = '★'.repeat(result.stars) + '☆'.repeat(5 - result.stars);
        const truncated = result.review.length > 200;
        
        const resultCard = document.createElement('div');
        resultCard.className = 'result-card';
        resultCard.innerHTML = `
            <div class="result-header">
                <div class="result-stars">${stars}</div>
                <div class="result-distance">Similarity: ${(1 - result.distance / 100).toFixed(3)}</div>
            </div>
            <div class="result-text ${truncated ? 'truncated' : ''}">
                ${result.review}
            </div>
            ${truncated ? `<button class="btn-expand" onclick="showFullReview('${result.id}', '${escapeHtml(result.full_review)}', ${result.stars})">Read Full Review</button>` : ''}
        `;
        resultsContainer.appendChild(resultCard);
    });
    
    resultsSection.style.display = 'block';
}

async function loadStats() {
    try {
        const response = await fetch('/api/stats');
        
        if (!response.ok) {
            throw new Error('Failed to load stats');
        }
        
        const stats = await response.json();
        displayStats(stats);
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

function displayStats(stats) {
    let starDistHtml = '';
    for (let star = 5; star >= 1; star--) {
        const count = stats.star_distribution[star] || 0;
        starDistHtml += `<div class="star-bar"><div>${star} ★</div><span>${count}</span></div>`;
    }
    
    statsContent.innerHTML = `
        <div class="stat-item">
            <h4>Total Reviews</h4>
            <div class="stat-value">${stats.total_reviews}</div>
        </div>
        <div class="stat-item">
            <h4>Average Rating</h4>
            <div class="stat-value">${stats.avg_stars.toFixed(2)} ★</div>
        </div>
        <div class="stat-item">
            <h4>Rating Distribution</h4>
            <div class="star-dist">
                ${starDistHtml}
            </div>
        </div>
    `;
}

function showFullReview(id, fullReview, stars) {
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.style.display = 'block';
    
    const stars_display = '★'.repeat(stars) + '☆'.repeat(5 - stars);
    
    modal.innerHTML = `
        <div class="modal-content">
            <span class="close" onclick="this.closest('.modal').style.display='none'">&times;</span>
            <h2 style="color: #667eea; margin-bottom: 15px;">Full Review</h2>
            <div style="margin-bottom: 15px; font-size: 1.3rem;">${stars_display}</div>
            <p style="line-height: 1.8; color: #555;">${fullReview}</p>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
            setTimeout(() => modal.remove(), 300);
        }
    });
}

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
}

function hideError() {
    errorMessage.style.display = 'none';
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML.replace(/'/g, "\\'");
}

// Allow Enter key to submit
queryInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        searchForm.dispatchEvent(new Event('submit'));
    }
});
