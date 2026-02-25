# CLAUDE CODE BUILD SPECIFICATION: Mobile Atlas Landing

## Context
You are building a mobile-first landing page for The Independent Journalism Atlas. All the HTML and CSS foundation has been provided. Your job is to complete the JavaScript implementation to bring this mobile experience to life.

## Files Already Created
- `/mobile/index.html` ✅ (mobile-index.html)
- `/mobile/css/variables.css` ✅ (variables.css)
- `/mobile/css/mobile.css` ✅ (mobile.css)
- `/mobile/css/animations.css` ✅ (animations.css)
- `/mobile/js/data-loader.js` ✅ (data-loader.js)

## Files You Need to Create

### 1. `/mobile/js/bubble-viz.js`

Create a D3.js force-directed bubble visualization with these specifications:

**Core Requirements:**
- Use D3.js v7 force simulation
- Display all 792 creators as circles (bubbles)
- Size bubbles based on number of platforms (more platforms = bigger bubble)
- Color bubbles by their primary topic group using `DataLoader.getTopicColor()`
- Implement smooth zoom and pan using `d3.zoom()`
- Touch-optimized interactions (larger hit targets, smooth gestures)

**Bubble Sizing:**
- Min radius: 8px (creators with 1 platform)
- Max radius: 40px (creators with 5+ platforms)
- Use `d3.scaleSqrt()` for natural area-based sizing

**Force Simulation:**
- `d3.forceCollide()` with padding to prevent overlap
- `d3.forceManyBody()` with slight repulsion
- `d3.forceCenter()` to keep bubbles centered
- `d3.forceX()` and `d3.forceY()` with weak strength for gentle clustering

**Entrance Animation:**
- Bubbles start from random positions around edges
- Animate to final positions over 1.5 seconds
- Stagger the entrance slightly for visual interest

**Touch Interactions:**
- **Tap bubble** → Call `BottomSheet.show(creator)`
- **Pinch zoom** → Scale between 0.5x and 3x
- **Pan** → Drag to explore canvas
- **Double-tap background** → Reset zoom to default view

**Filter Integration:**
- Export `updateBubbles(filteredCreators)` function
- When filtered, fade out non-matching bubbles (opacity 0.1)
- Highlight matching bubbles (opacity 1, slight scale increase)
- Smooth transition (300ms)

**Public API:**
```javascript
const BubbleViz = {
    init(containerId, creators) { },
    updateBubbles(filteredCreators) { },
    reset() { }
};
```

---

### 2. `/mobile/js/tag-cloud.js`

Create an interactive tag cloud filter interface:

**Core Requirements:**
- Display the 9 main topic groups as large primary tags
- Display platforms as smaller secondary tags below topics
- Show creator count next to each tag: "Power & Politics (143)"
- Multi-select functionality (tap to toggle)
- Active tags glow with `--color-brand-green`
- Display active filters as dismissible pills at top

**Tag Layout:**
- Use flexbox with `flex-wrap: wrap` and gaps
- Primary tags (topics): Large, prominent
- Secondary tags (platforms, geography): Smaller, lighter

**Interaction Flow:**
1. User taps filter button → Tag cloud slides up
2. User taps tags → Tags activate (green glow)
3. Active filters shown as pills at top with X to remove
4. Each tag change → Update `BubbleViz.updateBubbles()` with filtered data
5. "Clear All" button → Reset all filters

**Active State Management:**
```javascript
const activeFilters = {
    groups: [],
    platforms: [],
    geography: []
};
```

**Public API:**
```javascript
const TagCloud = {
    init(containerData) { },
    show() { },
    hide() { },
    getActiveFilters() { },
    clearFilters() { }
};
```

---

### 3. `/mobile/js/swipe-cards.js`

Create a swipeable category card carousel:

**Core Requirements:**
- Generate 9 cards (one per topic group)
- Each card contains a mini D3 bubble viz showing that topic's creators
- Horizontal scroll with snap-to-card behavior
- Progress indicators (dots) at top showing which card is active
- "Explore" button drills into filtered bubble view

**Card Structure:**
```javascript
{
    topicName: "Power & Politics",
    creatorCount: 143,
    creators: [...], // subset of creators
    color: "#FF6B6B"
}
```

**Mini Bubble Viz:**
- Smaller version of main bubble viz
- Shows only creators from that topic
- Static (no zoom/pan), just visual preview
- Tap bubble → Open bottom sheet for that creator

**Scroll Behavior:**
- CSS `scroll-snap-type: x mandatory`
- Update progress dots on scroll
- Smooth scroll animation

**"Explore" Button:**
- Apply filter for that topic
- Switch back to main bubble view
- Bubbles filter to show only that topic's creators

**Public API:**
```javascript
const SwipeCards = {
    init(topicGroups) { },
    show() { },
    hide() { },
    updateActiveCard(index) { }
};
```

---

### 4. `/mobile/js/bottom-sheet.js`

Create a slide-up bottom sheet for creator details:

**Core Requirements:**
- Slide up from bottom when bubble tapped
- Drag handle at top (swipe down to dismiss)
- Swipe left/right to navigate to next/previous creator
- Display all creator metadata in structured layout
- Action buttons: Share, Save, Similar

**Content Display:**
- Creator name and avatar (use first letter of name)
- Platform icons with links
- Topic tags
- Geography info
- "Visit on [Platform]" buttons for each platform

**Gestures:**
- **Swipe down** → Dismiss sheet
- **Swipe left** → Next creator in current view
- **Swipe right** → Previous creator in current view
- **Tap outside** → Dismiss sheet

**Navigation Context:**
- Keep track of current filtered creator list
- Navigate within that list only
- Wrap around (last → first, first → last)

**Share Functionality:**
- Use Web Share API if available: `navigator.share()`
- Fallback to clipboard copy with toast notification
- Share text: "Check out [Creator Name] on The Atlas - [URL]"

**Public API:**
```javascript
const BottomSheet = {
    show(creator, creatorList, currentIndex) { },
    hide() { },
    next() { },
    previous() { }
};
```

---

### 5. `/mobile/js/mobile-main.js`

Orchestrate the entire mobile app:

**Initialization Flow:**
```javascript
1. Show loading screen
2. Load data via DataLoader.loadData()
3. Initialize all modules:
   - BubbleViz.init('#bubble-canvas', creators)
   - TagCloud.init(topicGroups, platforms)
   - SwipeCards.init(topicGroups)
   - BottomSheet.init()
4. Set up event listeners for all UI buttons
5. Hide loading screen with fade animation
6. Start entrance animations
```

**Event Listeners:**
- Filter button → Show tag cloud
- View switcher → Toggle between bubble and swipe card views
- Info button → Show info overlay
- All close buttons → Hide respective overlays
- Handle back button (browser history) for overlay states

**State Management:**
```javascript
const AppState = {
    currentView: 'bubbles', // or 'cards'
    activeFilters: {},
    filteredCreators: [],
    selectedCreator: null
};
```

**Filter Coordination:**
When filters change in TagCloud:
1. Get active filters via `TagCloud.getActiveFilters()`
2. Filter creators via `DataLoader.filterCreators(filters)`
3. Update bubble viz via `BubbleViz.updateBubbles(filteredCreators)`
4. Update creator count badge in UI
5. Store filtered list for bottom sheet navigation

**View Switching:**
Toggle between bubble visualization and swipe cards:
- Smooth transition animations
- Persist current filters across views
- Update UI button states

**Error Handling:**
- Try/catch around data loading
- Show user-friendly error messages if data fails to load
- Console logging for debugging

**Performance Optimization:**
- Throttle zoom/pan events (max 60fps)
- Debounce filter updates (wait 150ms after last change)
- Use `requestAnimationFrame` for smooth animations

---

## Data Format Reference

The creators-data.json structure (from DataLoader):
```javascript
{
    id: 0,
    name: "Creator Name",
    channel: "@handle",
    link: "https://...",
    platformPrimary: "YouTube",
    platformSecondary: "Substack",
    platforms: ["YouTube", "Substack"],
    groups: ["Power & Politics", "General News"],
    geography: "US",
    tags: "...",
    specialLists: "...",
    notes: "..."
}
```

---

## Touch Gesture Library Setup

You have Hammer.js loaded. Use it for:

**Swipe Detection:**
```javascript
const hammer = new Hammer(element);
hammer.on('swipeleft', () => { /* next */ });
hammer.on('swiperight', () => { /* previous */ });
hammer.on('swipedown', () => { /* dismiss */ });
```

**Pinch Detection:**
```javascript
hammer.get('pinch').set({ enable: true });
hammer.on('pinch', (e) => {
    // Apply zoom based on e.scale
});
```

---

## Key Implementation Details

**D3 Force Simulation Example:**
```javascript
const simulation = d3.forceSimulation(creators)
    .force('charge', d3.forceManyBody().strength(-30))
    .force('center', d3.forceCenter(width / 2, height / 2))
    .force('collision', d3.forceCollide().radius(d => d.radius + 2))
    .on('tick', ticked);
```

**Zoom Behavior:**
```javascript
const zoom = d3.zoom()
    .scaleExtent([0.5, 3])
    .on('zoom', (event) => {
        g.attr('transform', event.transform);
    });

svg.call(zoom);
```

**Smooth Transitions:**
```javascript
bubbles.transition()
    .duration(300)
    .attr('opacity', d => filtered.includes(d) ? 1 : 0.1)
    .attr('r', d => filtered.includes(d) ? d.radius * 1.05 : d.radius);
```

---

## Testing Checklist

After implementation, verify:

✅ **Load Performance**
- Page loads in < 2 seconds on 4G
- No console errors
- Smooth entrance animations

✅ **Touch Interactions**
- Tap bubbles → Bottom sheet appears
- Pinch zoom → Smooth scaling
- Pan → Smooth dragging
- Swipe cards → Snap to each card
- Bottom sheet swipe → Navigate creators

✅ **Filtering**
- Tap tags → Bubbles filter correctly
- Multiple tags → Combined filters work
- Clear filters → All bubbles return
- Filter count updates in real-time

✅ **Bottom Sheet**
- All creator data displays correctly
- Platform links work
- Swipe gestures work
- Share functionality works

✅ **View Switching**
- Toggle between bubbles and cards
- Smooth transitions
- Filters persist across views

✅ **Mobile Optimization**
- No horizontal scroll issues
- Touch targets are large enough (44x44px minimum)
- Text is readable (no tiny fonts)
- Safe area handling on iOS (notch)

---

## Deployment

After building and testing:

1. Copy the entire `/mobile/` directory to your Cloudflare Pages repository
2. Deploy to subdomain: `mobile.journalismatlas.com`
3. Test on multiple devices (iPhone, Android)
4. Verify on different browsers (Safari, Chrome mobile)

---

## Additional Notes

- Keep all animations under 300ms for snappiness
- Use `will-change: transform` on animated elements for GPU acceleration
- Test on actual mobile devices, not just browser dev tools
- Consider adding haptic feedback where supported: `navigator.vibrate(10)`
- Add basic analytics events for filter usage, view switches, creator taps

---

**YOU HAVE EVERYTHING YOU NEED. BUILD THIS MOBILE EXPERIENCE TONIGHT! 🚀**
