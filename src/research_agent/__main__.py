#!/usr/bin/env python3
"""AI Research Agent 命令行入口。

用法：
    python -m research_agent "你的研究主题"
"""

import sys

from research_agent.graph import graph


def main() -> None:
    topic = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("请输入研究主题: ")
    topic = topic.strip()
    if not topic:
        print("请提供一个研究主题。")
        sys.exit(1)

    print(f"\n>> 正在研究: {topic}\n")

    result = graph.invoke({"topic": topic})

    print(f"\n{'='*60}")
    print(">> 研究报告")
    print(f"{'='*60}")
    print(result.get("report", "无报告生成。"))


if __name__ == "__main__":
    main()
