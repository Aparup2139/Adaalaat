"""
Web Search Service

Performs web searches for recent legal news, rulings, and information
not found in the local vector database.

Supports Serper API (Google Search) as the default provider.
"""

import os
import json
import logging
import requests
from dotenv import load_dotenv

# --- Load .env from the Backend root folder ---
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = os.path.join(backend_dir, ".env")
load_dotenv(dotenv_path)
# ----------------------------------------------

logger = logging.getLogger(__name__)


class WebSearchService:
    """Web search client for the legal agent pipeline."""

    def __init__(self, config_path: str = None):
        """Initialize with config."""
        self.api_key = None
        self.num_results = 5
        self.provider = "serper"

        if config_path:
            try:
                with open(config_path, "r") as f:
                    config = json.load(f)
                web_config = config.get("web_search", {})
                self.provider = web_config.get("provider", "serper")
                self.num_results = web_config.get("num_results", 5)

                # Use the environment variable loaded by dotenv
                api_key_env = web_config.get("api_key_env", "SERPER_API_KEY")
                self.api_key = os.getenv(api_key_env, "")
            except FileNotFoundError:
                logger.warning(f"Config file not found: {config_path}")
                # Fallback directly to the OS env if config is missing
                self.api_key = os.getenv("SERPER_API_KEY", "")
        else:
            # Fallback if no config path is provided
            self.api_key = os.getenv("SERPER_API_KEY", "")

    def search(self, query: str) -> str:
        """
        Perform a web search and return formatted results.

        Args:
            query: The search query

        Returns:
            str: Formatted search results text
        """
        if self.provider == "serper":
            return self._search_serper(query)
        else:
            return self._search_fallback(query)

    def _search_serper(self, query: str) -> str:
        """
        Search using Serper.dev Google Search API.

        Requires SERPER_API_KEY environment variable.
        Get a key at https://serper.dev/
        """
        if not self.api_key:
            logger.warning("SERPER_API_KEY not set, falling back to no results")
            return "Web search is not configured. Set SERPER_API_KEY in .env"

        try:
            response = requests.post(
                "https://google.serper.dev/search",
                headers={
                    "X-API-KEY": self.api_key,
                    "Content-Type": "application/json",
                },
                json={
                    "q": query,
                    "num": self.num_results,
                },
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()

            results = []
            for item in data.get("organic", []):
                title = item.get("title", "")
                snippet = item.get("snippet", "")
                link = item.get("link", "")
                results.append(f"**{title}**\n{snippet}\nURL: {link}")

            if not results:
                return "No relevant web results found."

            return "\n\n---\n\n".join(results)

        except requests.RequestException as e:
            logger.error(f"Serper search failed: {e}")
            return f"Web search failed: {str(e)}"

    def _search_fallback(self, query: str) -> str:
        """Fallback when no search provider is configured."""
        return (
            "Web search is not configured. "
            "Add a search provider (serper, serpapi) in config.json "
            "and set the corresponding API key in .env"
        )
