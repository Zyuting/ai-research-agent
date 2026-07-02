"""Search node — batch queries search engine, deduplicate results."""

from __future__ import annotations

from research_agent.state import ResearchState
from research_agent.tools import get_search_client


def search_node(state: ResearchState) -> dict:
    """Iterate through search_queries, merge and deduplicate results."""
    client = get_search_client()
    seen_urls: set[str] = set()
    all_results = []
    errors = state.get("errors", []).copy()

    for query in state.get("search_queries", []):
        try:
            results = client.search(query, max_results=5)
        except RuntimeError as e:
            errors.append(f"Search failed [{query}]: {e}")
            continue

        for r in results:
            if r.url not in seen_urls:
                seen_urls.add(r.url)
                all_results.append(r)

    return {"search_results": all_results[:10], "errors": errors}
