#!/usr/bin/env python3
"""LLM 连通性测试。

用法：
    python scripts/test_llm.py

验证通过后终端会打印 AI 回复和 token 用量。
"""

from research_agent.llm import get_llm


def main() -> None:
    llm = get_llm()

    print(f"Model: {llm.model}")
    print("-" * 40)

    resp = llm.invoke("你好，请用一句话介绍自己。")

    print(f"Response: {resp.content}")
    print(f"Usage  : {resp.usage}")


if __name__ == "__main__":
    main()
