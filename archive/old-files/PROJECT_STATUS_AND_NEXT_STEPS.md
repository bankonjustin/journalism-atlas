# Atlas Launch Sprint - Current Status & Next Steps
**Updated:** February 5, 2026 (Thursday Evening)
**Launch:** Thursday, February 12, 2026
**Design/Dev Lock:** Sunday, February 8 at 5pm

---

## 📊 PROJECT STATUS OVERVIEW

### ✅ What's Already Done (from Feb 4 QA Session)

**Critical Fixes Completed:**
1. ✅ Navigation links fixed on all 5 subpages (.html extensions added)
2. ✅ Mobile hamburger menu implemented
3. ✅ Character encoding fixed (mojibake resolved)
4. ✅ Data quality issues fixed (38 issues in creators-data.json)
   - Added https:// to 20+ URLs
   - Fixed "Newsetter" → "Newsletter" typo
   - Completed D.J. Byrnes record

**Current Site Status:**
- ✅ 498 creators in database (as of Feb 4)
- ✅ All 3 visualizations working (Grid, Bubble Map, Sunburst)
- ✅ Search and filters functional
- ✅ 6 HTML pages exist: index.html + 5 subpages
- ✅ Mobile responsive with working navigation
- ✅ No console errors

### 🔴 What Still Needs to Be Done (Your Feedback)

**Priority 1: Navigation Structure (CRITICAL)**
- ❌ Index.html nav links to hashes (#who-we-are, #what-we-do, etc.)
- ❌ Should link to actual .html files instead
- **Decision:** You confirmed this needs to be fixed

**Priority 2: Color Palette Implementation**
- ❌ Site currently uses basic greens (acid-green, lime-green)
- ❌ New style guide has 10+ secondary colors for visualizations
- ❌ Sunburst chart needs updated color palette
- ❌ Bubble map needs updated color palette
- **Decision:** You confirmed this needs to be done

**Priority 3: Data Updates**
- 🔄 Ryan is cleaning data, target 600-1000 creators by weekend
- 🔄 Current workflow: Google Sheets → CSV → JSON conversion
- ❓ Need to finalize data update process

---

## 📁 PROJECT FILES INVENTORY

### In Project Folder (/mnt/project):
```
✅ index.html (92K) - Main database page, needs nav fix
✅ who-we-are.html (14K) - Has content, nav links fixed
✅ what-we-do.html (18K) - Has content, nav links fixed  
✅ advisory.html (15K) - Has content, nav links fixed
✅ contact.html (17K) - Has content, nav links fixed
✅ research.html (17K) - Has content, nav links fixed (3 placeholder article links)

✅ creators-data.json (111K) - 498 creators, cleaned on Feb 4
✅ MegaDatabase_CLEAN_2_5_noon.xlsx (396K) - Latest data from Ryan
✅ MegaDatabase__Justin_Ryan_Liz__Creators_3.csv (76K) - CSV version

✅ QA_REPORT.md - Detailed QA findings from Feb 4
✅ QA_FIXES_SUMMARY.md - What was fixed on Feb 4
✅ TECHNICAL_QA_GUIDE.md - Technical documentation
✅ DEPLOY-INSTRUCTIONS.txt - Cloudflare Pages deployment guide

✅ Journalism_Atlas_favicon.png - Working favicon
✅ 15+ logo/icon files in various colors/formats

✅ The_Atlas_Style_Guide_2025.jpg - Secondary color palette
✅ The_Atlas_Style_Guide_2025_1.jpg - Primary color palette
✅ The_Atlas_Style_Guide_2025_2.pdf - Full style guide
```

### What You Just Received:
```
📄 5_Day_Launch_Sprint_Timeline.md - Day-by-day schedule
📄 QA_Checklist_GoogleSheets.csv - For your QA volunteers
📄 csv_to_json.py - Data conversion script for Ryan
📄 atlas_color_palette.css - Color values from style guide
```

---

## 🎯 IMMEDIATE NEXT STEPS (Tonight/Tomorrow)

### Option A: I Fix Everything Now (Recommended)
**What I'll do:**
1. ✅ Fix index.html navigation (hash links → .html files)
2. ✅ Update CSS with new color palette (all 15+ colors)
3. ✅ Update Sunburst chart to use new secondary colors
4. ✅ Update Bubble Map to use new secondary colors
5. ✅ Test all changes thoroughly
6. ✅ Create updated file package ready to deploy

**Time:** ~2 hours of focused work
**You provide:** Just approval to proceed

### Option B: Prioritized Approach
**Step 1 (30 min):** Fix navigation only
**Step 2 (1 hour):** Implement color palette
**Step 3 (30 min):** Test and verify

**Time:** Same ~2 hours, but in phases you can review

---

## 🤔 QUESTIONS I NEED ANSWERED

### Data Questions:
1. **Current Data:** Should I use the MegaDatabase_CLEAN_2_5_noon.xlsx (newer) or the CSV file?
2. **Conversion:** Want me to convert the latest XLSX to JSON right now?
3. **Weekend Updates:** When Ryan delivers new data, should he:
   - Export to CSV and use the python script?
   - Hand it to you and you'll convert it?
   - Something else?

### Color Implementation Questions:
4. **Sunburst Chart Colors:** Use all 10 secondary colors in sequence?
5. **Bubble Map Colors:** Use secondary colors to differentiate categories?
6. **Accent Colors:** Where else should secondary colors be used? (buttons, badges, highlights?)

### Content Questions:
7. **Research Page Links:** 3 article links are placeholders (#). Should I:
   - Hide them until you have real URLs?
   - Leave them as-is?
   - Add "Coming Soon" text?

8. **Advisory Board Page:** Currently has placeholder structure. Is that okay for launch?

### Deployment Questions:
9. **Hosting:** Confirmed Cloudflare Pages? Or different platform?
10. **Custom Domain:** Is journalismatlas.com already set up/pointed there?

---

## 🚀 RECOMMENDED WORKFLOW FOR TONIGHT

**My Suggestion:**
```
1. You answer the questions above (5 minutes)
2. I implement all the fixes (2 hours)
3. You review the updated files (30 minutes)
4. We identify any issues/tweaks (as needed)
5. Files ready for staging deployment (Tonight/Tomorrow AM)
```

**This gets us to:**
- ✅ Index navigation working correctly
- ✅ New color palette implemented throughout
- ✅ Latest data integrated (600+ creators)
- ✅ Ready for Friday QA testing by your volunteers

---

## 📋 WHAT YOUR QA TEAM NEEDS

**I Created:**
- `QA_Checklist_GoogleSheets.csv` - Upload this to Google Sheets

**Instructions for QA Team:**
1. Upload CSV to Google Sheets
2. Share with all QA volunteers (edit access)
3. Each tester claims items by entering their name
4. Test on their own devices (phones, tablets, laptops)
5. Mark Status as: TODO → IN PROGRESS → PASSED or FAILED
6. Add notes/screenshots for any issues found
7. You or dev marks Date Fixed when resolved

**100+ test items covering:**
- Core functionality (nav, search, filters, viz)
- Mobile responsive
- Browser compatibility
- Content accuracy
- Performance
- SEO

---

## 🎨 COLOR PALETTE REFERENCE

**Primary Colors (Already in use):**
- Light Gray: #efeff2
- Dark Gray: #313131
- Black: #000000
- White: #FFFFFF
- Acid Green: #ceff00 ⭐ (signature brand color)
- Lime Green: #97d600
- Olive Green: #5d7400

**NEW Secondary Colors (For visualizations):**
- Yellow: #ffff00
- Orange: #ff9600
- Pink: #ff66ff
- Magenta: #ff33cc
- Cyan: #00e5ff
- Olive: #606600
- Rust: #b35100
- Purple: #a100a1
- Berry: #a1006c
- Teal: #005aa3

---

## 📅 SPRINT TIMELINE RECAP

**Day 0 (Today - Thursday):** Planning, kickoff, start fixes
**Day 1 (Friday):** Nav fixed, colors implemented, first QA round
**Day 2 (Saturday):** Full dataset integrated, design tweaks, second QA
**Day 3 (Sunday 5pm):** DESIGN/DEV LOCK, final QA, deploy to staging
**Day 4 (Monday AM):** Share with friends for feedback
**Day 5 (Tuesday):** Final polish based on feedback
**Day 6 (Wednesday):** Pre-launch prep, production deploy
**Day 7 (Thursday):** LAUNCH! 🚀

---

## ⚡ READY TO PROCEED?

**Tell me:**
1. Should I proceed with Option A (fix everything now)?
2. Which data file should I use? (XLSX or CSV)
3. Any specific color preferences for visualizations?
4. Any other immediate concerns?

**Then I'll:**
- Fix the navigation
- Implement the color palette
- Update the data
- Package everything for deployment
- Have it ready for your Friday morning review

---

## 💬 COMMUNICATION

**For This Sprint:**
- Quick questions: Here in Claude
- Design decisions: Slack with James
- Data updates: Coordinate with Ryan
- QA issues: Google Sheet (link coming)

**Emergency Contact:**
- If something breaks: Flag immediately
- If timeline slips: Reassess Sunday go/no-go
- If scope creep: Team lead makes cut decisions

---

## ✨ BOTTOM LINE

You're in great shape! The heavy lifting from Feb 4 QA is done. Now we just need to:
1. Fix index.html navigation (30 min)
2. Add the beautiful new colors (1 hour)
3. Update with latest data (30 min)
4. Test everything (ongoing)

**Current Status:** 85% ready for launch
**After tonight's fixes:** 95% ready for launch
**After weekend QA/polish:** 100% ready! 🎉

---

**Ready when you are!** What would you like me to tackle first?
