# The Independent Journalism Atlas

A comprehensive directory of 792+ independent journalists and creators, mapping the new landscape of independent journalism worldwide.

## 🌐 Live Site Structure

### Main Desktop Experience
**URL**: `https://journalismatlas.com/`
**File**: `index.html`

The primary desktop experience featuring:
- Interactive D3.js treemap visualization
- Advanced search and filtering
- Creator profiles and metadata
- Responsive design for all screen sizes

### Mobile Experience
**URL**: `https://journalismatlas.com/mobile/`
**Directory**: `/mobile/`

Touch-optimized mobile experience featuring:
- D3.js force-directed bubble visualization
- Swipeable category cards
- Bottom sheet creator details
- Pinch zoom and pan gestures
- Multi-select tag filters

### Additional Pages
- **Who We Are**: `/who-we-are.html`
- **What We Do**: `/what-we-do.html`
- **How We Did This**: `/how-we-did-this.html`
- **Research**: `/research.html`
- **Advisory Board**: `/advisory.html`
- **Contact**: `/contact.html`
- **Thank You**: `/contact-thanks.html`

## 📁 Project Structure

```
Atlas.prototype/
├── index.html              # Main desktop application (root)
├── advisory.html           # Advisory board page
├── contact.html            # Contact form
├── contact-thanks.html     # Contact confirmation
├── how-we-did-this.html    # Methodology page
├── research.html           # Research page
├── what-we-do.html         # About our work
├── who-we-are.html         # About us page
├── README.md               # This file
│
├── mobile/                 # Mobile experience (/mobile/)
│   ├── index.html          # Mobile app entry point
│   ├── README.md           # Mobile documentation
│   ├── DEPLOYMENT.md       # Mobile deployment guide
│   ├── QUICK_START.md      # Mobile quick start
│   ├── css/                # Mobile stylesheets
│   │   ├── variables.css
│   │   ├── mobile.css
│   │   └── animations.css
│   ├── js/                 # Mobile JavaScript modules
│   │   ├── mobile-main.js
│   │   ├── bubble-viz.js
│   │   ├── tag-cloud.js
│   │   ├── swipe-cards.js
│   │   ├── bottom-sheet.js
│   │   └── data-loader.js
│   └── data/
│       └── creators-data.json
│
├── assets/                 # Shared assets
│   ├── css/                # Stylesheets
│   │   ├── variables.css
│   │   ├── animations.css
│   │   └── atlas_color_palette.css
│   ├── js/                 # JavaScript files
│   │   └── data-loader.js
│   ├── data/               # Data files
│   │   ├── creators-data.json
│   │   ├── creators-data-backup.json
│   │   └── *.csv (data sources)
│   └── images/             # Image assets
│       ├── icons/          # Favicons and icons
│       ├── logos/          # Brand logos
│       ├── advisory/       # Advisory board photos
│       └── partners/       # Partner logos
│
└── archive/                # Archived files
    ├── old-backups/        # Previous versions
    └── old-files/          # Deprecated files

```

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/atlas.git
   cd atlas
   ```

2. **Start a local server**
   ```bash
   python3 -m http.server 8080
   ```

3. **Open in browser**
   - Desktop: http://localhost:8080/
   - Mobile: http://localhost:8080/mobile/

### Testing

**Desktop Experience:**
- Open `index.html` in browser
- Test search functionality
- Test treemap interactions
- Check responsive design

**Mobile Experience:**
- Navigate to `/mobile/`
- Use Chrome DevTools mobile mode
- Test on actual devices
- Check all gestures work

## 🎨 Design System

### Colors
- **Black**: `#000000` - Primary text, navigation
- **Acid Green**: `#CCFF00` - Brand accent, CTAs
- **Light Gray**: `#efeff2` - Background
- **Dark Gray**: `#313131` - Secondary text
- **White**: `#FFFFFF` - Cards, overlays

### Typography
- **Primary**: Hanken Grotesk (400, 500, 600, 700, 800)
- **Secondary**: Merriweather (400, 700)

### Spacing Scale
- XS: 4px
- SM: 8px
- MD: 16px
- LG: 24px
- XL: 32px

## 📊 Data Format

The application uses `creators-data.json` with this structure:

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

### Data Fields
- **name**: Creator's full name
- **channel**: Channel/publication name
- **link**: Primary URL
- **platform**: Platform type (e.g., "Video - YouTube")
- **topic**: Specific topic focus
- **geography**: Geographic location
- **group**: Topic category (1 of 9 main groups)

## 🔧 Technology Stack

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with variables
- **JavaScript (ES6+)** - Vanilla JS, no frameworks
- **D3.js v7** - Data visualization

### Libraries
- **D3.js** - Desktop treemap & mobile bubbles
- **Hammer.js** - Mobile touch gestures (mobile only)
- **Google Fonts** - Hanken Grotesk, Merriweather
- **Material Icons** - UI icons

### Hosting
- **Cloudflare Pages** - Static hosting
- **Custom Domain** - journalismatlas.com

## 📱 Browser Support

### Desktop
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### Mobile
- Safari iOS 13+
- Chrome Android 90+

## 🚢 Deployment

### Cloudflare Pages

1. **Connect Repository**
   - Go to Cloudflare Pages dashboard
   - Connect your GitHub repository

2. **Configure Build Settings**
   - Framework preset: None
   - Build command: (leave empty)
   - Build output directory: `/`
   - Root directory: `/`

3. **Deploy**
   - Push to main branch
   - Automatic deployment

### Environment Variables
None required - this is a static site.

### Custom Domain
- Add `journalismatlas.com` in Cloudflare Pages
- Configure DNS records as instructed
- Enable HTTPS (automatic)

## 📈 Performance

### Targets
- **First Contentful Paint**: < 1.5s
- **Time to Interactive**: < 3s
- **Largest Contentful Paint**: < 2.5s

### Optimizations
- Lazy loading images
- Deferred JavaScript
- Minified CSS (inline)
- CDN for external libraries
- Efficient D3.js rendering

## 🔒 Security

### Headers (Cloudflare)
```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
```

### Content Security Policy
```
default-src 'self';
script-src 'self' 'unsafe-inline' https://d3js.org https://cdnjs.cloudflare.com;
style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
font-src 'self' https://fonts.gstatic.com;
img-src 'self' data: https:;
```

## 📝 Content Updates

### Adding New Creators

1. **Update Data File**
   - Edit `assets/data/creators-data.json`
   - Follow existing format
   - Validate JSON syntax

2. **Test Locally**
   - Refresh application
   - Verify creator appears
   - Check all fields display correctly

3. **Deploy**
   - Commit changes
   - Push to repository
   - Cloudflare auto-deploys

### Updating Copy

1. Edit HTML files directly
2. Test changes locally
3. Commit and push to deploy

## 🐛 Troubleshooting

### Issue: Data doesn't load
**Solution**: Check console for errors. Verify `creators-data.json` path is correct.

### Issue: Images don't appear
**Solution**: Check image paths use `assets/images/` prefix. Verify files exist.

### Issue: Mobile gestures not working
**Solution**: Ensure Hammer.js loads correctly. Check touch event listeners.

### Issue: Treemap doesn't render
**Solution**: Verify D3.js loads from CDN. Check browser console for errors.

## 📞 Support

For issues or questions:
- **Email**: [Your contact email]
- **GitHub Issues**: [Your repo URL]
- **Documentation**: Check `/mobile/README.md` for mobile-specific docs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📜 License

Copyright © 2026 The Independent Journalism Atlas

## 🙏 Credits

**Built with**:
- D3.js by Mike Bostock
- Hammer.js by Jorik Tangelder
- Google Fonts
- Material Icons

**Special Thanks**:
- Advisory Board members
- Partner organizations
- Independent journalism community

---

## 📋 Maintenance Checklist

### Monthly
- [ ] Update creator data
- [ ] Check for broken links
- [ ] Review analytics
- [ ] Test on latest browsers

### Quarterly
- [ ] Audit performance
- [ ] Review and update documentation
- [ ] Check accessibility compliance
- [ ] Update dependencies

### Annually
- [ ] Review design system
- [ ] Update technology stack
- [ ] Comprehensive QA testing
- [ ] Refresh content and copy

---

**Last Updated**: February 16, 2026
**Version**: 1.0.0
**Status**: Production Ready ✅
