"""Search client abstraction for ResearcherAgent."""

import json
import urllib.request
import urllib.error
from multi_agent_research_lab.core.config import get_settings
from multi_agent_research_lab.core.schemas import SourceDocument


class SearchClient:
    """Provider-agnostic search client implementation using Tavily."""

    def __init__(self):
        self.settings = get_settings()

    def search(self, query: str, max_results: int = 5) -> list[SourceDocument]:
        """Search for documents relevant to a query using Tavily API."""
        
        api_key = self.settings.tavily_api_key
        if not api_key:
            # Fallback to mock if no API key
            return [
                SourceDocument(
                    title="Mock Document",
                    url="https://mock.com",
                    snippet=f"This is a mock search result for: {query}"
                )
            ]

        url = "https://api.tavily.com/search"
        headers = {
            "Content-Type": "application/json",
        }
        data = {
            "api_key": api_key,
            "query": query,
            "search_depth": "basic",
            "max_results": max_results,
            "include_answer": False
        }

        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
        
        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode())
                
            docs = []
            for item in result.get('results', []):
                docs.append(SourceDocument(
                    title=item.get('title', 'Untitled'),
                    url=item.get('url', ''),
                    snippet=item.get('content', '')
                ))
            return docs
            
        except urllib.error.URLError as e:
            print(f"Search API Error: {e}")
            return []
