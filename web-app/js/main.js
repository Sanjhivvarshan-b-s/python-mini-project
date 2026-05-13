// Theme Toggle
const themeToggle = document.getElementById('themeToggle');
const html = document.documentElement;

themeToggle.addEventListener('click', () => {
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    
    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    
    // Update icon
    themeToggle.innerHTML = newTheme === 'light' 
        ? '<i class="fas fa-sun"></i>' 
        : '<i class="fas fa-moon"></i>';
});

// Load saved theme
const savedTheme = localStorage.getItem('theme') || 'dark';
html.setAttribute('data-theme', savedTheme);
themeToggle.innerHTML = savedTheme === 'light' 
    ? '<i class="fas fa-sun"></i>' 
    : '<i class="fas fa-moon"></i>';

// ===== MODERN SEARCH FUNCTIONALITY =====

// State Management
let currentCategory = 'all';
let currentSearchQuery = '';
let selectedSuggestionIndex = -1;
let recentSearches = JSON.parse(localStorage.getItem('recentSearches')) || [];

const projectCards = document.querySelectorAll('.project-card');
const tabs = document.querySelectorAll('.tab');
const searchInput = document.getElementById('projectSearch');
const searchClear = document.getElementById('searchClear');
const searchDropdown = document.getElementById('searchDropdown');
const searchShortcut = document.getElementById('searchShortcut');
const searchLoader = document.getElementById('searchLoader');
const emptyState = document.getElementById('emptyState');
const resultsList = document.getElementById('resultsList');
const resultsSection = document.getElementById('resultsSection');
const recentSearchesList = document.getElementById('recentSearchesList');
const recentSearchesSection = document.getElementById('recentSearchesSection');
const tipsSection = document.getElementById('tipsSection');

// Debounce function for smooth search performance
function debounce(func, delay) {
    let timeoutId;
    return function (...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func(...args), delay);
    };
}

// Get all matching projects for search query
function getMatchingProjects(query) {
    if (!query) return [];
    
    const matches = [];
    projectCards.forEach(card => {
        const category = card.getAttribute('data-category');
        const title = card.querySelector('h3').textContent.toLowerCase();
        const description = card.querySelector('p').textContent.toLowerCase();
        const tags = (card.getAttribute('data-tags') || '').toLowerCase();
        
        const categoryMatch = currentCategory === 'all' || category === currentCategory;
        const searchMatch = title.includes(query) || 
                           description.includes(query) || 
                           tags.includes(query);
        
        if (categoryMatch && searchMatch) {
            const project = {
                card: card,
                title: card.querySelector('h3').textContent,
                tags: card.getAttribute('data-tags') || '',
                category: category
            };
            matches.push(project);
        }
    });
    
    return matches;
}

// Render autocomplete suggestions
function renderSuggestions(query) {
    if (!query) {
        renderRecentSearches();
        return;
    }
    
    const matches = getMatchingProjects(query);
    
    if (matches.length === 0) {
        resultsSection.style.display = 'none';
        recentSearchesSection.style.display = 'none';
        tipsSection.style.display = 'block';
        return;
    }
    
    resultsList.innerHTML = '';
    matches.slice(0, 8).forEach((project, index) => {
        const item = document.createElement('div');
        item.className = 'dropdown-item' + (index === selectedSuggestionIndex ? ' selected' : '');
        item.innerHTML = `
            <div class="dropdown-item-icon">
                ${project.card.querySelector('.card-icon').textContent}
            </div>
            <div class="dropdown-item-text">${highlightMatch(project.title, query)}</div>
            <span class="dropdown-item-tag">${project.category}</span>
        `;
        item.addEventListener('click', () => selectSuggestion(project.title));
        item.addEventListener('mouseenter', () => {
            selectedSuggestionIndex = index;
            updateSuggestionHighlight();
        });
        resultsList.appendChild(item);
    });
    
    resultsSection.style.display = 'block';
    recentSearchesSection.style.display = 'none';
    tipsSection.style.display = 'none';
    selectedSuggestionIndex = -1;
}

// Highlight matching text in suggestions
function highlightMatch(text, query) {
    const parts = text.split(new RegExp(`(${query})`, 'gi'));
    return parts.map(part => 
        part.toLowerCase() === query.toLowerCase() 
            ? `<mark style="background: rgba(99, 102, 241, 0.3); color: var(--primary-color); font-weight: 600;">${part}</mark>`
            : part
    ).join('');
}

// Render recent searches
function renderRecentSearches() {
    if (recentSearches.length === 0) {
        recentSearchesSection.style.display = 'none';
        tipsSection.style.display = 'block';
        resultsSection.style.display = 'none';
        return;
    }
    
    recentSearchesList.innerHTML = '';
    recentSearches.slice(0, 5).forEach((search) => {
        const item = document.createElement('div');
        item.className = 'dropdown-recent-item';
        item.innerHTML = `
            <div class="dropdown-recent-text">
                <i class="fas fa-history" style="opacity: 0.5; font-size: 0.9rem;"></i>
                <span style="flex: 1; cursor: pointer; color: var(--text-secondary);">${search}</span>
            </div>
            <button class="dropdown-recent-remove" aria-label="Remove search">
                <i class="fas fa-x"></i>
            </button>
        `;
        
        const textElement = item.querySelector('span');
        const removeBtn = item.querySelector('.dropdown-recent-remove');
        
        textElement.addEventListener('click', () => {
            searchInput.value = search;
            currentSearchQuery = search;
            performSearch();
            closeDropdown();
        });
        
        removeBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            recentSearches = recentSearches.filter(s => s !== search);
            localStorage.setItem('recentSearches', JSON.stringify(recentSearches));
            renderRecentSearches();
        });
        
        recentSearchesList.appendChild(item);
    });
    
    recentSearchesSection.style.display = 'block';
    resultsSection.style.display = 'none';
    tipsSection.style.display = 'block';
}

// Select suggestion
function selectSuggestion(query) {
    searchInput.value = query;
    currentSearchQuery = query.toLowerCase().trim();
    performSearch();
    closeDropdown();
}

// Update suggestion highlight
function updateSuggestionHighlight() {
    const items = resultsList.querySelectorAll('.dropdown-item');
    items.forEach((item, index) => {
        item.classList.toggle('selected', index === selectedSuggestionIndex);
    });
}

// Close dropdown
function closeDropdown() {
    searchDropdown.style.display = 'none';
    selectedSuggestionIndex = -1;
}

// Perform search and filter projects
function performSearch() {
    let visibleCount = 0;
    
    projectCards.forEach(card => {
        const category = card.getAttribute('data-category');
        const title = card.querySelector('h3').textContent.toLowerCase();
        const description = card.querySelector('p').textContent.toLowerCase();
        const tags = (card.getAttribute('data-tags') || '').toLowerCase();
        
        const categoryMatch = currentCategory === 'all' || category === currentCategory;
        const searchMatch = currentSearchQuery === '' || 
                           title.includes(currentSearchQuery) || 
                           description.includes(currentSearchQuery) || 
                           tags.includes(currentSearchQuery);
        
        if (categoryMatch && searchMatch) {
            card.style.display = 'block';
            card.style.animation = 'fadeIn 0.6s ease';
            visibleCount++;
        } else {
            card.style.display = 'none';
        }
    });
    
    // Show/hide empty state
    if (visibleCount === 0 && currentSearchQuery) {
        emptyState.style.display = 'block';
    } else {
        emptyState.style.display = 'none';
    }
}

// Add recent search
function addToRecentSearches(query) {
    if (!query) return;
    
    recentSearches = recentSearches.filter(s => s !== query);
    recentSearches.unshift(query);
    if (recentSearches.length > 10) recentSearches.pop();
    localStorage.setItem('recentSearches', JSON.stringify(recentSearches));
}

// Debounced search handler
const debouncedSearch = debounce((query) => {
    renderSuggestions(query);
    searchLoader.style.display = 'none';
}, 300);

// Search input event listener
searchInput.addEventListener('input', (e) => {
    currentSearchQuery = e.target.value.toLowerCase().trim();
    
    // Show/hide elements
    searchClear.style.display = currentSearchQuery ? 'flex' : 'none';
    searchShortcut.style.display = currentSearchQuery ? 'none' : 'flex';
    
    if (currentSearchQuery) {
        searchDropdown.style.display = 'block';
        searchLoader.style.display = 'flex';
        debouncedSearch(currentSearchQuery);
    } else {
        renderRecentSearches();
        searchDropdown.style.display = 'block';
        searchLoader.style.display = 'none';
    }
    
    performSearch();
});

// Search focus event
searchInput.addEventListener('focus', () => {
    if (currentSearchQuery === '' && recentSearches.length > 0) {
        renderRecentSearches();
    } else if (currentSearchQuery) {
        renderSuggestions(currentSearchQuery);
    } else {
        renderRecentSearches();
    }
    searchDropdown.style.display = 'block';
});

// Clear button
searchClear.addEventListener('click', () => {
    searchInput.value = '';
    currentSearchQuery = '';
    searchClear.style.display = 'none';
    searchShortcut.style.display = 'flex';
    closeDropdown();
    performSearch();
    searchInput.focus();
});

// Keyboard navigation in dropdown
searchInput.addEventListener('keydown', (e) => {
    const items = resultsList.querySelectorAll('.dropdown-item');
    
    if (e.key === 'ArrowDown') {
        e.preventDefault();
        selectedSuggestionIndex = Math.min(selectedSuggestionIndex + 1, items.length - 1);
        updateSuggestionHighlight();
    } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        selectedSuggestionIndex = Math.max(selectedSuggestionIndex - 1, -1);
        updateSuggestionHighlight();
    } else if (e.key === 'Enter' && selectedSuggestionIndex >= 0) {
        e.preventDefault();
        items[selectedSuggestionIndex].click();
    } else if (e.key === 'Escape') {
        closeDropdown();
    }
});

// Close dropdown on outside click
document.addEventListener('click', (e) => {
    if (!searchDropdown.contains(e.target) && e.target !== searchInput) {
        closeDropdown();
    }
});

// Keyboard shortcut: Cmd+K or Ctrl+K
document.addEventListener('keydown', (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        searchInput.focus();
    }
});

// Category filtering
tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        tabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        
        currentCategory = tab.getAttribute('data-category');
        performSearch();
        
        // Re-render suggestions if dropdown is open
        if (searchDropdown.style.display === 'block' && currentSearchQuery) {
            renderSuggestions(currentSearchQuery);
        }
    });
});

// Initialize
renderRecentSearches();

// Modal Management
const modal = document.getElementById('projectModal');
const modalClose = document.getElementById('modalClose');
const modalBody = document.getElementById('modalBody');

// Close modal
modalClose.addEventListener('click', () => {
    modal.classList.remove('active');
    // Clean up any intervals/animations
    const iframe = modalBody.querySelector('iframe');
    if (iframe) {
        iframe.remove();
    }
});

// Close on outside click
modal.addEventListener('click', (e) => {
    if (e.target === modal) {
        modal.classList.remove('active');
    }
});

// Close on Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.classList.contains('active')) {
        modal.classList.remove('active');
    }
});

// Open Project Modal
projectCards.forEach(card => {
    const playButton = card.querySelector('.btn-play');
    
    playButton.addEventListener('click', (e) => {
        e.stopPropagation();
        const projectName = card.getAttribute('data-project');
        openProject(projectName);
    });
    
    card.addEventListener('click', () => {
        const projectName = card.getAttribute('data-project');
        openProject(projectName);
    });
});

function openProject(projectName) {
    modal.classList.add('active');
    loadProjectContent(projectName);
}

function loadProjectContent(projectName) {
    // This will be populated by projects.js
    const projectContent = getProjectHTML(projectName);
    modalBody.innerHTML = projectContent;
    
    // Initialize project-specific JavaScript
    initializeProject(projectName);
}

// Smooth scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// Add entrance animation on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.animation = 'fadeInUp 0.6s ease';
        }
    });
}, observerOptions);

projectCards.forEach(card => observer.observe(card));
