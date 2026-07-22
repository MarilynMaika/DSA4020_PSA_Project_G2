
"""
================================================================================
KENYA PSA CRAWLER - Hybrid Scraping Pipeline
================================================================================
A comprehensive web scraping framework for collecting Public Service Announcements
from Kenyan government, NGO, media, and social media sources.

Tools: Python, pandas, BeautifulSoup, Selenium, requests, langdetect, fasttext
================================================================================
"""

import requests
import pandas as pd
import json
import time
import hashlib
import re
from datetime import datetime
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

# Language detection
from langdetect import detect, DetectorFactory
DetectorFactory.seed = 0  # Reproducible

# Optional: fasttext for better language detection
# import fasttext
# lang_model = fasttext.load_model('lid.176.bin')

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('psa_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class PSAConfig:
    """Configuration for the PSA Crawler"""

    # Rate limiting (seconds between requests)
    RATE_LIMITS = {
        'gov_website': 10,
        'ngo_website': 5,
        'media': 3,
        'social_media': 1  # API-based, handled by API limits
    }

    # Request headers to identify crawler ethically
    HEADERS = {
        'User-Agent': 'KenyaPSACrawler/1.0 (Research Project; Contact: researcher@university.edu)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    }

    # PSA relevance keywords (English)
    PSA_KEYWORDS_EN = [
        'alert', 'warning', 'advisory', 'notice', 'announcement', 'reminder',
        'urgent', 'caution', 'beware', 'avoid', 'do not', 'must', 'should',
        'required', 'mandatory', 'prohibited', 'banned', 'suspended',
        'evacuate', 'shelter', 'prepare', 'precaution', 'measures',
        'advised', 'urged', 'reminded', 'instructed', 'directed',
        'flood', 'drought', 'disease', 'outbreak', 'vaccination',
        'register', 'verify', 'deadline', 'extension', 'closure',
        'curfew', 'lockdown', 'restriction', 'ban', 'safety'
    ]

    # PSA relevance keywords (Kiswahili)
    PSA_KEYWORDS_SW = [
        'onyo', 'tahadhari', 'ilani', 'tangazo', 'kumbusho',
        'haraka', 'epuka', 'usifanye', 'lazima', 'sharti',
        'katazwa', 'kusitishwa', 'hama', 'jihadhari', 'hatua',
        'shauri', 'onyeshwa', 'amri', 'mafuriko', 'ukame',
        'ugonjwa', 'chanjo', 'sajili', 'thibitisha', 'tarehe',
        'kufungwa', 'amri ya kutotoka', 'zuia', 'usalama'
    ]

    # Domains mapping
    DOMAINS = {
        'health': ['health', 'medical', 'disease', 'vaccine', 'hospital', 'clinic', 'sanitation'],
        'education': ['school', 'education', 'exam', 'student', 'teacher', 'university', 'college'],
        'security': ['police', 'security', 'crime', 'terror', 'bandit', 'curfew', 'safety'],
        'agriculture': ['farm', 'crop', 'livestock', 'drought', 'famine', 'food', 'harvest'],
        'governance': ['election', 'vote', 'register', 'iebc', 'tax', 'census', 'identity']
    }


class BaseScraper:
    """Base class for all scrapers with common utilities"""

    def __init__(self, source_id, source_name, source_url, domain):
        self.source_id = source_id
        self.source_name = source_name
        self.source_url = source_url
        self.domain = domain
        self.session = requests.Session()
        self.session.headers.update(PSAConfig.HEADERS)
        self.last_request_time = 0

    def _rate_limit(self, delay_seconds):
        """Respect rate limits between requests"""
        elapsed = time.time() - self.last_request_time
        if elapsed < delay_seconds:
            time.sleep(delay_seconds - elapsed)
        self.last_request_time = time.time()

    def _fetch(self, url, delay=5, retries=3):
        """Fetch URL with rate limiting and retry logic"""
        self._rate_limit(delay)
        for attempt in range(retries):
            try:
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                logger.warning(f"Attempt {attempt+1}/{retries} failed for {url}: {e}")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"Failed to fetch {url} after {retries} attempts")
                    return None
        return None

    def _clean_text(self, text):
        """Clean extracted text"""
        if not text:
            return ""
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s.,!?;:\-'"()]', '', text)
        return text.strip()

    def _detect_language(self, text):
        """Detect language of text"""
        try:
            if len(text) < 20:
                return 'unknown'
            lang = detect(text)
            return lang
        except:
            return 'unknown'

    def _is_psa_relevant(self, text):
        """Check if text is PSA-relevant using keyword matching"""
        text_lower = text.lower()
        en_score = sum(1 for kw in PSAConfig.PSA_KEYWORDS_EN if kw in text_lower)
        sw_score = sum(1 for kw in PSAConfig.PSA_KEYWORDS_SW if kw in text_lower)
        # Threshold: at least 2 keywords or clear directive patterns
        if en_score >= 2 or sw_score >= 2:
            return True
        # Check for directive patterns
        directive_patterns = [
            r'\b(urged|advised|reminded|directed|instructed|ordered)\b.*\b(to|the public|citizens|residents)\b',
            r'\b(avoid|do not|must not|should not| refrain from)\b',
            r'\b(warning|alert|caution)\b.*\b(public|residents|citizens|all)\b'
        ]
        for pattern in directive_patterns:
            if re.search(pattern, text_lower):
                return True
        return False

    def _classify_domain(self, text):
        """Classify PSA into domain category"""
        text_lower = text.lower()
        scores = {}
        for domain, keywords in PSAConfig.DOMAINS.items():
            scores[domain] = sum(1 for kw in keywords if kw in text_lower)
        if max(scores.values()) == 0:
            return 'general'
        return max(scores, key=scores.get)

    def _generate_id(self, text, source):
        """Generate unique PSA ID"""
        hash_input = f"{text[:100]}{source}{datetime.now().isoformat()}"
        return hashlib.md5(hash_input.encode()).hexdigest()[:12].upper()


class BeautifulSoupScraper(BaseScraper):
    """Scraper for static HTML websites using BeautifulSoup"""

    def __init__(self, source_id, source_name, source_url, domain, 
                 list_page_url, article_selector, title_selector, 
                 content_selector, date_selector, delay=5):
        super().__init__(source_id, source_name, source_url, domain)
        self.list_page_url = list_page_url
        self.article_selector = article_selector
        self.title_selector = title_selector
        self.content_selector = content_selector
        self.date_selector = date_selector
        self.delay = delay

    def scrape(self, max_pages=5):
        """Scrape PSA articles from website"""
        psas = []
        for page in range(1, max_pages + 1):
            url = self.list_page_url.format(page=page)
            response = self._fetch(url, delay=self.delay)
            if not response:
                continue

            soup = BeautifulSoup(response.content, 'html.parser')
            articles = soup.select(self.article_selector)

            for article in articles:
                try:
                    title_elem = article.select_one(self.title_selector)
                    content_elem = article.select_one(self.content_selector)
                    date_elem = article.select_one(self.date_selector)

                    title = self._clean_text(title_elem.get_text()) if title_elem else ""
                    content = self._clean_text(content_elem.get_text()) if content_elem else ""
                    date_str = date_elem.get_text().strip() if date_elem else datetime.now().isoformat()

                    full_text = f"{title} {content}"
                    if not self._is_psa_relevant(full_text):
                        continue
                    if len(full_text) < 30:
                        continue

                    psa = {
                        'PSA_ID': self._generate_id(full_text, self.source_id),
                        'Domain': self._classify_domain(full_text),
                        'English': full_text if self._detect_language(full_text) == 'en' else "",
                        'Kiswahili': "",
                        'Source': self.source_name,
                        'Source_ID': self.source_id,
                        'Date': date_str,
                        'URL': url,
                        'Language_Detected': self._detect_language(full_text),
                        'PSA_Score': sum(1 for kw in PSAConfig.PSA_KEYWORDS_EN if kw in full_text.lower()),
                        'Metadata': json.dumps({
                            'title': title,
                            'scraped_at': datetime.now().isoformat(),
                            'scraper_type': 'BeautifulSoup'
                        })
                    }
                    psas.append(psa)
                    logger.info(f"Found PSA: {title[:80]}...")

                except Exception as e:
                    logger.error(f"Error parsing article: {e}")
                    continue

        return psas


class SeleniumScraper(BaseScraper):
    """Scraper for JavaScript-rendered websites using Selenium"""

    def __init__(self, source_id, source_name, source_url, domain, 
                 start_url, scroll_times=3, delay=5):
        super().__init__(source_id, source_name, source_url, domain)
        self.start_url = start_url
        self.scroll_times = scroll_times
        self.delay = delay
        self.driver = None

    def _init_driver(self):
        """Initialize headless Chrome driver"""
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument(f'--user-agent={PSAConfig.HEADERS["User-Agent"]}')
        self.driver = webdriver.Chrome(options=options)

    def scrape(self):
        """Scrape dynamic content with Selenium"""
        if not self.driver:
            self._init_driver()

        psas = []
        try:
            self.driver.get(self.start_url)
            time.sleep(self.delay)

            # Scroll to load dynamic content
            for _ in range(self.scroll_times):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

            # Extract content (customize selectors per site)
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')

            # Example: Extract all paragraphs that look like PSAs
            for elem in soup.find_all(['p', 'div', 'article']):
                text = self._clean_text(elem.get_text())
                if self._is_psa_relevant(text) and len(text) > 30:
                    psa = {
                        'PSA_ID': self._generate_id(text, self.source_id),
                        'Domain': self._classify_domain(text),
                        'English': text if self._detect_language(text) == 'en' else "",
                        'Kiswahili': "",
                        'Source': self.source_name,
                        'Source_ID': self.source_id,
                        'Date': datetime.now().isoformat(),
                        'URL': self.start_url,
                        'Language_Detected': self._detect_language(text),
                        'PSA_Score': sum(1 for kw in PSAConfig.PSA_KEYWORDS_EN if kw in text.lower()),
                        'Metadata': json.dumps({
                            'scraped_at': datetime.now().isoformat(),
                            'scraper_type': 'Selenium'
                        })
                    }
                    psas.append(psa)

        except Exception as e:
            logger.error(f"Selenium scraping error: {e}")
        finally:
            if self.driver:
                self.driver.quit()

        return psas


class TwitterScraper(BaseScraper):
    """Scraper for X/Twitter using snscrape (no API key needed)"""

    def __init__(self, source_id, source_name, source_url, domain, 
                 username, max_tweets=100):
        super().__init__(source_id, source_name, source_url, domain)
        self.username = username
        self.max_tweets = max_tweets

    def scrape(self):
        """Scrape tweets using snscrape"""
        psas = []
        try:
            import snscrape.modules.twitter as sntwitter

            query = f"from:{self.username}"
            scraper = sntwitter.TwitterSearchScraper(query)

            for i, tweet in enumerate(scraper.get_items()):
                if i >= self.max_tweets:
                    break

                text = self._clean_text(tweet.rawContent)
                if not self._is_psa_relevant(text):
                    continue
                if len(text) < 20:
                    continue

                psa = {
                    'PSA_ID': self._generate_id(text, self.source_id),
                    'Domain': self._classify_domain(text),
                    'English': text if self._detect_language(text) == 'en' else "",
                    'Kiswahili': "",
                    'Source': self.source_name,
                    'Source_ID': self.source_id,
                    'Date': tweet.date.isoformat(),
                    'URL': tweet.url,
                    'Language_Detected': self._detect_language(text),
                    'PSA_Score': sum(1 for kw in PSAConfig.PSA_KEYWORDS_EN if kw in text.lower()),
                    'Metadata': json.dumps({
                        'tweet_id': str(tweet.id),
                        'likes': tweet.likeCount,
                        'retweets': tweet.retweetCount,
                        'scraped_at': datetime.now().isoformat(),
                        'scraper_type': 'snscrape'
                    })
                }
                psas.append(psa)
                logger.info(f"Found tweet PSA: {text[:80]}...")

        except ImportError:
            logger.error("snscrape not installed. Run: pip install snscrape")
        except Exception as e:
            logger.error(f"Twitter scraping error: {e}")

        return psas


# ============================================================
# PRE-CONFIGURED SCRAPER INSTANCES
# ============================================================

SCRAPER_INSTANCES = [
    # KMD Weather Warnings
    BeautifulSoupScraper(
        source_id="SRC001",
        source_name="Kenya Meteorological Department",
        source_url="https://meteo.go.ke",
        domain="Health/Disaster",
        list_page_url="https://meteo.go.ke/weather-warnings/",
        article_selector=".alert-item, .warning-item, article",
        title_selector="h2, h3, .alert-title",
        content_selector=".alert-content, .entry-content, p",
        date_selector=".date, time, .published",
        delay=5
    ),

    # IEBC News
    BeautifulSoupScraper(
        source_id="SRC002",
        source_name="IEBC Kenya",
        source_url="https://www.iebc.or.ke",
        domain="Governance",
        list_page_url="https://www.iebc.or.ke/news/",
        article_selector="article, .news-item, .post",
        title_selector="h2, h3, .entry-title",
        content_selector=".entry-content, .summary, p",
        date_selector=".date, time, .published",
        delay=10
    ),

    # NDOC
    BeautifulSoupScraper(
        source_id="SRC004",
        source_name="National Disaster Operations Centre",
        source_url="https://www.ndoc.go.ke",
        domain="Disaster/Security",
        list_page_url="https://www.ndoc.go.ke/",
        article_selector="article, .news-item, .alert",
        title_selector="h2, h3, .title",
        content_selector=".content, .summary, p",
        date_selector=".date, time",
        delay=10
    ),

    # Ministry of Education (X/Twitter)
    TwitterScraper(
        source_id="SRC005",
        source_name="Ministry of Education Kenya",
        source_url="https://x.com/EduMinKenya",
        domain="Education",
        username="EduMinKenya",
        max_tweets=200
    ),

    # Social Health Authority (X/Twitter)
    TwitterScraper(
        source_id="SRC006",
        source_name="Social Health Authority Kenya",
        source_url="https://x.com/_shakenya",
        domain="Health",
        username="_shakenya",
        max_tweets=200
    ),

    # National Police Service (X/Twitter)
    TwitterScraper(
        source_id="SRC007",
        source_name="National Police Service Kenya",
        source_url="https://x.com/NPSOfficial_KE",
        domain="Security",
        username="NPSOfficial_KE",
        max_tweets=200
    ),

    # Kenya Red Cross (X/Twitter)
    TwitterScraper(
        source_id="SRC008",
        source_name="Kenya Red Cross",
        source_url="https://x.com/kenyaredcross",
        domain="Health/Disaster",
        username="kenyaredcross",
        max_tweets=300
    ),
]


def run_all_scrapers():
    """Run all configured scrapers and collect results"""
    all_psas = []
    for scraper in SCRAPER_INSTANCES:
        logger.info(f"Starting scraper: {scraper.source_name}")
        try:
            psas = scraper.scrape()
            all_psas.extend(psas)
            logger.info(f"Scraper {scraper.source_name} found {len(psas)} PSAs")
        except Exception as e:
            logger.error(f"Scraper {scraper.source_name} failed: {e}")
    return all_psas


# ============================================================
# DATA CLEANING & VALIDATION PIPELINE
# ============================================================

class PSACleaner:
    """Clean and validate scraped PSA data"""

    def __init__(self, psas):
        self.df = pd.DataFrame(psas)

    def deduplicate(self):
        """Remove duplicate PSAs based on content similarity"""
        initial_count = len(self.df)
        # Exact duplicate removal
        self.df = self.df.drop_duplicates(subset=['English'], keep='first')
        # Fuzzy duplicate removal (simplified)
        self.df = self.df.drop_duplicates(subset=['PSA_ID'], keep='first')
        logger.info(f"Deduplication: {initial_count} -> {len(self.df)} (removed {initial_count - len(self.df)})")
        return self

    def filter_relevance(self, min_score=2):
        """Filter by PSA relevance score"""
        initial_count = len(self.df)
        self.df = self.df[self.df['PSA_Score'] >= min_score]
        logger.info(f"Relevance filter: {initial_count} -> {len(self.df)}")
        return self

    def validate_language(self):
        """Validate language detection and flag uncertain cases"""
        self.df['Language_Validated'] = self.df['Language_Detected'].apply(
            lambda x: x in ['en', 'sw', 'so', 'unknown']
        )
        return self

    def add_kiswahili_placeholders(self):
        """Add placeholder columns for target languages"""
        self.df['Kiswahili'] = ""  # To be filled by translation/NMT
        self.df['Target_Languages'] = json.dumps({
            'Kiswahili': 'placeholder',
            'Somali': 'placeholder',
            'Kikuyu': 'placeholder',
            'Luo': 'placeholder',
            'Kalenjin': 'placeholder'
        })
        return self

    def get_clean_data(self):
        return self.df


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    # Run scrapers
    raw_psas = run_all_scrapers()
    logger.info(f"Total raw PSAs collected: {len(raw_psas)}")

    # Clean and validate
    cleaner = PSACleaner(raw_psas)
    cleaner.deduplicate().filter_relevance().validate_language().add_kiswahili_placeholders()

    clean_df = cleaner.get_clean_data()

    # Save outputs
    clean_df.to_csv('kenya_psa_dataset.csv', index=False)
    clean_df.to_json('kenya_psa_dataset.json', orient='records', indent=2)

    logger.info(f"Final dataset saved: {len(clean_df)} PSAs")
    logger.info(f"Domain distribution: {clean_df['Domain'].value_counts().to_dict()}")
