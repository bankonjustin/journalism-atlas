# Directory Structure Guide

## 📂 Complete File Organization

```
Atlas.prototype/
│
├── 🌐 PUBLIC HTML PAGES (Root Level)
│   ├── index.html                      # MAIN DESKTOP APP (/)
│   ├── who-we-are.html                 # About us page
│   ├── what-we-do.html                 # What we do page
│   ├── how-we-did-this.html            # Methodology page
│   ├── research.html                   # Research page
│   ├── advisory.html                   # Advisory board
│   ├── contact.html                    # Contact form
│   └── contact-thanks.html             # Thank you page
│
├── 📱 MOBILE/ - Mobile Experience (/mobile/)
│   ├── index.html                      # Mobile app entry
│   ├── README.md                       # Mobile docs
│   ├── DEPLOYMENT.md                   # Deployment guide
│   ├── IMPLEMENTATION_SUMMARY.md       # Technical details
│   ├── QUICK_START.md                  # Quick start guide
│   │
│   ├── css/                            # Mobile styles
│   │   ├── variables.css               # Design tokens
│   │   ├── mobile.css                  # Mobile-specific styles
│   │   └── animations.css              # Entrance animations
│   │
│   ├── js/                             # Mobile JavaScript
│   │   ├── mobile-main.js              # Main orchestrator
│   │   ├── bubble-viz.js               # D3 bubble visualization
│   │   ├── tag-cloud.js                # Filter system
│   │   ├── swipe-cards.js              # Card carousel
│   │   ├── bottom-sheet.js             # Creator details
│   │   └── data-loader.js              # Data processing
│   │
│   └── data/                           # Mobile data
│       └── creators-data.json          # Creator database
│
├── 🎨 ASSETS/ - Shared Resources
│   │
│   ├── css/                            # Stylesheets
│   │   ├── variables.css               # CSS variables
│   │   ├── animations.css              # Animations
│   │   └── atlas_color_palette.css     # Color system
│   │
│   ├── js/                             # JavaScript
│   │   └── data-loader.js              # Desktop data loader
│   │
│   ├── data/                           # Data Files
│   │   ├── creators-data.json          # Main creator database (792 creators)
│   │   ├── creators-data-backup.json   # Backup copy
│   │   ├── Creators_Feb8.csv           # Original CSV
│   │   ├── Launch_clean_list.csv       # Clean data
│   │   ├── mega_list_2_7_clean.csv     # Combined data
│   │   └── QA_Checklist*.csv           # QA data
│   │
│   └── images/                         # Image Assets
│       │
│       ├── icons/                      # Icons & Favicons
│       │   ├── Journalism_Atlas_favicon.png
│       │   ├── Journalism_Atlas_icon_black.png
│       │   ├── Journalism_Atlas_icon_black_transparent.png
│       │   ├── Journalism_Atlas_icon_green_black.png
│       │   ├── Journalism_Atlas_icon_green_transparent.png
│       │   ├── Journalism_Atlas_icon_light_gray_transarent.png
│       │   ├── Journalism_Atlas_icon_white_black.png
│       │   └── Journalism_Atlas_icon_white_transparent.png
│       │
│       ├── logos/                      # Brand Logos
│       │   ├── Journalism_Atlas_logo_acid_green.png
│       │   ├── Journalism_Atlas_logo_black.png
│       │   ├── Journalism_Atlas_logo_dark_gray.png
│       │   ├── Journalism_Atlas_logo_light_gray.png
│       │   ├── Journalism_Atlas_wordmark_lockup_black.png
│       │   ├── Journalism_Atlas_wordmark_lockup_white.png
│       │   ├── Journalism_Atlas_wordmark_stacked_black.png
│       │   ├── Journalism_Atlas_wordmark_stacked_dark_gray.png
│       │   ├── Journalism_Atlas_wordmark_stacked_gray.png
│       │   ├── Journalism_Atlas_wordmark_stacked_green_white.png
│       │   ├── Journalism_Atlas_wordmark_stacked_green_white (3).png
│       │   └── Journalism_Atlas_wordmark_stacked_white.png
│       │
│       ├── advisory/                   # Advisory Board Photos
│       │   └── [Advisory board member photos]
│       │
│       ├── partners/                   # Partner Logos
│       │   └── [Partner organization logos]
│       │
│       └── IMG_9565.JPG                # Other image asset
│
├── 📦 ARCHIVE/ - Old & Backup Files
│   │
│   ├── old-backups/                   # Previous Versions
│   │   ├── index_feb_6_backup.html     # Feb 6 backup
│   │   └── index_feb_7_firstworkingtreemap.html  # Feb 7 version
│   │
│   └── old-files/                     # Deprecated Files
│       ├── files/                      # Old files folder
│       ├── convert_data.py             # Data conversion script
│       ├── csv_to_json.py              # CSV converter
│       ├── files.zip                   # Archived files
│       ├── FILE_MANIFEST.txt           # Old manifest
│       └── *.md                        # Old documentation files
│           ├── 5_Day_Launch_Sprint_Timeline.md
│           ├── CHANGES_VISUAL_GUIDE.md
│           ├── CLAUDE-CODE-PROMPT.md
│           ├── DEPLOYMENT_CHECKLIST.md
│           ├── DEPLOYMENT_SUMMARY.md
│           ├── PROJECT_STATUS_AND_NEXT_STEPS.md
│           ├── QA_Checklist.csv
│           ├── QUICK_START.md
│           └── README_START_HERE.md
│
├── 📄 ROOT DOCUMENTATION
│   ├── README.md                       # Main documentation (this file)
│   └── DIRECTORY_STRUCTURE.md          # This file
│
└── ⚙️  CONFIGURATION
    └── .claude/                        # Claude Code settings
        └── settings.local.json

```

## 🗂️ File Categories

### Production Files (Deployed)
✅ All HTML files in root
✅ `/mobile/` directory
✅ `/assets/` directory (excluding old data files)

### Development Files (Not Deployed)
❌ `/archive/` directory
❌ `.claude/` directory
❌ Python scripts
❌ Old backups

## 📍 URL Mapping

| URL Path | File Location | Description |
|----------|---------------|-------------|
| `/` | `index.html` | Main desktop app |
| `/mobile/` | `mobile/index.html` | Mobile experience |
| `/who-we-are.html` | `who-we-are.html` | About page |
| `/what-we-do.html` | `what-we-do.html` | Services page |
| `/how-we-did-this.html` | `how-we-did-this.html` | Methodology |
| `/research.html` | `research.html` | Research page |
| `/advisory.html` | `advisory.html` | Advisory board |
| `/contact.html` | `contact.html` | Contact form |
| `/contact-thanks.html` | `contact-thanks.html` | Thank you page |

## 🎯 Asset References

### Desktop HTML Files Reference:
```html
<!-- Favicon -->
<link rel="icon" href="assets/images/icons/Journalism_Atlas_favicon.png">

<!-- Logo in Nav -->
<img src="assets/images/logos/Journalism_Atlas_wordmark_lockup_white.png">

<!-- Hero Logo -->
<img src="assets/images/logos/Journalism_Atlas_wordmark_stacked_green_white (3).png">

<!-- Data -->
<script>fetch('assets/data/creators-data.json')</script>
```

### Mobile HTML References:
```html
<!-- Relative paths from /mobile/ -->
<link rel="stylesheet" href="css/mobile.css">
<script src="js/mobile-main.js"></script>
<script>fetch('data/creators-data.json')</script>
```

## 📦 Deployment Structure

When deployed to Cloudflare Pages:

```
yoursite.com/
├── index.html              ← Root loads desktop
├── mobile/                 ← /mobile/ loads mobile app
│   └── index.html
├── assets/                 ← Static assets
│   ├── css/
│   ├── js/
│   ├── data/
│   └── images/
└── [other HTML pages]
```

## 🚫 .gitignore Recommendations

Add these to `.gitignore`:

```
# Archives
archive/

# System files
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/

# Temp files
*.log
*.tmp

# Keep .claude for settings
!.claude/
```

## 📊 File Size Overview

### Large Files (> 100KB)
- `assets/data/creators-data.json` (~262KB)
- `assets/images/IMG_9565.JPG` (~2MB)
- Logo PNGs (varies, 20-140KB each)

### Total Project Size
- **Production files**: ~4MB
- **Archive files**: ~1MB
- **Total**: ~5MB

## 🔄 Update Workflow

### Adding New Creator Data
1. Edit `assets/data/creators-data.json`
2. Test on desktop (`/`)
3. Copy to `mobile/data/creators-data.json`
4. Test mobile (`/mobile/`)
5. Commit and deploy

### Adding New Images
1. Place in appropriate `assets/images/` subdirectory
2. Reference with `assets/images/[category]/filename.png`
3. Update HTML if needed
4. Commit and deploy

### Updating Pages
1. Edit HTML file in root
2. Test locally
3. Commit and deploy

## 🎨 Image Organization Logic

### Icons (`assets/images/icons/`)
- Favicons (16x16, 32x32, etc.)
- App icons
- Small UI elements

### Logos (`assets/images/logos/`)
- Wordmarks (horizontal layout)
- Stacked logos (vertical layout)
- Color variations (black, white, green, gray)
- Different backgrounds (transparent, black, white)

### Advisory (`assets/images/advisory/`)
- Advisory board member photos
- Headshots and portraits

### Partners (`assets/images/partners/`)
- Partner organization logos
- Sponsor logos

## ✅ Organization Benefits

1. **Clear Separation** - Desktop vs Mobile vs Assets
2. **Easy Deployment** - Clean production structure
3. **Simple Updates** - Know where everything goes
4. **Better Caching** - Assets in dedicated folders
5. **Version Control** - Archive old versions safely
6. **Team Collaboration** - Obvious structure for contributors

## 🔍 Quick Find Guide

**Need to update...**
- Desktop app? → `index.html`
- Mobile app? → `mobile/`
- Creator data? → `assets/data/creators-data.json`
- Logos? → `assets/images/logos/`
- About pages? → `who-we-are.html`, `what-we-do.html`, etc.

**Looking for...**
- Old versions? → `archive/old-backups/`
- Deprecated files? → `archive/old-files/`
- Documentation? → `README.md`, `mobile/README.md`
- Mobile docs? → `mobile/*.md`

---

**Last Updated**: February 16, 2026
**Structure Version**: 1.0.0
