import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from playwright.async_api import async_playwright
import asyncio

async def get_rendered_html(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        )
        page = await context.new_page()
        await page.goto(url, wait_until="networkidle", timeout=60000)
        try:
            await page.wait_for_function(
                "() => document.body.innerText.includes('Let's work together')",
                timeout=10000
            )
        except:
            pass
        html = await page.content()
        await browser.close()
        return html

def rewrite_html(html, base_url, base_dir):
    soup = BeautifulSoup(html, 'html.parser')
    html_file = os.path.join(base_dir, 'index.html')
    base_netloc = urlparse(base_url).netloc

    tags_attrs = [
        ('link', 'href'), ('script', 'src'), ('img', 'src'),
        ('source', 'src'), ('video', 'src'), ('audio', 'src'),
        ('iframe', 'src'), ('embed', 'src'), ('object', 'data'),
    ]

    for tag, attr in tags_attrs:
        for element in soup.find_all(tag):
            link = element.get(attr)
            if not link:
                continue
            absolute_url = urljoin(base_url, link)
            parsed = urlparse(absolute_url)
            if parsed.netloc != base_netloc:
                continue
            parsed = parsed._replace(fragment='')
            path = parsed.path
            if parsed.query:
                path = path + '?' + parsed.query
            if not path or path.endswith('/'):
                path = path + 'index.html'
            if path.startswith('/'):
                path = path[1:]
            local_path = os.path.join(base_dir, path)
            local_path = os.path.normpath(local_path)
            if os.path.exists(local_path):
                rel_path = os.path.relpath(local_path, os.path.dirname(html_file))
                rel_path = rel_path.replace(os.sep, '/')
                element[attr] = rel_path
    return str(soup)

async def main():
    url = "https://www.offmenu.design/?trk=public_post_main-feed-card-text"
    base_dir = "www.offmenu.design"
    print("Fetching rendered HTML...")
    html = await get_rendered_html(url)
    print("Rewriting HTML...")
    new_html = rewrite_html(html, url, base_dir)
    html_file = os.path.join(base_dir, "index.html")
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f"Updated {html_file}")

if __name__ == "__main__":
    asyncio.run(main())
