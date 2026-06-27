# Offmenu.design Website Scraping

## What Was Done

The website https://www.offmenu.design has been successfully scraped and mirrored using `wget`. The complete site including all HTML, CSS, JavaScript, images, and other assets has been downloaded to the `www.offmenu.design/` directory.

## Files Created

1. **www.offmenu.design/** - Complete mirrored website using wget
2. **scrape_offmenu.py** - Python script for scraping (alternative method)
3. **scraped_offmenu/** - Directory for alternative scraping attempts

## How the Scraping Was Done

### Method 1: wget (Used for actual scraping)
```bash
wget \
  --recursive \
  --no-clobber \
  --page-requisites \
  --html-extension \
  --convert-links \
  --restrict-file-names=windows \
  --domains www.offmenu.design \
  --no-parent \
  https://www.offmenu.design/
```

This command:
- Downloads the entire website recursively
- Gets all necessary assets (CSS, JS, images, fonts)
- Converts links for offline viewing
- Stays within the offmenu.design domain
- Doesn't go up to parent directories

### Method 2: Python Script
The included Python script provides two approaches:
1. Using wget (same as above)
2. Using requests + BeautifulSoup for selective scraping

## To Re-run or Modify

### Using wget directly:
```bash
wget --recursive --no-clobber --page-requisites --html-extension --convert-links --restrict-file-names=windows --domains www.offmenu.design --no-parent https://www.offmenu.design/
```

### Using the Python script:
```bash
python3 scrape_offmenu.py
```

## Site Structure

The downloaded site maintains the original structure:
- HTML files in root directory
- Assets in `_next/`, `images/`, `fonts/`, `logos/` directories
- All links converted to work offline

## Notes

- The scraping was performed on 2026-06-26
- All assets appear to have been downloaded successfully
- The site can be viewed locally by opening `www.offmenu.design/index.html` in a browser
- For dynamic content (React/Next.js), the static export provides the pre-rendered HTML which is what was captured

