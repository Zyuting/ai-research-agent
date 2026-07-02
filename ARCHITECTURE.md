# Architecture

## Overview

Research Agent is a **LangGraph**-powered AI research assistant. Input a topic — get a structured Markdown report. It automates the full pipeline: search, read, analyze, and write.

The architecture follows a **layered, decoupled** design:

```
┌──────────────────────────────────────────┐
│              Command Line                 │
│         (__main__.py / scripts/)          │
├──────────────────────────────────────────┤
│              Workflow Layer               │
│          (graph/ + state/)                │
├──────────────────────────────────────────┤
│   Nodes         │   Prompts               │
│   (nodes/)      │   (prompts/)            │
├──────────────────────────────────────────┤
│   Tools Layer                             │
│   (tools/ - search / web_reader)          │
├──────────────────────────────────────────┤
│   LLM Layer                               │
│   (llm/ - base class + OpenAI Compatible) │
└──────────────────────────────────────────┘
```

## Module responsibilities

### LLM layer (`llm/`)

**Responsibility**: Provide a unified LLM interface that abstracts over different model providers.

**Key design decisions**:

- **Abstract base class** `BaseLLMClient` defines the `invoke` / `ainvoke` contract
- **Factory function** `get_llm()` returns the correct implementation based on config — callers never instantiate clients directly
- **Error mapping** translates SDK-specific exceptions (`APIStatusError`, etc.) into domain exceptions (`LLMAuthenticationError`, `LLMRateLimitError`, etc.)
- **Current implementation**: `OpenAICompatibleClient` works with any OpenAI Chat Completions-compatible API (Qwen, GPT, DeepSeek, etc.)

**扩展方式**：

```python
class GPTClient(BaseLLMClient):
    def invoke(self, message: str, **kwargs) -> LLMResponse: ...
    async def ainvoke(self, message: str, **kwargs) -> LLMResponse: ...

register_provider("gpt", GPTClient)
```

### Tool layer (`tools/`)

**Responsibility**: Provide search and web reading as standalone, swappable capabilities.

**Key design decisions**:

- **Search**: `BaseSearchClient` abstract base + Registry pattern. Current: DuckDuckGo via `ddgs`. Add new engines with `register_search_engine()`
- **Web reader**: `BaseWebReader` abstract base. `HtmlWebReader` uses httpx + BeautifulSoup with auto-fallback (403 → alternate UA + verify=False)
- **Data models**: `SearchResult` and `WebPage` dataclasses serve as the contract between layers

**扩展方式**：

```python
register_search_engine("tavily", TavilySearchClient)
register_web_reader("jina", JinaWebReader)
```

### Prompt layer (`prompts/`)

**Responsibility**: Centralize all LLM prompts, keeping them separate from code.

**Key design decisions**:

- Prompts are `.txt` files — changing a prompt never requires changing Python code
- `load_prompt(name, **kwargs)` uses `str.format()` for template rendering
- Variables use `{topic}`, `{pages_text}` placeholders

### Node layer (`nodes/`)

**Responsibility**: Implement the logic for each workflow step.

**Design principles**:

- **Single responsibility**: Each node does exactly one thing (planner generates queries, search searches, reader fetches...)
- **Functional style**: Receives `ResearchState`, returns a `dict` delta — no side effects
- **Error isolation**: A single node failure doesn't break the entire graph

### Workflow layer (`graph/` + `state/`)

**Responsibility**: Orchestrate node execution order and maintain global state via LangGraph.

**Key design decisions**:

- `StateGraph(ResearchState)` compiles into a callable object
- Nodes communicate **only through State** — no direct function calls
- `ResearchState` uses `TypedDict` with fields ordered by data flow direction

## Workflow

```mermaid
graph TD
    START((START))
    Planner[Planner<br/>topic → search_queries]
    Search[Search<br/>search_queries → search_results]
    Reader[Reader<br/>search_results → web_pages]
    Summarizer[Summarizer<br/>web_pages → summary]
    Writer[Writer<br/>summary → report]
    END((END))

    START --> Planner
    Planner --> Search
    Search --> Reader
    Reader --> Summarizer
    Summarizer --> Writer
    Writer --> END
```

## Data flow

```
topic (str)
  ↓ Planner (LLM)
search_queries (list[str])
  ↓ Search (DuckDuckGo)
search_results (list[SearchResult])
  ↓ Reader (httpx + BeautifulSoup)
web_pages (list[WebPage])
  ↓ Summarizer (LLM)
summary (str)
  ↓ Writer (LLM)
report (str)
```

## Extensibility guide

### Add a new search provider

1. Inherit `BaseSearchClient` in `tools/search.py`
2. Call `register_search_engine("engine_name", YourClient)`
3. Use `get_search_client("engine_name")` anywhere

### Add a new workflow node

1. Add a field to `ResearchState` in `state/__init__.py`
2. Create a node function in `nodes/`
3. `add_node()` + `add_edge()` in `graph/__init__.py`

### Switch LLM model

Edit `.env`:
```env
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o-mini
DASHSCOPE_API_KEY=sk-xxxxx
```

## Tech stack

| Component | Choice | Rationale |
|---|---|---|
| Workflow engine | LangGraph | DAG-driven, built-in state management, conditional edges, human-in-the-loop |
| LLM interface | OpenAI Compatible | Unified protocol for Qwen, GPT, DeepSeek, etc. |
| Web scraping | httpx + BeautifulSoup | No third-party service dependency, strong noise removal |
| Search | ddgs (DuckDuckGo) | No API key required, zero-config |
| Config | pydantic-settings | Type validation, auto .env loading |
