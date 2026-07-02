"""Web reader tool — HTML content extractor with noise removal and auto-fallback.

Prioritizes <article> / <main> regions, strips navigation and ads.
Auto-fallback on 403: retries with a different User-Agent and verify=False.
"""

from __future__ import annotations

import asyncio
import re
from abc import ABC, abstractmethod

import httpx
from bs4 import BeautifulSoup, Tag

from research_agent.tools.models import WebPage

_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/125.0.0.0 Safari/537.36"
)
_FALLBACK_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
)
_DEFAULT_TIMEOUT = 15.0
_MAX_CONTENT_LENGTH = 10_000

_REMOVE_TAGS = {
    "script", "style", "nav", "footer", "header", "aside",
    "form", "iframe", "noscript", "svg",
}
_REMOVE_PATTERNS = re.compile(
    r"\b(ad|ads|advertisement|sidebar|menu|nav|navbar|footer|header|"
    r"cookie|popup|modal|overlay|banner|social|share|comment|related)\b",
    re.I,
)


class BaseWebReader(ABC):
    """Abstract base class for web page readers."""

    @abstractmethod
    def read(self, url: str) -> WebPage:
        ...

    @abstractmethod
    async def aread(self, url: str) -> WebPage:
        ...


class HtmlWebReader(BaseWebReader):
    """HTML web page reader using httpx + BeautifulSoup.

    Features:
    - Extracts title and main content from <article> / <main> / <body>
    - Removes navigation, ads, scripts, and other noise elements
    - Auto-fallback on 403 or connection errors
    """

    def __init__(
        self,
        timeout: float = _DEFAULT_TIMEOUT,
        max_content_length: int = _MAX_CONTENT_LENGTH,
    ) -> None:
        self._timeout = timeout
        self._max_content_length = max_content_length

    def read(self, url: str) -> WebPage:
        return self._read_with_fallback(url)

    async def aread(self, url: str) -> WebPage:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._read_with_fallback, url)

    # ---- private ----

    def _read_with_fallback(self, url: str) -> WebPage:
        """Read with fallback strategy for 403 and connection errors."""
        try:
            return self._request_and_parse(url, verify=True, ua=_USER_AGENT)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 403:
                return self._request_and_parse(
                    url, verify=False, ua=_FALLBACK_UA
                )
            raise
        except httpx.ConnectError:
            return self._request_and_parse(
                url, verify=False, ua=_USER_AGENT
            )

    def _request_and_parse(
        self, url: str, *, verify: bool, ua: str
    ) -> WebPage:
        transport = httpx.HTTPTransport(retries=1)
        with httpx.Client(
            timeout=self._timeout,
            follow_redirects=True,
            transport=transport,
            verify=verify,
        ) as client:
            resp = client.get(url, headers={"User-Agent": ua})
            resp.raise_for_status()

        content_type = resp.headers.get("content-type", "")
        if "charset" not in content_type:
            resp.encoding = resp.apparent_encoding

        html = resp.text
        soup = BeautifulSoup(html, "html.parser")
        self._remove_noise(soup)

        title = self._extract_title(soup)
        content = self._extract_content(soup)
        content = self._clean_text(content)
        content = content[: self._max_content_length]

        return WebPage(url=url, title=title, content=content, html=html)

    @staticmethod
    def _remove_noise(soup: BeautifulSoup) -> None:
        """Remove unwanted tags and advertisement regions."""
        for tag in _REMOVE_TAGS:
            for el in soup.find_all(tag):
                el.decompose()

        for el in list(soup.find_all(True)):
            if isinstance(el, Tag):
                classes = " ".join(el.get("class", []))
                elem_id = el.get("id", "") or ""
                if _REMOVE_PATTERNS.search(classes) or _REMOVE_PATTERNS.search(elem_id):
                    el.decompose()

    @staticmethod
    def _extract_title(soup: BeautifulSoup) -> str:
        title_tag = soup.find("title")
        return title_tag.get_text(strip=True) if title_tag else ""

    @staticmethod
    def _extract_content(soup: BeautifulSoup) -> str:
        """Extract main content from the page body."""
        container: Tag | None = (
            soup.find("article")
            or soup.find("main")
            or soup.find(attrs={"role": "main"})
        )
        if container is None:
            container = soup.find("body")
        if container is None:
            return ""

        paragraphs: list[str] = []
        for p in container.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6", "li"]):
            text = p.get_text(strip=True)
            if text and len(text) > 10:
                paragraphs.append(text)

        return "\n\n".join(paragraphs)

    @staticmethod
    def _clean_text(text: str) -> str:
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)
        return text.strip()


# ---- Registry & factory ----

_REGISTRY: dict[str, type[BaseWebReader]] = {
    "html": HtmlWebReader,
}


def register_web_reader(name: str, client_cls: type[BaseWebReader]) -> None:
    _REGISTRY[name] = client_cls


def get_web_reader(reader_type: str | None = None) -> BaseWebReader:
    reader_type = reader_type or "html"
    client_cls = _REGISTRY.get(reader_type)
    if client_cls is None:
        raise ValueError(f"Unsupported web reader: {reader_type}")
    return client_cls()
