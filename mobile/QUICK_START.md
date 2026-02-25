# Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Start Local Server
```bash
cd /Users/justinbank/Documents/Code/Atlas.prototype/mobile
python3 -m http.server 8080
```

### 2. Open in Browser
```
http://localhost:8080
```

### 3. Test on Mobile
- Open Chrome DevTools (F12)
- Click device toolbar icon (Ctrl+Shift+M)
- Select iPhone or Android device
- Interact with the app!

## 🎯 What You'll See

### Main View - Bubble Visualization
- 792 colorful bubbles representing creators
- Each bubble sized by platform count
- Colors represent topic groups

### Interactions
- **Tap a bubble** → See creator details
- **Pinch zoom** → Zoom in/out
- **Pan/drag** → Explore the canvas
- **Double-tap** → Reset zoom

### Filter Button (Bottom Left)
- Opens tag cloud overlay
- Tap topics to filter bubbles
- Multiple selections allowed
- See active filters as green pills

### View Switcher (Bottom Right)
- Switch to swipeable cards view
- 9 category cards with mini visualizations
- Swipe left/right to browse
- Tap "Explore" to filter by that category

### Bottom Sheet
- Appears when you tap a bubble
- Shows creator name, platforms, topics
- **Swipe left** → Next creator
- **Swipe right** → Previous creator
- **Swipe down** → Close
- **Share button** → Share creator

## 📱 Mobile Testing

### Test on Your Phone
1. Get your computer's local IP:
   ```bash
   ifconfig | grep "inet " | grep -v 127.0.0.1
   ```

2. Make sure your phone is on same WiFi

3. Open on phone:
   ```
   http://YOUR_IP_ADDRESS:8080
   ```

4. Test all gestures!

## 🐛 Troubleshooting

### Page doesn't load?
- Check server is running
- Try http://127.0.0.1:8080
- Check browser console for errors

### No bubbles appear?
- Open browser console (F12)
- Check for error messages
- Verify data file loaded

### Gestures not working?
- Make sure you're in mobile device mode
- Try actual mobile device
- Check Hammer.js loaded

## 📂 File Structure

```
mobile/
├── index.html              ← Main page
├── css/
│   ├── variables.css       ← Colors & spacing
│   ├── mobile.css          ← Styles
│   └── animations.css      ← Animations
├── js/
│   ├── mobile-main.js      ← Start here
│   ├── bubble-viz.js       ← D3 visualization
│   ├── tag-cloud.js        ← Filter system
│   ├── swipe-cards.js      ← Card carousel
│   ├── bottom-sheet.js     ← Creator details
│   └── data-loader.js      ← Data processing
└── data/
    └── creators-data.json  ← 792 creators
```

## 🎨 Customization

### Change Colors
Edit `css/variables.css`:
```css
--color-brand-green: #CCFF00;  /* Your color */
--color-topic-1: #FF6B6B;      /* Topic colors */
```

### Adjust Bubble Size
Edit `js/bubble-viz.js`:
```javascript
.range([8, 40])  // Min and max radius
```

### Change Animation Speed
Edit `css/animations.css`:
```css
transition: 300ms ease;  /* Make faster/slower */
```

## 🚀 Deploy to Production

### Option 1: Cloudflare Pages
1. Push code to GitHub
2. Connect repo to Cloudflare Pages
3. Deploy!

### Option 2: Netlify
1. Drag & drop `mobile/` folder
2. Done!

### Option 3: Any Web Server
1. Copy `mobile/` folder to server
2. Point domain to folder
3. Done!

## 📊 Performance Tips

### Fast Loading
- All files under 50KB each
- D3.js and Hammer.js load from CDN
- No build process needed

### Smooth Animations
- GPU-accelerated transforms
- Throttled zoom/pan events
- Debounced filter updates

## 🆘 Getting Help

### Check Console
Open browser console (F12) to see:
- Loading progress
- Error messages
- Debug info

### Common Issues

**Issue**: Blank screen
**Fix**: Check data file path in data-loader.js

**Issue**: Bubbles overlap
**Fix**: Adjust collision force in bubble-viz.js

**Issue**: Slow performance
**Fix**: Reduce creator count or adjust simulation

## ✅ Checklist

Before deploying:
- [ ] Test on iPhone Safari
- [ ] Test on Android Chrome
- [ ] Test all gestures
- [ ] Test filtering
- [ ] Test view switching
- [ ] Check console for errors
- [ ] Verify creator count (792)
- [ ] Test share functionality

## 🎉 You're Ready!

The mobile experience is complete and ready to use. Enjoy exploring 792 independent creator-journalists!

---

**Need more help?** Check out:
- README.md - Full documentation
- DEPLOYMENT.md - Production deployment guide
- IMPLEMENTATION_SUMMARY.md - Technical details
