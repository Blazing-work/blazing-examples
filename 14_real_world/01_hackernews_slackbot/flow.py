"""
Hacker News Slackbot Example for Blazing

Demonstrates scheduled workflow execution with external API integration.
This bot fetches top Hacker News stories, filters by score, and posts to Slack
on an automated schedule using Blazing's Period scheduler.

Key features:
- Scheduled execution via @app.workflow(schedule=Period(hours=1))
- HTTP session reuse for performance
- Concurrent request limiting with asyncio.Semaphore
- SlackConnector integration for posting
- Egress control for HN API and Slack domains
"""

import asyncio
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

import httpx
from blazing import Blazing, BaseService, Period

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Blazing app (placeholder credentials for demo)
app = Blazing(
    api_url=os.getenv("BLAZING_API_URL", "http://localhost:8000"),
    api_token=os.getenv("BLAZING_API_TOKEN", "demo-token-placeholder")
)


@app.service(egress=[
    "hacker-news.firebaseio.com",  # HN API
    "hooks.slack.com",              # Slack webhook URLs
    "*.slack.com",                  # Slack API endpoints
])
class HackerNewsBot(BaseService):
    """
    Automated Hacker News digest bot.

    Fetches top HN stories, filters by score threshold, formats them for Slack,
    and posts to a channel. Designed for scheduled execution.
    """

    def __init__(self, connector_instances=None):
        """
        Initialize HN bot.

        Args:
            connector_instances: Dict of connector instances (injected by Blazing)
        """
        super().__init__(connector_instances)
        self.slack = connector_instances.get('slack') if connector_instances else None
        self.session: Optional[httpx.AsyncClient] = None
        logger.info("HackerNewsBot initialized")

    async def connect(self) -> None:
        """
        Establish connections for the bot.

        Creates HTTP session for HN API requests. AsyncClient requires an event loop,
        so must be created here (not in __init__).
        """
        self.session = httpx.AsyncClient(timeout=30.0)
        logger.info("HN bot session created")

    async def disconnect(self) -> None:
        """Clean up HTTP session."""
        if self.session:
            await self.session.aclose()
            self.session = None
            logger.info("HN bot session closed")

    async def fetch_top_stories(self, limit: int = 30) -> List[int]:
        """
        Fetch IDs of top Hacker News stories.

        Args:
            limit: Number of story IDs to retrieve

        Returns:
            List of story IDs (integers)
        """
        url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        logger.info(f"Fetching top {limit} story IDs from HN")

        response = await self.session.get(url)
        response.raise_for_status()

        story_ids = response.json()
        return story_ids[:limit]

    async def fetch_story_details(self, story_id: int) -> Dict:
        """
        Fetch details for a specific story.

        Args:
            story_id: HN story ID

        Returns:
            Story data dict with title, url, score, etc.
        """
        url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        response = await self.session.get(url)
        response.raise_for_status()
        return response.json()

    async def fetch_high_scoring_stories(
        self,
        min_score: int = 100,
        limit: int = 10
    ) -> List[Dict]:
        """
        Fetch top stories that meet minimum score threshold.

        Uses a semaphore to limit concurrent HN API requests to prevent
        overwhelming the API and getting rate limited.

        Args:
            min_score: Minimum score threshold
            limit: Maximum number of stories to return

        Returns:
            List of story dicts, sorted by score descending
        """
        # Fetch top story IDs (over-fetch to ensure enough high-scoring ones)
        story_ids = await self.fetch_top_stories(limit=50)

        # Fetch story details concurrently with rate limiting
        semaphore = asyncio.Semaphore(10)  # Max 10 concurrent requests

        async def fetch_with_limit(story_id: int) -> Optional[Dict]:
            """Fetch story with semaphore limiting."""
            async with semaphore:
                try:
                    return await self.fetch_story_details(story_id)
                except Exception as e:
                    logger.warning(f"Failed to fetch story {story_id}: {e}")
                    return None

        # Fetch all stories concurrently
        stories = await asyncio.gather(*[
            fetch_with_limit(story_id) for story_id in story_ids
        ])

        # Filter out failed fetches and stories below threshold
        valid_stories = [
            story for story in stories
            if story and story.get('score', 0) >= min_score
        ]

        # Sort by score descending and limit
        valid_stories.sort(key=lambda s: s.get('score', 0), reverse=True)

        logger.info(f"Found {len(valid_stories)} stories with score >= {min_score}")
        return valid_stories[:limit]

    def format_stories(self, stories: List[Dict]) -> str:
        """
        Format stories for Slack posting.

        Creates a numbered list with title, score, URL, and HN discussion link.

        Args:
            stories: List of story dicts

        Returns:
            Formatted text string for Slack
        """
        if not stories:
            return "No high-scoring stories found."

        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
        header = f"*Hacker News Top Stories* ({len(stories)} stories)\n_{timestamp}_\n\n"

        story_lines = []
        for idx, story in enumerate(stories, 1):
            title = story.get('title', 'No title')
            score = story.get('score', 0)
            url = story.get('url', '')
            story_id = story.get('id', '')
            hn_url = f"https://news.ycombinator.com/item?id={story_id}"

            # Format: 1. Title (123 points) [Link] [HN Discussion]
            if url:
                story_line = f"{idx}. *{title}* ({score} points)\n   <{url}|Link> | <{hn_url}|HN Discussion>"
            else:
                # Some stories don't have external URLs (Ask HN, Show HN)
                story_line = f"{idx}. *{title}* ({score} points)\n   <{hn_url}|HN Discussion>"

            story_lines.append(story_line)

        return header + "\n\n".join(story_lines)

    async def post_digest(
        self,
        channel: str = "#hacker-news",
        min_score: int = 100
    ) -> int:
        """
        Fetch stories and post digest to Slack.

        Args:
            channel: Slack channel (e.g., "#hacker-news")
            min_score: Minimum story score threshold

        Returns:
            Number of stories posted
        """
        logger.info(f"Generating HN digest for {channel} (min_score={min_score})")

        stories = await self.fetch_high_scoring_stories(min_score=min_score, limit=10)

        if not stories:
            logger.info("No stories to post")
            return 0

        formatted_text = self.format_stories(stories)

        if self.slack:
            result = await self.slack.post_message(
                channel=channel,
                text=formatted_text
            )
            logger.info(f"Posted {len(stories)} stories to {channel} (ts={result.get('ts')})")
        else:
            logger.warning("SlackConnector not available - skipping post")

        return len(stories)


# ============================================================================
# SCHEDULED WORKFLOW - runs every hour automatically
# ============================================================================

@app.workflow(schedule=Period(hours=1))
async def hourly_hn_digest(services=None):
    """
    Scheduled workflow that runs every hour.

    Blazing's scheduler automatically invokes this function every hour based on
    the Period(hours=1) schedule. The 'services' dict contains all registered
    services keyed by class name (e.g., services['HackerNewsBot']).
    """
    logger.info("Hourly HN digest workflow triggered")

    bot = services['HackerNewsBot']
    count = await bot.post_digest(min_score=200)  # Higher threshold for hourly digests

    logger.info(f"Hourly HN digest complete: {count} stories posted")
    return {"stories_posted": count}


# ============================================================================
# HTTP ENDPOINTS - for manual triggers and testing
# ============================================================================

@app.endpoint.post("/digest")
async def trigger_digest(request, services=None):
    """
    Manually trigger HN digest.

    Request body:
        {
            "min_score": 100,          # optional: minimum story score (default: 100)
            "channel": "#hacker-news"  # optional: Slack channel (default: #hacker-news)
        }

    Response:
        {"stories_posted": 5, "channel": "#hacker-news"}
    """
    body = await request.json()
    bot = services['HackerNewsBot']

    channel = body.get("channel", "#hacker-news")
    min_score = body.get("min_score", 100)

    count = await bot.post_digest(channel=channel, min_score=min_score)

    return {
        "stories_posted": count,
        "channel": channel
    }


if __name__ == "__main__":
    import asyncio

    async def test_bot():
        """Fetch and print stories (no Slack connector needed)."""
        bot = HackerNewsBot()
        await bot.connect()

        stories = await bot.fetch_high_scoring_stories(min_score=100, limit=5)
        formatted = bot.format_stories(stories)

        print(formatted)

        await bot.disconnect()

    asyncio.run(test_bot())
