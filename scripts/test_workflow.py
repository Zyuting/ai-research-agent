#!/usr/bin/env python3
"""Workflow 端到端测试。

运行一次完整的研究流程并保存报告到文件。
"""

import json
import sys
from pathlib import Path

from research_agent.graph import graph


def main() -> None:
    topic = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Python 异步编程的最佳实践"
    print(f"📋 测试主题: {topic}\n")

    result = graph.invoke({"topic": topic})

    # 输出统计
    print(f"\n📊 统计")
    print(f"  搜索关键词: {result.get('search_queries', [])}")
    print(f"  搜索结果数: {len(result.get('search_results', []))}")
    print(f"  成功读取页: {len(result.get('web_pages', []))}")
    print(f"  摘要长度: {len(result.get('summary', ''))} 字符")
    print(f"  报告长度: {len(result.get('report', ''))} 字符")

    # 保存报告
    safe_name = topic.replace(" ", "_").replace("/", "_")[:50]
    report_path = Path(f"reports/{safe_name}.md")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(result["report"], encoding="utf-8")
    print(f"\n📝 报告已保存: {report_path}")

    # 保存完整 trace（调试用）
    trace_path = Path(f"reports/{safe_name}_trace.json")
    trace = {
        k: v for k, v in result.items()
        if k != "report"
    }
    # 将 dataclass 序列化
    trace["search_results"] = [
        {"title": r.title, "url": r.url, "snippet": r.snippet[:100]}
        for r in trace.get("search_results", [])
    ]
    trace["web_pages"] = [
        {"title": p.title, "url": p.url, "content_length": len(p.content)}
        for p in trace.get("web_pages", [])
    ]
    trace_path.write_text(json.dumps(trace, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"📋 Trace 已保存: {trace_path}")


if __name__ == "__main__":
    main()
