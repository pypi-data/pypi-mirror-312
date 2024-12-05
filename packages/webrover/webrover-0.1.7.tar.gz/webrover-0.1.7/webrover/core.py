import asyncio
import aiohttp
from bs4 import BeautifulSoup
from pathlib import Path
from typing import List, Dict, Union
import json
import yaml
import re
import time
import random
from concurrent.futures import ThreadPoolExecutor
from googlesearch import search
import logging
from .utils import clean_text, extract_content, save_json, load_json, validate_url, create_dataset_entry
from tqdm import tqdm
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class WebRover:
    def __init__(self, output_dir: str = "final_dataset"):
        """Initialize WebRover with optional output directory."""
        logger.info("🚀 Initializing WebRover...")
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        logger.info(f"📁 Output directory set to: {output_dir}")
        
        self.master_urls = {}
        self.completed_urls = {}
        self.error_urls = {}
        self.dataset = []

    def _search_google_sync(self, topic: str) -> List[str]:
        """Synchronous Google search."""
        try:
            logger.info(f"🔍 Starting Google search for topic: {topic}")
            urls = []
            for url in search(topic, num_results=self.urls_per_topic, lang="en"):
                urls.append(url)
                time.sleep(2.0)  # Be nice to Google
            logger.info(f"✨ Found {len(urls)} URLs for topic: {topic}")
            return urls
        except Exception as e:
            logger.error(f"❌ Error during search for {topic}: {e}")
            return []

    async def _search_google(self, topic: str, session: aiohttp.ClientSession) -> List[str]:
        """Asynchronous wrapper for Google search."""
        logger.info(f"🌐 Starting asynchronous search for topic: {topic}")
        with ThreadPoolExecutor() as executor:
            urls = await asyncio.get_event_loop().run_in_executor(
                executor,
                self._search_google_sync,
                topic
            )
            return urls

    async def _scrape_website(self, url: str, session: aiohttp.ClientSession) -> Dict:
        """Scrape a single website."""
        logger.info(f"🔄 Attempting to scrape: {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        
        try:
            async with session.get(url, headers=headers, timeout=30) as response:
                if response.status == 200:
                    logger.info(f"✅ Successfully retrieved content from: {url}")
                    html = await response.text()
                    content = extract_content(html)
                    entry = create_dataset_entry(url, content['title'], content['content'])
                    return entry
                else:
                    logger.warning(f"⚠️ HTTP {response.status} for URL: {url}")
                    raise Exception(f"HTTP {response.status}")
        except Exception as e:
            logger.error(f"❌ Error scraping {url}: {str(e)}")
            self.error_urls[url] = str(e)
            return None

    async def _process_urls(self):
        """Process all URLs and scrape websites."""
        logger.info("🔄 Starting URL processing...")
        async with aiohttp.ClientSession() as session:
            # First, collect URLs if master list is empty
            if not self.master_urls:
                logger.info("🌐 Collecting URLs from Google...")
                for topic in self.topics:
                    urls = await self._search_google(topic, session)
                    for url in urls:
                        if validate_url(url):
                            self.master_urls[url] = topic
                    
                    await asyncio.sleep(random.uniform(1, 3))

            # Process URLs that haven't been completed or errored
            pending_urls = [url for url in self.master_urls.keys() 
                          if url not in self.completed_urls and url not in self.error_urls]

            logger.info(f"📊 Processing {len(pending_urls)} websites...")
            
            # Create progress bar
            with tqdm(total=len(pending_urls), desc="🔄 Scraping Progress", 
                     bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]') as pbar:
                
                for i, url in enumerate(pending_urls, 1):
                    # Update progress description with current website
                    pbar.set_description(f"🔄 Scraping {i}/{len(pending_urls)}: {url[:50]}...")
                    
                    result = await self._scrape_website(url, session)
                    if result:
                        self.completed_urls[url] = result
                        self.dataset.append(result)
                        logger.info(f"✅ Successfully processed: {url}")
                    
                    # Update progress bar
                    pbar.update(1)
                    await asyncio.sleep(random.uniform(0.5, 1.5))

    def scrape_topics(self, topics: Union[str, List[str], Path], num_websites: int = 100) -> None:
        """Main method to scrape websites based on topics."""
        logger.info("🚀 Starting scraping process...")
        
        # Process topics input
        if isinstance(topics, (str, Path)) and Path(topics).exists():
            logger.info(f"📄 Loading topics from file: {topics}")
            topics_list = self._load_topics_from_file(topics)
        elif isinstance(topics, str):
            logger.info("📝 Processing comma-separated topics string")
            topics_list = [t.strip() for t in topics.split(',')]
        elif isinstance(topics, list):
            logger.info("📋 Using provided topics list")
            topics_list = topics
        else:
            logger.error("❌ Invalid topics format")
            raise ValueError("Invalid topics format")

        self.num_websites = num_websites
        self.topics = topics_list
        self.urls_per_topic = num_websites // len(self.topics)
        logger.info(f"🎯 Will scrape {self.urls_per_topic} URLs per topic")

        # Run the scraping
        asyncio.run(self._process_urls())
        logger.info("🏁 Scraping process completed")

    def save_dataset(self, filename: str = "dataset.jsonl") -> None:
        """Save the scraped dataset to a JSONL file."""
        output_file = self.output_dir / filename
        with open(output_file, 'w') as f:
            for item in self.dataset:
                f.write(json.dumps(item) + '\n')
        
        # Log the absolute path of the saved dataset
        abs_path = os.path.abspath(output_file)
        logger.info(f"💾 Dataset saved to: {abs_path}")
        
        # Log completion status with stats
        stats = self.get_stats()
        logger.info(f"📊 Final Statistics:")
        logger.info(f"   • Total URLs processed: {stats['total_urls']}")
        logger.info(f"   • Successfully scraped: {stats['completed']}")
        logger.info(f"   • Failed to scrape: {stats['errors']}")
        logger.info(f"   • Success rate: {stats['success_rate']*100:.1f}%")

    def get_dataset(self) -> List[Dict]:
        """Get the scraped dataset as a list of dictionaries."""
        return self.dataset

    def get_stats(self) -> Dict:
        """Get scraping statistics."""
        return {
            'total_urls': len(self.master_urls),
            'completed': len(self.completed_urls),
            'errors': len(self.error_urls),
            'success_rate': len(self.completed_urls) / len(self.master_urls) if self.master_urls else 0
        }

    @staticmethod
    def _load_topics_from_file(file_path: Union[str, Path]) -> List[str]:
        """Load topics from various file formats."""
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Handle different file formats
        if path.suffix == '.json':
            with open(path, 'r') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict) and 'topics' in data:
                    return data['topics']
                raise ValueError("JSON file must contain a list or a dict with 'topics' key")
                
        elif path.suffix in ['.yaml', '.yml']:
            with open(path, 'r') as f:
                data = yaml.safe_load(f)
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict) and 'topics' in data:
                    return data['topics']
                raise ValueError("YAML file must contain a list or a dict with 'topics' key")
                
        elif path.suffix == '.txt':
            with open(path, 'r') as f:
                return [line.strip() for line in f.readlines() if line.strip()]
                
        elif path.suffix == '.md':
            with open(path, 'r') as f:
                content = f.read()
                topics = re.findall(r'[-*]\s*(.+)', content)
                if topics:
                    return [topic.strip() for topic in topics]
                return [line.strip() for line in content.split('\n') if line.strip()]
        
        else:
            raise ValueError(f"Unsupported file format: {path.suffix}")
