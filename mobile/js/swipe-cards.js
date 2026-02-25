// Swipe Cards Module
const SwipeCards = {
    container: null,
    indicatorsContainer: null,
    topicGroups: [],
    activeCardIndex: 0,

    init(topicGroups) {
        this.topicGroups = topicGroups || DataLoader.getTopicGroups();
        this.container = document.getElementById('cards-container');
        this.indicatorsContainer = document.getElementById('card-indicators');

        this.render();
        this.setupEventListeners();
    },

    render() {
        this.container.innerHTML = '';
        this.indicatorsContainer.innerHTML = '';

        // Create cards for each topic group
        this.topicGroups.forEach((topic, index) => {
            const card = this.createCard(topic, index);
            this.container.appendChild(card);

            // Create indicator dot
            const indicator = document.createElement('div');
            indicator.className = `card-indicator ${index === 0 ? 'active' : ''}`;
            indicator.dataset.index = index;
            this.indicatorsContainer.appendChild(indicator);
        });

        // Set initial active card
        this.updateActiveCard(0);
    },

    createCard(topic, index) {
        const card = document.createElement('div');
        card.className = 'category-card';
        card.dataset.index = index;

        // Create mini visualization container
        const vizContainer = document.createElement('div');
        vizContainer.className = 'card-viz';
        vizContainer.id = `card-viz-${index}`;

        // Create card info
        const cardInfo = document.createElement('div');
        cardInfo.className = 'card-info';
        cardInfo.innerHTML = `
            <h3>${topic.name}</h3>
            <p class="creator-count-text">${topic.count} creators</p>
            <button class="explore-button" data-topic="${topic.name}">
                Explore ${topic.name}
            </button>
        `;

        card.appendChild(vizContainer);
        card.appendChild(cardInfo);

        // Render mini bubble viz for this card
        setTimeout(() => {
            this.renderMiniViz(vizContainer, topic.creators, index);
        }, 100);

        return card;
    },

    renderMiniViz(container, creators, topicIndex) {
        const width = container.clientWidth;
        const height = container.clientHeight;

        // Create SVG
        const svg = d3.select(container)
            .append('svg')
            .attr('width', width)
            .attr('height', height);

        const g = svg.append('g');

        // Scale for mini bubbles
        const radiusScale = d3.scaleSqrt()
            .domain([1, 5])
            .range([4, 20]);

        // Process creators
        const processedCreators = creators.slice(0, 50).map(c => ({
            ...c,
            radius: radiusScale(c.platforms.length),
            x: width / 2,
            y: height / 2
        }));

        // Create simulation
        const simulation = d3.forceSimulation(processedCreators)
            .force('charge', d3.forceManyBody().strength(-10))
            .force('center', d3.forceCenter(width / 2, height / 2))
            .force('collision', d3.forceCollide().radius(d => d.radius + 1))
            .on('tick', ticked);

        // Render bubbles
        const bubbles = g.selectAll('.mini-bubble')
            .data(processedCreators)
            .join('circle')
            .attr('class', 'mini-bubble')
            .attr('r', d => d.radius)
            .attr('fill', d => d.color)
            .attr('opacity', 0.7)
            .style('cursor', 'pointer')
            .on('click', (event, d) => {
                event.stopPropagation();
                if (window.BottomSheet) {
                    BottomSheet.show(d, creators, processedCreators.findIndex(c => c.id === d.id));
                }
            });

        function ticked() {
            bubbles
                .attr('cx', d => d.x)
                .attr('cy', d => d.y);
        }
    },

    setupEventListeners() {
        // Scroll event to update active card
        this.container.addEventListener('scroll', () => {
            this.handleScroll();
        });

        // Explore buttons
        this.container.addEventListener('click', (event) => {
            if (event.target.classList.contains('explore-button')) {
                const topicName = event.target.dataset.topic;
                this.handleExplore(topicName);
            }
        });

        // Close button
        document.getElementById('close-swipe-cards').addEventListener('click', () => {
            this.hide();
        });
    },

    handleScroll() {
        const scrollLeft = this.container.scrollLeft;
        const cardWidth = this.container.clientWidth;
        const newIndex = Math.round(scrollLeft / cardWidth);

        if (newIndex !== this.activeCardIndex) {
            this.updateActiveCard(newIndex);
        }
    },

    updateActiveCard(index) {
        this.activeCardIndex = index;

        // Update indicators
        this.indicatorsContainer.querySelectorAll('.card-indicator').forEach((indicator, i) => {
            if (i === index) {
                indicator.classList.add('active');
            } else {
                indicator.classList.remove('active');
            }
        });
    },

    handleExplore(topicName) {
        // Apply filter for this topic
        if (window.MobileMain) {
            MobileMain.applyTopicFilter(topicName);
        }

        // Switch back to bubble view
        this.hide();
    },

    show() {
        const view = document.getElementById('swipe-cards-view');
        view.classList.remove('hidden');

        // Scroll to first card
        this.container.scrollLeft = 0;
        this.updateActiveCard(0);
    },

    hide() {
        const view = document.getElementById('swipe-cards-view');
        view.classList.add('hidden');
    }
};
