from __future__ import annotations

from dataclasses import is_dataclass
from typing import TypeVar

from src.ast import nodes as ast

T = TypeVar("T", bound=ast.Node)

FONTAWESOME_CDN = (
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css"
)


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
    def __init__(self) -> None:
        self.variables: dict[str, str] = {}

    def emit(self, doc: ast.Document) -> tuple[str, str]:
        self.variables = dict(doc.variables)

        fonts = self._collect_nodes(doc.body, ast.Font)
        icons = self._collect_nodes(doc.body, ast.Icon)

        head_links = self._emit_external_links(fonts, icons)
        styles = self._emit_styles(doc.head)
        body = "\n  ".join(
            line
            for n in doc.body
            if (line := self._emit_node(n))
        )

        html = (
            "<!DOCTYPE html>\n"
            '<html lang="pl">\n'
            "<head>\n\n"
            '<meta charset="UTF-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            f"{head_links}"
            '<link rel="stylesheet" href="out.css">\n'
            "\n</head>\n\n"
            "<body>\n\n"
            f"  {body}\n\n"
            "</body>\n\n"
            "</html>"
        )
        return html, styles

    def _resolve_value(self, value: str) -> str:
        return self.variables.get(value, value)

    def _collect_nodes(self, nodes: list[ast.Node], node_type: type[T]) -> list[T]:
        found: list[T] = []
        for node in nodes:
            if isinstance(node, node_type):
                found.append(node)
            if isinstance(node, (ast.Div, ast.Section, ast.Form)):
                found.extend(self._collect_nodes(node.children, node_type))
        return found

    def _emit_external_links(self, fonts: list[ast.Font], icons: list[ast.Icon]) -> str:
        lines: list[str] = []
        if fonts:
            family_params = "&family=".join(
                f"{f.family.replace(' ', '+')}:wght@400;700" for f in fonts
            )
            lines.append(
                '<link rel="stylesheet" '
                f'href="https://fonts.googleapis.com/css2?family={family_params}&display=swap">'
            )
        if icons:
            lines.append(
                f'<link rel="stylesheet" href="{_escape_html(FONTAWESOME_CDN)}">'
            )
        if not lines:
            return ""
        return "\n".join(lines) + "\n"

    def _emit_styles(self, head: ast.Head) -> str:
        reset_css = (
            "* { margin: 0; padding: 0; box-sizing: border-box; }\n"
            "body { font-family: 'Segoe UI', Tahoma, sans-serif; }\n"
        )
        if not head.styles:
            return reset_css
        css = "\n".join(self._emit_style_rule(r) for r in head.styles)
        return f"{reset_css}{css}\n"

    def _emit_style_rule(self, rule: ast.StyleRule) -> str:
        decls = "\n  ".join(
            f"{d.property_name}: {self._resolve_value(d.value)};"
            for d in rule.declarations
        )
        return f"{rule.selector} {{\n  {decls}\n}}"

    def _normalize_icon_classes(self, icon_name: str, class_name: str | None) -> str:
        social_icons = ["facebook", "instagram", "linkedin", "twitter", "github"]

        prefix = "fa-brands" if icon_name.lower() in social_icons else "fa-solid"

        classes = [prefix, f"fa-{icon_name}"]
        if class_name:
            classes.append(class_name)

        return " ".join(classes)

    def _emit_node(self, node: ast.Node) -> str:
        if not is_dataclass(node):
            raise TypeError(f"Expected AST dataclass node, got: {type(node)}")

        # Head-only / metadata nodes — no HTML output in body
        if isinstance(node, (ast.Font, ast.VariableDefinition)):
            return ""

        if isinstance(node, ast.Heading):
            return (
                f"<h{node.level}{_attr('class', node.class_name)}>"
                f"{_escape_html(node.text)}</h{node.level}>"
            )
        if isinstance(node, ast.Paragraph):
            return f"<p{_attr('class', node.class_name)}>{_escape_html(node.text)}</p>"
        if isinstance(node, ast.Link):
            return (
                f'<a href="{_escape_html(node.url)}">'
                f"{_escape_html(node.label)}</a>"
            )
        if isinstance(node, ast.Image):
            return (
                f"<img{_attr('class', node.class_name)} "
                f'src="{_escape_html(node.src)}" '
                f'alt="{_escape_html(node.alt)}">'
            )
        if isinstance(node, ast.Button):
            return (
                f"<button{_attr('class', node.class_name)}>"
                f"{_escape_html(node.text)}</button>"
            )
        if isinstance(node, ast.Icon):
            classes = self._normalize_icon_classes(node.icon_class, node.class_name)
            return f'<i class="{_escape_html(classes)}"></i>'
        if isinstance(node, ast.ListBlock):
            tag = "ol" if node.ordered else "ul"
            items = "\n".join(
                f"  <li>{_escape_html(it.text)}</li>" for it in node.items
            )
            return f"<{tag}>\n{items}\n</{tag}>"
        if isinstance(node, ast.Div):
            inner = "\n  ".join(
                line for c in node.children if (line := self._emit_node(c))
            )
            return f"<div{_attr('class', node.class_name)}>\n  {inner}\n</div>"
        if isinstance(node, ast.Section):
            inner = "\n  ".join(
                line for c in node.children if (line := self._emit_node(c))
            )
            return f"<section{_attr('class', node.class_name)}>\n  {inner}\n</section>"
        if isinstance(node, ast.Input):
            return (
                f'<input type="text"{_attr("class", node.class_name)} '
                f'placeholder="{_escape_html(node.text)}">'
            )
        if isinstance(node, ast.Form):
            inner = "\n  ".join(
                line for c in node.children if (line := self._emit_node(c))
            )
            return f'<form action="#"{_attr("class", node.class_name)}>\n  {inner}\n</form>'

        raise TypeError(f"Unhandled AST node: {type(node)}")
