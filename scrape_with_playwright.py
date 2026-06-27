import asyncio
import os
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

async def download_resource(page, url, base_dir, visited):
    """Download a resource and save it to base_dir, returning the local path."""
    if url in visited:
        return None
    visited.add(url)

    # Parse the URL
    parsed = urlparse(url)
    # Remove query and fragment for file path
    path = parsed.path
    if not path or path.endswith('/'):
        path = path + 'index.html'
    elif not os.path.splitext(path)[1]:
        # If no extension, treat as HTML
        path = path + '.html'

    # Build the local file path
    netloc = parsed.netloc.replace(':', '_')  # Replace colon to avoid issues on Windows
    local_path = os.path.join(base_dir, netloc, path.lstrip('/'))
    # Ensure the directory exists
    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    # Skip if already downloaded
    if os.path.exists(local_path):
        return local_path

    try:
        # Use the page's request context to fetch the resource
        response = await page.request.fetch(url)
        if not response.ok:
            print(f"Failed to download {url}: {response.status}")
            return None

        # Get the response body
        body = await response.body()

        # Write the file
        with open(local_path, 'wb') as f:
            f.write(body)

        print(f"Downloaded: {url} -> {local_path}")
        return local_path
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return None

async def main():
    # The URL to scrape
    url = "https://www.offmenu.design/?trk=public_post_main-feed-card-text"
    # Base directory for saving the site
    base_dir = "offmenu_design_playwright"
    os.makedirs(base_dir, exist_ok=True)

    async with async_playwright() as p:
        # Launch browser (we'll use Chromium)
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'
        )
        page = await context.new_page()

        # Go to the page
        print(f"Navigating to {url}")
        await page.goto(url, wait_until="networkidle", timeout=60000)

        # Wait for the main content to appear
        # We'll wait for the text "Let's work together" to appear in the viewport
        try:
            await page.wait_for_function("() => document.body.innerText.includes(\"Let's work together\")", timeout=10000)
            print("Main content detected.")
        except Exception as e:
            print(f"Waiting for content timed out: {e}")
            # Continue anyway, we'll get the current content

        # Get the page content after JavaScript execution
        html = await page.content()

        # Parse the HTML
        soup = BeautifulSoup(html, 'html.parser')

        # Set to track visited URLs to avoid duplicates
        visited = set()

        # Find all tags with URLs
        tags_attrs = [
            ('link', 'href'),
            ('script', 'src'),
            ('img', 'src'),
            ('source', 'src'),
            ('video', 'src'),
            ('audio', 'src'),
            ('iframe', 'src'),
            ('embed', 'src'),
            ('object', 'data'),
        ]

        for tag, attr in tags_attrs:
            for element in soup.find_all(tag):
                link = element.get(attr)
                if link:
                    # Make absolute URL
                    absolute_url = urljoin(url, link)
                    # Only download from the same domain to avoid crawling the entire web
                    if urlparse(absolute_url).netloc == urlparse(url).netloc:
                        local_path = await download_resource(page, absolute_url, base_dir, visited)
                        if local_path:
                            # Update the attribute to be relative to the base_dir
                            # We want the path to be relative to the HTML file's location.
                            # Since we are saving the HTML in the base_dir, we can make the path relative to base_dir.
                            # Compute the relative path from the base_dir to the local_path.
                            rel_path = os.path.relpath(local_path, base_dir)
                            # Convert to forward slashes for web
                            rel_path = rel_path.replace(os.sep, '/')
                            element[attr] = rel_path
                        else:
                            # If download failed, we leave the original attribute (which might break the page)
                            pass

        # Save the modified HTML
        html_file = os.path.join(base_dir, "index.html")
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f"Saved HTML to {html_file}")

        # Close the browser
        await browser.close()

    print("Done!")

if __name__ == "__main__":
    asyncio.run(main())
