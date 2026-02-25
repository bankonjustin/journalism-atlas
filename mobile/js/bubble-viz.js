// Bubble Visualization Module
const BubbleViz = {
    svg: null,
    g: null,
    simulation: null,
    creators: [],
    filteredCreators: [],
    width: 0,
    height: 0,
    zoom: null,

    init(containerId, creators) {
        this.creators = creators;
        this.filteredCreators = creators;

        // Get container dimensions
        const container = document.querySelector(containerId);
        this.width = container.clientWidth;
        this.height = container.clientHeight;

        // Create SVG
        this.svg = d3.select(containerId)
            .append('svg')
            .attr('width', this.width)
            .attr('height', this.height);

        // Create main group for zoom/pan
        this.g = this.svg.append('g');

        // Setup zoom behavior
        this.setupZoom();

        // Process creators with positions and radius
        this.processCreators();

        // Create force simulation
        this.createSimulation();

        // Render bubbles
        this.renderBubbles();

        // Handle window resize
        window.addEventListener('resize', () => this.handleResize());
    },

    processCreators() {
        // Calculate radius based on number of platforms
        const radiusScale = d3.scaleSqrt()
            .domain([1, 5])
            .range([8, 40]);

        this.creators.forEach(creator => {
            const platformCount = creator.platforms.length;
            creator.radius = radiusScale(platformCount);

            // Get color from primary group
            const topicGroups = DataLoader.getTopicGroups();
            const groupIndex = topicGroups.findIndex(g => g.name === creator.groups[0]);
            creator.color = this.getTopicColor(groupIndex >= 0 ? groupIndex : 0);

            // Random initial position around edges
            const angle = Math.random() * Math.PI * 2;
            const distance = Math.max(this.width, this.height) * 0.6;
            creator.x = this.width / 2 + Math.cos(angle) * distance;
            creator.y = this.height / 2 + Math.sin(angle) * distance;
        });
    },

    getTopicColor(index) {
        const colors = [
            '#FF6B6B', // Power & Politics
            '#4ECDC4', // Money & Work
            '#45B7D1', // Civic Life
            '#FFA07A', // Social Issues
            '#98D8C8', // Science/Health/Environment
            '#F7DC6F', // Culture & Media
            '#BB8FCE', // Lifestyle & Personal Life
            '#85C1E2', // Journalism Formats
            '#95A5A6'  // General News
        ];
        return colors[index % colors.length];
    },

    createSimulation() {
        this.simulation = d3.forceSimulation(this.creators)
            .force('charge', d3.forceManyBody().strength(-30))
            .force('center', d3.forceCenter(this.width / 2, this.height / 2))
            .force('collision', d3.forceCollide().radius(d => d.radius + 2))
            .force('x', d3.forceX(this.width / 2).strength(0.05))
            .force('y', d3.forceY(this.height / 2).strength(0.05))
            .on('tick', () => this.ticked());
    },

    renderBubbles() {
        const bubbles = this.g.selectAll('.bubble')
            .data(this.creators, d => d.id)
            .join('circle')
            .attr('class', 'bubble')
            .attr('r', d => d.radius)
            .attr('fill', d => d.color)
            .attr('opacity', 0)
            .style('cursor', 'pointer')
            .on('click', (event, d) => this.handleBubbleClick(event, d));

        // Entrance animation
        bubbles.transition()
            .duration(1500)
            .delay((d, i) => i * 2)
            .attr('opacity', 0.85);
    },

    ticked() {
        this.g.selectAll('.bubble')
            .attr('cx', d => d.x)
            .attr('cy', d => d.y);
    },

    setupZoom() {
        this.zoom = d3.zoom()
            .scaleExtent([0.5, 3])
            .on('zoom', (event) => {
                this.g.attr('transform', event.transform);
            });

        this.svg.call(this.zoom);

        // Double-tap to reset
        let lastTap = 0;
        this.svg.on('click', (event) => {
            const currentTime = new Date().getTime();
            const tapLength = currentTime - lastTap;

            if (tapLength < 300 && tapLength > 0) {
                this.resetZoom();
                event.preventDefault();
            }
            lastTap = currentTime;
        });
    },

    resetZoom() {
        this.svg.transition()
            .duration(750)
            .call(this.zoom.transform, d3.zoomIdentity);
    },

    handleBubbleClick(event, creator) {
        event.stopPropagation();

        // Get current filtered list for navigation
        const currentIndex = this.filteredCreators.findIndex(c => c.id === creator.id);

        // Call bottom sheet
        if (window.BottomSheet) {
            BottomSheet.show(creator, this.filteredCreators, currentIndex);
        }
    },

    updateBubbles(filteredCreators) {
        this.filteredCreators = filteredCreators;

        const filteredIds = new Set(filteredCreators.map(c => c.id));

        this.g.selectAll('.bubble')
            .transition()
            .duration(300)
            .attr('opacity', d => filteredIds.has(d.id) ? 0.85 : 0.1)
            .attr('r', d => {
                if (filteredIds.has(d.id)) {
                    return d.radius * 1.05;
                }
                return d.radius;
            });
    },

    reset() {
        this.updateBubbles(this.creators);
        this.resetZoom();
    },

    handleResize() {
        const container = document.querySelector('#bubble-canvas');
        this.width = container.clientWidth;
        this.height = container.clientHeight;

        this.svg
            .attr('width', this.width)
            .attr('height', this.height);

        // Update simulation forces
        this.simulation
            .force('center', d3.forceCenter(this.width / 2, this.height / 2))
            .force('x', d3.forceX(this.width / 2).strength(0.05))
            .force('y', d3.forceY(this.height / 2).strength(0.05))
            .alpha(0.3)
            .restart();
    }
};
