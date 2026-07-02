"""Tools 模块单元测试。"""

from dataclasses import dataclass

from research_agent.tools import (
    BaseSearchClient,
    BaseWebReader,
    SearchResult,
    WebPage,
    register_search_engine,
    register_web_reader,
)
from research_agent.tools.models import SearchResult, WebPage


def test_search_result_dataclass():
    """验证 SearchResult 数据类。"""
    r = SearchResult(title="Test", url="https://example.com", snippet="desc")
    assert r.title == "Test"
    assert r.url == "https://example.com"
    assert r.snippet == "desc"


def test_webpage_dataclass():
    """验证 WebPage 数据类。"""
    p = WebPage(url="https://example.com", title="Page", content="body")
    assert p.url == "https://example.com"
    assert p.title == "Page"
    assert p.content == "body"


def test_register_custom_search_engine():
    """验证自定义搜索引擎注册。"""

    class MockSearch(BaseSearchClient):
        def search(self, query, max_results=5):
            return [SearchResult(title="mock", url="https://mock", snippet="")]
        async def asearch(self, query, max_results=5):
            return self.search(query, max_results)

    register_search_engine("mock", MockSearch)


def test_register_custom_web_reader():
    """验证自定义网页读取器注册。"""

    class MockReader(BaseWebReader):
        def read(self, url):
            return WebPage(url=url, title="mock", content="")
        async def aread(self, url):
            return self.read(url)

    register_web_reader("mock", MockReader)
