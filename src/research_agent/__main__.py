"""CLI entry point for Research Agent.

Usage:
    python -m research_agent "your research topic"
"""

import sys

from research_agent.graph import graph


def main() -> None:
    topic = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Enter research topic: ")
    topic = topic.strip()
    if not topic:
        print("Please provide a research topic.")
        sys.exit(1)

    print(f"\n>> Researching: {topic}\n")

    result = graph.invoke({"topic": topic})

    print(f"\n{'='*60}")
    print(">> Research Report")
    print(f"{'='*60}")
    print(result.get("report", "No report generated."))


if __name__ == "__main__":
    main()
