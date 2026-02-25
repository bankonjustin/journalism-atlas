# Creator Portal - Independent Journalism Atlas

## Overview

The Creator Portal is a static HTML page that allows creators included in the Independent Journalism Atlas to:
1. Generate custom social sharing graphics
2. Submit corrections to their listing
3. Nominate other creators

## File Structure

```
/atlas-portal/
  ├── index.html      # Main portal page
  ├── script.js       # Social graphic generator functionality
  └── README.md       # This file
```

## Features

### 1. Social Graphic Generator

The generator creates custom graphics in two formats:
- **Square (1080×1080)**: Optimized for Instagram
- **Wide (1200×630)**: Optimized for Twitter/LinkedIn

**Steps:**
1. **Creator Info & Photo**: Optionally provide name, email, and upload a profile photo (or use placeholder avatar)
2. **Choose Message**: Select from 4 pre-written messages or write a custom message (max 280 characters)
3. **Customize Style**: Choose background and text colors from Atlas brand colors
4. **Generate & Download**: Preview the graphic, copy social media caption, and download in either format

**Photo Collection Feature:**
- When users download their graphic, if they uploaded a photo and provided name/email, their info is automatically submitted to a Google Form
- Clear disclosure about photo usage is shown before upload
- All fields are optional - users can still generate graphics without sharing info
- Photos may be used in creator Atlas profiles as the platform develops

**Copy Caption Feature:**
- After generating a graphic, users get a ready-to-use social media caption
- Includes their chosen message + hashtags (#IndependentJournalism #CreatorEconomy)
- One-click copy to clipboard functionality
- Caption text is also manually selectable for easy copying
- Helps ensure consistent messaging across social platforms

### 2. Corrections & Nominations

Links to the main Atlas submission form for:
- Correcting existing listings
- Nominating new creators

## Integration with Main Site

### Asset References

The portal references existing site assets from the parent directory:

```html
<!-- Logo -->
<img src="../assets/images/logos/Journalism_Atlas_logo_black.png">

<!-- Favicon -->
<link rel="icon" href="../assets/images/icons/Journalism_Atlas_favicon.png">

<!-- Fonts (via Google Fonts) -->
<link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600;700;800&family=Merriweather:wght@400;700&display=swap" rel="stylesheet">
```

### CSS/Styling

All styles are embedded in `index.html` and match the existing Atlas design system:
- **Colors**: Uses Atlas brand colors (acid-green, lime-green, dark-gray, etc.)
- **Typography**: Hanken Grotesk font family
- **Layout**: Follows existing site patterns
- **Navigation**: Matches main site navigation structure

### Navigation Links

The portal includes navigation back to main site pages:
- Atlas Home (`../index.html`)
- Submit (`../submit.html`)
- About (`../who-we-are.html`)

## Technical Details

### Canvas Rendering

The graphic generator uses HTML5 Canvas API to render images with:
- Circular profile photos (or placeholder avatars)
- Text wrapping for messages
- Brand colors for backgrounds and text
- **Atlas logo branding** (icon + wordmark)
  - Automatically selects white or black logos based on background color
  - Square format: Stacked layout (icon above wordmark) in bottom right
  - Wide format: Side-by-side layout in bottom right
  - Preloaded images for smooth rendering
- URL attribution

### Image Processing

- **Supported formats**: JPG, PNG
- **Max file size**: 5MB
- **Recommended size**: 500×500px or larger (square)
- **Processing**: Client-side only using FileReader API

### Text Handling

- **Pre-written messages**: 4 options optimized for different tones
- **Custom messages**: 280 character limit (Twitter-optimized)
- **Text wrapping**: Automatic line breaking based on canvas width
- **Font**: Hanken Grotesk, 600 weight

### Download Functionality

- **Format**: PNG images
- **Method**: Canvas.toBlob() with download trigger
- **Filenames**: `atlas-share-[format]-[timestamp].png`

## Form Submission

### Corrections & Nominations Form

The portal links to the existing Google Form at:
```
../submit.html
```

This reuses the main Atlas submission infrastructure—no separate form handling needed.

### Photo Collection Form

A separate Google Form collects creator photos and contact information:

**What's Collected:**
- Creator name (optional)
- Email address (optional)
- Profile photo (optional)
- Timestamp (automatic)

**When It's Submitted:**
- Automatically when user downloads their graphic
- Only if they uploaded a photo AND provided name or email
- Uses no-cors fetch request to Google Form endpoint

**Setup Instructions:**
See `GOOGLE_FORM_SETUP.md` for complete instructions on:
1. Creating the Google Form
2. Getting entry IDs
3. Connecting the form to the portal
4. Testing the integration

**Configuration:**
Edit `GOOGLE_FORM_CONFIG` in `script.js`:
```javascript
const GOOGLE_FORM_CONFIG = {
    actionUrl: 'YOUR_GOOGLE_FORM_URL',
    fields: {
        creatorName: 'entry.XXXXXXXX',
        email: 'entry.XXXXXXXX',
        photo: 'entry.XXXXXXXX'
    }
};
```

## Testing Checklist

Before deployment, verify:

- [ ] Photo upload works with various image sizes/formats
- [ ] Custom message character counter works correctly
- [ ] All 4 pre-written messages render properly
- [ ] Custom message option shows/hides textarea correctly
- [ ] Background color selection updates preview
- [ ] Text color selection updates preview
- [ ] Generate button validates message presence
- [ ] Square (1080×1080) download works
- [ ] Wide (1200×630) download works
- [ ] Placeholder avatar renders when no photo uploaded
- [ ] Navigation links work correctly
- [ ] Page is mobile-responsive
- [ ] All interactions work on touch devices
- [ ] Form submission link works

## Browser Compatibility

**Supported browsers:**
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

**Required features:**
- HTML5 Canvas API
- FileReader API
- CSS Grid & Flexbox
- ES6 JavaScript

## Accessibility

- Semantic HTML structure
- ARIA labels on form inputs
- Keyboard navigation support
- Focus states on interactive elements
- Color contrast meets WCAG AA standards
- Alt text on images

## Responsive Design

**Breakpoints:**
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

**Mobile optimizations:**
- Stack navigation vertically
- Full-width buttons
- Reduced padding/margins
- Larger touch targets
- Simplified color selector layout

## Performance

- No external dependencies (except Google Fonts)
- All JavaScript is vanilla (no frameworks)
- Images processed client-side (no server load)
- Minimal CSS (embedded in HTML)
- Fast page load (< 1s on 3G)

## Customization

### Adding New Background Colors

Edit the color selector in `index.html`:

```html
<div class="color-option" data-color="#NEW_COLOR" style="background-color: #NEW_COLOR;" title="Color Name"></div>
```

### Adding New Pre-written Messages

Edit the `messages` object in `script.js`:

```javascript
const messages = {
    message1: "...",
    message2: "...",
    message3: "...",
    message4: "...",
    message5: "New message here" // Add new message
};
```

Then add corresponding radio button in `index.html`.

### Changing Canvas Dimensions

Edit render functions in `script.js`:

```javascript
renderCanvas(canvas, 1080, 1080, true);  // Square
renderCanvas(canvas, 1200, 630, false);   // Wide
```

## Logo Assets

The generator uses actual Atlas logo files:

**For Dark Backgrounds** (black, dark gray, olive green):
- Icon: `Journalism_Atlas_icon_white_transparent.png`
- Wordmark: `Journalism_Atlas_wordmark_lockup_white.png`

**For Light Backgrounds** (acid green, lime green):
- Icon: `Journalism_Atlas_icon_black_transparent.png`
- Wordmark: `Journalism_Atlas_wordmark_lockup_black.png`

The logos are:
- Preloaded on page init for smooth rendering
- Automatically selected based on background color
- Positioned in bottom right corner with subtle opacity (0.9)
- Scaled appropriately for each format

## Known Limitations

1. **Font Rendering**: Canvas may render fonts slightly differently than browser
   - Ensure Hanken Grotesk is loaded before rendering
   - Font weights may vary based on system

2. **Image Quality**: Canvas rendering at high resolution
   - 1080×1080 and 1200×630 are good quality for social media
   - For print quality, increase canvas dimensions proportionally

3. **Logo Loading**: If logos fail to load, falls back to placeholder "A" icon
   - Check browser console for image loading errors
   - Verify asset paths are correct relative to portal directory

## Future Enhancements

Possible improvements:
- Add more background color options
- Support video profile pictures (GIF/MP4)
- Add text shadow/outline options
- Include more graphic templates
- Support custom logo upload
- Add animation effects
- Generate multiple graphics at once
- Export to other formats (WEBP, SVG)

## Support

For questions or issues with the Creator Portal:
- Check the main Atlas site: https://journalismatlas.com
- Review existing submission form: ../submit.html
- Contact Atlas team via main site contact form

## License

Part of the Independent Journalism Atlas project.
© 2025 Independent Journalism Atlas

---

**Version**: 1.0
**Last Updated**: February 2025
**Maintained By**: Atlas Development Team
