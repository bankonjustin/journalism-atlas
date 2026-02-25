# Atlas Logo Implementation Guide

## Overview

The social graphic generator now includes proper Atlas branding with the icon and wordmark logos dynamically loaded from the assets folder.

## Logo Selection Logic

The generator automatically chooses logo colors based on the background color:

### Dark Backgrounds → White Logos
- **Black** (#000000) → White logos
- **Dark Gray** (#313131) → White logos
- **Olive Green** (#5d7400) → White logos

### Light Backgrounds → Black Logos
- **Acid Green** (#ceff00) → Black logos
- **Lime Green** (#97d600) → Black logos

## Logo Assets Used

### White Logos (for dark backgrounds)
```
Icon:     assets/images/icons/Journalism_Atlas_icon_white_transparent.png
Wordmark: assets/images/logos/Journalism_Atlas_wordmark_lockup_white.png
```

### Black Logos (for light backgrounds)
```
Icon:     assets/images/icons/Journalism_Atlas_icon_black_transparent.png
Wordmark: assets/images/logos/Journalism_Atlas_wordmark_lockup_black.png
```

## Logo Placement

### Square Format (1080×1080) - Instagram

```
┌─────────────────────────────────────┐
│                                     │
│                                     │
│            [Creator Photo]          │
│                                     │
│                                     │
│                                     │
│       Creator message text          │
│       wraps across multiple         │
│       lines as needed               │
│                                     │
│                                     │
│      journalismatlas.com            │
│                           [Icon]    │
│                         [Wordmark]  │
└─────────────────────────────────────┘

Layout:
- Icon: 50×50px
- Wordmark: 120px wide (proportional height)
- Stack: Icon above wordmark
- Position: Bottom right corner
- Padding: 30px from edges
- Gap: 10px between icon and wordmark
```

### Wide Format (1200×630) - Twitter/LinkedIn

```
┌───────────────────────────────────────────────────────┐
│                                                       │
│  [Photo]    Creator message text wraps               │
│             across multiple lines here                │
│             positioned to the right                   │
│             of the profile photo                      │
│                                                       │
│  journalismatlas.com         [Icon][Wordmark]        │
└───────────────────────────────────────────────────────┘

Layout:
- Icon: 45×45px
- Wordmark: 35px tall (proportional width)
- Arrangement: Side by side (horizontal)
- Position: Bottom right corner
- Padding: 25px from edges
- Gap: 10px between icon and wordmark
```

## Technical Implementation

### 1. Logo Preloading

Logos are preloaded when the page initializes:

```javascript
function loadLogos() {
    const logoSources = {
        whiteIcon: '../assets/images/icons/Journalism_Atlas_icon_white_transparent.png',
        whiteWordmark: '../assets/images/logos/Journalism_Atlas_wordmark_lockup_white.png',
        blackIcon: '../assets/images/icons/Journalism_Atlas_icon_black_transparent.png',
        blackWordmark: '../assets/images/logos/Journalism_Atlas_wordmark_lockup_black.png'
    };

    // Load all images and store in state
    Object.keys(logoSources).forEach(key => {
        const img = new Image();
        img.onload = () => { state.logoImages[key] = img; };
        img.src = logoSources[key];
    });
}
```

### 2. Dynamic Logo Selection

```javascript
function getLogoType(backgroundColor) {
    const lightBackgrounds = ['#ceff00', '#97d600'];

    if (lightBackgrounds.includes(backgroundColor)) {
        return 'black'; // Use black logos on light backgrounds
    } else {
        return 'white'; // Use white logos on dark backgrounds
    }
}
```

### 3. Canvas Rendering

```javascript
function drawAtlasLogo(ctx, canvasWidth, canvasHeight, format) {
    const logoType = getLogoType(state.backgroundColor);
    const icon = state.logoImages[`${logoType}Icon`];
    const wordmark = state.logoImages[`${logoType}Wordmark`];

    // Draw icon and wordmark with proper positioning
    ctx.globalAlpha = 0.9; // Subtle transparency
    ctx.drawImage(icon, x, y, width, height);
    ctx.drawImage(wordmark, x, y, width, height);
    ctx.globalAlpha = 1;
}
```

## Visual Hierarchy

The logo placement follows these design principles:

1. **Subtle but Present**: 0.9 opacity ensures logos are visible without overpowering
2. **Corner Placement**: Bottom right keeps focus on creator photo and message
3. **Adaptive Contrast**: Color selection ensures readability on all backgrounds
4. **Consistent Branding**: Icon + wordmark combination reinforces Atlas identity
5. **Proportional Sizing**: Logos scale appropriately for each format

## Design Specifications

### Square Format (1080×1080)
- **Icon Size**: 50×50px (4.6% of canvas width)
- **Wordmark Width**: 120px (11% of canvas width)
- **Total Height**: ~110px (icon + gap + wordmark)
- **Position**: 30px from bottom and right edges
- **Layout**: Vertical stack (icon above wordmark)

### Wide Format (1200×630)
- **Icon Size**: 45×45px (3.75% of canvas width)
- **Wordmark Height**: 35px (5.6% of canvas height)
- **Total Width**: ~135px (icon + gap + wordmark)
- **Position**: 25px from bottom and right edges
- **Layout**: Horizontal (side by side)

## Fallback Behavior

If logos fail to load:
- Falls back to simple placeholder: circular "A" icon
- Placeholder uses text color with reduced opacity
- No error shown to user (silent fallback)
- Console logs error for debugging

```javascript
function drawLogoPlaceholder(ctx, x, y, size) {
    // Draw simple circular background
    ctx.fillStyle = state.textColor;
    ctx.globalAlpha = 0.3;
    ctx.beginPath();
    ctx.arc(x, y, size / 2, 0, Math.PI * 2);
    ctx.fill();

    // Draw "A" text
    ctx.globalAlpha = 0.6;
    ctx.font = `bold ${size * 0.6}px Hanken Grotesk, sans-serif`;
    ctx.fillText('A', x, y);
    ctx.globalAlpha = 1;
}
```

## Testing Checklist

Verify logos render correctly:

- [ ] White logos show on black background
- [ ] White logos show on dark gray background
- [ ] White logos show on olive green background
- [ ] Black logos show on acid green background
- [ ] Black logos show on lime green background
- [ ] Square format: Icon and wordmark stack vertically
- [ ] Wide format: Icon and wordmark side by side
- [ ] Logos maintain aspect ratio
- [ ] Logo position is consistent across backgrounds
- [ ] Fallback placeholder works if images don't load
- [ ] Both download sizes include logos correctly

## Troubleshooting

### Logos Not Showing
**Problem**: No logos appear on generated graphics
**Solutions**:
1. Check browser console for image loading errors
2. Verify asset paths are correct (relative to `atlas-portal/` directory)
3. Ensure logo files exist in assets folder
4. Check network tab to see if images are being requested
5. Verify no CORS issues with local file loading

### Wrong Logo Color
**Problem**: Black logos on dark background or white on light
**Solutions**:
1. Check `getLogoType()` function logic
2. Verify background color values match exactly (case-sensitive)
3. Add console.log to debug logo selection
4. Check if new background colors were added without updating logic

### Logo Position Off
**Problem**: Logos appear in wrong position or cut off
**Solutions**:
1. Check padding values in `drawAtlasLogo()`
2. Verify canvas dimensions are correct
3. Ensure logo sizes are appropriate for canvas size
4. Check if icon/wordmark aspect ratios are maintained

### Blurry Logos
**Problem**: Logos appear pixelated or blurry
**Solutions**:
1. Verify source images are high resolution
2. Check if scaling calculations are correct
3. Ensure canvas is rendering at full resolution (not scaled CSS)
4. Use PNG files with transparency (not JPG)

## Future Enhancements

Possible improvements:
- Add logo size options (small, medium, large)
- Allow users to choose logo position (corners)
- Support custom logo opacity
- Add logo color customization
- Include alternative logo styles
- Add animation effects (for video exports)

---

**Status**: ✅ Implemented
**Version**: 1.0
**Last Updated**: February 2025
