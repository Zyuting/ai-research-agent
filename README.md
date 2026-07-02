<div align="center">

# Research Agent

**AI-powered research assistant** — Input a topic, get a structured Markdown report.
Automates the full research pipeline: **search → read → summarize → write**.

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-%20-purple)](https://langchain-ai.github.io/langgraph/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

</div>

---

## Overview

Research Agent is a modular, LLM-powered system that autonomously researches any topic and produces a structured report. It orchestrates a 5-stage LangGraph pipeline with pluggable search engines, web readers, and LLM providers.

## Architecture

The system follows a layered, decoupled design:

```
CLI Layer          (__main__.py)
Workflow Layer     (LangGraph StateGraph)
Node Layer         (Planner → Search → Reader → Summarizer → Writer)
Tool Layer         (Search + Web Reader engines)
LLM Layer          (BaseLLMClient + OpenAI-compatible providers)
```

### Workflow

```
topic → [Planner] → search_queries → [Search] → search_results → [Reader]
→ web_pages → [Summarizer] → summary → [Writer] → report
```

Each node has a single responsibility and communicates exclusively through `ResearchState` (TypedDict), enabling independent error isolation and easy extensibility.

## Features

- **LLM-powered planning** — Generates optimal search queries from your topic
- **Multi-engine search** — DuckDuckGo built-in (zero config), pluggable for Tavily, Google, etc.
- **Intelligent web reading** — Extracts main content, strips noise, auto-fallback on 403
- **Model-agnostic LLM layer** — Switch between Qwen, GPT, DeepSeek via single `.env` variable. Abstract base + factory + Registry pattern
- **Structured reports** — Markdown with sections, citations, and references
- **13 unit tests** covering config, LLM, prompts, tools, and workflow

## Quick Start

```bash
# Install
pip install -r requirements.txt

# Configure
cp .env.example .env   # set DASHSCOPE_API_KEY

# Run
python -m research_agent "Transformer architecture evolution"
```

### Python API

```python
from research_agent.graph import graph

result = graph.invoke({"topic": "Rust in system programming"})
print(result["report"])
```

## Extensibility

| Want to... | Do this |
|---|---|
| Add a search engine | `register_search_engine("tavily", TavilyClient)` |
| Add a web reader | `register_web_reader("jina", JinaReader)` |
| Change the LLM | Edit `.env` → `LLM_BASE_URL` + `LLM_MODEL` |
| Add a workflow node | 1) Add field in `State` 2) Create node function 3) `add_node()` + `add_edge()` |

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed design docs.

## License

[MIT](LICENSE) © 2026 Yueting Zhang
