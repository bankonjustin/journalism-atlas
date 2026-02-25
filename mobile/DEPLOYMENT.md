# Mobile App Deployment Guide

## Quick Start

### Local Testing

1. **Start Local Server**
   ```bash
   cd /Users/justinbank/Documents/Code/Atlas.prototype/mobile
   python3 -m http.server 8080
   ```

2. **Open in Browser**
   - Desktop: http://localhost:8080
   - Mobile: http://YOUR_LOCAL_IP:8080

3. **Test on Mobile Device**
   - Enable responsive design mode in Chrome DevTools
   - Or connect your phone to the same WiFi and visit your local IP

### Production Deployment to Cloudflare Pages

1. **Prepare Repository**
   ```bash
   # Make sure you're in the Atlas.prototype directory
   cd /Users/justinbank/Documents/Code/Atlas.prototype

   # Initialize git if not already done
   git init
   git add mobile/
   git commit -m "Add mobile experience"
   ```

2. **Push to GitHub**
   ```bash
   # Create a new GitHub repository
   # Then push your code
   git remote add origin https://github.com/YOUR_USERNAME/atlas-mobile.git
   git branch -M main
   git push -u origin main
   ```

3. **Deploy to Cloudflare Pages**
   - Go to Cloudflare Dashboard
   - Navigate to Pages
   - Click "Create a project"
   - Connect to your GitHub repository
   - Configure build settings:
     - Framework preset: None
     - Build command: (leave empty)
     - Build output directory: `/mobile`
   - Click "Save and Deploy"

4. **Configure Custom Domain**
   - After deployment, go to Custom domains
   - Add `mobile.journalismatlas.com`
   - Follow DNS configuration instructions

## File Structure Check

Ensure your mobile directory has this structure:

```
mobile/
├── index.html
├── README.md
├── DEPLOYMENT.md
├── css/
│   ├── animations.css
│   ├── mobile.css
│   └── variables.css
├── data/
│   └── creators-data.json
└── js/
    ├── bottom-sheet.js
    ├── bubble-viz.js
    ├── data-loader.js
    ├── mobile-main.js
    ├── swipe-cards.js
    └── tag-cloud.js
```

## Pre-Deployment Checklist

### Code Quality
- [ ] All JavaScript files are error-free
- [ ] Data file loads correctly
- [ ] No console errors in production build

### Performance
- [ ] Images optimized (if any)
- [ ] JSON data file is under 1MB
- [ ] Page loads in < 2 seconds on 4G

### Mobile Optimization
- [ ] Touch targets are 44x44px minimum
- [ ] Text is readable (minimum 14px)
- [ ] Safe area handling works on iOS notch
- [ ] No horizontal scroll issues
- [ ] Pinch zoom disabled on inputs

### Cross-Browser Testing
- [ ] Tested on Safari iOS
- [ ] Tested on Chrome Android
- [ ] Tested on Chrome Desktop
- [ ] Tested on Safari Desktop

### Functionality Testing
- [ ] Bubble visualization loads
- [ ] Bubbles are tappable
- [ ] Filter system works
- [ ] Swipe cards work
- [ ] Bottom sheet appears on tap
- [ ] Share functionality works
- [ ] All gestures respond correctly

## Troubleshooting

### Issue: Data doesn't load
**Solution:** Check that `creators-data.json` is in the `data/` directory and the path is correct in `data-loader.js`

### Issue: Bubbles don't appear
**Solution:** Open browser console and check for D3.js errors. Ensure D3.js v7 is loading from CDN.

### Issue: Touch gestures don't work
**Solution:** Verify Hammer.js is loading correctly. Check that touch event listeners are properly set up.

### Issue: Blank screen on mobile
**Solution:** Check for JavaScript errors in mobile Safari. Some ES6 features may need transpilation.

## Performance Monitoring

After deployment, monitor:
- Page load time (target: < 2s)
- Time to interactive (target: < 3s)
- First contentful paint (target: < 1s)
- Number of creators loaded (should be 792)

## Analytics Integration

To add analytics, insert before closing `</head>` tag in `index.html`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=YOUR_GA_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'YOUR_GA_ID');
</script>
```

Track events in `mobile-main.js`:
```javascript
// Track filter usage
gtag('event', 'filter_applied', {
  'filter_type': 'topic',
  'filter_value': topicName
});

// Track creator views
gtag('event', 'creator_viewed', {
  'creator_name': creator.name
});
```

## Security Headers

Configure these headers in Cloudflare Pages:
```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
```

## CDN Configuration

The app uses these CDN resources:
- D3.js v7: https://d3js.org/d3.v7.min.js
- Hammer.js: https://cdnjs.cloudflare.com/ajax/libs/hammer.js/2.0.8/hammer.min.js
- Google Fonts: https://fonts.googleapis.com/

Ensure these are allowed in your CSP headers.

## Backup Strategy

Before deploying:
1. Backup `creators-data.json`
2. Create a git tag for the release
3. Document any configuration changes

```bash
git tag -a v1.0.0 -m "Mobile app launch"
git push origin v1.0.0
```

## Rollback Procedure

If issues arise after deployment:
1. Go to Cloudflare Pages dashboard
2. Find the previous deployment
3. Click "Rollback to this deployment"
4. Verify the rollback worked
5. Investigate and fix the issue locally
6. Redeploy when ready

## Support & Maintenance

### Regular Updates
- Update creator data monthly
- Check for broken links quarterly
- Update dependencies annually

### Monitoring
- Set up uptime monitoring (e.g., UptimeRobot)
- Monitor error logs in Cloudflare
- Track user feedback

## Contact

For deployment issues, contact:
- Developer: [Your contact info]
- Project: The Independent Journalism Atlas

Last updated: February 2026
