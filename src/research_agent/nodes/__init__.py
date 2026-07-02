"""Workflow nodes — each node is a self-contained function.

Nodes communicate only through ResearchState. Every node receives
a ResearchState dict and returns a partial dict to be merged.
"""

from research_agent.nodes.planner import planner_node
from research_agent.nodes.reader import reader_node
from research_agent.nodes.search_node import search_node
from research_agent.nodes.summarizer import summarizer_node
from research_agent.nodes.writer import writer_node

__all__ = [
    "planner_node",
    "search_node",
    "reader_node",
    "summarizer_node",
    "writer_node",
]
