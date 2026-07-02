#!/usr/bin/env python3
"""Web Reader Tool 连通性测试。

验证网页抓取与正文提取是否正常工作。
"""

from research_agent.tools import get_web_reader


def main() -> None:
    reader = get_web_reader()

    # 测试两个不同结构的网站
    urls = [
        "https://httpbin.org/html",
        "https://www.python.org/doc/",
    ]

    for url in urls:
        print(f"{'='*60}")
        print(f"URL: {url}")
        print(f"{'='*60}")

        try:
            page = reader.read(url)
            print(f"标题: {page.title}")
            print(f"正文长度: {len(page.content)} 字符")
            print(f"正文预览:\n{page.content[:400]}...\n")
        except Exception as e:
            print(f"读取失败: {e}\n")


if __name__ == "__main__":
    main()
