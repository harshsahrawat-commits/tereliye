#!/usr/bin/env python3
"""
Script to scrape the offmenu.design website
"""

import requests
from bs4 import BeautifulSoup
import os
import urllib.parse
from urllib.parse import urljoin, urlparse
import time

def download_website(base_url, output_dir="scraped_site"):
    """
    Download a website using wget for comprehensive scraping
    """
    import subprocess
    
    print(f"Downloading website from {base_url}")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Use wget to mirror the site
    cmd = [
        "wget",
        "--recursive",
        "--no-clobber",
        "--page-requisites",
        "--html-extension",
        "--convert-links",
        "--restrict-file-names=windows",
        "--domains", urlparse(base_url).netloc,
        "--no-parent",
        base_url
    ]
    
    try:
        subprocess.run(cmd, cwd=output_dir, check=True)
        print(f"Website downloaded to {output_dir}/")
    except subprocess.CalledProcessError as e:
        print(f"Error downloading website: {e}")
        return False
    
    return True

def scrape_with_python(base_url, output_dir="scraped_python"):
    """
    Scrape website using Python requests and BeautifulSoup
    Good for extracting specific data or metadata
    """
    print(f"Scraping {base_url} with Python...")
    
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Get the main page
        response = requests.get(base_url, timeout=10)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Save the main page
        with open(os.path.join(output_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        
        # Extract and save CSS
        css_links = soup.find_all('link', rel='stylesheet')
        css_dir = os.path.join(output_dir, 'css')
        os.makedirs(css_dir, exist_ok=True)
        
        for i, link in enumerate(css_links):
            href = link.get('href')
            if href:
                css_url = urljoin(base_url, href)
                try:
                    css_response = requests.get(css_url, timeout=10)
                    css_response.raise_for_status()
                    css_filename = f"style_{i}.css"
                    with open(os.path.join(css_dir, css_filename), 'w', encoding='utf-8') as f:
                        f.write(css_response.text)
                except Exception as e:
                    print(f"Could not download CSS {css_url}: {e}")
        
        # Extract and save JavaScript
        js_scripts = soup.find_all('script', src=True)
        js_dir = os.path.join(output_dir, 'js')
        os.makedirs(js_dir, exist_ok=True)
        
        for i, script in enumerate(js_scripts):
            src = script.get('src')
            if src:
                js_url = urljoin(base_url, src)
                try:
                    js_response = requests.get(js_url, timeout=10)
                    js_response.raise_for_status()
                    js_filename = f"script_{i}.js"
                    with open(os.path.join(js_dir, js_filename), 'w', encoding='utf-8') as f:
                        f.write(js_response.text)
                except Exception as e:
                    print(f"Could not download JS {js_url}: {e}")
        
        # Extract images
        img_tags = soup.find_all('img')
        img_dir = os.path.join(output_dir, 'images')
        os.makedirs(img_dir, exist_ok=True)
        
        for i, img in enumerate(img_tags):
            src = img.get('src')
            if src:
                img_url = urljoin(base_url, src)
                try:
                    img_response = requests.get(img_url, timeout=10)
                    img_response.raise_for_status()
                    # Try to get filename from URL or generate one
                    parsed = urlparse(img_url)
                    filename = os.path.basename(parsed.path)
                    if not filename:
                        filename = f"image_{i}.jpg"
                    with open(os.path.join(img_dir, filename), 'wb') as f:
                        f.write(img_response.content)
                except Exception as e:
                    print(f"Could not download image {img_url}: {e}")
        
        print(f"Python scraping completed. Files saved to {output_dir}/")
        return True
        
    except Exception as e:
        print(f"Error during scraping: {e}")
        return False

if __name__ == "__main__":
    URL = "https://www.offmenu.design"
    
    print("Choose scraping method:")
    print("1. wget (comprehensive site mirror)")
    print("2. Python requests + BeautifulSoup (selective scraping)")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        download_website(URL)
    elif choice == "2":
        scrape_with_python(URL)
    else:
        print("Invalid choice. Running wget method by default.")
        download_website(URL)
