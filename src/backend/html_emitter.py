from __future__ import annotations

from dataclasses import is_dataclass

from src.ast import nodes as ast


def _escape_html(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _attr(name: str, value: str | None) -> str:
    if value is None:
        return ""
    return f' {name}="{_escape_html(value)}"'


class HtmlEmitter:
    def emit(self, doc: ast.Document) -> str:
        head = self._emit_head(doc.head)
        body = "\n  ".join(self._emit_node(n) for n in doc.body)
        return (
            "<!DOCTYPE html>\n"
            '<html lang="pl">\n'
            "<head>\n\n"
            '<meta charset="UTF-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            f"{head}"
            "\n</head>\n\n"
            "<body>\n\n"
            f"  {body}\n\n"
            "</body>\n\n"
            "</html>"
        )

    def _emit_head(self, head: ast.Head) -> str:
        if not head.styles:
            return ""
        css = "\n".join(self._emit_style_rule(r) for r in head.styles)
        return f"\n<style>\n{css}\n</style>\n"

    def _emit_style_rule(self, rule: ast.StyleRule) -> str:
        decls = "\n  ".join(f"{d.property_name}: {d.value};" for d in rule.declarations)
        return f"{rule.selector} {{\n  {decls}\n}}"

    def _emit_node(self, node: ast.Node) -> str:
        if not is_dataclass(node):
            raise TypeError(f"Expected AST dataclass node, got: {type(node)}")

        if isinstance(node, ast.Heading):
            return f"<h{node.level}{_attr('class', node.class_name)}>{_escape_html(node.text)}</h{node.level}>"
        if isinstance(node, ast.Paragraph):
            return f"<p{_attr('class', node.class_name)}>{_escape_html(node.text)}</p>"
        if isinstance(node, ast.Link):
            return f'<a href="{_escape_html(node.url)}">{_escape_html(node.label)}</a>'
        if isinstance(node, ast.Image):
            return f'<img src="{_escape_html(node.src)}" alt="{_escape_html(node.alt)}">'
        if isinstance(node, ast.Button):
            return f"<button{_attr('class', node.class_name)}>{_escape_html(node.text)}</button>"
        if isinstance(node, ast.ListBlock):
            tag = "ol" if node.ordered else "ul"
            items = "\n".join(f"  <li>{_escape_html(it.text)}</li>" for it in node.items)
            return f"<{tag}>\n{items}\n</{tag}>"
        if isinstance(node, ast.Div):
            inner = "\n  ".join(self._emit_node(c) for c in node.children)
            return f"<div{_attr('class', node.class_name)}>\n  {inner}\n</div>"
        if isinstance(node, ast.Section):
            inner = "\n  ".join(self._emit_node(c) for c in node.children)
            return f"<section{_attr('class', node.class_name)}>\n  {inner}\n</section>"

        raise TypeError(f"Unhandled AST node: {type(node)}")

