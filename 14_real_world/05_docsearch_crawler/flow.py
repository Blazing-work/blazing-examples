#!/usr/bin/env python3
"""
Algolia Docsearch Crawler Example

Crawls a documentation site with BFS, extracts text with trafilatura, and batch-indexes to Algolia.
Demonstrates: robots.txt compliance, URL normalization, SHA256 objectID generation, batch indexing.
"""
import asyncio
import hashlib
import logging
import os
from collections import deque
from typing import Dict, List, Set, Optional
from urllib.parse import urljoin, urlparse, urlunparse, parse_qs, urlencode
from urllib.robotparser import RobotFileParser

import httpx
import trafilatura
from bs4 import BeautifulSoup

from blazing import Blazing, BaseService

app = Blazing(
    api_url=os.getenv("BLAZING_API_URL", "http://localhost:8000"),
    api_token=os.getenv("BLAZING_API_TOKEN", "demo-token-placeholder")
)

logger = logging.getLogger(__name__)


@app.service(egress=["*.algolia.net", "*.algolianet.com"])
class DocsCrawlerService(BaseService):
    """Service for crawling documentation sites and indexing to Algolia."""

    def __init__(self, connector_instances=None):
        super().__init__(connector_instances)
        self.algolia = connector_instances.get('algolia') if connector_instances else None

        if not self.algolia:
            raise ValueError("AlgoliaConnector required in connector_instances")

    def _normalize_url(self, url: str) -> str:
        """
        Normalize URL for deduplication.

        - Remove trailing slashes
        - Remove fragments (#section)
        - Sort query parameters alphabetically
        """
        parsed = urlparse(url)

        path = parsed.path.rstrip('/')
        if not path:
            path = '/'

        query_dict = parse_qs(parsed.query)
        sorted_query = urlencode(sorted(query_dict.items()), doseq=True)

        return urlunparse((
            parsed.scheme,
            parsed.netloc,
            path,
            parsed.params,
            sorted_query,
            ''  # No fragment
        ))

    def _generate_object_id(self, url: str) -> str:
        """Generate Algolia objectID from URL using SHA256 hash."""
        return hashlib.sha256(url.encode('utf-8')).hexdigest()

    async def _check_robots_txt(self, base_url: str, user_agent: str = "*") -> RobotFileParser:
        """Fetch and parse robots.txt for a domain."""
        parsed = urlparse(base_url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

        parser = RobotFileParser()
        parser.set_url(robots_url)

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(robots_url)
                if response.status_code == 200:
                    parser.parse(response.text.splitlines())
                    logger.info(f"Loaded robots.txt from {robots_url}")
                else:
                    logger.info(f"No robots.txt found at {robots_url}, allowing all")
        except Exception as e:
            logger.warning(f"Failed to fetch robots.txt from {robots_url}: {e}, allowing all")

        return parser

    def _get_crawl_delay(self, parser: RobotFileParser, user_agent: str = "*") -> float:
        """Get crawl-delay from robots.txt."""
        delay = parser.crawl_delay(user_agent)
        return float(delay) if delay else 0.0

    async def _fetch_page(
        self,
        client: httpx.AsyncClient,
        url: str,
        parser: RobotFileParser,
        user_agent: str = "Blazing-DocsCrawler/1.0"
    ) -> Optional[str]:
        """Fetch page HTML if allowed by robots.txt."""
        if not parser.can_fetch(user_agent, url):
            logger.info(f"Blocked by robots.txt: {url}")
            return None

        try:
            response = await client.get(
                url,
                headers={"User-Agent": user_agent},
                follow_redirects=True
            )
            return response.text if response.status_code == 200 else None
        except Exception as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return None

    def _extract_text(self, html: str, url: str) -> tuple[Optional[str], Optional[str]]:
        """
        Extract title and main text content from HTML.

        Uses trafilatura for text extraction (F1 score 0.958) with BeautifulSoup fallback.
        Truncates to 10,000 chars (Algolia 10KB limit per record).
        """
        title = None
        try:
            soup = BeautifulSoup(html, 'lxml')
            title_tag = soup.find('title')
            if title_tag:
                title = title_tag.get_text(strip=True)
        except Exception as e:
            logger.warning(f"Failed to extract title: {e}")

        content = trafilatura.extract(
            html,
            include_tables=True,
            no_fallback=False,
            url=url
        )

        if not content:
            return title, None

        if len(content) > 10000:
            content = content[:10000] + "..."

        return title, content

    def _extract_links(self, html: str, base_url: str) -> Set[str]:
        """Extract same-domain links from HTML."""
        links = set()
        base_parsed = urlparse(base_url)

        try:
            soup = BeautifulSoup(html, 'lxml')
            for anchor in soup.find_all('a', href=True):
                href = anchor['href']

                if href.startswith('#'):
                    continue

                absolute_url = urljoin(base_url, href)
                link_parsed = urlparse(absolute_url)

                if link_parsed.netloc == base_parsed.netloc:
                    normalized = self._normalize_url(absolute_url)
                    links.add(normalized)
        except Exception as e:
            logger.error(f"Failed to extract links: {e}")

        return links

    async def crawl_bfs(
        self,
        start_url: str,
        index_name: str,
        max_depth: int = 3,
        max_pages: int = 100
    ) -> Dict[str, any]:
        """
        Crawl a documentation site using breadth-first search.

        Respects robots.txt, extracts text with trafilatura, and batch-indexes to Algolia.

        Args:
            start_url: Starting URL for crawl
            index_name: Algolia index name
            max_depth: Maximum crawl depth (default 3)
            max_pages: Maximum pages to crawl (default 100)

        Returns:
            Dict with documents_indexed, index_name, crawl_duration_seconds
        """
        import time
        start_time = time.time()

        start_url = self._normalize_url(start_url)
        parser = await self._check_robots_txt(start_url)
        crawl_delay = self._get_crawl_delay(parser)
        logger.info(f"Crawl delay: {crawl_delay}s")

        queue = deque([(start_url, 0)])  # (url, depth)
        visited: Set[str] = set()
        documents: List[Dict[str, any]] = []

        async with httpx.AsyncClient(timeout=30.0) as client:
            while queue and len(visited) < max_pages:
                url, depth = queue.popleft()

                if url in visited or depth > max_depth:
                    continue

                visited.add(url)
                logger.info(f"Crawling [{depth}/{max_depth}]: {url}")

                html = await self._fetch_page(client, url, parser)
                if not html:
                    continue

                if crawl_delay > 0:
                    await asyncio.sleep(crawl_delay)

                title, content = self._extract_text(html, url)
                if content:
                    doc = {
                        "objectID": self._generate_object_id(url),
                        "url": url,
                        "title": title or url,
                        "content": content,
                        "depth": depth
                    }
                    documents.append(doc)

                if depth < max_depth:
                    links = self._extract_links(html, url)
                    for link in links:
                        if link not in visited:
                            queue.append((link, depth + 1))

        # Batch index to Algolia (1000 records per batch recommended)
        if documents:
            batch_size = 1000
            for i in range(0, len(documents), batch_size):
                batch = documents[i:i + batch_size]
                await self.algolia.batch_index(batch, index_name=index_name)
                logger.info(f"Indexed batch {i//batch_size + 1}: {len(batch)} documents")

        duration = time.time() - start_time

        return {
            "documents_indexed": len(documents),
            "index_name": index_name,
            "crawl_duration_seconds": round(duration, 2)
        }


@app.endpoint.post("/crawl")
async def crawl_and_index(request, services=None):
    """
    Crawl a documentation site and index to Algolia.

    Request body:
    {
        "start_url": "https://docs.example.com",
        "index_name": "docs_index",
        "max_depth": 3,
        "max_pages": 100
    }

    Note: Add the target domain to egress rules before crawling.
    """
    body = await request.json()

    start_url = body.get("start_url")
    index_name = body.get("index_name")
    max_depth = body.get("max_depth", 3)
    max_pages = body.get("max_pages", 100)

    if not start_url:
        return {"error": "Missing 'start_url' field"}, 400
    if not index_name:
        return {"error": "Missing 'index_name' field"}, 400

    crawler = services['DocsCrawlerService']

    result = await crawler.crawl_bfs(
        start_url=start_url,
        index_name=index_name,
        max_depth=max_depth,
        max_pages=max_pages
    )

    return result


if __name__ == "__main__":
    import asyncio
    asyncio.run(app.publish())
