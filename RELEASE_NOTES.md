## v1.0.0 (2026-07-02)

### Initial Release — MVP

The first public release of **Research Agent**, an AI-powered research assistant that automates the full research pipeline: search → read → summarize → write.

### Features

- **End-to-end automation** — Input a topic, get a structured Markdown report
- **LLM-powered planning** — Generates optimal search queries using Qwen / GPT / DeepSeek
- **DuckDuckGo search** — Built-in, zero-config, no API key required
- **Intelligent web reading** — Extracts main content, strips ads/navigation, auto-fallback on 403
- **Structured reports** — Overview, analysis, conclusion, and references with citation markers
- **Model-agnostic** — Switch between Qwen, GPT, DeepSeek via single `.env` variable
- **Modular architecture** — Abstract base classes + Registry pattern for easy extension

### Architecture

```
5-layer decoupled design: CLI → LangGraph Workflow → Nodes + Prompts → Tools → LLM
```

Workflow: `Planner (LLM) → Search (DuckDuckGo) → Reader (httpx+BS4) → Summarizer (LLM) → Writer (LLM)`

### Technical Highlights

- **LangGraph StateGraph** — DAG-driven workflow orchestration with typed state management
- **Pluggable LLM layer** — Abstract `BaseLLMClient` with factory + Registry pattern. One `.env` change to swap providers
- **Pluggable search** — `BaseSearchClient` with DuckDuckGo built-in. `register_search_engine("tavily", ...)` to add more
- **Intelligent content extraction** — HtmlWebReader auto-removes nav/ads, priority-falls back from `<article>` → `<main>` → `<body>`, auto-retries with alternate UA on 403
- **Error isolation** — Each node runs independently. Failures are recorded in `errors[]` without crashing the graph

### Testing

- 13 unit tests covering config, LLM, prompts, tools, and workflow
- pytest-based, run with `pytest tests/ -v`

### Project Structure

```
research-agent/
├── src/research_agent/
│   ├── __main__.py       CLI entry point
│   ├── config.py         pydantic-settings (.env)
│   ├── graph/            StateGraph assembly
│   ├── state/            ResearchState (TypedDict)
│   ├── nodes/            5 workflow nodes
│   ├── tools/            Search + Web Reader
│   ├── prompts/          Prompt templates (.txt)
│   └── llm/              LLM abstraction layer
├── tests/                pytest suite
├── ARCHITECTURE.md       Design docs
└── README.md
```

### What's Included

- Full source code under `src/research_agent/`
- 5 workflow nodes with single responsibility
- 3 prompt templates (planner, summarizer, report writer)
- Search and web reader tools with abstract base classes
- 13 unit tests
- Architecture documentation (ARCHITECTURE.md)
- MIT License

### Known Limitations

- DuckDuckGo search may be unreliable in regions where it is blocked (fallback: use a proxy or switch to Tavily/Google via the pluggable architecture)
- Web reader may fail on sites with aggressive anti-bot protections (Cloudflare, etc.)
- Single-turn research only — no iterative refinement or follow-up questions yet
- No structured logging (uses print statements)
- Synchronous node execution only (async support planned)
