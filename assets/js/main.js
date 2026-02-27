        // Global state
        let allCreators = [];
        let filteredCreators = [];
        let currentView = 'grid';
        let currentBubbleMode = 'platform';

        // Shared ordered groups list (used in filters and treemap)
        const ORDERED_GROUPS = [
            'Power & Politics',
            'Money & Work',
            'Civic Life',
            'Social Issues',
            'Science, Health & Environment',
            'Culture & Media',
            'Lifestyle & Personal Life',
            'Journalism Formats',
            'General News'
        ];

        // Master abbreviation dictionary for consistent label shortening
        const LABEL_ABBREVIATIONS = {
            // Platforms
            'Newsletter - Substack': 'Substack',
            'Newsletter - Ghost': 'Ghost',
            'Newsletter - Beehiiv': 'Beehiiv',
            'Newsletter - ConvertKit': 'ConvertKit',
            'Newsletter - Medium': 'Medium',
            'Newsletter - Buttondown': 'Buttondown',
            'Video - YouTube': 'YouTube',
            'Video - Instagram': 'Instagram',
            'Video - TikTok': 'TikTok',
            'Video - Vimeo': 'Vimeo',
            'Video - Facebook': 'Facebook',
            'Podcast': 'Podcast',
            'Website': 'Website',
            'Social Media': 'Social',

            // Groups
            'Science, Health & Environment': 'Science & Health',
            'Lifestyle & Personal Life': 'Lifestyle',
            'Power & Politics': 'Politics',
            'Culture & Media': 'Culture',
            'Money & Work': 'Business',
            'Journalism Formats': 'Journalism',
            'General News': 'General',
            'Civic Life': 'Civic',
            'Social Issues': 'Social Issues',

            // Common Topics
            'Entertainment/Hollywood': 'Entertainment',
            'Finance/Economics': 'Finance',
            'Climate/Environment': 'Climate',
            'Local Government/Politics': 'Local Gov',
            'International/Foreign Affairs': 'International',
            'Technology/Innovation': 'Tech',
            'Media/Power': 'Media/Power',
            'Health/Wellness': 'Health',
            'Education': 'Education',
            'Sports': 'Sports',
            'Food/Dining': 'Food',
            'Travel': 'Travel',
            'Real Estate': 'Real Estate',
            'Criminal Justice': 'Justice',
            'Immigration': 'Immigration',

            // Geographies
            'United States': 'US',
            'United Kingdom': 'UK',
            'International': 'Intl'
        };

        // Smart abbreviation function with fallback logic
        function abbreviateLabel(text, maxLength = 15) {
            if (!text) return '';

            // First try dictionary lookup
            if (LABEL_ABBREVIATIONS[text]) {
                const abbrev = LABEL_ABBREVIATIONS[text];
                if (abbrev.length <= maxLength) return abbrev;
            }

            // If text fits, return as-is
            if (text.length <= maxLength) return text;

            // Try to break at word boundary or separator
            const separators = [' - ', ' / ', ' & ', ' ', '-', '/'];
            for (const sep of separators) {
                if (text.includes(sep)) {
                    const parts = text.split(sep);
                    // Take first significant part if it fits
                    if (parts[0].length > 0 && parts[0].length <= maxLength) {
                        return parts[0];
                    }
                }
            }

            // Last resort: smart truncate with ellipsis
            return text.substring(0, maxLength - 1) + '…';
        }

        // Legacy function kept for backward compatibility but uses abbreviateLabel
        function truncateToFit(text, availableWidth, fontSize) {
            fontSize = fontSize || 12;
            const charWidth = fontSize * 0.6; // Approximate for Hanken Grotesk
            const maxChars = Math.max(3, Math.floor((availableWidth - 10) / charWidth));
            return abbreviateLabel(text, maxChars);
        }

        // Centralized Filter State Manager
        class FilterStateManager {
            constructor() {
                this.filters = {
                    group: new Set(),
                    platform: new Set(),
                    geography: new Set(),
                    topic: new Set(),
                    search: ''
                };
            }
            
            // Toggle a filter value (add if not present, remove if present)
            toggle(type, value) {
                if (this.filters[type].has(value)) {
                    this.filters[type].delete(value);
                } else {
                    this.filters[type].add(value);
                }
                this.syncUI(type, value);
                this.applyFilters();
            }

            // Toggle filter without re-rendering views (for in-visualization navigation)
            toggleSilent(type, value) {
                if (this.filters[type].has(value)) {
                    this.filters[type].delete(value);
                } else {
                    this.filters[type].add(value);
                }
                this.syncUI(type, value);
                this.applyFiltersSilent();
            }

            // Apply filters and update counts/URL but skip view re-render
            applyFiltersSilent() {
                filteredCreators = allCreators.filter(creator => {
                    if (this.filters.group.size > 0 && !this.filters.group.has(creator.group)) return false;
                    if (this.filters.platform.size > 0 && !this.filters.platform.has(creator.platform)) return false;
                    if (this.filters.geography.size > 0 && !this.filters.geography.has(creator.geography)) return false;
                    if (this.filters.topic.size > 0 && !this.filters.topic.has(creator.topic)) return false;
                    if (this.filters.search) {
                        const s = this.filters.search.toLowerCase();
                        return creator.name.toLowerCase().includes(s) || creator.channel.toLowerCase().includes(s) ||
                               (creator.topic && creator.topic.toLowerCase().includes(s)) ||
                               (creator.geography && creator.geography.toLowerCase().includes(s)) ||
                               (creator.group && creator.group.toLowerCase().includes(s));
                    }
                    return true;
                });
                updateResultsCount();
                updateURL();
                if (typeof updateFilterCountBadge === 'function') updateFilterCountBadge();
            }

            // Clear all filters silently (no view re-render)
            clearAllSilent() {
                this.filters.group.clear();
                this.filters.platform.clear();
                this.filters.geography.clear();
                this.filters.topic.clear();
                this.filters.search = '';
                document.querySelectorAll('input[type="checkbox"]').forEach(cb => cb.checked = false);
                const navSearch = document.getElementById('navSearch');
                if (navSearch) navSearch.value = '';
                this.applyFiltersSilent();
            }
            
            // Add a filter value (without removing others)
            add(type, value) {
                this.filters[type].add(value);
                this.syncUI(type, value);
                this.applyFilters();
            }
            
            // Remove a filter value
            remove(type, value) {
                this.filters[type].delete(value);
                this.syncUI(type, value);
                this.applyFilters();
            }
            
            // Clear specific filter type
            clearType(type) {
                if (type === 'search') {
                    this.filters.search = '';
                } else {
                    this.filters[type].clear();
                }
                this.syncUIForType(type);
                this.applyFilters();
            }
            
            // Clear all filters
            clearAll() {
                this.filters.group.clear();
                this.filters.platform.clear();
                this.filters.geography.clear();
                this.filters.topic.clear();
                this.filters.search = '';
                
                // Uncheck all checkboxes
                document.querySelectorAll('input[type="checkbox"]').forEach(cb => cb.checked = false);
                
                // Clear search inputs
                const navSearch = document.getElementById('navSearch');
                if (navSearch) navSearch.value = '';
                
                this.applyFilters();
            }
            
            // Set search filter
            setSearch(value) {
                this.filters.search = value;
                this.applyFilters();
            }
            
            // Get active filters
            getFilters() {
                return this.filters;
            }
            
            // Check if a filter is active
            has(type, value) {
                return this.filters[type].has(value);
            }
            
            // Sync UI checkboxes when filters change programmatically
            syncUI(type, value) {
                if (type === 'search') return;
                
                const isActive = this.filters[type].has(value);
                
                // Find and update checkbox
                const checkboxes = document.querySelectorAll(`input[type="checkbox"][data-filter-type="${type}"]`);
                checkboxes.forEach(cb => {
                    if (cb.value === value) {
                        cb.checked = isActive;
                    }
                });
            }
            
            // Sync all UI elements for a filter type
            syncUIForType(type) {
                if (type === 'search') {
                    const navSearch = document.getElementById('navSearch');
                    if (navSearch) navSearch.value = '';
                    return;
                }
                
                const checkboxes = document.querySelectorAll(`input[type="checkbox"][data-filter-type="${type}"]`);
                checkboxes.forEach(cb => {
                    cb.checked = this.filters[type].has(cb.value);
                });
            }
            
            // Apply filters and update views
            applyFilters() {
                filteredCreators = allCreators.filter(creator => {
                    // Group filter
                    if (this.filters.group.size > 0 && !this.filters.group.has(creator.group)) {
                        return false;
                    }
                    
                    // Platform filter
                    if (this.filters.platform.size > 0 && !this.filters.platform.has(creator.platform)) {
                        return false;
                    }
                    
                    // Geography filter
                    if (this.filters.geography.size > 0 && !this.filters.geography.has(creator.geography)) {
                        return false;
                    }
                    
                    // Topic filter
                    if (this.filters.topic.size > 0 && !this.filters.topic.has(creator.topic)) {
                        return false;
                    }
                    
                    // Search filter
                    if (this.filters.search) {
                        const searchLower = this.filters.search.toLowerCase();
                        return (
                            creator.name.toLowerCase().includes(searchLower) ||
                            creator.channel.toLowerCase().includes(searchLower) ||
                            (creator.topic && creator.topic.toLowerCase().includes(searchLower)) ||
                            (creator.geography && creator.geography.toLowerCase().includes(searchLower)) ||
                            (creator.group && creator.group.toLowerCase().includes(searchLower))
                        );
                    }
                    
                    return true;
                });
                
                updateResultsCount();
                updateURL();
                if (typeof updateFilterCountBadge === 'function') updateFilterCountBadge();

                // Only render the active view
                if (currentView === 'grid' || currentView === 'list') {
                    renderCreators();
                } else if (currentView === 'bubbles') {
                    renderBubbleChart();
                } else if (currentView === 'wheel') {
                    renderSunburstChart();
                } else if (currentView === 'treemap') {
                    treemapDrillGroup = null; // Reset drill state on external filter change
                    renderTreemapChart();
                }
            }
        }
        
        // Initialize filter state manager
        const filterState = new FilterStateManager();

        // Initialize on page load
        document.addEventListener('DOMContentLoaded', function() {
            loadCreatorsData();
            setupScrollBehavior();
            setupReadMore();
            loadFiltersFromURL();
        });

        // Re-render active visualization on window resize (debounced)
        let resizeTimer;
        window.addEventListener('resize', function() {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(function() {
                if (currentView === 'bubbles') renderBubbleChart();
                else if (currentView === 'wheel') renderSunburstChart();
                else if (currentView === 'treemap') renderTreemapChart();
            }, 250);
        });

        // Load and parse CSV data
        async function loadCreatorsData() {
            try {
                const response = await fetch('assets/data/creators-data.json');
                const data = await response.json();
                
                allCreators = data;
                
                // Update total count in the intro text
                document.getElementById('totalCreatorsCount').textContent = allCreators.length;
                
                // Build filter options
                buildFilterOptions();
                
                // Initial render
                filterState.applyFilters();
                
                // Hide loading state
                document.getElementById('loadingState').style.display = 'none';
                
            } catch (error) {
                console.error('Error loading data:', error);
                document.getElementById('loadingState').innerHTML = '<p style="color: red;">Error loading data. Please refresh the page.</p>';
            }
        }

        // Build filter options from data
        function buildFilterOptions() {
            const groups = new Map();
            const platforms = new Map();
            const geographies = new Map();
            const topics = new Map();
            
            allCreators.forEach(creator => {
                // Group (NEW!)
                if (creator.group) {
                    groups.set(creator.group, (groups.get(creator.group) || 0) + 1);
                }
                
                // Platform
                if (creator.platform) {
                    platforms.set(creator.platform, (platforms.get(creator.platform) || 0) + 1);
                }
                
                // Geography
                if (creator.geography) {
                    geographies.set(creator.geography, (geographies.get(creator.geography) || 0) + 1);
                }
                
                // Topic
                if (creator.topic) {
                    topics.set(creator.topic, (topics.get(creator.topic) || 0) + 1);
                }
            });
            
            // Populate group filters (FIRST - primary filter!)
            const groupFilters = document.getElementById('groupFilters');
            ORDERED_GROUPS.forEach(groupName => {
                const count = groups.get(groupName);
                if (count) {
                    groupFilters.appendChild(createFilterOption('group', groupName, count));
                }
            });
            // Add any groups not in the ordered list
            Array.from(groups.entries())
                .filter(([group]) => !ORDERED_GROUPS.includes(group))
                .sort((a, b) => a[0].localeCompare(b[0]))
                .forEach(([group, count]) => {
                    groupFilters.appendChild(createFilterOption('group', group, count));
                });
            
            // Populate platform filters
            const platformFilters = document.getElementById('platformFilters');
            Array.from(platforms.entries())
                .sort((a, b) => b[1] - a[1]) // Sort by count descending
                .forEach(([platform, count]) => {
                    platformFilters.appendChild(createFilterOption('platform', platform, count));
                });
            
            // Populate geography filters
            const geographyFilters = document.getElementById('geographyFilters');
            Array.from(geographies.entries())
                .sort((a, b) => a[0].localeCompare(b[0])) // Sort alphabetically
                .forEach(([geography, count]) => {
                    geographyFilters.appendChild(createFilterOption('geography', geography, count));
                });
            
            // Populate topic filters
            const topicFilters = document.getElementById('topicFilters');
            Array.from(topics.entries())
                .sort((a, b) => a[0].localeCompare(b[0])) // Sort alphabetically
                .forEach(([topic, count]) => {
                    topicFilters.appendChild(createFilterOption('topic', topic, count));
                });
        }

        // Create filter option element
        function createFilterOption(type, value, count) {
            const div = document.createElement('div');
            div.className = 'filter-option';
            
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.id = `${type}-${value.replace(/\s+/g, '-')}`;
            checkbox.value = value;
            checkbox.setAttribute('data-filter-type', type); // Add for filter state sync
            checkbox.onchange = () => toggleFilter(type, value);
            
            const label = document.createElement('label');
            label.htmlFor = checkbox.id;
            label.textContent = value;
            
            const countSpan = document.createElement('span');
            countSpan.className = 'filter-count';
            countSpan.textContent = `(${count})`;
            
            div.appendChild(checkbox);
            div.appendChild(label);
            div.appendChild(countSpan);
            
            return div;
        }

        // Toggle filter selection
        function toggleFilter(type, value) {
            filterState.toggle(type, value);
        }

        // Render creators in current view
        function renderCreators() {
            if (filteredCreators.length === 0) {
                document.getElementById('creatorsGrid').style.display = 'none';
                document.getElementById('creatorsList').style.display = 'none';
                document.getElementById('emptyState').style.display = 'block';
                return;
            }
            
            document.getElementById('emptyState').style.display = 'none';
            
            if (currentView === 'grid') {
                renderGridView();
            } else {
                renderListView();
            }
        }

        // Render grid view
        function renderGridView() {
            const grid = document.getElementById('creatorsGrid');
            grid.innerHTML = '';
            // Remove inline style to let CSS handle it properly
            grid.style.display = '';
            
            filteredCreators.forEach(creator => {
                const card = createCreatorCard(creator);
                grid.appendChild(card);
            });
        }

        // Render list view
        function renderListView() {
            const list = document.getElementById('creatorsList');
            list.innerHTML = '';
            list.classList.add('active');
            
            // Create table
            const table = document.createElement('table');
            table.className = 'creators-table';
            
            // Create header
            const thead = document.createElement('thead');
            thead.innerHTML = `
                <tr>
                    <th data-sort="name" class="sortable">Name <span class="sort-icon">↕</span></th>
                    <th data-sort="channel" class="sortable">Channel <span class="sort-icon">↕</span></th>
                    <th data-sort="platform" class="sortable">Platform <span class="sort-icon">↕</span></th>
                    <th data-sort="geography" class="sortable">Geography <span class="sort-icon">↕</span></th>
                    <th data-sort="topic" class="sortable">Topic <span class="sort-icon">↕</span></th>
                    <th data-sort="group" class="sortable">Group <span class="sort-icon">↕</span></th>
                </tr>
            `;
            table.appendChild(thead);
            
            // Create body
            const tbody = document.createElement('tbody');
            filteredCreators.forEach(creator => {
                const row = document.createElement('tr');
                row.className = 'creator-row';
                row.onclick = () => window.open(creator.link, '_blank');
                
                row.innerHTML = `
                    <td class="creator-name-cell">${creator.name || '-'}</td>
                    <td>${creator.channel || '-'}</td>
                    <td>${creator.platform || '-'}</td>
                    <td>${creator.geography || '-'}</td>
                    <td>${creator.topic || '-'}</td>
                    <td>${creator.group || '-'}</td>
                `;
                
                tbody.appendChild(row);
            });
            table.appendChild(tbody);
            
            // Add sorting functionality
            thead.querySelectorAll('.sortable').forEach(th => {
                th.addEventListener('click', () => {
                    const sortKey = th.dataset.sort;
                    sortTable(sortKey, th);
                });
            });
            
            list.appendChild(table);
        }
        
        // Sort table by column
        let currentSortKey = '';
        let currentSortDirection = 'asc';
        
        function sortTable(key, headerElement) {
            // Toggle direction if clicking same column
            if (currentSortKey === key) {
                currentSortDirection = currentSortDirection === 'asc' ? 'desc' : 'asc';
            } else {
                currentSortDirection = 'asc';
                currentSortKey = key;
            }
            
            // Sort filteredCreators array
            filteredCreators.sort((a, b) => {
                let aVal = (a[key] || '').toString().toLowerCase();
                let bVal = (b[key] || '').toString().toLowerCase();
                
                if (currentSortDirection === 'asc') {
                    return aVal.localeCompare(bVal);
                } else {
                    return bVal.localeCompare(aVal);
                }
            });
            
            // Update sort icons
            document.querySelectorAll('.sortable').forEach(th => {
                th.classList.remove('sort-asc', 'sort-desc');
            });
            headerElement.classList.add(currentSortDirection === 'asc' ? 'sort-asc' : 'sort-desc');
            
            // Re-render
            renderListView();
        }

        // Create creator card for grid view
        function createCreatorCard(creator) {
            const card = document.createElement('div');
            card.className = 'creator-card';
            card.onclick = () => window.open(creator.link, '_blank');

            const initials = creator.name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();

            card.innerHTML = `
                <div class="creator-header">
                    <div class="creator-avatar">${initials}</div>
                    <div class="creator-info">
                        <div class="creator-name">${creator.name}</div>
                        <div class="creator-channel">${creator.channel}</div>
                    </div>
                </div>
                <div class="creator-meta">
                    ${creator.geography ? `
                        <div class="creator-meta-item clickable-tag" data-filter-type="geography" data-filter-value="${creator.geography}">
                            <span class="material-icons-outlined creator-meta-icon">location_on</span>
                            <span>${creator.geography}</span>
                        </div>
                    ` : ''}
                    ${creator.platform ? `
                        <div class="creator-meta-item clickable-tag" data-filter-type="platform" data-filter-value="${creator.platform}">
                            <span class="material-icons-outlined creator-meta-icon">devices</span>
                            <span>${creator.platform}</span>
                        </div>
                    ` : ''}
                    ${creator.topic ? `
                        <div class="creator-meta-item clickable-tag" data-filter-type="topic" data-filter-value="${creator.topic}">
                            <span class="material-icons-outlined creator-meta-icon">tag</span>
                            <span class="creator-tag">${creator.topic}</span>
                        </div>
                    ` : ''}
                </div>
                <a href="submit.html?edit=${encodeURIComponent(creator.name)}" class="suggest-edits-btn" onclick="event.stopPropagation();">
                    <span class="material-icons-outlined">edit</span>
                    <span>Suggest Edits</span>
                </a>
            `;

            // Add click handlers to tags
            card.querySelectorAll('.clickable-tag').forEach(tag => {
                tag.addEventListener('click', (e) => {
                    e.stopPropagation();
                    const filterType = tag.dataset.filterType;
                    const filterValue = tag.dataset.filterValue;
                    handleTagClick(e, filterType, filterValue);
                });
            });

            return card;
        }

        // Update results count
        function updateResultsCount() {
            const count = filteredCreators.length;
            const total = allCreators.length;
            document.getElementById('resultsCount').innerHTML = `
                Showing <strong>${count}</strong> of <strong>${total}</strong> creators
            `;
        }

        // Handle tag clicks to apply filters
        function handleTagClick(event, filterType, filterValue) {
            filterState.toggle(filterType, filterValue);
        }

        // Toggle accordion
        function toggleAccordion(accordionId) {
            const accordion = document.getElementById(accordionId);
            accordion.classList.toggle('open');
        }

        // Filter options within accordion
        function filterOptions(searchId, containerId) {
            const searchInput = document.getElementById(searchId);
            const searchTerm = searchInput.value.toLowerCase();
            const container = document.getElementById(containerId);
            const options = container.getElementsByClassName('filter-option');
            
            Array.from(options).forEach(option => {
                const label = option.querySelector('label').textContent.toLowerCase();
                option.style.display = label.includes(searchTerm) ? 'flex' : 'none';
            });
        }

        // Clear all filters
        function clearAllFilters() {
            filterState.clearAll();
        }

        // Toggle view
        function toggleView(view) {
            currentView = view;
            
            // Update button states
            document.querySelectorAll('.view-btn').forEach(btn => {
                btn.classList.remove('active');
                if (btn.textContent.toLowerCase() === view) {
                    btn.classList.add('active');
                }
            });
            
            // Hide all views first - use classes instead of inline styles
            const grid = document.getElementById('creatorsGrid');
            const list = document.getElementById('creatorsList');
            const bubbles = document.getElementById('bubblesView');
            const sunburst = document.getElementById('sunburstView');
            const treemap = document.getElementById('treemapView');
            const empty = document.getElementById('emptyState');
            
            // Reset all views
            grid.style.display = 'none';
            grid.classList.remove('active');
            list.style.display = 'none';
            list.classList.remove('active');
            bubbles.classList.remove('active');
            sunburst.classList.remove('active');
            treemap.classList.remove('active');
            empty.style.display = 'none';
            
            // Show selected view
            if (view === 'grid') {
                if (filteredCreators.length === 0) {
                    empty.style.display = 'block';
                } else {
                    grid.style.display = 'grid';
                    grid.classList.add('active');
                    renderGridView();
                }
            } else if (view === 'list') {
                if (filteredCreators.length === 0) {
                    empty.style.display = 'block';
                } else {
                    list.style.display = '';  // Clear inline style so CSS class takes effect
                    list.classList.add('active');
                    renderListView();
                }
            } else if (view === 'bubbles') {
                bubbles.classList.add('active');
                renderBubbleChart();
            } else if (view === 'wheel') {
                sunburst.classList.add('active');
                renderSunburstChart();
            } else if (view === 'treemap') {
                treemap.classList.add('active');
                renderTreemapChart();
            }
        }

        // Nav search functionality (debounced for performance)
        let searchDebounceTimer;
        document.getElementById('navSearch').addEventListener('input', function(e) {
            clearTimeout(searchDebounceTimer);
            searchDebounceTimer = setTimeout(() => filterState.setSearch(e.target.value), 150);
        });

        // URL parameter handling for permalinks
        function updateURL() {
            const params = new URLSearchParams();
            
            if (filterState.filters.group.size > 0) {
                params.set('group', Array.from(filterState.filters.group).join(','));
            }
            if (filterState.filters.platform.size > 0) {
                params.set('platform', Array.from(filterState.filters.platform).join(','));
            }
            if (filterState.filters.geography.size > 0) {
                params.set('geography', Array.from(filterState.filters.geography).join(','));
            }
            if (filterState.filters.topic.size > 0) {
                params.set('topic', Array.from(filterState.filters.topic).join(','));
            }
            if (filterState.filters.search) {
                params.set('search', filterState.filters.search);
            }
            
            const newURL = params.toString() ? `?${params.toString()}` : window.location.pathname;
            window.history.replaceState({}, '', newURL);
        }

        function loadFiltersFromURL() {
            const params = new URLSearchParams(window.location.search);
            
            // Load group filters
            if (params.has('group')) {
                params.get('group').split(',').forEach(value => {
                    filterState.filters.group.add(value);
                    const checkbox = document.querySelector(`input[value="${value}"]`);
                    if (checkbox) checkbox.checked = true;
                });
            }
            
            // Load platform filters
            if (params.has('platform')) {
                params.get('platform').split(',').forEach(value => {
                    filterState.filters.platform.add(value);
                    const checkbox = document.querySelector(`input[value="${value}"]`);
                    if (checkbox) checkbox.checked = true;
                });
            }
            
            // Load geography filters
            if (params.has('geography')) {
                params.get('geography').split(',').forEach(value => {
                    filterState.filters.geography.add(value);
                    const checkbox = document.querySelector(`input[value="${value}"]`);
                    if (checkbox) checkbox.checked = true;
                });
            }
            
            // Load topic filters
            if (params.has('topic')) {
                params.get('topic').split(',').forEach(value => {
                    filterState.filters.topic.add(value);
                    const checkbox = document.querySelector(`input[value="${value}"]`);
                    if (checkbox) checkbox.checked = true;
                });
            }
            
            // Load search
            if (params.has('search')) {
                filterState.filters.search = params.get('search');
                document.getElementById('navSearch').value = params.get('search');
            }
        }

        // Scroll behavior
        function setupScrollBehavior() {
            const nav = document.querySelector('.top-nav');

            window.addEventListener('scroll', () => {
                if (window.pageYOffset > 100) {
                    nav.classList.add('scrolled');
                } else {
                    nav.classList.remove('scrolled');
                }
            });
        }

        // Read more button
        function setupReadMore() {
            const btn = document.getElementById('readMoreBtn');
            const intro = document.getElementById('heroIntro');
            const text = document.getElementById('readMoreText');
            
            btn.addEventListener('click', () => {
                intro.classList.toggle('expanded');
                if (intro.classList.contains('expanded')) {
                    text.textContent = 'Show Less';
                } else {
                    text.textContent = 'Learn More About Creator Journalism';
                }
            });
        }

        // Bubble visualization functions
        function setBubbleMode(mode, evt) {
            currentBubbleMode = mode;
            document.querySelectorAll('.bubble-mode-btn').forEach(btn => btn.classList.remove('active'));
            if (evt && evt.target) evt.target.classList.add('active');
            renderBubbleChart();
        }

        function renderBubbleChart() {
            // On mobile, fall back from topic mode (hidden on mobile)
            if (window.innerWidth <= 768 && currentBubbleMode === 'topic') {
                currentBubbleMode = 'platform';
                document.querySelectorAll('.bubble-mode-btn').forEach(btn => {
                    btn.classList.toggle('active', btn.getAttribute('data-mode') === 'platform');
                });
            }

            const svg = d3.select('#bubbleChart');
            const container = document.getElementById('bubblesView');
            const width = container.clientWidth - 40;
            const height = window.innerWidth <= 768 ? 400 : 600;

            svg.attr('width', width).attr('height', height).attr('viewBox', `0 0 ${width} ${height}`);
            svg.selectAll('*').remove();

            // Prepare data based on mode - generic counting by field
            const counts = {};
            filteredCreators.forEach(c => {
                const val = c[currentBubbleMode];
                if (val) counts[val] = (counts[val] || 0) + 1;
            });
            let bubbleData = Object.entries(counts).map(([name, count]) => ({
                name,
                count,
                type: currentBubbleMode
            }));

            // Aggregate small bubbles below threshold
            const MIN_CREATORS = 3;
            const smallBubbles = bubbleData.filter(d => d.count < MIN_CREATORS);
            if (smallBubbles.length > 1) {
                const smallTotal = smallBubbles.reduce((sum, d) => sum + d.count, 0);
                bubbleData = bubbleData.filter(d => d.count >= MIN_CREATORS);
                bubbleData.push({
                    name: `Other (${smallBubbles.length} categories)`,
                    count: smallTotal,
                    type: currentBubbleMode,
                    isAggregate: true
                });
            }

            if (bubbleData.length === 0) {
                svg.append('text')
                    .attr('x', width / 2)
                    .attr('y', height / 2)
                    .attr('text-anchor', 'middle')
                    .style('font-size', '18px')
                    .style('fill', '#999')
                    .text('No data to display');
                return;
            }

            // Sort by count descending for better layout
            bubbleData.sort((a, b) => b.count - a.count);

            // Create scale for bubble size
            const maxCount = d3.max(bubbleData, d => d.count);
            const totalBubbles = bubbleData.length;

            // Dynamically adjust radius range based on number of bubbles
            const minRadius = totalBubbles > 30 ? 15 : 20;
            const maxRadius = totalBubbles > 30 ? 70 : 100;

            const radiusScale = d3.scaleSqrt()
                .domain([1, maxCount])
                .range([minRadius, maxRadius]);

            // Add radius to data
            bubbleData.forEach(d => {
                d.radius = radiusScale(d.count);
                d.x = Math.random() * width;
                d.y = Math.random() * height;
            });

            // Create color scale
            const colorScale = d3.scaleLinear()
                .domain([0, maxCount / 2, maxCount])
                .range(['#97d600', '#ceff00', '#e8ff6b']);

            // Create zoomable container
            const g = svg.append('g').attr('class', 'bubble-container');

            // Add zoom behavior
            const zoom = d3.zoom()
                .scaleExtent([0.5, 4])
                .on('zoom', (event) => {
                    g.attr('transform', event.transform);
                });

            svg.call(zoom);

            // Add zoom controls hint
            svg.append('text')
                .attr('x', 10)
                .attr('y', height - 10)
                .attr('class', 'zoom-hint')
                .style('font-size', '12px')
                .style('fill', '#999')
                .text('Scroll to zoom • Drag to pan • Click bubble to filter');

            // Create force simulation
            const collisionStrength = totalBubbles > 30 ? 3 : 4;
            const simulation = d3.forceSimulation(bubbleData)
                .force('charge', d3.forceManyBody().strength(10))
                .force('center', d3.forceCenter(width / 2, height / 2))
                .force('collision', d3.forceCollide(d => d.radius + collisionStrength))
                .force('x', d3.forceX(width / 2).strength(0.07))
                .force('y', d3.forceY(height / 2).strength(0.07));

            // Create bubble groups
            const bubbles = g.selectAll('.bubble-group')
                .data(bubbleData)
                .enter()
                .append('g')
                .attr('class', 'bubble-group')
                .style('cursor', 'pointer');

            // Add circles
            bubbles.append('circle')
                .attr('class', 'bubble')
                .attr('r', d => d.radius)
                .attr('fill', d => colorScale(d.count))
                .attr('stroke', '#000000')
                .attr('stroke-width', 2)
                .on('click', function(event, d) {
                    event.stopPropagation();
                    handleBubbleClick(d);
                })
                .on('mouseover', function(event, d) {
                    d3.select(this).attr('opacity', 0.8).attr('stroke-width', 3);
                    showBubbleTooltip(event, d);
                })
                .on('mouseout', function(event, d) {
                    d3.select(this).attr('opacity', 1).attr('stroke-width', 2);
                    hideBubbleTooltip();
                })
                .append('title')
                .text(d => `${d.name}\n${d.count} creator${d.count !== 1 ? 's' : ''}\nClick to filter`);

            // Only show count on bubbles with radius > threshold
            const labelThreshold = totalBubbles > 30 ? 25 : 20;

            bubbles.filter(d => d.radius >= labelThreshold)
                .append('text')
                .attr('class', 'bubble-count')
                .attr('dy', d => d.radius >= 40 ? '-0.3em' : '0.35em')
                .text(d => d.count);

            // Only show label text on larger bubbles
            bubbles.filter(d => d.radius >= 40)
                .append('text')
                .attr('class', 'bubble-label')
                .attr('dy', '1.2em')
                .text(d => truncateToFit(d.name, d.radius * 1.6, 12))
                .append('title')
                .text(d => `${d.name}\n${d.count} creator${d.count !== 1 ? 's' : ''}\nClick to filter`);

            // Update positions on tick
            simulation.on('tick', () => {
                bubbles.attr('transform', d => `translate(${d.x},${d.y})`);
            });

            // Add legend showing top categories
            const legendData = bubbleData.slice(0, Math.min(5, bubbleData.length));
            const isMobile = window.innerWidth <= 768;
            const mobileLegendEl = document.getElementById('bubbleLegendMobile');

            if (isMobile && mobileLegendEl) {
                // Render legend as HTML below the chart on mobile
                let legendHTML = '';
                legendData.forEach(d => {
                    const clickAttr = d.isAggregate ? '' : `onclick="handleBubbleClick({name:'${d.name.replace(/'/g, "\\'")}',type:'${d.type}',count:${d.count}})"`;
                    legendHTML += `<div class="legend-item" ${clickAttr} style="${d.isAggregate ? 'cursor:default;opacity:0.6;' : ''}">
                        <span class="legend-dot" style="background:${colorScale(d.count)}"></span>
                        ${abbreviateLabel(d.name, 20)} (${d.count})
                    </div>`;
                });
                // Size reference
                const sizeSamples = [1, Math.max(1, Math.round(maxCount / 3)), maxCount];
                legendHTML += '<div class="legend-size-section">';
                legendHTML += '<span style="font-weight:600;">Bubble size = creators:</span>';
                sizeSamples.forEach(val => {
                    const r = Math.min(Math.round(radiusScale(val)), 10);
                    legendHTML += `<span class="size-sample"><span class="size-dot" style="width:${r*2}px;height:${r*2}px;"></span>${val}</span>`;
                });
                legendHTML += '</div>';
                mobileLegendEl.innerHTML = legendHTML;
            } else {
                // Desktop: render legend inside SVG
                if (mobileLegendEl) mobileLegendEl.innerHTML = '';
                const legend = svg.append('g')
                    .attr('class', 'bubble-legend')
                    .attr('transform', `translate(${width - 150}, 20)`);

                legend.append('text')
                    .attr('class', 'legend-title')
                    .style('font-size', '12px')
                    .style('font-weight', '600')
                    .text('Top Categories');

                legendData.forEach((d, i) => {
                    const legendItem = legend.append('g')
                        .attr('transform', `translate(0, ${20 + i * 18})`)
                        .style('cursor', d.isAggregate ? 'default' : 'pointer')
                        .on('click', function() {
                            if (!d.isAggregate) handleBubbleClick(d);
                        })
                        .on('mouseover', function() {
                            if (!d.isAggregate) d3.select(this).style('opacity', 0.7);
                        })
                        .on('mouseout', function() {
                            d3.select(this).style('opacity', 1);
                        });

                    legendItem.append('circle')
                        .attr('r', 6)
                        .attr('fill', colorScale(d.count));

                    legendItem.append('text')
                        .attr('x', 12)
                        .attr('y', 4)
                        .style('font-size', '11px')
                        .text(`${abbreviateLabel(d.name, 18)} (${d.count})`);
                });

                // Size legend — explains what bubble size means
                const sizeLegendY = 20 + Math.min(5, legendData.length) * 18 + 30;
                const sizeLegend = svg.append('g')
                    .attr('class', 'size-legend')
                    .attr('transform', `translate(${width - 150}, ${sizeLegendY})`);

                sizeLegend.append('text')
                    .style('font-size', '12px')
                    .style('font-weight', '600')
                    .text('Bubble Size = Creators');

                const sizeSamples = [
                    { val: 1, label: '1' },
                    { val: Math.max(1, Math.round(maxCount / 3)), label: String(Math.round(maxCount / 3)) },
                    { val: maxCount, label: String(maxCount) }
                ];
                let sizeY = 20;
                sizeSamples.forEach((s) => {
                    const r = Math.min(radiusScale(s.val), 14);
                    sizeLegend.append('circle')
                        .attr('cx', 14)
                        .attr('cy', sizeY)
                        .attr('r', r)
                        .attr('fill', 'none')
                        .attr('stroke', '#999')
                        .attr('stroke-width', 1);
                    sizeLegend.append('text')
                        .attr('x', 34)
                        .attr('y', sizeY + 4)
                        .style('font-size', '11px')
                        .style('fill', '#666')
                        .text(s.label + ' creator' + (s.val !== 1 ? 's' : ''));
                    sizeY += 28;
                });
            }
        }

        function handleBubbleClick(bubble) {
            if (bubble.isAggregate) return; // Don't filter aggregate "Other" bubble
            // Toggle the filter based on bubble type (additive behavior)
            // Stay in current view — applyFilters() will re-render the active visualization
            if (bubble.type === 'geography') {
                filterState.toggle('geography', bubble.name);
            } else if (bubble.type === 'platform') {
                filterState.toggle('platform', bubble.name);
            } else if (bubble.type === 'topic') {
                filterState.toggle('topic', bubble.name);
            } else if (bubble.type === 'group') {
                filterState.toggle('group', bubble.name);
            }
        }

        function showBubbleTooltip(event, d) {
            const tooltip = document.getElementById('bubbleTooltip');
            tooltip.innerHTML = `
                <strong>${d.name}</strong><br>
                ${d.count} creator${d.count !== 1 ? 's' : ''}
            `;
            // Keep tooltip within viewport
            const x = Math.min(event.pageX + 10, window.innerWidth - 200);
            tooltip.style.left = x + 'px';
            tooltip.style.top = (event.pageY - 10) + 'px';
            tooltip.style.opacity = 1;
        }

        function hideBubbleTooltip() {
            document.getElementById('bubbleTooltip').style.opacity = 0;
        }

        // Sunburst/Wheel visualization functions
        function renderSunburstChart() {
            const svg = d3.select('#sunburstChart');
            const sunburstContainer = document.getElementById('sunburstView');
            const containerWidth = sunburstContainer ? sunburstContainer.clientWidth - 32 : 700;
            const size = Math.min(containerWidth, 700);
            const width = size;
            const height = size;
            const radius = size / 2;

            // Reset breadcrumb and creators on fresh render
            const breadcrumb = document.getElementById('sunburstBreadcrumb');
            if (breadcrumb) {
                breadcrumb.innerHTML = '<span class="breadcrumb-item active" title="You are viewing all creators">&#x1F30F;  All Creators</span>';
            }
            hideVizCreators('wheelCreators');
            const legendEl = document.getElementById('sunburstLegend');
            if (legendEl) legendEl.style.display = '';

            svg.attr('viewBox', `0 0 ${width} ${height}`)
               .attr('width', null).attr('height', null)
               .style('width', '100%').style('max-width', width + 'px').style('height', 'auto');
            svg.selectAll('*').remove();

            const g = svg.append('g')
                .attr('transform', `translate(${width / 2},${height / 2})`);

            // Build hierarchical data structure: Platform → Group
            const platformData = {};
            
            filteredCreators.forEach(creator => {
                const platform = creator.platform || 'Unknown';
                const group = creator.group || 'Uncategorized';
                
                if (!platformData[platform]) {
                    platformData[platform] = {};
                }
                if (!platformData[platform][group]) {
                    platformData[platform][group] = 0;
                }
                platformData[platform][group]++;
            });

            // Convert to hierarchy
            const hierarchyData = {
                name: 'All Creators',
                children: Object.entries(platformData).map(([platform, groups]) => ({
                    name: platform,
                    children: Object.entries(groups).map(([group, count]) => ({
                        name: group,
                        value: count,
                        platform: platform
                    }))
                }))
            };

            // Create hierarchy
            const root = d3.hierarchy(hierarchyData)
                .sum(d => d.value)
                .sort((a, b) => b.value - a.value);

            // Create partition layout with larger center
            const innerRadiusOffset = Math.round(radius * 0.18);
            const partition = d3.partition()
                .size([2 * Math.PI, radius - innerRadiusOffset]);

            partition(root);

            // Offset all y values outward to create larger center space
            root.each(d => {
                d.y0 += innerRadiusOffset;
                d.y1 += innerRadiusOffset;
            });

            // Track current focused node
            let focusedNode = root;
            // Expose for breadcrumb navigation
            window._sunburstRoot = root;
            window._sunburstZoomTo = null; // Will be set after zoomTo is defined

            // Color scales for different platforms - improved palette with better contrast
            const platformColors = {
                'Newsletter - Substack': '#FF6B35',    // Vibrant orange
                'Newsletter - Beehiiv': '#F7931E',     // Golden orange
                'Newsletter - Other': '#FDB833',       // Warm yellow
                'Newsletter - Ghost': '#FFD23F',       // Bright yellow
                'Video - YouTube': '#E74C3C',          // YouTube red
                'Video - Instagram': '#E4405F',        // Instagram pink
                'Video - TikTok': '#00F2EA',           // TikTok cyan
                'Social - Twitter / X': '#1DA1F2',     // Twitter blue
                'Social - BlueSky': '#0560FF',         // BlueSky blue
                'Social - LinkedIn': '#0A66C2',        // LinkedIn blue
                'Social - Facebook': '#1877F2',        // Facebook blue
                'Podcast': '#9B59B6',                  // Purple
                'Website': '#16A085'                    // Teal/green
            };

            // Get default color if platform not in map
            function getPlatformColor(platform) {
                if (platformColors[platform]) return platformColors[platform];
                if (platform.includes('Newsletter')) return '#3b82f6';
                if (platform.includes('Video')) return '#ef4444';
                if (platform.includes('Social')) return '#8b5cf6';
                if (platform.includes('Podcast')) return '#9333ea';
                return '#97d600'; // Default acid green
            }

            // Create arc generator
            const arc = d3.arc()
                .startAngle(d => Math.max(0, Math.min(2 * Math.PI, d.x0)))
                .endAngle(d => Math.max(0, Math.min(2 * Math.PI, d.x1)))
                .padAngle(d => {
                    // Reduce padding for very small segments to keep them visible
                    const angleSize = d.x1 - d.x0;
                    if (angleSize < 0.05) return 0.001;
                    return Math.min((d.x1 - d.x0) / 2, 0.005);
                })
                .padRadius(radius / 2)
                .innerRadius(d => Math.max(0, d.y0))
                .outerRadius(d => Math.max(0, d.y1 - 1));

            // Draw arcs
            const path = g.selectAll('path')
                .data(root.descendants().filter(d => d.depth > 0))
                .enter()
                .append('path')
                .attr('class', 'sunburst-arc')
                .attr('d', arc)
                .attr('fill', d => {
                    if (d.depth === 1) {
                        return getPlatformColor(d.data.name);
                    } else {
                        const baseColor = getPlatformColor(d.data.platform);
                        return d3.color(baseColor).brighter(0.5);
                    }
                })
                .attr('opacity', 0.95)
                .style('cursor', 'pointer')
                .on('click', function(event, d) {
                    event.stopPropagation();
                    // Sync filters with wheel navigation (silent — no re-render)
                    if (d.depth === 1) {
                        // Platform level: clear previous wheel filters, set this platform
                        filterState.clearAllSilent();
                        filterState.toggleSilent('platform', d.data.name);
                    } else if (d.depth === 2) {
                        // Group level: set platform + group filters
                        filterState.clearAllSilent();
                        filterState.toggleSilent('platform', d.parent.data.name);
                        filterState.toggleSilent('group', d.data.name);
                    }
                    zoomTo(d);
                })
                .on('mouseover', function(event, d) {
                    d3.select(this)
                        .attr('opacity', 0.85)
                        .style('filter', 'brightness(1.15)');
                    showSunburstTooltip(event, d);
                })
                .on('mouseout', function(event, d) {
                    d3.select(this)
                        .attr('opacity', 0.95)
                        .style('filter', 'none');
                    hideSunburstTooltip();
                })
                .append('title')
                .text(d => {
                    if (d.depth === 1) {
                        return `${d.data.name}\n${d.value} creator${d.value !== 1 ? 's' : ''}\nClick to explore`;
                    } else if (d.depth === 2) {
                        return `${d.data.name}\n${d.value} creator${d.value !== 1 ? 's' : ''}\nPlatform: ${d.parent.data.name}\nClick to explore`;
                    }
                    return `${d.data.name}\n${d.value} creator${d.value !== 1 ? 's' : ''}`;
                });

            // Add labels
            const labels = g.selectAll('text')
                .data(root.descendants().filter(d => d.depth > 0))
                .enter()
                .append('text')
                .attr('class', 'sunburst-label')
                .attr('transform', d => {
                    const angle = (d.x0 + d.x1) / 2 * 180 / Math.PI;
                    const radius = (d.y0 + d.y1) / 2;
                    return `rotate(${angle - 90}) translate(${radius},0) rotate(${angle < 180 ? 0 : 180})`;
                })
                .attr('dy', '0.35em')
                .attr('opacity', d => {
                    const angle = d.x1 - d.x0;
                    const radiusSize = d.y1 - d.y0;
                    return (angle > 0.1 && radiusSize > 30) ? 1 : 0;
                })
                .text(d => {
                    const arcAngle = d.x1 - d.x0;
                    const midRadius = (d.y0 + d.y1) / 2;
                    const arcLength = arcAngle * midRadius;
                    const fontSize = d.depth === 1 ? 11 : 9;
                    return truncateToFit(d.data.name, arcLength * 0.85, fontSize);
                })
                .style('font-size', d => d.depth === 1 ? '11px' : '9px')
                .style('pointer-events', 'none')
                .append('title')
                .text(d => {
                    if (d.depth === 1) {
                        return `${d.data.name}\n${d.value} creator${d.value !== 1 ? 's' : ''}\nClick to explore`;
                    } else if (d.depth === 2) {
                        return `${d.data.name}\n${d.value} creator${d.value !== 1 ? 's' : ''}\nPlatform: ${d.parent.data.name}\nClick to explore`;
                    }
                    return `${d.data.name}\n${d.value} creator${d.value !== 1 ? 's' : ''}`;
                });

            // Add center circle (clickable to zoom out)
            const centerGroup = g.append('g')
                .attr('class', 'sunburst-center-group')
                .style('cursor', 'pointer')
                .on('click', () => {
                    // If at root, do nothing. Otherwise, go up one level.
                    if (focusedNode === root) return;
                    atlasCloseDrawer();
                    if (focusedNode.depth === 2) {
                        // Go up to platform level — keep platform filter, clear group
                        filterState.filters.group.clear();
                        filterState.syncUIForType('group');
                        filterState.applyFiltersSilent();
                        zoomTo(focusedNode.parent);
                    } else {
                        // Go back to root — clear all filters
                        filterState.clearAllSilent();
                        zoomTo(root);
                    }
                });

            // Add subtle shadow/glow effect
            const defs = svg.append('defs');
            const filter = defs.append('filter')
                .attr('id', 'center-glow')
                .attr('x', '-50%')
                .attr('y', '-50%')
                .attr('width', '200%')
                .attr('height', '200%');
            
            filter.append('feGaussianBlur')
                .attr('in', 'SourceGraphic')
                .attr('stdDeviation', '3');

            const centerCircle = centerGroup.append('circle')
                .attr('r', innerRadiusOffset - 5)
                .attr('fill', 'var(--white)')
                .attr('stroke', 'var(--black)')
                .attr('stroke-width', 3)
                .attr('filter', 'url(#center-glow)')
                .style('transition', 'all 0.3s ease');

            // Center text elements with improved spacing
            const centerText = centerGroup.append('g');
            
            // Add "BACK" indicator that shows on hover when zoomed in
            const backIndicator = centerText.append('text')
                .attr('class', 'sunburst-center-text sunburst-center-back')
                .attr('dy', '-2.5em')
                .style('font-size', '12px')
                .style('font-weight', '700')
                .style('letter-spacing', '1px')
                .style('fill', '#666')
                .text('← BACK');
            
            const titleText = centerText.append('text')
                .attr('class', 'sunburst-center-text')
                .attr('dy', '-1em')
                .style('font-size', '14px')
                .style('font-weight', '700')
                .style('letter-spacing', '2px')
                .style('fill', '#666')
                .text('ATLAS');

            const countText = centerText.append('text')
                .attr('class', 'sunburst-center-text')
                .attr('dy', '0.7em')
                .style('font-size', '48px')
                .style('font-weight', '900')
                .style('letter-spacing', '-2px')
                .text(filteredCreators.length);

            const labelText = centerText.append('text')
                .attr('class', 'sunburst-center-text')
                .attr('dy', '2.8em')
                .style('font-size', '13px')
                .style('font-weight', '600')
                .style('fill', '#666')
                .text('creators');

            // Zoom function
            function zoomTo(p) {
                focusedNode = p;

                // Update breadcrumb with home icon
                const breadcrumb = document.getElementById('sunburstBreadcrumb');
                let breadcrumbHTML = '<span class="breadcrumb-item" onclick="resetSunburst()" style="cursor: pointer;" title="Reset to view all creators">&#x1F30F;  All Creators</span>';

                if (p.depth >= 1) {
                    const platform = p.depth === 1 ? p : p.parent;
                    breadcrumbHTML += ' <span class="breadcrumb-separator">&rsaquo;</span> ';
                    if (p.depth === 1) {
                        // At platform level — active, no click needed
                        breadcrumbHTML += `<span class="breadcrumb-item active">${platform.data.name}</span>`;
                    } else {
                        // At group level — platform is clickable to go back
                        breadcrumbHTML += `<span class="breadcrumb-item" onclick="sunburstNavigateToPlatform('${platform.data.name}')" style="cursor: pointer;">${platform.data.name}</span>`;
                    }
                }

                if (p.depth === 2) {
                    breadcrumbHTML += ' <span class="breadcrumb-separator">&rsaquo;</span> ';
                    breadcrumbHTML += `<span class="breadcrumb-item active">${p.data.name}</span>`;
                }

                breadcrumb.innerHTML = breadcrumbHTML;

                // Update center text based on what's focused
                const legendEl = document.getElementById('sunburstLegend');
                if (p === root) {
                    // At root - hide back indicator, show legend, hide creators
                    backIndicator.style('opacity', '0');
                    titleText.text('ATLAS')
                        .style('font-size', '14px')
                        .style('letter-spacing', '2px')
                        .style('fill', '#666');
                    countText.text(filteredCreators.length)
                        .style('font-size', '48px')
                        .style('letter-spacing', '-2px');
                    labelText.text('creators')
                        .style('font-size', '13px');
                    hideVizCreators('wheelCreators');
                    atlasCloseDrawer();
                    centerCircle.classed('atlas-center-pulsing', false);
                    if (legendEl) legendEl.style.display = '';
                } else if (p.depth === 1) {
                    // Platform level - show platform creators table, hide legend
                    backIndicator.style('opacity', '0.6');
                    const centerDiam = (innerRadiusOffset - 5) * 2;
                    const platformName = truncateToFit(p.data.name, centerDiam - 20, 12);
                    titleText.text(platformName.toUpperCase())
                        .style('font-size', '12px')
                        .style('letter-spacing', '1px')
                        .style('fill', '#666');
                    countText.text(p.value)
                        .style('font-size', '48px')
                        .style('letter-spacing', '-2px');
                    labelText.text(`creators in ${p.children.length} group${p.children.length !== 1 ? 's' : ''}`)
                        .style('font-size', '12px');
                    if (legendEl) legendEl.style.display = 'none';
                    centerCircle.classed('atlas-center-pulsing', window.innerWidth <= 768);
                    // Show all creators for this platform
                    const platformCreators = filteredCreators.filter(c => c.platform === p.data.name);
                    if (window.innerWidth <= 768) {
                        clearTimeout(_drawerOpenTimer);
                        _drawerOpenTimer = setTimeout(() => atlasOpenDrawer(p.data.name, platformCreators, null), 800);
                    } else {
                        showVizCreators('wheelCreators', platformCreators, p.data.name);
                    }
                } else if (p.depth === 2) {
                    // Group level - show group creators table, hide legend
                    backIndicator.style('opacity', '0.6');
                    const centerDiam2 = (innerRadiusOffset - 5) * 2;
                    const topicName = truncateToFit(p.data.name, centerDiam2 - 20, 11);
                    titleText.text(topicName.toUpperCase())
                        .style('font-size', '11px')
                        .style('letter-spacing', '0.5px')
                        .style('fill', '#666');
                    countText.text(p.value)
                        .style('font-size', '56px')
                        .style('letter-spacing', '-2px');
                    labelText.text(`creator${p.value !== 1 ? 's' : ''}`)
                        .style('font-size', '13px');
                    if (legendEl) legendEl.style.display = 'none';
                    centerCircle.classed('atlas-center-pulsing', window.innerWidth <= 768);
                    // Show creators for this specific group on this platform
                    const groupCreators = filteredCreators.filter(c => c.platform === p.data.platform && c.group === p.data.name);
                    if (window.innerWidth <= 768) {
                        clearTimeout(_drawerOpenTimer);
                        _drawerOpenTimer = setTimeout(() => atlasOpenDrawer(p.data.platform, groupCreators, p.data.name), 800);
                    } else {
                        showVizCreators('wheelCreators', groupCreators, p.data.name);
                    }
                }

                root.each(d => d.target = {
                    x0: Math.max(0, Math.min(1, (d.x0 - p.x0) / (p.x1 - p.x0))) * 2 * Math.PI,
                    x1: Math.max(0, Math.min(1, (d.x1 - p.x0) / (p.x1 - p.x0))) * 2 * Math.PI,
                    y0: Math.max(0, d.y0 - p.y0),
                    y1: Math.max(0, d.y1 - p.y0)
                });

                const t = g.transition()
                    .duration(750)
                    .ease(d3.easeCubicOut);

                // Transition arcs
                path.transition(t)
                    .tween('data', d => {
                        const i = d3.interpolate(d.current, d.target);
                        return t => d.current = i(t);
                    })
                    .attr('d', d => {
                        const arcGen = d3.arc()
                            .startAngle(d => d.x0)
                            .endAngle(d => d.x1)
                            .padAngle(d => Math.min((d.x1 - d.x0) / 2, 0.005))
                            .padRadius(radius / 2)
                            .innerRadius(d => d.y0)
                            .outerRadius(d => d.y1 - 1);
                        return arcGen(d.current);
                    })
                    .attr('opacity', d => {
                        // Fade out arcs not in focused subtree with better contrast
                        return d.depth === 0 || (d.depth === 1 && p === root) || 
                               (p.depth === 1 && d.parent === p) ||
                               (p.depth === 2 && (d === p || d === p.parent)) ? 0.95 : 0.2;
                    });

                // Transition labels
                labels.transition(t)
                    .attr('transform', d => {
                        const angle = (d.current.x0 + d.current.x1) / 2 * 180 / Math.PI;
                        const radius = (d.current.y0 + d.current.y1) / 2;
                        return `rotate(${angle - 90}) translate(${radius},0) rotate(${angle < 180 ? 0 : 180})`;
                    })
                    .attr('opacity', d => {
                        if (d.depth === 0) return 0;
                        const angle = d.current.x1 - d.current.x0;
                        const radiusSize = d.current.y1 - d.current.y0;
                        const isInFocus = (p === root) || (d.parent === p) || (d === p) || (p.depth === 2 && d === p.parent);
                        return (angle > 0.1 && radiusSize > 30 && isInFocus) ? 1 : 0;
                    });
            }

            // Expose zoomTo for breadcrumb navigation
            window._sunburstZoomTo = zoomTo;

            // Initialize current positions
            root.each(d => d.current = {
                x0: d.x0,
                x1: d.x1,
                y0: d.y0,
                y1: d.y1
            });

            // Build legend
            const uniquePlatforms = [...new Set(Object.keys(platformData))];
            const legendHTML = uniquePlatforms.map(platform => {
                const count = Object.values(platformData[platform]).reduce((a, b) => a + b, 0);
                return `
                    <div class="legend-item">
                        <div class="legend-color" style="background-color: ${getPlatformColor(platform)}"></div>
                        <span>${platform} (${count})</span>
                    </div>
                `;
            }).join('');
            document.getElementById('sunburstLegend').innerHTML = legendHTML;
        }

        // Treemap Chart Rendering
        // Treemap drill-down state
        let treemapDrillGroup = null; // null = show all groups, string = drilled into a group

        function renderTreemapChart() {
            const container = document.getElementById('treemapChart');
            container.innerHTML = ''; // Clear previous
            hideVizCreators('treemapCreators'); // Clear creator results on re-render

            const width = container.clientWidth || 1000;
            const height = window.innerWidth <= 768 ? 500 : 600;

            // Color scale for groups
            const groupColors = {
                'Power & Politics': '#FF6B6B',
                'Money & Work': '#4ECDC4',
                'Civic Life': '#45B7D1',
                'Social Issues': '#FFA07A',
                'Science, Health & Environment': '#98D8C8',
                'Culture & Media': '#F7B801',
                'Lifestyle & Personal Life': '#E056FD',
                'Journalism Formats': '#686DE0',
                'General News': '#95A5A6'
            };

            // Build hierarchy from filtered creators
            const fullHierarchy = buildTreemapHierarchy(filteredCreators);

            let displayData;
            if (treemapDrillGroup) {
                // Drilled into a group — show only that group's topics as top-level
                const groupNode = fullHierarchy.children.find(c => c.name === treemapDrillGroup);
                if (groupNode && groupNode.children && groupNode.children.length > 0) {
                    displayData = { name: 'root', children: groupNode.children };
                } else {
                    displayData = { name: 'root', children: [{ name: 'No topics', value: 1 }] };
                }
            } else {
                // Top level — show groups with nested topic subdivisions
                displayData = {
                    name: 'root',
                    children: fullHierarchy.children.map(g => ({
                        name: g.name,
                        isGroup: true,
                        children: g.children && g.children.length > 0
                            ? g.children.map(t => ({
                                name: t.name,
                                value: t.value,
                                parentGroup: g.name,
                                isTopicInGroup: true
                            }))
                            : [{ name: g.name, value: 0, parentGroup: g.name, isTopicInGroup: true }]
                    }))
                };
            }

            // Create SVG
            const svg = d3.select(container)
                .append('svg')
                .attr('width', width)
                .attr('height', height)
                .attr('viewBox', `0 0 ${width} ${height}`)
                .style('max-width', '100%')
                .style('height', 'auto');

            // Create treemap layout
            const isNested = !treemapDrillGroup;
            const treemap = d3.treemap()
                .size([width, height])
                .paddingOuter(3)
                .paddingTop(isNested ? 26 : 3)
                .paddingInner(isNested ? 1 : 3)
                .round(true);

            const root = d3.hierarchy(displayData)
                .sum(d => d.value || 0)
                .sort((a, b) => b.value - a.value);

            treemap(root);

            // Function to get color for a leaf node
            function getColor(d) {
                if (treemapDrillGroup) {
                    // Inside a group — all topics share the group's color but varied
                    const baseColor = groupColors[treemapDrillGroup] || '#666666';
                    const siblings = d.parent ? d.parent.children : [d];
                    const idx = siblings.indexOf(d);
                    const brightness = 0.3 + (idx % 5) * 0.15;
                    return d3.color(baseColor).brighter(brightness);
                } else if (d.data.isTopicInGroup || d.data.parentGroup) {
                    // Top level nested — topic cell within a group
                    const groupName = d.data.parentGroup || (d.parent ? d.parent.data.name : '');
                    const baseColor = groupColors[groupName] || '#666666';
                    const siblings = d.parent ? d.parent.children : [d];
                    const idx = siblings.indexOf(d);
                    const brightness = 0.15 + (idx % 4) * 0.2;
                    return d3.color(baseColor).brighter(brightness);
                } else {
                    return groupColors[d.data.name] || '#666666';
                }
            }

            // Function to determine text color based on background brightness
            function getTextColor(bgColor) {
                const c = d3.color(bgColor);
                if (!c) return '#000';
                const r = c.r || 0, g = c.g || 0, b = c.b || 0;
                const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
                return luminance > 0.55 ? '#000' : '#fff';
            }

            if (isNested) {
                // === NESTED TOP-LEVEL VIEW ===
                // Draw group backgrounds (depth 1) with group name labels
                const groupNodes = root.children || [];
                const groupCells = svg.selectAll('.treemap-group')
                    .data(groupNodes)
                    .enter()
                    .append('g')
                    .attr('class', 'treemap-group')
                    .attr('transform', d => `translate(${d.x0},${d.y0})`);

                // Group background rectangles
                groupCells.append('rect')
                    .attr('width', d => d.x1 - d.x0)
                    .attr('height', d => d.y1 - d.y0)
                    .style('fill', d => {
                        const c = d3.color(groupColors[d.data.name] || '#666');
                        c.opacity = 0.12;
                        return c;
                    })
                    .style('stroke', '#fff')
                    .style('stroke-width', '3px')
                    .style('cursor', 'pointer')
                    .on('click', function(event, d) {
                        event.stopPropagation();
                        treemapDrillGroup = d.data.name;
                        filterState.toggleSilent('group', d.data.name);
                        renderTreemapChart();
                        showVizCreators('treemapCreators', filteredCreators, d.data.name);
                        updateTreemapBreadcrumb();
                    });

                // Group name labels at top of each group cell
                groupCells.filter(d => (d.x1 - d.x0) > 50)
                    .append('text')
                    .attr('x', 5)
                    .attr('y', -8)
                    .style('font-size', d => (d.x1 - d.x0) > 140 ? '12px' : '10px')
                    .style('font-weight', '800')
                    .style('fill', d => groupColors[d.data.name] || '#333')
                    .style('pointer-events', 'none')
                    .text(d => {
                        const w = d.x1 - d.x0;
                        const fontSize = w > 140 ? 12 : 10;
                        return truncateToFit(d.data.name, w - 10, fontSize);
                    });

                // Topic leaf cells (depth 2) within each group
                const topicCells = svg.selectAll('.treemap-cell')
                    .data(root.leaves())
                    .enter()
                    .append('g')
                    .attr('class', 'treemap-cell')
                    .attr('transform', d => `translate(${d.x0},${d.y0})`);

                topicCells.append('rect')
                    .attr('width', d => Math.max(0, d.x1 - d.x0))
                    .attr('height', d => Math.max(0, d.y1 - d.y0))
                    .style('fill', d => getColor(d))
                    .style('stroke', 'rgba(255,255,255,0.7)')
                    .style('stroke-width', '1px')
                    .style('cursor', 'pointer')
                    .on('click', function(event, d) {
                        event.stopPropagation();
                        // Clicking a topic at top level drills into its parent group
                        const groupName = d.data.parentGroup || (d.parent ? d.parent.data.name : '');
                        treemapDrillGroup = groupName;
                        filterState.toggleSilent('group', groupName);
                        renderTreemapChart();
                        showVizCreators('treemapCreators', filteredCreators, groupName);
                        updateTreemapBreadcrumb();
                    })
                    .on('mouseover', function(event, d) {
                        d3.select(this)
                            .style('opacity', 0.8)
                            .style('stroke-width', '2px')
                            .style('stroke', '#fff');
                        showTreemapTooltip(event, d);
                    })
                    .on('mouseout', function(event, d) {
                        d3.select(this)
                            .style('opacity', 1)
                            .style('stroke-width', '1px')
                            .style('stroke', 'rgba(255,255,255,0.7)');
                        hideTreemapTooltip();
                    })
                    .append('title')
                    .text(d => {
                        const groupName = d.data.parentGroup || (d.parent ? d.parent.data.name : '');
                        return `${d.data.name}\n${d.value} creator${d.value !== 1 ? 's' : ''}\nGroup: ${groupName}\nClick to drill down`;
                    });

                // Topic name labels — only on cells large enough
                topicCells.filter(d => (d.x1 - d.x0) > 45 && (d.y1 - d.y0) > 22)
                    .append('text')
                    .attr('class', 'treemap-label')
                    .attr('x', 4)
                    .attr('y', 14)
                    .style('font-size', d => {
                        const area = (d.x1 - d.x0) * (d.y1 - d.y0);
                        return area > 8000 ? '11px' : '9px';
                    })
                    .style('font-weight', '600')
                    .style('fill', d => getTextColor(getColor(d)))
                    .style('pointer-events', 'none')
                    .text(d => {
                        const w = d.x1 - d.x0;
                        const area = w * (d.y1 - d.y0);
                        const fontSize = area > 8000 ? 11 : 9;
                        return truncateToFit(d.data.name, w - 8, fontSize);
                    })
                    .append('title')
                    .text(d => d.data.name);

                // Count labels on larger topic cells
                topicCells.filter(d => (d.x1 - d.x0) > 55 && (d.y1 - d.y0) > 38)
                    .append('text')
                    .attr('class', 'treemap-count')
                    .attr('x', 4)
                    .attr('y', d => (d.y1 - d.y0) - 5)
                    .style('font-size', '10px')
                    .style('font-weight', '400')
                    .style('fill', d => {
                        const textCol = getTextColor(getColor(d));
                        return textCol === '#fff' ? 'rgba(255,255,255,0.7)' : 'rgba(0,0,0,0.5)';
                    })
                    .style('pointer-events', 'none')
                    .text(d => d.value);

            } else {
                // === DRILLED VIEW (existing flat view) ===
                const cells = svg.selectAll('g')
                    .data(root.leaves())
                    .enter()
                    .append('g')
                    .attr('class', 'treemap-cell')
                    .attr('transform', d => `translate(${d.x0},${d.y0})`);

                cells.append('rect')
                    .attr('width', d => d.x1 - d.x0)
                    .attr('height', d => d.y1 - d.y0)
                    .style('fill', d => getColor(d))
                    .style('stroke', '#fff')
                    .style('stroke-width', '2px')
                    .style('cursor', 'pointer')
                    .append('title')
                    .text(d => `${d.data.name}\n${d.value} creator${d.value !== 1 ? 's' : ''}\nClick to filter`);

                cells.select('rect')
                    .on('click', function(event, d) {
                        event.stopPropagation();
                        const name = d.data.name;
                        const wasActive = filterState.has('topic', name);
                        filterState.toggleSilent('topic', name);
                        if (!wasActive) {
                            const topicCreators = filteredCreators.filter(c => c.topic === name);
                            showVizCreators('treemapCreators', topicCreators, name);
                        } else {
                            const activeTopics = filterState.filters.topic;
                            if (activeTopics.size > 0) {
                                const topicCreators = filteredCreators.filter(c => activeTopics.has(c.topic));
                                showVizCreators('treemapCreators', topicCreators, [...activeTopics].join(', '));
                            } else {
                                showVizCreators('treemapCreators', filteredCreators, treemapDrillGroup);
                            }
                        }
                        svg.selectAll('rect').style('stroke', '#fff').style('stroke-width', '2px');
                        svg.selectAll('rect').filter(function(r) {
                            return filterState.has('topic', r.data.name);
                        }).style('stroke', '#000').style('stroke-width', '3px');
                        updateTreemapBreadcrumb();
                    })
                    .on('mouseover', function(event, d) {
                        d3.select(this)
                            .style('opacity', 0.8)
                            .style('stroke-width', '3px');
                        showTreemapTooltip(event, d);
                    })
                    .on('mouseout', function(event, d) {
                        d3.select(this)
                            .style('opacity', 1);
                        const isSelected = filterState.has('topic', d.data.name);
                        d3.select(this)
                            .style('stroke-width', isSelected ? '3px' : '2px')
                            .style('stroke', isSelected ? '#000' : '#fff');
                        hideTreemapTooltip();
                    });

                cells.append('text')
                    .attr('class', 'treemap-label')
                    .attr('x', 6)
                    .attr('y', 20)
                    .style('font-size', d => {
                        const area = (d.x1 - d.x0) * (d.y1 - d.y0);
                        return area > 15000 ? '15px' : area > 5000 ? '13px' : area > 2000 ? '11px' : '9px';
                    })
                    .style('font-weight', '700')
                    .style('fill', d => getTextColor(getColor(d)))
                    .style('pointer-events', 'none')
                    .text(d => {
                        const w = d.x1 - d.x0;
                        const area = w * (d.y1 - d.y0);
                        const fontSize = area > 15000 ? 15 : area > 5000 ? 13 : area > 2000 ? 11 : 9;
                        return truncateToFit(d.data.name, w - 12, fontSize);
                    })
                    .append('title')
                    .text(d => `${d.data.name}\n${d.value} creator${d.value !== 1 ? 's' : ''}`);

                cells.filter(d => (d.x1 - d.x0) > 80 && (d.y1 - d.y0) > 45)
                    .append('text')
                    .attr('class', 'treemap-count')
                    .attr('x', 6)
                    .attr('y', d => (d.y1 - d.y0) - 8)
                    .style('font-size', '12px')
                    .style('font-weight', '400')
                    .style('fill', d => {
                        const textCol = getTextColor(getColor(d));
                        return textCol === '#fff' ? 'rgba(255,255,255,0.8)' : 'rgba(0,0,0,0.6)';
                    })
                    .style('pointer-events', 'none')
                    .text(d => `${d.value} creator${d.value !== 1 ? 's' : ''}`);
            }

            // Update breadcrumb
            updateTreemapBreadcrumb();
        }

        // Treemap breadcrumb management
        function updateTreemapBreadcrumb() {
            const breadcrumb = document.getElementById('treemapBreadcrumb');
            if (!breadcrumb) return;

            let html = '<span class="breadcrumb-item' + (!treemapDrillGroup ? ' active' : '') + '" onclick="treemapNavigateTo(\'root\')" style="cursor:pointer;">All Groups</span>';

            if (treemapDrillGroup) {
                html += ' <span class="breadcrumb-separator">&rsaquo;</span> ';
                const activeTopics = filterState.filters.topic;
                const isGroupOnly = activeTopics.size === 0;
                html += `<span class="breadcrumb-item${isGroupOnly ? ' active' : ''}" onclick="treemapNavigateTo('group')" style="cursor:pointer;">${treemapDrillGroup}</span>`;

                if (activeTopics.size > 0) {
                    html += ' <span class="breadcrumb-separator">&rsaquo;</span> ';
                    html += `<span class="breadcrumb-item active">${[...activeTopics].join(', ')}</span>`;
                }
            }

            breadcrumb.innerHTML = html;
        }

        function treemapNavigateTo(level) {
            if (level === 'root') {
                // Go back to all groups view
                treemapDrillGroup = null;
                filterState.filters.group.clear();
                filterState.filters.topic.clear();
                filterState.syncUIForType('group');
                filterState.syncUIForType('topic');
                filterState.applyFiltersSilent();
                renderTreemapChart();
            } else if (level === 'group') {
                // Stay in group but clear topic selection
                filterState.filters.topic.clear();
                filterState.syncUIForType('topic');
                filterState.applyFiltersSilent();
                // Re-render to clear topic highlighting
                const container = document.getElementById('treemapChart');
                // Don't re-render whole treemap, just clear visual selection + update creators
                const svg = container.querySelector('svg');
                if (svg) {
                    d3.select(svg).selectAll('rect')
                        .style('stroke', '#fff')
                        .style('stroke-width', '2px');
                }
                showVizCreators('treemapCreators', filteredCreators, treemapDrillGroup);
                updateTreemapBreadcrumb();
            }
        }

        function buildTreemapHierarchy(creators) {
            const hierarchy = {
                name: 'root',
                children: []
            };
            
            const byGroup = {};
            creators.forEach(creator => {
                const group = creator.group || 'Uncategorized';
                if (!byGroup[group]) {
                    byGroup[group] = {};
                }
                
                const topic = creator.topic || 'Other';
                if (!byGroup[group][topic]) {
                    byGroup[group][topic] = [];
                }
                
                byGroup[group][topic].push(creator);
            });
            
            ORDERED_GROUPS.forEach(group => {
                if (!byGroup[group]) return;
                
                const groupNode = {
                    name: group,
                    children: []
                };
                
                Object.keys(byGroup[group]).sort().forEach(topic => {
                    const creators = byGroup[group][topic];
                    groupNode.children.push({
                        name: topic,
                        value: creators.length,
                        creators: creators
                    });
                });
                
                hierarchy.children.push(groupNode);
            });
            
            Object.keys(byGroup).forEach(group => {
                if (!ORDERED_GROUPS.includes(group)) {
                    const groupNode = {
                        name: group,
                        children: []
                    };
                    
                    Object.keys(byGroup[group]).sort().forEach(topic => {
                        const creators = byGroup[group][topic];
                        groupNode.children.push({
                            name: topic,
                            value: creators.length,
                            creators: creators
                        });
                    });
                    
                    hierarchy.children.push(groupNode);
                }
            });
            
            return hierarchy;
        }

        // Create treemap tooltip once
        const treemapTooltipEl = document.createElement('div');
        treemapTooltipEl.className = 'treemap-tooltip';
        document.body.appendChild(treemapTooltipEl);

        function showTreemapTooltip(event, d) {
            const tooltip = treemapTooltipEl;

            let label;
            let extra = '';
            if (d.data.isTopicInGroup) {
                label = 'Topic';
                extra = `<span style="opacity: 0.6; font-size: 11px;">${d.data.parentGroup}</span><br>`;
            } else if (treemapDrillGroup) {
                label = 'Topic';
            } else {
                label = 'Group';
            }

            tooltip.innerHTML = `
                ${extra}
                <strong>${label}: ${d.data.name}</strong><br>
                ${d.value} creator${d.value !== 1 ? 's' : ''}<br>
                <span style="opacity: 0.7; font-size: 11px;">Click to explore</span>
            `;
            
            tooltip.style.display = 'block';
            tooltip.style.left = Math.min(event.pageX + 10, window.innerWidth - 260) + 'px';
            tooltip.style.top = (event.pageY + 10) + 'px';
        }

        function hideTreemapTooltip() {
            treemapTooltipEl.style.display = 'none';
        }

        function resetSunburst() {
            atlasCloseDrawer();
            // clearAll() resets filters, re-filters data, updates URL, and re-renders current view
            filterState.clearAll();
        }

        function sunburstNavigateToPlatform(platformName) {
            atlasCloseDrawer();
            // Navigate back to platform level from group level
            if (!window._sunburstZoomTo || !window._sunburstRoot) return;
            const root = window._sunburstRoot;
            // Find the platform node
            const platformNode = root.children ? root.children.find(c => c.data.name === platformName) : null;
            if (platformNode) {
                // Clear group filter, keep platform filter
                filterState.filters.group.clear();
                filterState.syncUIForType('group');
                filterState.applyFiltersSilent();
                window._sunburstZoomTo(platformNode);
            }
        }

        function showCreatorsForSelection(platform, group) {
            const creatorsContainer = document.getElementById('sunburstCreators');

            // Filter creators — hierarchy is Platform → Group
            let selectedCreators = filteredCreators.filter(c => {
                if (group) {
                    return c.platform === platform && c.group === group;
                } else {
                    return c.platform === platform;
                }
            });

            if (selectedCreators.length === 0) {
                creatorsContainer.innerHTML = '<p style="text-align: center; color: #666;">No creators found</p>';
                creatorsContainer.classList.add('active');
                return;
            }

            // Build creator cards
            const cardsHTML = selectedCreators.map(creator => {
                const initials = creator.name
                    .split(' ')
                    .map(word => word[0])
                    .join('')
                    .substring(0, 2)
                    .toUpperCase();

                return `
                    <div class="sunburst-creator-card" onclick="window.open('${creator.link}', '_blank')">
                        <div class="sunburst-creator-avatar">${initials}</div>
                        <div class="sunburst-creator-name">${creator.name}</div>
                        <div class="sunburst-creator-channel">${creator.channel || 'Creator'}</div>
                    </div>
                `;
            }).join('');

            creatorsContainer.innerHTML = cardsHTML;
            creatorsContainer.classList.add('active');
        }

        function hideCreators() {
            document.getElementById('sunburstCreators').classList.remove('active');
        }

        // Shared function to render a creator results table inside any visualization
        function showVizCreators(containerId, creators, title) {
            const container = document.getElementById(containerId);
            if (!container) return;

            if (!creators || creators.length === 0) {
                container.innerHTML = '<p style="text-align: center; color: #666; padding: 1rem;">No creators found</p>';
                container.classList.add('active');
                return;
            }

            const rows = creators.map(c => `
                <tr>
                    <td><a href="${c.link}" target="_blank" rel="noopener">${c.name}</a></td>
                    <td>${c.channel || ''}</td>
                    <td>${c.platform || ''}</td>
                    <td>${c.topic || ''}</td>
                </tr>
            `).join('');

            container.innerHTML = `
                <div class="viz-creators-header">
                    <h3>${title}</h3>
                    <span>${creators.length} creator${creators.length !== 1 ? 's' : ''}</span>
                </div>
                <table class="viz-creators-table">
                    <thead>
                        <tr><th>Name</th><th>Channel</th><th>Platform</th><th>Topic</th></tr>
                    </thead>
                    <tbody>${rows}</tbody>
                </table>
            `;
            container.classList.add('active');
        }

        function hideVizCreators(containerId) {
            const container = document.getElementById(containerId);
            if (container) {
                container.classList.remove('active');
                container.innerHTML = '';
            }
        }

        function showSunburstTooltip(event, d) {
            const tooltip = document.getElementById('sunburstTooltip');
            
            if (d.depth === 1) {
                // Platform level
                const groupCount = d.children.length;
                const percentage = ((d.value / filteredCreators.length) * 100).toFixed(1);
                tooltip.innerHTML = `
                    <div style="font-weight: 700; font-size: 14px; margin-bottom: 4px;">${d.data.name}</div>
                    <div style="font-size: 13px; color: #666;">${d.value} creators (${percentage}%)</div>
                    <div style="font-size: 12px; color: #999; margin-top: 2px;">${groupCount} group${groupCount !== 1 ? 's' : ''}</div>
                `;
            } else if (d.depth === 2) {
                // Group level (outer ring)
                const percentage = ((d.value / filteredCreators.length) * 100).toFixed(1);
                tooltip.innerHTML = `
                    <div style="font-size: 12px; color: #999;">${d.data.platform}</div>
                    <div style="font-weight: 700; font-size: 14px; margin: 2px 0 4px 0;">${d.data.name}</div>
                    <div style="font-size: 13px; color: #666;">${d.value} creator${d.value !== 1 ? 's' : ''} (${percentage}%)</div>
                `;
            }
            
            const tx = Math.min(event.pageX + 15, window.innerWidth - 220);
            tooltip.style.left = tx + 'px';
            tooltip.style.top = (event.pageY - 15) + 'px';
            tooltip.style.opacity = 1;
        }

        function hideSunburstTooltip() {
            document.getElementById('sunburstTooltip').style.opacity = 0;
        }

        // ── Share this view ──────────────────────────────────────────────────
        function shareCurrentView() {
            const url = window.location.href;
            navigator.clipboard.writeText(url).then(() => {
                const btn = document.getElementById('shareViewBtn');
                const original = btn.innerHTML;
                btn.innerHTML = '✓ Copied!';
                btn.classList.add('copied');
                setTimeout(() => {
                    btn.innerHTML = original;
                    btn.classList.remove('copied');
                }, 2000);
            }).catch(() => {
                // Fallback for browsers that block clipboard without https
                prompt('Copy this link:', url);
            });
        }

        // ── Mobile Bottom Drawer (wheel view, ≤768px) ────────────────────────
        let _atlasDrawerData = null;

        function _atlasExtractTopic(topicString) {
            return topicString ? topicString.split(',')[0].trim() : '';
        }

        // ── Drawer state machine ─────────────────────────────────────────
        // States: 'closed' | 'full' | 'peek' | 'pill'
        let _drawerState = 'closed';
        let _fromPopstate = false;    // true during popstate handling — skip pushState
        let _drawerOpenTimer = null;  // tracks pending 800ms open delay — cancel on re-tap

        function _setDrawerState(state) {
            const drawer = document.getElementById('atlasBottomDrawer');
            const backdrop = document.getElementById('atlasDrawerBackdrop');
            if (!drawer || !backdrop) return;

            _drawerState = state;

            // Remove all state classes
            drawer.classList.remove('visible', 'peek', 'pill');
            backdrop.classList.remove('visible', 'peek', 'pill');

            if (state === 'full') {
                drawer.classList.add('visible');
                backdrop.classList.add('visible');
                // Push history entry so back button can collapse (skip during popstate)
                if (!_fromPopstate) {
                    const curState = history.state && history.state.drawerState;
                    if (curState !== 'full') history.pushState({ drawerState: 'full' }, '');
                }
            } else if (state === 'peek') {
                drawer.classList.add('visible', 'peek');
                backdrop.classList.add('peek'); // transparent, passes touches through
                if (!_fromPopstate) {
                    const curState = history.state && history.state.drawerState;
                    if (curState !== 'peek') history.pushState({ drawerState: 'peek' }, '');
                }
            } else if (state === 'pill') {
                drawer.classList.add('visible', 'pill');
                backdrop.classList.add('pill');
                if (!_fromPopstate) {
                    const curState = history.state && history.state.drawerState;
                    if (curState !== 'pill') history.pushState({ drawerState: 'pill' }, '');
                }
            }
            // 'closed': no classes added, drawer slides out via translateY(100%)
        }

        function atlasOpenDrawer(platform, creators, specificGroup) {
            if (window.innerWidth > 768) return;
            if (!creators || creators.length === 0) return; // nothing to show
            _atlasDrawerData = { platform, creators, specificGroup };
            _packCurrentDrawerCreators = creators;

            // Update title
            const title = document.getElementById('atlasDrawerTitle');
            if (title) {
                const label = specificGroup || platform;
                title.textContent = `${label} · ${creators.length} creator${creators.length !== 1 ? 's' : ''}`;
            }

            // Build content HTML
            const topicGroups = new Map();
            creators.forEach(c => {
                const t = _atlasExtractTopic(c.topic);
                if (!topicGroups.has(t)) topicGroups.set(t, []);
                topicGroups.get(t).push(c);
            });
            const sorted = Array.from(topicGroups.entries()).sort((a, b) => b[1].length - a[1].length);

            let html = '';
            sorted.forEach(([topic, list]) => {
                const key = _atlasTopicKey(topic);
                html += `<div class="atlas-drawer-topic-group" data-topic-key="${key}" data-topic-name="${topic.replace(/"/g, '&quot;')}">`;
                html += `<div class="atlas-drawer-topic-header">${topic} (${list.length})</div>`;
                const show = list.slice(0, 10);
                show.forEach(c => { html += _atlasDrawerCard(c); });
                if (list.length > 10) {
                    const rem = list.length - 10;
                    html += `<button class="atlas-drawer-show-more" onclick="atlasExpandTopic('${key}')">Show ${rem} more</button>`;
                }
                html += `</div>`;
            });

            document.getElementById('atlasDrawerContent').innerHTML = html;

            // If already open (switching segments), update content without re-animating
            if (_drawerState === 'full' || _drawerState === 'peek') {
                // Scroll content back to top on segment switch
                const content = document.getElementById('atlasDrawerContent');
                if (content) content.scrollTop = 0;
            } else {
                _setDrawerState('full');
            }

            setTimeout(function() {
                if (typeof _packMaybeEnableSelection === 'function') _packMaybeEnableSelection();
            }, 60);
        }

        function atlasCloseDrawer() {
            const drawer = document.getElementById('atlasBottomDrawer');
            const backdrop = document.getElementById('atlasDrawerBackdrop');
            if (drawer) drawer.classList.remove('visible', 'peek', 'pill');
            if (backdrop) backdrop.classList.remove('visible', 'peek', 'pill');
            _drawerState = 'closed';
            _atlasDrawerData = null;
        }

        function _atlasDrawerCard(creator) {
            const topic = _atlasExtractTopic(creator.topic);
            // Use data-link instead of inline onclick to avoid any XSS risk from creator URLs
            const escapedLink = (creator.link || '').replace(/"/g, '&quot;');
            return `
                <div class="atlas-drawer-card" data-link="${escapedLink}">
                    <div class="atlas-drawer-card-name">${creator.name}</div>
                    <div class="atlas-drawer-card-channel">${creator.channel || ''}</div>
                    <span class="atlas-drawer-card-tag">${topic}</span>
                </div>`;
        }

        // Use a sanitised key for data-topic to avoid querySelector issues with special chars
        function _atlasTopicKey(topic) {
            return topic.replace(/[^a-zA-Z0-9-_]/g, '_');
        }

        window.atlasExpandTopic = function(topicKey) {
            if (!_atlasDrawerData) return;
            const group = document.querySelector(`.atlas-drawer-topic-group[data-topic-key="${topicKey}"]`);
            if (!group) return;
            const topicName = group.dataset.topicName;
            const all = _atlasDrawerData.creators.filter(c => _atlasExtractTopic(c.topic) === topicName);
            const drawerContent = document.getElementById('atlasDrawerContent');
            const scrollBefore = drawerContent ? drawerContent.scrollTop : 0;
            let html = `<div class="atlas-drawer-topic-header">${topicName} (${all.length})</div>`;
            all.forEach(c => { html += _atlasDrawerCard(c); });
            group.innerHTML = html;
            // Restore scroll position — innerHTML reflow can jump the viewport
            if (drawerContent) drawerContent.scrollTop = scrollBefore;
        };

// ─────────────────────────────────────────────────────────────────────────
// Mobile Menu, Filter Toggle, Pack System
// ─────────────────────────────────────────────────────────────────────────

    // Mobile Menu Toggle
    (function() {
        const menuButton = document.getElementById('mobileMenuButton');
        const mobileMenu = document.getElementById('mobileMenu');
        const menuOverlay = document.getElementById('mobileMenuOverlay');
        const menuClose = document.getElementById('mobileMenuClose');

        function openMenu() {
            mobileMenu.classList.add('active');
            menuOverlay.classList.add('active');
            document.body.style.overflow = 'hidden';
        }

        function closeMenu() {
            mobileMenu.classList.remove('active');
            menuOverlay.classList.remove('active');
            document.body.style.overflow = '';
        }

        if (menuButton) {
            menuButton.addEventListener('click', openMenu);
        }

        if (menuClose) {
            menuClose.addEventListener('click', closeMenu);
        }

        if (menuOverlay) {
            menuOverlay.addEventListener('click', closeMenu);
        }

        // Close menu on escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && mobileMenu.classList.contains('active')) {
                closeMenu();
            }
        });
    })();

    // ── Drawer gesture, history & touch containment ───────────────────────
    (function() {
        const drawer   = document.getElementById('atlasBottomDrawer');
        const handle   = document.getElementById('atlasDrawerHandle');
        const header   = document.getElementById('atlasDrawerHeader');  // may not exist
        const closeBtn = document.getElementById('atlasDrawerClose');
        const backdrop = document.getElementById('atlasDrawerBackdrop');
        const content  = document.getElementById('atlasDrawerContent');

        // Close button → collapse to peek (not full close)
        if (closeBtn) {
            closeBtn.addEventListener('click', function(e) {
                e.stopPropagation(); // don't let click fall through to backdrop or wheel
                if (_drawerState === 'full') {
                    _setDrawerState('peek');
                } else if (_drawerState === 'peek') {
                    _setDrawerState('pill');
                } else {
                    atlasCloseDrawer();
                }
            });
        }

        // Tapping the pill / handle when collapsed → expand back to full
        if (handle) {
            handle.addEventListener('click', function() {
                if (_drawerState === 'pill') _setDrawerState('full');
                else if (_drawerState === 'peek') _setDrawerState('full');
            });
        }

        // Backdrop tap — only fires when backdrop is actually pointer-events:auto (full state)
        if (backdrop) {
            backdrop.addEventListener('click', function() {
                _setDrawerState('peek');
            });
        }

        // ── Drag gesture on handle ──────────────────────────────────────
        // Only the handle has touch-action:none — the content still scrolls normally
        let dragStartY = 0;
        let dragStartState = 'full';
        let isDragging = false;

        function onDragStart(e) {
            dragStartY = e.touches ? e.touches[0].clientY : e.clientY;
            dragStartState = _drawerState;
            isDragging = true;
        }

        function onDragMove(e) {
            if (!isDragging) return;
            const currentY = e.touches ? e.touches[0].clientY : e.clientY;
            const delta = currentY - dragStartY; // positive = dragging down

            // Live-drag the drawer for tactile feel (no transition during drag)
            drawer.style.transition = 'none';
            const baseHeight = dragStartState === 'full' ? window.innerHeight * 0.72
                             : dragStartState === 'peek' ? window.innerHeight * 0.28
                             : 52;
            // delta > 0 = dragging down (collapsing), delta < 0 = dragging up (expanding)
            const maxHeight = window.innerHeight * 0.92;
            const newHeight = Math.min(maxHeight, Math.max(40, baseHeight - delta));
            drawer.style.height = newHeight + 'px';
        }

        function onDragEnd(e) {
            if (!isDragging) return;
            isDragging = false;

            // Re-enable transition
            drawer.style.transition = '';
            drawer.style.height = '';

            const endY = e.changedTouches ? e.changedTouches[0].clientY : e.clientY;
            const delta = endY - dragStartY;
            const velocity = delta; // simplification — positive = swipe down

            // Snap to state based on drag distance + direction
            if (dragStartState === 'full') {
                if (velocity > 160) _setDrawerState('pill');
                else if (velocity > 60) _setDrawerState('peek');
                else _setDrawerState('full'); // snap back
            } else if (dragStartState === 'peek') {
                if (velocity > 60) _setDrawerState('pill');
                else if (velocity < -60) _setDrawerState('full');
                else _setDrawerState('peek');
            } else if (dragStartState === 'pill') {
                if (velocity < -40) _setDrawerState('full');
                else _setDrawerState('pill');
            }
        }

        if (handle) {
            handle.addEventListener('touchstart', onDragStart, { passive: true });
            // Non-passive so we can preventDefault and block iOS page scroll during handle drag
            handle.addEventListener('touchmove', function(e) {
                e.preventDefault(); // stops the page from scrolling while dragging the handle
                onDragMove(e);
            }, { passive: false });
            handle.addEventListener('touchend', onDragEnd, { passive: true });
        }

        // ── Delegated click handler for creator cards ───────────────────
        // Cards use data-link instead of inline onclick — safer, no XSS risk
        if (content) {
            content.addEventListener('click', function(e) {
                const card = e.target.closest('.atlas-drawer-card:not(.selectable)');
                if (card && card.dataset.link) {
                    window.open(card.dataset.link, '_blank', 'noopener');
                }
            });
        }

        // ── Prevent page scroll bleed on drawer content ────────────────
        // Non-passive so we can preventDefault when we need to contain scroll
        if (content) {
            content.addEventListener('touchstart', function(e) {
                // Record starting scroll position
                content._touchStartY = e.touches[0].clientY;
                content._scrollTop = content.scrollTop;
            }, { passive: true });

            content.addEventListener('touchmove', function(e) {
                const dy = e.touches[0].clientY - content._touchStartY;
                const atTop = content.scrollTop <= 0 && dy > 0;
                const atBottom = content.scrollTop >= content.scrollHeight - content.clientHeight && dy < 0;

                // At the top, pulling down → collapse to peek
                if (atTop && dy > 14) {
                    if (_drawerState === 'full') _setDrawerState('peek');
                    e.preventDefault(); // stop page scroll
                    return;
                }
                // At the bottom, pulling up further → nothing useful, block page scroll
                if (atBottom) {
                    e.preventDefault();
                    return;
                }
                // Mid-list — let the content scroll, but stop it from bleeding to the page
                e.stopPropagation();
            }, { passive: false });
        }

        // ── Back button / swipe-back history handling ──────────────────
        // _fromPopstate is declared in the drawer script block above
        window.addEventListener('popstate', function(e) {
            if (_drawerState === 'closed') return; // let normal back navigate
            // Intercept: step the drawer down one level
            _fromPopstate = true;
            if (_drawerState === 'full') {
                _setDrawerState('peek');
            } else if (_drawerState === 'peek') {
                _setDrawerState('pill');
            } else if (_drawerState === 'pill') {
                atlasCloseDrawer();
            }
            _fromPopstate = false;
        });
    })();

    // Mobile Filter Toggle
    function toggleMobileFilters() {
        const sidebar = document.getElementById('sidebarFilters');
        const toggle = document.getElementById('mobileFilterToggle');
        const isVisible = sidebar.classList.contains('mobile-visible');

        if (isVisible) {
            sidebar.classList.remove('mobile-visible');
            toggle.classList.remove('filters-visible');
        } else {
            sidebar.classList.add('mobile-visible');
            toggle.classList.add('filters-visible');
            // Smooth scroll to filters
            sidebar.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    }

    // Update active filter count badge + reveal/hide Create a Pack button
    function updateFilterCountBadge() {
        const badge = document.getElementById('activeFilterCount');
        const packBtn = document.getElementById('shareViewBtn');
        if (!badge) return;
        const count = filterState.filters.group.size +
                      filterState.filters.platform.size +
                      filterState.filters.geography.size +
                      filterState.filters.topic.size +
                      (filterState.filters.search ? 1 : 0);
        if (count > 0) {
            badge.textContent = count;
            badge.style.display = 'inline';
            if (packBtn) packBtn.classList.add('visible');
            // Also show drawer pack footer if drawer is open
            const footer = document.getElementById('atlasDrawerPackFooter');
            if (footer) footer.style.display = 'flex';
        } else {
            badge.style.display = 'none';
            if (packBtn) packBtn.classList.remove('visible');
            const footer = document.getElementById('atlasDrawerPackFooter');
            if (footer) footer.style.display = 'none';
        }
    }

    // ── Pack / Starter Pack System ─────────────────────────────────────────

    let _packSelectedCreators = [];  // { name, channel, platform, link, topic }
    let _packCurrentDrawerCreators = [];
    let _packStampImg = null;

    // Preload the distressed stamp
    (function() {
        const img = new Image();
        img.onload = function() { _packStampImg = img; };
        img.onerror = function() { console.warn('Pack stamp not loaded'); };
        img.src = 'assets/images/logos/Journalism_Atlas_logo_acid_green_distressed (4).png';
    })();

    // ── Selection mode in drawer ──────────────────────────────────────────

    // Make drawer cards selectable — called after atlasOpenDrawer renders content
    function _packEnableDrawerSelection() {
        const content = document.getElementById('atlasDrawerContent');
        if (!content) return;
        content.querySelectorAll('.atlas-drawer-card').forEach(card => {
            card.classList.add('selectable');
            // Find creator name from card content
            const nameEl = card.querySelector('.atlas-drawer-card-name');
            const channelEl = card.querySelector('.atlas-drawer-card-channel');
            const tagEl = card.querySelector('.atlas-drawer-card-tag');
            if (!nameEl) return;

            // Store data on the element
            const name = nameEl.textContent.trim();
            const channel = channelEl ? channelEl.textContent.trim() : '';
            const topic = tagEl ? tagEl.textContent.trim() : '';

            // Find matching creator from drawer data
            const creator = _packCurrentDrawerCreators.find(c => c.name === name) || null;

            // Mark already-selected cards
            if (_packSelectedCreators.find(c => c.name === name)) {
                card.classList.add('selected');
            }

            card.onclick = function(e) {
                e.preventDefault();
                const alreadySelected = _packSelectedCreators.findIndex(c => c.name === name);
                if (alreadySelected >= 0) {
                    // Deselect
                    _packSelectedCreators.splice(alreadySelected, 1);
                    card.classList.remove('selected');
                } else {
                    // Select (max 12)
                    if (_packSelectedCreators.length >= 12) {
                        // Flash the count to show limit
                        const counter = document.getElementById('atlasDrawerSelectCount');
                        if (counter) {
                            counter.textContent = 'Max 12 reached';
                            setTimeout(() => _packUpdateDrawerCount(), 1200);
                        }
                        return;
                    }
                    _packSelectedCreators.push(creator || { name, channel, platform: '', link: '', topic });
                    card.classList.add('selected');
                }
                _packUpdateDrawerCount();
            };
        });
    }

    function _packUpdateDrawerCount() {
        const count = _packSelectedCreators.length;
        const counter = document.getElementById('atlasDrawerSelectCount');
        const cta = document.getElementById('atlasDrawerPackCta');
        if (counter) {
            counter.textContent = count === 0 ? 'Tap to select' : `${count} selected`;
            counter.className = 'atlas-drawer-select-count' + (count > 0 ? ' has-selection' : '');
        }
        if (cta) cta.disabled = count === 0;
    }

    // Called by atlasOpenDrawer after content renders — enables selection if filters active
    function _packMaybeEnableSelection() {
        if (typeof filterState === 'undefined' || !filterState.filters) return;
        const hasFilters = (filterState.filters.group.size + filterState.filters.platform.size +
                            filterState.filters.geography.size + filterState.filters.topic.size +
                            (filterState.filters.search ? 1 : 0)) > 0;
        if (hasFilters) {
            _packEnableDrawerSelection();
            _packUpdateDrawerCount();
            const footer = document.getElementById('atlasDrawerPackFooter');
            if (footer) footer.style.display = 'flex';
        }
    }

    // ── Pack Modal ────────────────────────────────────────────────────────

    function openPackModal() {
        // On desktop, use filteredCreators if nothing selected yet in drawer
        if (_packSelectedCreators.length === 0 && typeof filteredCreators !== 'undefined') {
            // Pre-populate with up to 12 from filtered set
            _packSelectedCreators = filteredCreators.slice(0, 12).map(c => ({
                name: c.name, channel: c.channel || '', platform: c.platform || '',
                link: c.link || '', topic: _atlasExtractTopic(c.topic)
            }));
        }

        // Suggest a pack name from active filters
        const nameInput = document.getElementById('packNameInput');
        if (nameInput && !nameInput.value) {
            nameInput.value = _packSuggestName();
        }

        _packRenderPreviewList();
        renderPackCanvas();

        document.getElementById('packModalBackdrop').classList.add('visible');
        if (nameInput) setTimeout(() => nameInput.focus(), 300);
    }

    function closePackModal() {
        document.getElementById('packModalBackdrop').classList.remove('visible');
    }

    function _packSuggestName() {
        if (filterState.filters.group.size === 1) {
            return `My ${Array.from(filterState.filters.group)[0]} Reads`;
        }
        if (filterState.filters.platform.size === 1) {
            const p = Array.from(filterState.filters.platform)[0];
            const short = p.replace('Newsletter - ', '').replace('Video - ', '').replace('Podcast - ', '');
            return `My ${short} Picks`;
        }
        if (filterState.filters.geography.size === 1) {
            return `${Array.from(filterState.filters.geography)[0]} Creators`;
        }
        if (filterState.filters.search) {
            return `"${filterState.filters.search}" Creators`;
        }
        return 'My Atlas Pack';
    }

    function _packRenderPreviewList() {
        const list = document.getElementById('packPreviewList');
        const summary = document.getElementById('packSelectionSummary');
        if (!list) return;

        if (_packSelectedCreators.length === 0) {
            list.innerHTML = '<div style="padding:16px;color:#999;text-align:center;font-size:13px;">No creators selected yet</div>';
            if (summary) summary.innerHTML = 'Select up to 12 creators from the drawer below.';
            return;
        }

        if (summary) {
            summary.innerHTML = `<strong>${_packSelectedCreators.length}</strong> creator${_packSelectedCreators.length !== 1 ? 's' : ''} selected · Max 12`;
        }

        list.innerHTML = _packSelectedCreators.map((c, i) => {
            const escapedLink = (c.link || '').replace(/"/g, '&quot;');
            const nameEl = c.link
                ? `<a class="pack-preview-item-name" href="${escapedLink}" target="_blank" rel="noopener">${c.name} ↗</a>`
                : `<div class="pack-preview-item-name">${c.name}</div>`;
            return `
            <div class="pack-preview-item">
                <div>
                    ${nameEl}
                    <div class="pack-preview-item-channel">${c.channel}</div>
                </div>
                <button class="pack-preview-item-remove" onclick="_packRemoveCreator(${i})" title="Remove">×</button>
            </div>`;
        }).join('');
    }

    window._packRemoveCreator = function(index) {
        _packSelectedCreators.splice(index, 1);
        _packRenderPreviewList();
        renderPackCanvas();
        _packUpdateDrawerCount();
    };

    // ── Canvas Postcard Renderer ──────────────────────────────────────────

    function renderPackCanvas() {
        const canvas = document.getElementById('packPreviewCanvas');
        if (!canvas) return;
        const W = 1080, H = 1080;
        canvas.width = W;
        canvas.height = H;
        const ctx = canvas.getContext('2d');
        if (!ctx) return; // shouldn't happen, but guard against null context
        const packName = (document.getElementById('packNameInput') || {}).value || 'My Atlas Pack';
        const creators = _packSelectedCreators;

        // ── Background
        ctx.fillStyle = '#0d0d0d';
        ctx.fillRect(0, 0, W, H);

        // ── Film grain noise
        _packDrawGrain(ctx, W, H);

        // ── Large watermark stamp (center, low opacity)
        if (_packStampImg) {
            ctx.save();
            ctx.globalAlpha = 0.10;
            const stampSize = 780;
            ctx.drawImage(_packStampImg, (W - stampSize) / 2, (H - stampSize) / 2, stampSize, stampSize);
            ctx.restore();
        }

        // ── Outer border
        ctx.strokeStyle = 'rgba(255,255,255,0.08)';
        ctx.lineWidth = 2;
        ctx.strokeRect(36, 36, W - 72, H - 72);

        // ── Top label: INDEPENDENT JOURNALISM ATLAS
        ctx.fillStyle = 'rgba(255,255,255,0.35)';
        ctx.font = '600 13px "Hanken Grotesk", sans-serif';
        ctx.textAlign = 'center';
        ctx.letterSpacing = '3px';
        ctx.fillText('INDEPENDENT JOURNALISM ATLAS', W / 2, 76);
        ctx.letterSpacing = '0px';

        // ── Acid green rules
        const ruleY1 = 96, ruleX = 60, ruleW = W - 120;
        ctx.strokeStyle = '#ceff00';
        ctx.lineWidth = 2;
        ctx.beginPath(); ctx.moveTo(ruleX, ruleY1); ctx.lineTo(ruleX + ruleW, ruleY1); ctx.stroke();

        // ── "A STARTER PACK" label
        ctx.fillStyle = '#ceff00';
        ctx.font = '700 11px "Hanken Grotesk", sans-serif';
        ctx.textAlign = 'left';
        ctx.fillText('A  S T A R T E R  P A C K', ruleX, 118);

        // ── Pack name
        ctx.fillStyle = '#ffffff';
        ctx.textAlign = 'left';
        const nameFontSize = packName.length > 24 ? 52 : packName.length > 16 ? 62 : 72;
        ctx.font = `800 ${nameFontSize}px "Hanken Grotesk", sans-serif`;
        _packDrawWrappedText(ctx, packName.toUpperCase(), ruleX, 190, ruleW, nameFontSize * 1.1, '#ffffff');

        // Figure out where name ends for creator list start
        const nameLines = _packMeasureLines(ctx, packName.toUpperCase(), ruleW);
        const nameEndY = 190 + (nameLines * nameFontSize * 1.1);

        // ── Second rule below name
        const ruleY2 = Math.max(nameEndY + 24, 310);
        ctx.strokeStyle = '#ceff00';
        ctx.lineWidth = 1.5;
        ctx.globalAlpha = 0.5;
        ctx.beginPath(); ctx.moveTo(ruleX, ruleY2); ctx.lineTo(ruleX + ruleW, ruleY2); ctx.stroke();
        ctx.globalAlpha = 1;

        // ── Creator list
        const listStartY = ruleY2 + 32;
        const maxCreatorsToShow = Math.min(creators.length, 8);
        const lineH = 72;

        for (let i = 0; i < maxCreatorsToShow; i++) {
            const c = creators[i];
            const y = listStartY + i * lineH;
            if (y + lineH > H - 140) break;

            // Creator name
            ctx.fillStyle = '#ffffff';
            ctx.font = '700 24px "Hanken Grotesk", sans-serif';
            ctx.textAlign = 'left';
            ctx.fillText(c.name, ruleX, y);

            // Channel · Platform in muted green
            ctx.fillStyle = 'rgba(206,255,0,0.65)';
            ctx.font = '400 16px "Hanken Grotesk", sans-serif';
            const sub = [c.channel, c.platform].filter(Boolean).join('  ·  ');
            ctx.fillText(sub, ruleX, y + 24);

            // Thin separator
            ctx.strokeStyle = 'rgba(255,255,255,0.07)';
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(ruleX, y + lineH - 8);
            ctx.lineTo(ruleX + ruleW, y + lineH - 8);
            ctx.stroke();
        }

        // ── "and N more" if truncated
        if (creators.length > maxCreatorsToShow) {
            const moreY = listStartY + maxCreatorsToShow * lineH - 8;
            if (moreY < H - 130) {
                ctx.fillStyle = 'rgba(255,255,255,0.35)';
                ctx.font = '600 15px "Hanken Grotesk", sans-serif';
                ctx.textAlign = 'left';
                ctx.fillText(`· · ·  and ${creators.length - maxCreatorsToShow} more`, ruleX, moreY);
            }
        }

        // ── Bottom rule
        ctx.strokeStyle = '#ceff00';
        ctx.lineWidth = 1.5;
        ctx.globalAlpha = 0.4;
        ctx.beginPath(); ctx.moveTo(ruleX, H - 112); ctx.lineTo(ruleX + ruleW, H - 112); ctx.stroke();
        ctx.globalAlpha = 1;

        // ── URL at bottom
        ctx.fillStyle = 'rgba(255,255,255,0.45)';
        ctx.font = '500 15px "Hanken Grotesk", sans-serif';
        ctx.textAlign = 'left';
        ctx.fillText('journalismatlas.com', ruleX, H - 88);

        // ── Small stamp seal (bottom right)
        if (_packStampImg) {
            ctx.save();
            ctx.globalAlpha = 0.82;
            const sealSize = 120;
            ctx.drawImage(_packStampImg, W - ruleX - sealSize, H - 60 - sealSize, sealSize, sealSize);
            ctx.restore();
        }
    }

    // Draw film grain
    function _packDrawGrain(ctx, W, H) {
        ctx.save();
        ctx.globalAlpha = 0.035;
        for (let i = 0; i < 18000; i++) {
            const x = Math.random() * W;
            const y = Math.random() * H;
            const r = Math.random() * 1.2;
            ctx.fillStyle = Math.random() > 0.5 ? '#ffffff' : '#ceff00';
            ctx.fillRect(x, y, r, r);
        }
        ctx.restore();
    }

    // Measure how many lines a string wraps to
    function _packMeasureLines(ctx, text, maxWidth) {
        const words = text.split(' ');
        let line = '', lines = 1;
        for (let i = 0; i < words.length; i++) {
            const test = line + words[i] + ' ';
            if (ctx.measureText(test).width > maxWidth && i > 0) {
                lines++;
                line = words[i] + ' ';
            } else { line = test; }
        }
        return lines;
    }

    // Draw wrapped text, return final Y
    function _packDrawWrappedText(ctx, text, x, y, maxW, lineH, color) {
        ctx.fillStyle = color;
        const words = text.split(' ');
        let line = '';
        let curY = y;
        for (let i = 0; i < words.length; i++) {
            const test = line + words[i] + ' ';
            if (ctx.measureText(test).width > maxW && i > 0) {
                ctx.fillText(line.trim(), x, curY);
                curY += lineH;
                line = words[i] + ' ';
            } else { line = test; }
        }
        ctx.fillText(line.trim(), x, curY);
        return curY;
    }

    // ── Pack share — one button, one action ──────────────────────────────

    function packShare() {
        const btn = document.getElementById('packShareBtn');
        const packName = (document.getElementById('packNameInput') || {}).value || 'Atlas Pack';
        const shareUrl = window.location.href;
        const shareTitle = `${packName} — Atlas Starter Pack`;
        const nameList = _packSelectedCreators.slice(0, 3).map(c => c.name).join(', ');
        const moreCount = _packSelectedCreators.length > 3 ? ` + ${_packSelectedCreators.length - 3} more` : '';
        const shareText = `${nameList}${moreCount} — curated on the Independent Journalism Atlas`;
        const slug = packName.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || 'atlas-pack';

        // Set loading state
        if (btn) { btn.textContent = '…'; btn.disabled = true; }

        // Render a fresh full-res canvas for export
        const exportCanvas = document.createElement('canvas');
        exportCanvas.width = 1080; exportCanvas.height = 1080;
        const exportCtx = exportCanvas.getContext('2d');
        if (!exportCtx) {
            if (btn) { btn.textContent = '✦ Share this Pack'; btn.disabled = false; }
            return;
        }
        exportCtx.drawImage(document.getElementById('packPreviewCanvas'), 0, 0);

        exportCanvas.toBlob(blob => {
            const canShare = navigator.canShare && navigator.canShare({
                files: [new File([blob], `${slug}.png`, { type: 'image/png' })]
            });

            if (canShare) {
                // ── Best path: OS share sheet with image + URL together
                navigator.share({
                    title: shareTitle,
                    text: shareText,
                    url: shareUrl,
                    files: [new File([blob], `${slug}.png`, { type: 'image/png' })]
                }).then(() => {
                    _packShareFeedback(btn, '✓ Shared!');
                }).catch(err => {
                    if (err.name !== 'AbortError') {
                        // User cancelled or share failed — fall back silently
                        _packShareFallback(blob, slug, shareUrl, btn);
                    } else {
                        _packShareFeedback(btn, '✦ Share this Pack');
                    }
                });
            } else {
                // ── Fallback: download image + copy URL simultaneously
                _packShareFallback(blob, slug, shareUrl, btn);
            }
        }, 'image/png');
    }

    function _packShareFallback(blob, slug, shareUrl, btn) {
        // 1. Trigger image download
        const objUrl = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.download = `atlas-pack-${slug}.png`;
        a.href = objUrl;
        a.click();
        URL.revokeObjectURL(objUrl);

        // 2. Copy link to clipboard simultaneously
        navigator.clipboard.writeText(shareUrl).then(() => {
            _packShareFeedback(btn, '✓ Image saved + link copied!');
        }).catch(() => {
            // Clipboard failed — at least the download happened
            _packShareFeedback(btn, '✓ Image downloaded');
            prompt('Copy your pack link:', shareUrl);
        });
    }

    function _packShareFeedback(btn, message) {
        if (!btn) return;
        btn.textContent = message;
        btn.disabled = false;
        setTimeout(() => {
            btn.textContent = '✦ Share this Pack';
        }, 3000);
    }

    // Close modal on backdrop click
    document.getElementById('packModalBackdrop').addEventListener('click', function(e) {
        if (e.target === this) closePackModal();
    });
