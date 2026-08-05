# !pip install beautifulsoup4 langdetect requests ftfy openai -q

import os
import re
import csv
import time
import urllib.robotparser as robotparser
import urllib3
from datetime import datetime
from urllib.parse import urljoin, urlparse

import pandas as pd
import requests
import ftfy
from bs4 import BeautifulSoup
from langdetect import detect, LangDetectException
from openai import OpenAI

REQUEST_DELAY = 2
_ssl_warning_shown = False
client = OpenAI(api_key="YOUR_OPENAI_API_KEY_HERE")

SOURCES = [
    {"name": "Kenya News Agency - Security", "url": "https://www.kenyanews.go.ke/category/natsec/", "max_pages": 20},
    {"name": "NPSC News", "url": "https://www.npsc.go.ke/news/", "max_pages": 10},
    {"name": "ReliefWeb Kenya", "url": "https://reliefweb.int/country/ken", "max_pages": 15},
]

NAV_NOISE = {
    "home", "about us", "news", "contact us", "view more", "read on", "resources",
    "tenders", "vacancies", "projects", "you must be logged in to post a comment",
    "skip to main content", "skip to content", "leave a comment", "faqs",
}

NAV_PATTERNS = [
    r"\| Home$", r"^Kenya Skip to main content", r"please message us",
    r"^Disclaimer -", r"Skip to (main )?content", r"^Frequently Asked Questions",
    r"^You must be logged in", r"^Read on",
]


def robots_allowed(url: str) -> bool:
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    rp = robotparser.RobotFileParser()
    try:
        rp.set_url(robots_url)
        rp.read()
        return rp.can_fetch(HEADERS["User-Agent"], url)
    except Exception:
        return False


def fetch(url: str, max_retries: int = 3):
    if not robots_allowed(url):
        print(f"Skipping (robots.txt disallows): {url}")
        return None
    for attempt in range(1, max_retries + 1):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=(10, 30))
            resp.raise_for_status()
            time.sleep(REQUEST_DELAY)
            return resp.text
        except requests.exceptions.SSLError:
            global _ssl_warning_shown
            if not _ssl_warning_shown:
                print(f"Note: {urlparse(url).netloc} has certificate issues — continuing without SSL verification.")
                _ssl_warning_shown = True
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            try:
                resp = requests.get(url, headers=HEADERS, timeout=(10, 30), verify=False)
                resp.raise_for_status()
                time.sleep(REQUEST_DELAY)
                return resp.text
            except requests.exceptions.RequestException as e:
                print(f"  [retry {attempt}/{max_retries}] SSL fallback failed for {url}: {e}")
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            print(f"  [retry {attempt}/{max_retries}] {type(e).__name__} for {url}")
            if attempt < max_retries:
                time.sleep(REQUEST_DELAY * attempt * 2)
                continue
        except requests.exceptions.RequestException as e:
            print(f"  Failed permanently for {url}: {e}")
            return None
    print(f"  Giving up on {url} after {max_retries} attempts")
    return None


def is_english(text: str) -> bool:
    try:
        return detect(text) == "en"
    except LangDetectException:
        return False


def get_listing_items(listing_url: str, max_pages: int = 1):
    items, seen_urls = [], set()
    for page in range(1, max_pages + 1):
        page_url = listing_url if page == 1 else urljoin(listing_url, f"page/{page}/")
        html = fetch(page_url)
        if not html:
            break
        soup = BeautifulSoup(html, "html.parser")
        found_this_page = False
        for a in soup.find_all("a", href=True):
            title = a.get_text(strip=True)
            href = urljoin(page_url, a["href"])
            if len(title) < 15 or title.lower() in NAV_NOISE:
                continue
            if urlparse(href).netloc != urlparse(listing_url).netloc:
                continue
            if href in seen_urls:
                continue
            seen_urls.add(href)
            items.append({"title": title, "url": href})
            found_this_page = True
        if not found_this_page:
            break
    return items


def get_article_body(article_url: str) -> str:
    html = fetch(article_url)
    if not html:
        return ""
    soup = BeautifulSoup(html, "html.parser")
    paragraphs = soup.select("article p, .entry-content p, .post-content p, main p")
    seen, unique_paras = set(), []
    for p in paragraphs:
        text = p.get_text(strip=True)
        if text and text not in seen:
            seen.add(text)
            unique_paras.append(text)
    return " ".join(unique_paras)


def clean_text(text):
    if not isinstance(text, str):
        return text
    text = ftfy.fix_text(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def scrape_source(listing_url: str, source_name: str, max_pages: int, running_rows: list):
    listing_items = get_listing_items(listing_url, max_pages=max_pages)
    print(f"  {source_name}: {len(listing_items)} article links found")

    kept, skipped_short, skipped_lang, skipped_nav = 0, 0, 0, 0
    for item in listing_items:
        title = clean_text(item["title"])
        if re.search("|".join(NAV_PATTERNS), title, re.IGNORECASE):
            skipped_nav += 1
            continue

        body = clean_text(get_article_body(item["url"]))
        text = f"{title}. {body}".strip()
        if len(text) < 60:
            skipped_short += 1
            continue
        if not is_english(text):
            skipped_lang += 1
            continue

        running_rows.append({
            "Domain": "Security & Safety",
            "Class": "PSA",
            "English": text,
            "Kiswahili": "", "Ekegusii": "", "Dholuo": "", "Somali": "",
            "Source": item["url"],
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Metadata": f"scraped:{source_name}",
        })
        kept += 1

        if kept % 25 == 0:
            pd.DataFrame(running_rows).to_csv("security_scrape_checkpoint.csv", index=False, encoding="utf-8-sig")
            print(f"    [checkpoint] {len(running_rows)} total rows so far")

    print(f"  {source_name}: kept {kept} (dropped {skipped_nav} nav, {skipped_short} too-short, {skipped_lang} non-English)")


all_rows = []
for src in SOURCES:
    print(f"Scraping {src['name']} -> {src['url']}")
    scrape_source(src["url"], src["name"], src["max_pages"], all_rows)

df_new = pd.DataFrame(all_rows)
print(f"\nNewly scraped: {len(df_new)} rows")