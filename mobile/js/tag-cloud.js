// Tag Cloud Filter Module
const TagCloud = {
    container: null,
    activeFilters: {
        groups: [],
        platforms: [],
        geography: []
    },
    topicGroups: [],
    platforms: [],

    init(containerData) {
        this.container = document.getElementById('tag-cloud-container');
        this.topicGroups = DataLoader.getTopicGroups();
        this.platforms = Array.from(DataLoader.platforms).sort();

        this.render();
        this.setupEventListeners();
    },

    render() {
        this.container.innerHTML = '';

        // Render topic groups (primary tags)
        this.topicGroups.forEach(topic => {
            const tag = this.createTag(
                topic.name,
                topic.count,
                'primary',
                'groups'
            );
            this.container.appendChild(tag);
        });

        // Render platforms (secondary tags)
        this.platforms.forEach(platform => {
            const count = DataLoader.creators.filter(c =>
                c.platforms.includes(platform)
            ).length;

            const tag = this.createTag(
                platform,
                count,
                'secondary',
                'platforms'
            );
            this.container.appendChild(tag);
        });
    },

    createTag(name, count, type, filterType) {
        const tag = document.createElement('div');
        tag.className = `tag ${type}`;
        tag.dataset.name = name;
        tag.dataset.filterType = filterType;

        tag.innerHTML = `
            ${name}
            <span class="tag-count">(${count})</span>
        `;

        tag.addEventListener('click', () => this.toggleTag(name, filterType, tag));

        return tag;
    },

    toggleTag(name, filterType, element) {
        const filterArray = this.activeFilters[filterType];
        const index = filterArray.indexOf(name);

        if (index > -1) {
            // Remove filter
            filterArray.splice(index, 1);
            element.classList.remove('active');
        } else {
            // Add filter
            filterArray.push(name);
            element.classList.add('active');
        }

        this.updateActiveFiltersDisplay();
        this.notifyFilterChange();
    },

    updateActiveFiltersDisplay() {
        const activeFiltersContainer = document.getElementById('active-filters');
        activeFiltersContainer.innerHTML = '';

        // Combine all active filters
        const allFilters = [
            ...this.activeFilters.groups,
            ...this.activeFilters.platforms,
            ...this.activeFilters.geography
        ];

        allFilters.forEach(filterName => {
            const pill = document.createElement('div');
            pill.className = 'filter-pill';
            pill.innerHTML = `
                ${filterName}
                <span class="material-icons" data-filter="${filterName}">close</span>
            `;

            pill.querySelector('.material-icons').addEventListener('click', () => {
                this.removeFilter(filterName);
            });

            activeFiltersContainer.appendChild(pill);
        });
    },

    removeFilter(name) {
        // Find and remove from all filter arrays
        ['groups', 'platforms', 'geography'].forEach(filterType => {
            const index = this.activeFilters[filterType].indexOf(name);
            if (index > -1) {
                this.activeFilters[filterType].splice(index, 1);

                // Update tag visual state
                const tag = this.container.querySelector(`[data-name="${name}"]`);
                if (tag) {
                    tag.classList.remove('active');
                }
            }
        });

        this.updateActiveFiltersDisplay();
        this.notifyFilterChange();
    },

    clearFilters() {
        this.activeFilters = {
            groups: [],
            platforms: [],
            geography: []
        };

        // Remove active class from all tags
        this.container.querySelectorAll('.tag.active').forEach(tag => {
            tag.classList.remove('active');
        });

        this.updateActiveFiltersDisplay();
        this.notifyFilterChange();
    },

    notifyFilterChange() {
        // Call mobile main to update visualization
        if (window.MobileMain) {
            MobileMain.handleFilterChange();
        }
    },

    getActiveFilters() {
        return this.activeFilters;
    },

    show() {
        const overlay = document.getElementById('tag-cloud-overlay');
        overlay.classList.remove('hidden');
    },

    hide() {
        const overlay = document.getElementById('tag-cloud-overlay');
        overlay.classList.add('hidden');
    },

    setupEventListeners() {
        // Close button
        document.getElementById('close-tag-cloud').addEventListener('click', () => {
            this.hide();
        });

        // Clear filters button
        document.getElementById('clear-filters').addEventListener('click', () => {
            this.clearFilters();
        });
    }
};
