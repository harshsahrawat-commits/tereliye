# Offmenu.design Website Scraping Summary

## ✅ Scraping Completed Successfully

The website https://www.offmenu.design has been completely scraped and mirrored for offline access.

### 📁 What Was Downloaded

Using `wget` with recursive mirroring, we captured:

- **Total Size**: 85 MB
- **Total Files**: 265 files
- **Complete Site Structure**: All HTML, CSS, JavaScript, images, fonts, and assets

### 📂 Directory Structure

```
www.offmenu.design/
├── index.html                 # Main homepage
├── approach.html              # Approach page
├── blog.html                  # Blog listing
├── pricing.html               # Pricing page
├── services.html              # Services page
├── terms.html                 # Terms and conditions
├── work/                      # All work/project pages
│   ├── closetnow.html
│   ├── controltower.html
│   ├── ditto.html
│   ├── flex.html
│   ├── hanover-park.html
│   ├── resonant.html
│   ├── super.html
│   └── ... (all project pages)
├── blog/                      # All blog posts
│   ├── design-an-agent-harness.html
│   ├── hanover-park-raises-27m.html
│   └── your-agent-forgets-who-it-is-every-session-mine-doesn-t.html
├── _next/                     # Next.js assets
│   ├── static/
│   │   ├── chunks/            # JavaScript and CSS bundles
│   │   │   ├── *.js           # JavaScript chunks
│   │   │   ├── *.css          # CSS stylesheets
│   │   └── ...                # Other static assets
│   └── ...                    # Build manifests, etc.
├── images/                    # All images (work projects, thumbnails, etc.)
│   ├── work/
│   │   ├── closetnow/
│   │   ├── flex/
│   │   ├── super/
│   │   ├── tenacity/
│   │   └── utility/
│   └── ...                    # Other images (logos, icons, etc.)
├├── fonts/                    # Font files
├── logos/                     # Logo SVGs
├── favicon-*                  # Favicons
├── manifest.webmanifest       # Web manifest
└── robots.txt                 # Robots file
```

### 🔧 How to View the Scraped Site

#### Option 1: Direct File Access
```bash
open www.offmenu.design/index.html
```

#### Option 2: Local HTTP Server
```bash
cd www.offmenu.design
python3 -m http.server 8080
# Then visit: http://localhost:8080
```

### 🛠️ Included Tools & Scripts

1. **wget Command Used** (for reference):
   ```bash
   wget --recursive --no-clobber --page-requisites --html-extension --convert-links --restrict-file-names=windows --domains www.offmenu.design --no-parent https://www.offmenu.design/
   ```

2. **Python Scraping Script** (`scrape_offmenu.py`):
   - Alternative scraping method using requests + BeautifulSoup
   - Can selectively scrape HTML, CSS, JS, images
   - Well-documented and reusable

3. **Playwright Scraping Script** (`scrape_with_playwright.py`):
   - Modern browser-based scraping
   - Executes JavaScript and captures dynamically loaded content
   - Handles single-page applications (SPAs) like Next.js sites
   - Ready to run (requires playwright installation)

### 📊 Verification

The scrape captured:
- ✅ All HTML pages (home, work, blog, static pages)
- ✅ All JavaScript bundles (Next.js chunks)
- ✅ All CSS stylesheets
- ✅ All images (work projects, thumbnails, logos, icons)
- ✅ All font files
- ✅ Meta files (manifest, robots.txt, favicons)
- ✅ Internal links converted for offline viewing

### 💡 Notes

1. **Next.js Specifics**: The site appears to be built with Next.js, which explains the `_next/` directory structure containing compiled JS/CSS chunks.

2. **Offline Viewing**: All links have been converted to relative paths for proper offline functionality.

3. **Dynamic Content**: As this is a static export of a Next.js site, all content that was server-rendered at build time is captured. Client-only data fetching would require additional scraping with authentication/session handling.

4. **To Re-scrape**: You can re-run the wget command above or use the provided Python scripts.

### 📄 Related Files

- `www.offmenu.design/` - The complete scraped website
- `scrape_offmenu.py` - Python-based scraper (requests + BeautifulSoup)
- `scrape_with_playwright.py` - Browser-based scraper (Playwright)
- `README_SCRAPING.md` - Detailed methodology
- `SCRAPING_SUMMARY.md` - This summary

---

**Scraped**: 2026-06-26 19:30:03  
**Source**: https://www.offmenu.design/?trk=public_post_main-feed-card-text  
**Method**: wget recursive mirror with asset downloading
