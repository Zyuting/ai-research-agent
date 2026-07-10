<div align="center">

# AI Research Agent — Agent Workflow System

**An LLM-powered agent workflow** that autonomously decomposes research tasks, executes multi-step tool calls, and produces structured deliverables. Designed with modular agent architecture — planning, tool integration, and LLM-based analysis.

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Agent%20Workflow-purple)](https://langchain-ai.github.io/langgraph/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

</div>

---

## Overview

This project implements an **AI Agent workflow system** for automated research. Given a topic, the agent autonomously decomposes the task, searches the web, reads and extracts content from multiple sources, analyzes findings via LLM, and generates a structured Markdown report.

The system demonstrates core agent engineering concepts: **task decomposition**, **tool calling** (web search + content extraction), **multi-step workflow orchestration**, and **modular tool integration** — all through a clean, extensible architecture.

```
User Topic → [Planner Agent] → Search Queries → [Search Tool] → Results
  → [Reader Tool] → Web Content → [Analyzer Agent] → Summary → [Writer Agent] → Report
```

## Architecture: Agent Workflow Design

The system implements a **layered, decoupled agent architecture**:

```
┌─────────────────────────────────────────────────────┐
│                    CLI Layer                         │
├─────────────────────────────────────────────────────┤
│              Workflow Layer (LangGraph)              │
│    StateGraph orchestrating multi-step execution     │
├─────────────────────────────────────────────────────┤
│   Node Layer (Planner → Search → Reader → Writer)   │
│      Each node = single responsibility agent step    │
├─────────────────────────────────────────────────────┤
│              Tool Layer (Pluggable)                  │
│     Search engines + Web readers as callable tools   │
├─────────────────────────────────────────────────────┤
│           LLM Layer (Provider-Agnostic)              │
│   Abstract client + Factory + Registry pattern       │
└─────────────────────────────────────────────────────┘
```

### Agent Workflow: Step by Step

1. **Planner Agent** — Receives user topic, generates targeted search queries via LLM
2. **Search Tool** — Executes queries via configurable search engine (DuckDuckGo/Tavily/Google)
3. **Reader Tool** — Fetches and extracts main content from web pages, strips noise, handles errors
4. **Analyzer Agent** — LLM-powered summarization and analysis of retrieved content
5. **Writer Agent** — Synthesizes all findings into structured Markdown report with citations

## Key Agent Engineering Features

### Tool Calling & Integration

- **Modular tool registration** — `register_search_engine()` / `register_web_reader()` pattern for pluggable tool integration
- **Tool abstraction layer** — Consistent interface across different tool providers
- **Error isolation** — Each tool call handles failures independently; auto-fallback on HTTP errors

### Multi-Step Task Execution

- **StateGraph workflow** — LangGraph-powered orchestration with typed state (ResearchState TypedDict)
- **Sequential node execution** — Each agent node completes before the next begins
- **Independent error handling** — Per-node error isolation prevents cascading failures

### LLM Integration

- **Provider-agnostic design** — Abstract BaseLLMClient with Factory + Registry pattern
- **Switchable backends** — Qwen, GPT, DeepSeek via single environment variable
- **OpenAI-compatible API** — Works with any provider supporting the OpenAI API standard

## Quick Start

```bash
# Install
pip install -r requirements.txt

# Configure
cp .env.example .env   # set LLM_API_KEY

# Run the agent
python -m research_agent "Impact of AI on urban planning"
```

### Python API

```python
from research_agent.graph import graph

# Invoke the agent workflow
result = graph.invoke({"topic": "Rust in system programming"})
print(result["report"])
```

## Extensibility: Adding Tools & Capabilities

| Want to... | Do this |
|---|---|
| Add a search engine | `register_search_engine("tavily", TavilyClient)` |
| Add a web reader | `register_web_reader("jina", JinaReader)` |
| Switch LLM provider | Edit `.env`: `LLM_BASE_URL` + `LLM_MODEL` |
| Add workflow node | 1) Add field in `State` 2) Create node function 3) `add_node()` + `add_edge()` |

## Test Coverage

- **13 unit tests** covering agent configuration, LLM client, prompts, tool layer, and workflow graph
- Isolated testing of each agent node and tool component

## Keywords

`Agent Workflow` `Tool Calling` `Function Calling` `LLM API Integration` `Multi-Step Task Execution` `LangGraph` `AI Agent` `Research Automation` `Pluggable Architecture` `LLM Application`

## License

[MIT](LICENSE) © 2026 Yueting Zhang
