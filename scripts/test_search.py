#!/usr/bin/env python3
"""Search Tool 连通性测试。

验证 DuckDuckGo 搜索是否正常工作。
"""

from research_agent.tools import get_search_client


def main() -> None:
    client = get_search_client()
    results = client.search("Python 异步编程", max_results=5)

    print(f"共找到 {len(results)} 条结果\n")
    for i, r in enumerate(results, 1):
        print(f"{i}. {r.title}")
        print(f"   URL: {r.url}")
        print(f"   摘要: {r.snippet[:120]}...")
        print()


if __name__ == "__main__":
    main()
