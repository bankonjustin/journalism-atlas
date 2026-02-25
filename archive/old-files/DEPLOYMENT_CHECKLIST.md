# Deployment Checklist for journalismatlas.com

## Pre-Deployment Code Updates ✅
- [x] Added SEO meta tags to all HTML pages
- [x] Added Open Graph tags for social media sharing
- [x] Added Twitter Card tags
- [x] Added canonical URLs pointing to journalismatlas.com
- [x] Added meta descriptions to all pages
- [x] Verified no hardcoded subdomain references

## Cloudflare Configuration

### 1. DNS Settings
- [ ] Verify A/CNAME records point to correct destination
- [ ] Ensure SSL/TLS is set to "Full" or "Full (strict)"
- [ ] Check that DNS propagation is complete

### 2. SSL/TLS Certificate
- [ ] Confirm SSL certificate covers journalismatlas.com
- [ ] Enable "Always Use HTTPS" in SSL/TLS settings
- [ ] Set minimum TLS version to 1.2 or higher

### 3. Page Rules (Recommended)
- [ ] Set up 301 redirect from www.atlas.journalismatlas.com → journalismatlas.com
- [ ] Consider adding www.journalismatlas.com → journalismatlas.com redirect
- [ ] Enable cache settings for static assets

### 4. Security Settings
- [ ] Enable "Auto Minify" for HTML, CSS, JS (optional, test first)
- [ ] Consider enabling "Brotli" compression
- [ ] Review firewall rules if any were set for subdomain

### 5. Analytics & Monitoring
- [ ] Update Google Analytics property (if applicable)
- [ ] Update Cloudflare Web Analytics (if applicable)
- [ ] Set up uptime monitoring

## Deployment Steps

### 1. Backup Current Mission Statement
- [ ] Download current HTML file from root domain
- [ ] Save backup locally with timestamp

### 2. Upload New Files
- [ ] Upload all HTML files
- [ ] Upload favicon (Journalism_Atlas_favicon.png)
- [ ] Upload any CSS/JS files
- [ ] Upload any data files (CSV, JSON)
- [ ] Verify file permissions

### 3. Test After Deployment
- [ ] Visit https://journalismatlas.com and verify homepage loads
- [ ] Test all navigation links
- [ ] Test search functionality
- [ ] Test contact form submission
- [ ] Verify favicon displays correctly
- [ ] Test on mobile device

### 4. SEO Verification
- [ ] Test social media preview on Facebook Debugger
- [ ] Test social media preview on Twitter Card Validator
- [ ] Submit sitemap to Google Search Console (if applicable)
- [ ] Verify robots.txt (if applicable)

### 5. Cross-Browser Testing
- [ ] Chrome
- [ ] Firefox
- [ ] Safari
- [ ] Edge
- [ ] Mobile browsers (iOS Safari, Chrome Android)

### 6. Performance Check
- [ ] Run Lighthouse audit
- [ ] Check page load times
- [ ] Verify all external resources load (fonts, D3.js)

## Post-Deployment

### Immediate (Within 24 hours)
- [ ] Monitor error logs in Cloudflare
- [ ] Check analytics for traffic
- [ ] Test email (hello@journalismatlas.com) still works
- [ ] Respond to any user reports

### Week 1
- [ ] Monitor search console for any crawl errors
- [ ] Check for broken links
- [ ] Review analytics for unusual patterns

## Rollback Plan
If issues arise:
1. Keep backup of old mission statement HTML accessible
2. Can quickly re-upload via Cloudflare Pages dashboard
3. DNS changes take time to propagate, so plan accordingly

## Contact Information
- Cloudflare account owner: [Add name/email]
- DNS provider: Cloudflare
- Hosting: Cloudflare Pages

## Notes
- Old subdomain: www.atlas.journalismatlas.com
- New main domain: journalismatlas.com
- All pages now include proper SEO meta tags and canonical URLs
- Backup files kept in repo: index_feb_6_backup.html, index_feb_7_firstworkingtreemap.html
