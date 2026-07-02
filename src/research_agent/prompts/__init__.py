"""Prompt 加载工具。"""

from __future__ import annotations

import pathlib

_PROMPTS_DIR = pathlib.Path(__file__).parent


def load_prompt(name: str, **kwargs: str) -> str:
    """加载 prompt 模板并填充变量。

    Args:
        name: 模板文件名（不含路径，如 planner.txt）。
        **kwargs: 模板变量值。

    Returns:
        填充后的 prompt 字符串。
    """
    path = _PROMPTS_DIR / name
    template = path.read_text(encoding="utf-8")
    return template.format(**kwargs)


def list_prompts() -> list[str]:
    """列出所有可用的 prompt 模板。"""
    return sorted(p.name for p in _PROMPTS_DIR.glob("*.txt"))
