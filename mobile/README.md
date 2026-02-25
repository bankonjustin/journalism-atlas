# The Independent Journalism Atlas - Mobile Experience

## Overview
A mobile-first, touch-optimized web application for discovering 792+ independent creator-journalists across multiple platforms.

## Features

### 🎯 Interactive Bubble Visualization
- D3.js force-directed layout with 792 creator bubbles
- Bubble size based on platform presence (1-5+ platforms)
- Color-coded by topic groups (9 distinct categories)
- Smooth zoom (0.5x-3x) and pan gestures
- Touch-optimized interactions

### 🏷️ Advanced Filtering
- Multi-select tag cloud interface
- Filter by topic groups, platforms, and geography
- Real-time bubble updates with smooth transitions
- Active filter pills with quick removal
- Clear all functionality

### 📱 Swipeable Category Cards
- 9 topic-based cards with mini visualizations
- Horizontal scroll with snap-to-card behavior
- Progress indicators (dots)
- Direct exploration of each category
- Touch-optimized navigation

### 📝 Creator Detail Sheet
- Slide-up bottom sheet on bubble tap
- Swipe left/right to navigate creators
- Swipe down to dismiss
- Full creator metadata display
- Platform links and action buttons
- Web Share API integration

## File Structure

```
mobile/
├── index.html              # Main HTML structure
├── css/
│   ├── variables.css       # Design tokens and theme
│   ├── mobile.css          # Mobile-specific styles
│   └── animations.css      # Entrance and transition animations
├── js/
│   ├── data-loader.js      # Data loading and processing
│   ├── bubble-viz.js       # D3.js bubble visualization
│   ├── tag-cloud.js        # Filter interface
│   ├── swipe-cards.js      # Category card carousel
│   ├── bottom-sheet.js     # Creator detail sheet
│   └── mobile-main.js      # Main app orchestrator
└── data/
    └── creators-data.json  # Creator database
```

## Technologies Used

- **D3.js v7** - Force-directed graph visualization
- **Hammer.js** - Touch gesture recognition
- **CSS Variables** - Theming and design system
- **Vanilla JavaScript** - No framework dependencies
- **Web Share API** - Native sharing capabilities

## Key Interactions

### Bubble View
- **Tap bubble** → Open creator detail
- **Pinch** → Zoom in/out (0.5x-3x)
- **Pan** → Explore canvas
- **Double-tap background** → Reset zoom

### Tag Cloud
- **Tap tag** → Toggle filter (green glow when active)
- **Tap pill X** → Remove specific filter
- **Clear All** → Reset all filters

### Swipe Cards
- **Swipe left/right** → Navigate cards
- **Tap bubble** → Open creator detail
- **Tap Explore** → Apply filter and return to bubble view

### Bottom Sheet
- **Swipe down** → Dismiss
- **Swipe left** → Next creator
- **Swipe right** → Previous creator
- **Tap outside** → Dismiss
- **Tap Share** → Open share menu or copy link

## Performance Optimizations

- Throttled zoom/pan events (60fps max)
- Debounced filter updates (150ms)
- RequestAnimationFrame for smooth animations
- Lazy rendering of mini visualizations
- Efficient D3 force simulation

## Mobile-First Design

- Safe area handling for iOS notch
- Prevented zoom on input focus
- Touch-optimized hit targets (44x44px minimum)
- GPU-accelerated animations (will-change: transform)
- No horizontal scroll issues
- Haptic feedback where supported

## Data Format

The app expects `creators-data.json` with the following structure:

```json
[
  {
    "name": "Creator Name",
    "channel": "Channel Name",
    "link": "https://...",
    "platform": "Video - YouTube",
    "topic": "Politics",
    "geography": "US",
    "group": "Power & Politics"
  }
]
```

## Local Development

1. Navigate to the mobile directory:
```bash
cd mobile
```

2. Start a local server:
```bash
python3 -m http.server 8080
```

3. Open in browser:
```
http://localhost:8080
```

## Testing Checklist

### Load Performance
- ✅ Page loads in < 2 seconds on 4G
- ✅ No console errors
- ✅ Smooth entrance animations

### Touch Interactions
- ✅ Tap bubbles → Bottom sheet appears
- ✅ Pinch zoom → Smooth scaling
- ✅ Pan → Smooth dragging
- ✅ Swipe cards → Snap to each card
- ✅ Bottom sheet swipe → Navigate creators

### Filtering
- ✅ Tap tags → Bubbles filter correctly
- ✅ Multiple tags → Combined filters work
- ✅ Clear filters → All bubbles return
- ✅ Filter count updates in real-time

### Bottom Sheet
- ✅ All creator data displays correctly
- ✅ Platform links work
- ✅ Swipe gestures work
- ✅ Share functionality works

### View Switching
- ✅ Toggle between bubbles and cards
- ✅ Smooth transitions
- ✅ Filters persist across views

## Deployment

To deploy to Cloudflare Pages:

1. Copy the entire `mobile/` directory to your repository
2. Configure build settings:
   - Build command: (none)
   - Build output directory: `/mobile`
3. Deploy to subdomain: `mobile.journalismatlas.com`
4. Test on multiple devices (iPhone, Android)

## Browser Support

- Safari iOS 13+
- Chrome Android 90+
- Chrome Desktop (for testing)
- Safari Desktop (for testing)

## Credits

Built with Claude Code for The Independent Journalism Atlas.
Designed for mobile-first discovery of independent creator journalism.

## License

Copyright © 2026 The Independent Journalism Atlas
