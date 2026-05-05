from __future__ import annotations

from pathlib import Path

from lark import Lark


def build_parser(grammar_path: str | Path) -> Lark:
    grammar_path = Path(grammar_path)
    grammar_text = grammar_path.read_text(encoding="utf-8")
    return Lark(grammar_text, parser="lalr")

