"""Tools - Search & Web Reader 统一导出。"""

from research_agent.tools.models import SearchResult, WebPage
from research_agent.tools.search import (
    BaseSearchClient,
    DuckDuckGoSearchClient,
    get_search_client,
    register_search_engine,
)
from research_agent.tools.web_reader import (
    BaseWebReader,
    HtmlWebReader,
    get_web_reader,
    register_web_reader,
)

__all__ = [
    # Models
    "SearchResult",
    "WebPage",
    # Search
    "BaseSearchClient",
    "DuckDuckGoSearchClient",
    "get_search_client",
    "register_search_engine",
    # Web Reader
    "BaseWebReader",
    "HtmlWebReader",
    "get_web_reader",
    "register_web_reader",
]
