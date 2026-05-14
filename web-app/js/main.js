// Theme Toggle
const themeToggle = document.getElementById('themeToggle');
const themeColorMeta = document.getElementById('themeColorMeta');
const html = document.documentElement;
const mainContent = document.getElementById('main-content');

function prefersReducedMotion() {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

function syncThemeColor(theme) {
    if (!themeColorMeta) return;
    themeColorMeta.setAttribute('content', theme === 'light' ? '#f8fafc' : '#0f172a');
}

function updateThemeToggleAria(isLightTheme) {
    themeToggle.setAttribute(
        'aria-label',
        isLightTheme ? 'Switch to dark mode' : 'Switch to light mode'
    );
}

themeToggle.addEventListener('click', () => {
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';

    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    syncThemeColor(newTheme);

    themeToggle.innerHTML =
        newTheme === 'light'
            ? '<i class="fas fa-sun" aria-hidden="true"></i>'
            : '<i class="fas fa-moon" aria-hidden="true"></i>';
    updateThemeToggleAria(newTheme === 'light');
});

const savedTheme = localStorage.getItem('theme') || 'dark';
html.setAttribute('data-theme', savedTheme);
syncThemeColor(savedTheme);
themeToggle.innerHTML =
    savedTheme === 'light'
        ? '<i class="fas fa-sun" aria-hidden="true"></i>'
        : '<i class="fas fa-moon" aria-hidden="true"></i>';
updateThemeToggleAria(savedTheme === 'light');

// Category Filtering (tabs)
const tabs = Array.from(document.querySelectorAll('.tab[role="tab"]'));
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

function applyCategoryFilter(category) {
    projectCards.forEach((card) => {
        if (category === 'all' || card.getAttribute('data-category') === category) {
            card.style.display = 'block';
            if (!prefersReducedMotion()) {
                card.style.animation = 'fadeIn 0.6s ease';
            } else {
                card.style.animation = 'none';
            }
        } else {
            card.style.display = 'none';
        }
    });
}

function moveTabFocus(fromIndex, delta) {
    const len = tabs.length;
    const next = (fromIndex + delta + len) % len;
    tabs.forEach((t, i) => {
        const selected = i === next;
        t.classList.toggle('active', selected);
        t.setAttribute('aria-selected', selected ? 'true' : 'false');
        t.setAttribute('tabindex', selected ? '0' : '-1');
    });
    tabs[next].focus();
    applyCategoryFilter(tabs[next].getAttribute('data-category'));
}

tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => {
        tabs.forEach((t, i) => {
            const selected = t === tab;
            t.classList.toggle('active', selected);
            t.setAttribute('aria-selected', selected ? 'true' : 'false');
            t.setAttribute('tabindex', selected ? '0' : '-1');
        });
        applyCategoryFilter(tab.getAttribute('data-category'));
    });

    tab.addEventListener('keydown', (e) => {
        let handled = false;
        if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
            moveTabFocus(index, 1);
            handled = true;
        } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
            moveTabFocus(index, -1);
            handled = true;
        } else if (e.key === 'Home') {
            moveTabFocus(index, -index);
            handled = true;
        } else if (e.key === 'End') {
            moveTabFocus(index, tabs.length - 1 - index);
            handled = true;
        }
        if (handled) {
            e.preventDefault();
        }
    });
});

// Initialize
renderRecentSearches();

// Modal Management
const modal = document.getElementById('projectModal');
const modalClose = document.getElementById('modalClose');
const modalBody = document.getElementById('modalBody');
const modalDialogTitle = document.getElementById('modalDialogTitle');

let lastFocusedElement = null;
let modalTabTrapHandler = null;

function getFocusableElements(root) {
    const selector =
        'button:not([disabled]), [href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';
    return Array.from(root.querySelectorAll(selector)).filter(
        (el) => !el.closest('[aria-hidden="true"]') && !el.classList.contains('visually-hidden')
    );
}

function focusModalInitial() {
    const bodyFocusables = getFocusableElements(modalBody);
    if (bodyFocusables.length > 0) {
        bodyFocusables[0].focus();
    } else {
        modalClose.focus();
    }
}

function attachModalFocusTrap() {
    if (modalTabTrapHandler) {
        document.removeEventListener('keydown', modalTabTrapHandler, true);
    }
    modalTabTrapHandler = (e) => {
        if (e.key !== 'Tab' || !modal.classList.contains('active')) return;
        const modalContentEl = modal.querySelector('.modal-content');
        const focusables = getFocusableElements(modalContentEl);
        if (focusables.length === 0) return;
        const first = focusables[0];
        const last = focusables[focusables.length - 1];
        if (e.shiftKey) {
            if (document.activeElement === first) {
                e.preventDefault();
                last.focus();
            }
        } else if (document.activeElement === last) {
            e.preventDefault();
            first.focus();
        }
    };
    document.addEventListener('keydown', modalTabTrapHandler, true);
}

function setMainInert(isInert) {
    if (!mainContent) return;
    if (isInert) {
        mainContent.setAttribute('inert', '');
    } else {
        mainContent.removeAttribute('inert');
    }
}

function closeModal() {
    if (!modal.classList.contains('active')) return;
    modal.classList.remove('active');
    modal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
    setMainInert(false);

    const iframe = modalBody.querySelector('iframe');
    if (iframe) {
        iframe.remove();
    }

    if (modalTabTrapHandler) {
        document.removeEventListener('keydown', modalTabTrapHandler, true);
        modalTabTrapHandler = null;
    }

    if (lastFocusedElement && typeof lastFocusedElement.focus === 'function') {
        lastFocusedElement.focus();
    }
    lastFocusedElement = null;
}

modalClose.addEventListener('click', closeModal);

modal.addEventListener('click', (e) => {
    if (e.target === modal) {
        closeModal();
    }
});

document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.classList.contains('active')) {
        e.preventDefault();
        closeModal();
    }
});

projectCards.forEach((card) => {
    const playButton = card.querySelector('.btn-play');
    const titleText = card.querySelector('h3')?.textContent?.trim() || 'project';
    playButton.setAttribute('aria-label', `Open ${titleText}`);

    playButton.addEventListener('click', (e) => {
        e.stopPropagation();
        const projectName = card.getAttribute('data-project');
        openProject(projectName, playButton);
    });

    card.addEventListener('click', () => {
        const projectName = card.getAttribute('data-project');
        openProject(projectName, card);
    });
});

function openProject(projectName, triggerElement) {
    lastFocusedElement = triggerElement || document.activeElement;
    modalDialogTitle.textContent = formatProjectTitle(projectName, triggerElement);
    modal.classList.add('active');
    modal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    setMainInert(true);

    loadProjectContent(projectName);

    requestAnimationFrame(() => {
        focusModalInitial();
        attachModalFocusTrap();
    });
}

function formatProjectTitle(projectName, triggerElement) {
    if (triggerElement) {
        const card = triggerElement.closest('.project-card');
        const h3 = card?.querySelector('h3');
        if (h3?.textContent) return h3.textContent.trim();
    }
    return projectName
        .split('-')
        .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
        .join(' ');
}

function loadProjectContent(projectName) {
    const projectContent = getProjectHTML(projectName);
    modalBody.innerHTML = projectContent;
    initializeProject(projectName);
}

// Smooth scroll (respects reduced motion)
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: prefersReducedMotion() ? 'auto' : 'smooth'
            });
        }
    });
});

// Add entrance animation on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    if (prefersReducedMotion()) return;
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            entry.target.style.animation = 'fadeInUp 0.6s ease';
        }
    });
}, observerOptions);

projectCards.forEach((card) => observer.observe(card));
