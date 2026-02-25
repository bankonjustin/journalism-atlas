// Bottom Sheet Module
const BottomSheet = {
    sheet: null,
    content: null,
    currentCreator: null,
    creatorList: [],
    currentIndex: 0,
    hammer: null,
    startY: 0,
    currentY: 0,

    init() {
        this.sheet = document.getElementById('bottom-sheet');
        this.content = document.getElementById('bottom-sheet-content');

        this.setupGestures();
        this.setupEventListeners();
    },

    setupGestures() {
        // Setup Hammer.js for swipe gestures
        this.hammer = new Hammer(this.sheet);
        this.hammer.get('swipe').set({ direction: Hammer.DIRECTION_ALL });

        // Swipe down to dismiss
        this.hammer.on('swipedown', () => {
            this.hide();
        });

        // Swipe left for next
        this.hammer.on('swipeleft', () => {
            this.next();
        });

        // Swipe right for previous
        this.hammer.on('swiperight', () => {
            this.previous();
        });
    },

    setupEventListeners() {
        // Click outside to dismiss
        this.sheet.addEventListener('click', (event) => {
            if (event.target === this.sheet) {
                this.hide();
            }
        });
    },

    show(creator, creatorList, currentIndex) {
        this.currentCreator = creator;
        this.creatorList = creatorList || [creator];
        this.currentIndex = currentIndex || 0;

        this.render();
        this.sheet.classList.remove('hidden');

        // Add haptic feedback if supported
        if (navigator.vibrate) {
            navigator.vibrate(10);
        }
    },

    hide() {
        this.sheet.classList.add('hidden');
        this.currentCreator = null;
    },

    render() {
        if (!this.currentCreator) return;

        const creator = this.currentCreator;

        // Get first letter for avatar
        const avatarLetter = creator.name.charAt(0).toUpperCase();

        // Format platforms
        const platformsHTML = creator.platforms.map(platform => {
            return `<span class="platform-icon">${platform}</span>`;
        }).join('');

        // Format topic tags
        const topicsHTML = creator.groups.map(group => {
            return `<span class="topic-tag">${group}</span>`;
        }).join('');

        // Platform links
        const linksHTML = creator.link ? `
            <div class="creator-links">
                <a href="${creator.link}" target="_blank" class="platform-link">
                    <span class="material-icons">launch</span>
                    Visit ${creator.channel}
                </a>
            </div>
        ` : '';

        // Render content
        this.content.innerHTML = `
            <div class="creator-header">
                <div class="creator-avatar">${avatarLetter}</div>
                <div class="creator-info">
                    <h3>${creator.name}</h3>
                    <p class="creator-handle">${creator.channel || ''}</p>
                </div>
            </div>

            <div class="creator-meta">
                <div class="meta-section">
                    <div class="meta-label">Platforms</div>
                    <div class="platform-icons">
                        ${platformsHTML}
                    </div>
                </div>

                <div class="meta-section">
                    <div class="meta-label">Topics</div>
                    <div class="topic-tags">
                        ${topicsHTML}
                    </div>
                </div>

                ${creator.geography ? `
                <div class="meta-section">
                    <div class="meta-label">Geography</div>
                    <div>${creator.geography}</div>
                </div>
                ` : ''}
            </div>

            ${linksHTML}

            <div class="creator-actions">
                <button class="action-button" id="share-creator">
                    <span class="material-icons">share</span>
                    Share
                </button>
                <button class="action-button" id="save-creator">
                    <span class="material-icons">bookmark_border</span>
                    Save
                </button>
            </div>
        `;

        // Setup action buttons
        this.setupActionButtons();
    },

    setupActionButtons() {
        // Share button
        const shareBtn = document.getElementById('share-creator');
        if (shareBtn) {
            shareBtn.addEventListener('click', () => this.handleShare());
        }

        // Save button (placeholder functionality)
        const saveBtn = document.getElementById('save-creator');
        if (saveBtn) {
            saveBtn.addEventListener('click', () => this.handleSave());
        }
    },

    async handleShare() {
        const creator = this.currentCreator;
        const shareData = {
            title: `${creator.name} - The Atlas`,
            text: `Check out ${creator.name} on The Independent Journalism Atlas`,
            url: creator.link || window.location.href
        };

        // Try Web Share API
        if (navigator.share) {
            try {
                await navigator.share(shareData);
            } catch (err) {
                if (err.name !== 'AbortError') {
                    this.fallbackShare(shareData);
                }
            }
        } else {
            this.fallbackShare(shareData);
        }
    },

    fallbackShare(shareData) {
        // Fallback to clipboard
        const text = `${shareData.text}\n${shareData.url}`;

        navigator.clipboard.writeText(text).then(() => {
            this.showToast('Link copied to clipboard!');
        }).catch(() => {
            console.error('Failed to copy to clipboard');
        });
    },

    handleSave() {
        // Placeholder for save functionality
        // Could integrate with localStorage or backend
        this.showToast('Creator saved!');

        // Add haptic feedback
        if (navigator.vibrate) {
            navigator.vibrate(10);
        }
    },

    showToast(message) {
        // Simple toast notification
        const toast = document.createElement('div');
        toast.style.cssText = `
            position: fixed;
            bottom: 100px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 12px 24px;
            border-radius: 24px;
            font-size: 14px;
            z-index: 10000;
            animation: fadeIn 0.3s ease;
        `;
        toast.textContent = message;
        document.body.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transition = 'opacity 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, 2000);
    },

    next() {
        if (this.creatorList.length === 0) return;

        this.currentIndex = (this.currentIndex + 1) % this.creatorList.length;
        this.currentCreator = this.creatorList[this.currentIndex];
        this.render();

        // Add haptic feedback
        if (navigator.vibrate) {
            navigator.vibrate(10);
        }
    },

    previous() {
        if (this.creatorList.length === 0) return;

        this.currentIndex = (this.currentIndex - 1 + this.creatorList.length) % this.creatorList.length;
        this.currentCreator = this.creatorList[this.currentIndex];
        this.render();

        // Add haptic feedback
        if (navigator.vibrate) {
            navigator.vibrate(10);
        }
    }
};
