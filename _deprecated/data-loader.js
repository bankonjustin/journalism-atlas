// Data Loader Module
const DataLoader = {
    creators: [],
    topicGroups: {},
    platforms: new Set(),
    
    async loadData() {
        try {
            const response = await fetch('../data/creators-data.json');
            const data = await response.json();
            this.processData(data);
            return this.creators;
        } catch (error) {
            console.error('Error loading data:', error);
            throw error;
        }
    },
    
    processData(data) {
        // Process creators from JSON
        this.creators = data.map((creator, index) => {
            // Extract topic groups
            const groups = this.parseGroups(creator.Groups || creator['Topic/Category']);
            
            // Extract platforms
            const platforms = this.extractPlatforms(creator);
            platforms.forEach(p => this.platforms.add(p));
            
            return {
                id: index,
                name: creator['Creator Name'],
                channel: creator['Creator Channel'],
                link: creator['Link Primary'],
                platformPrimary: creator['Platform Primary'],
                platformSecondary: creator['Platform Secondary'],
                platforms: platforms,
                groups: groups,
                geography: creator.Geography || 'US',
                tags: creator['New Tags'] || '',
                specialLists: creator['Special Lists'] || '',
                notes: creator.Notes || ''
            };
        });
        
        // Build topic groups map
        this.buildTopicGroups();
    },
    
    parseGroups(groupString) {
        if (!groupString) return ['General News'];
        
        // Split by common delimiters and clean
        const groups = groupString.split(/[,;|]/)
            .map(g => g.trim())
            .filter(g => g.length > 0);
        
        return groups.length > 0 ? groups : ['General News'];
    },
    
    extractPlatforms(creator) {
        const platforms = new Set();
        
        if (creator['Platform Primary']) {
            platforms.add(creator['Platform Primary']);
        }
        
        if (creator['Platform Secondary']) {
            const secondary = creator['Platform Secondary'].split(/[,;|]/)
                .map(p => p.trim())
                .filter(p => p.length > 0);
            secondary.forEach(p => platforms.add(p));
        }
        
        return Array.from(platforms);
    },
    
    buildTopicGroups() {
        this.topicGroups = {};
        
        this.creators.forEach(creator => {
            creator.groups.forEach(group => {
                if (!this.topicGroups[group]) {
                    this.topicGroups[group] = [];
                }
                this.topicGroups[group].push(creator);
            });
        });
    },
    
    getTopicGroups() {
        // Return sorted by creator count
        return Object.entries(this.topicGroups)
            .sort((a, b) => b[1].length - a[1].length)
            .map(([name, creators]) => ({
                name,
                count: creators.length,
                creators
            }));
    },
    
    filterCreators(filters) {
        if (!filters || Object.keys(filters).length === 0) {
            return this.creators;
        }
        
        return this.creators.filter(creator => {
            // Filter by topic groups
            if (filters.groups && filters.groups.length > 0) {
                const hasGroup = creator.groups.some(g => 
                    filters.groups.includes(g)
                );
                if (!hasGroup) return false;
            }
            
            // Filter by platforms
            if (filters.platforms && filters.platforms.length > 0) {
                const hasPlatform = creator.platforms.some(p => 
                    filters.platforms.includes(p)
                );
                if (!hasPlatform) return false;
            }
            
            // Filter by geography
            if (filters.geography && filters.geography.length > 0) {
                if (!filters.geography.includes(creator.geography)) {
                    return false;
                }
            }
            
            return true;
        });
    },
    
    getTopicColor(topicName, topicIndex) {
        // Map topic to color variable
        const colors = [
            'var(--color-topic-1)',
            'var(--color-topic-2)',
            'var(--color-topic-3)',
            'var(--color-topic-4)',
            'var(--color-topic-5)',
            'var(--color-topic-6)',
            'var(--color-topic-7)',
            'var(--color-topic-8)',
            'var(--color-topic-9)'
        ];
        
        // Use index if provided, otherwise hash the name
        if (topicIndex !== undefined) {
            return colors[topicIndex % colors.length];
        }
        
        // Simple hash function for consistent colors
        let hash = 0;
        for (let i = 0; i < topicName.length; i++) {
            hash = topicName.charCodeAt(i) + ((hash << 5) - hash);
        }
        return colors[Math.abs(hash) % colors.length];
    }
};
