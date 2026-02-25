// Mobile Main Orchestrator
const MobileMain = {
    state: {
        currentView: 'bubbles',
        activeFilters: {},
        filteredCreators: [],
        allCreators: []
    },

    async init() {
        try {
            // Show loading screen
            this.showLoading();

            // Load data
            console.log('Loading creator data...');
            const creators = await DataLoader.loadData();
            this.state.allCreators = creators;
            this.state.filteredCreators = creators;

            console.log(`Loaded ${creators.length} creators`);

            // Initialize all modules
            console.log('Initializing modules...');

            BubbleViz.init('#bubble-canvas', creators);
            TagCloud.init();
            SwipeCards.init(DataLoader.getTopicGroups());
            BottomSheet.init();

            // Setup event listeners
            this.setupEventListeners();

            // Hide loading screen
            setTimeout(() => {
                this.hideLoading();
            }, 1000);

            console.log('App initialized successfully!');

        } catch (error) {
            console.error('Error initializing app:', error);
            this.showError('Failed to load data. Please refresh the page.');
        }
    },

    setupEventListeners() {
        // Filter button
        document.getElementById('filter-button').addEventListener('click', () => {
            TagCloud.show();
        });

        // View switcher
        document.getElementById('view-switcher').addEventListener('click', () => {
            this.toggleView();
        });

        // Info button
        document.getElementById('info-button').addEventListener('click', () => {
            this.showInfo();
        });

        // Close info
        document.getElementById('close-info').addEventListener('click', () => {
            this.hideInfo();
        });

        // Handle browser back button
        window.addEventListener('popstate', () => {
            this.handleBackButton();
        });
    },

    toggleView() {
        if (this.state.currentView === 'bubbles') {
            // Switch to cards view
            this.state.currentView = 'cards';
            SwipeCards.show();

            // Update button icon
            document.querySelector('#view-switcher .material-icons').textContent = 'bubble_chart';

        } else {
            // Switch to bubbles view
            this.state.currentView = 'bubbles';
            SwipeCards.hide();

            // Update button icon
            document.querySelector('#view-switcher .material-icons').textContent = 'dashboard';
        }
    },

    handleFilterChange() {
        // Get active filters from tag cloud
        const filters = TagCloud.getActiveFilters();
        this.state.activeFilters = filters;

        // Filter creators
        const filteredCreators = DataLoader.filterCreators(filters);
        this.state.filteredCreators = filteredCreators;

        // Update bubble visualization
        BubbleViz.updateBubbles(filteredCreators);

        // Update creator count badge
        this.updateCreatorCount(filteredCreators.length);

        // Debounce for performance
        this.debounce(() => {
            console.log(`Filtered to ${filteredCreators.length} creators`);
        }, 150)();
    },

    applyTopicFilter(topicName) {
        // Clear existing filters
        TagCloud.clearFilters();

        // Apply topic filter
        TagCloud.activeFilters.groups = [topicName];

        // Manually update the tag visual state
        const tags = document.querySelectorAll('.tag.primary');
        tags.forEach(tag => {
            if (tag.dataset.name === topicName) {
                tag.classList.add('active');
            }
        });

        TagCloud.updateActiveFiltersDisplay();

        // Apply filter
        this.handleFilterChange();
    },

    updateCreatorCount(count) {
        const badge = document.getElementById('creator-count');
        badge.textContent = `${count} Creator${count !== 1 ? 's' : ''}`;
    },

    showInfo() {
        const overlay = document.getElementById('info-overlay');
        overlay.classList.remove('hidden');
    },

    hideInfo() {
        const overlay = document.getElementById('info-overlay');
        overlay.classList.add('hidden');
    },

    showLoading() {
        const loadingScreen = document.getElementById('loading-screen');
        loadingScreen.classList.remove('hidden');
    },

    hideLoading() {
        const loadingScreen = document.getElementById('loading-screen');
        loadingScreen.classList.add('hidden');
    },

    showError(message) {
        const loadingScreen = document.getElementById('loading-screen');
        const loadingContent = loadingScreen.querySelector('.loading-content');

        loadingContent.innerHTML = `
            <div class="loading-logo">⚠️</div>
            <div class="loading-text">${message}</div>
        `;
    },

    handleBackButton() {
        // Close any open overlays when back button is pressed
        if (!document.getElementById('tag-cloud-overlay').classList.contains('hidden')) {
            TagCloud.hide();
        } else if (!document.getElementById('swipe-cards-view').classList.contains('hidden')) {
            SwipeCards.hide();
        } else if (!document.getElementById('bottom-sheet').classList.contains('hidden')) {
            BottomSheet.hide();
        } else if (!document.getElementById('info-overlay').classList.contains('hidden')) {
            this.hideInfo();
        }
    },

    // Utility functions
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    throttle(func, limit) {
        let inThrottle;
        return function(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
};

// Initialize app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        MobileMain.init();
    });
} else {
    MobileMain.init();
}

// Expose to window for debugging
window.MobileMain = MobileMain;
