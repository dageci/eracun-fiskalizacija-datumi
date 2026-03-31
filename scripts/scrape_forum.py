#!/usr/bin/env python3
"""
Scraper for forum.hr thread "Fiskalizacija za developere"
Thread: https://www.forum.hr/showthread.php?t=1040421
Pages 100-232 (27.11.2025 - 31.03.2026)

Extracts all posts with: post_id, post_number, author, date, content (text), quotes
Saves as JSON for later analysis.
"""

import re
import json
import time
import sys
import os
import urllib.request
from html.parser import HTMLParser
from html import unescape

BASE_URL = "https://www.forum.hr/showthread.php?t=1040421&page={}"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "hr,en;q=0.5",
}
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "forum_data")


def fetch_page(page_num, max_retries=3):
    """Fetch a single forum page with retries."""
    url = BASE_URL.format(page_num)
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=30) as resp:
                # Page is windows-1250 encoded
                raw = resp.read()
                return raw.decode("windows-1250", errors="replace")
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 * (attempt + 1))
            else:
                print(f"  FAILED page {page_num}: {e}", file=sys.stderr)
                return None


def strip_html(html_text):
    """Remove HTML tags and decode entities, preserving line breaks."""
    if not html_text:
        return ""
    # Convert <br> and <br/> to newlines
    text = re.sub(r'<br\s*/?>', '\n', html_text, flags=re.IGNORECASE)
    # Convert </p>, </div>, </li> to newlines
    text = re.sub(r'</(?:p|div|li|tr)>', '\n', text, flags=re.IGNORECASE)
    # Remove all remaining HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Decode HTML entities
    text = unescape(text)
    # Clean up whitespace
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    return text.strip()


def extract_posts(html):
    """Extract all posts from a page's HTML."""
    posts = []

    # Pattern for each post block
    # Post table starts with: <table id="post{ID}" class="tborder"
    post_pattern = re.compile(
        r'<table\s+id="post(\d+)"\s+class="tborder".*?'
        r'<!-- status icon and date -->.*?'
        r'<a\s+name="post\1">.*?</a>\s*'
        r'([\d.]+,\s*[\d:]+)\s*'          # date
        r'.*?postcount\1.*?name="(\d+)".*?<strong>\3</strong>'  # post number
        r'.*?class="bigusername"[^>]*>([^<]+)</a>'  # author
        r'.*?<div\s+id="post_message_\1">(.*?)</div>\s*'
        r'(?:<!-- / message -->|$)',
        re.DOTALL
    )

    for m in post_pattern.finditer(html):
        post_id = m.group(1)
        date_str = m.group(2).strip()
        post_num = m.group(3)
        author = m.group(4).strip()
        raw_content = m.group(5)

        # Extract quoted text separately
        quotes = []
        quote_pattern = re.compile(
            r'<div[^>]*>\s*<strong>([^<]*)</strong>\s*ka[^:]*:\s*'
            r'(?:<a[^>]*>.*?</a>\s*)?'
            r'</div>\s*<div[^>]*>(.*?)</div>',
            re.DOTALL
        )
        for qm in quote_pattern.finditer(raw_content):
            quotes.append({
                "author": strip_html(qm.group(1)),
                "text": strip_html(qm.group(2))
            })

        # Get clean text content
        content = strip_html(raw_content)

        # Build post URL
        post_url = f"https://www.forum.hr/showpost.php?p={post_id}&postcount={post_num}"

        posts.append({
            "post_id": post_id,
            "post_number": int(post_num),
            "author": author,
            "date": date_str,
            "content": content,
            "quotes": quotes,
            "url": post_url,
        })

    return posts


def parse_page_simple(html):
    """Simpler extraction using split-based approach as fallback."""
    posts = []

    # Split by post tables
    chunks = re.split(r'<table\s+id="post(\d+)"\s+class="tborder"', html)

    for i in range(1, len(chunks), 2):
        post_id = chunks[i]
        block = chunks[i + 1] if i + 1 < len(chunks) else ""

        # Date - format: DD.MM.YYYY., HH:MM (after the <img> + </a>, with \r\n whitespace)
        date_m = re.search(
            r'name="post' + post_id + r'">.*?</a>\s*(\d{2}\.\d{2}\.\d{4}\.,\s*\d{2}:\d{2})',
            block, re.DOTALL
        )
        if not date_m:
            # Try relative dates (Danas, Jucer)
            date_m = re.search(
                r'name="post' + post_id + r'">.*?</a>\s*((?:Danas|Ju.er),\s*\d{2}:\d{2})',
                block, re.DOTALL
            )
        date_str = date_m.group(1).strip() if date_m else "unknown"

        # Post number
        num_m = re.search(
            r'postcount' + post_id + r'.*?name="(\d+)"',
            block, re.DOTALL
        )
        post_num = int(num_m.group(1)) if num_m else 0

        # Author
        auth_m = re.search(r'class="bigusername"[^>]*>([^<]+)</a>', block)
        author = auth_m.group(1).strip() if auth_m else "unknown"
        # Skip ads
        if author == "Oglas":
            continue

        # Content - everything in post_message div
        content_m = re.search(
            r'<div\s+id="post_message_' + post_id + r'">(.*?)(?:</div>\s*<!-- / message -->)',
            block, re.DOTALL
        )
        raw_content = content_m.group(1) if content_m else ""

        # Extract quotes
        quotes = []
        for qm in re.finditer(
            r'<strong>([^<]*)</strong>\s*ka[^:]*:.*?<div\s+style="font-style:italic">(.*?)</div>',
            raw_content, re.DOTALL
        ):
            quotes.append({
                "author": strip_html(qm.group(1)),
                "text": strip_html(qm.group(2))
            })

        content = strip_html(raw_content)
        post_url = f"https://www.forum.hr/showpost.php?p={post_id}&postcount={post_num}"

        if content.strip():
            posts.append({
                "post_id": post_id,
                "post_number": post_num,
                "author": author,
                "date": date_str,
                "content": content,
                "quotes": quotes,
                "url": post_url,
            })

    return posts


def scrape_range(start_page, end_page, output_file=None):
    """Scrape a range of pages and save results."""
    all_posts = []

    for page in range(start_page, end_page + 1):
        print(f"  Fetching page {page}...", end=" ", flush=True)
        html = fetch_page(page)
        if not html:
            print("SKIP")
            continue

        posts = parse_page_simple(html)
        print(f"{len(posts)} posts")
        all_posts.extend(posts)

        # Be polite - don't hammer the server
        if page < end_page:
            time.sleep(0.5)

    if output_file:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(all_posts, f, ensure_ascii=False, indent=2)
        print(f"\nSaved {len(all_posts)} posts to {output_file}")

    return all_posts


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        start = int(sys.argv[1])
        end = int(sys.argv[2])
        batch_name = f"batch_{start}_{end}"
    else:
        start = 100
        end = 232
        batch_name = "all"

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_file = os.path.join(OUTPUT_DIR, f"posts_{batch_name}.json")

    print(f"Scraping pages {start}-{end}...")
    posts = scrape_range(start, end, out_file)
    print(f"\nTotal: {len(posts)} posts from pages {start}-{end}")
