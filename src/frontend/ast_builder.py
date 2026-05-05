from __future__ import annotations

from lark import Transformer

from src.ast.nodes import (
    Button,
    CssDeclaration,
    Div,
    Document,
    Head,
    Heading,
    Image,
    Link,
    ListBlock,
    ListItem,
    Paragraph,
    Section,
    StyleRule,
)


class AstBuilder(Transformer):
    # ---- tokens -> python primitives ----
    def STRING(self, s):
        return s.strip('"')

    def INTEGER(self, i):
        return str(i)

    def IDENTIFIER(self, id_):
        return str(id_)

    def HEX_COLOR(self, h):
        return str(h)

    def DIMENSION(self, d):
        return str(d)

    def ORDERED(self, _):
        return "ORDERED"

    def UNORDERED(self, _):
        return "UNORDERED"

    # ---- body nodes ----
    def put_heading(self, args):
        if len(args) == 2:
            class_name, text = args
            return Heading(level=1, text=text, class_name=class_name)
        (text,) = args
        return Heading(level=1, text=text)

    def put_subtitle(self, args):
        if len(args) == 2:
            class_name, text = args
            return Heading(level=2, text=text, class_name=class_name)
        (text,) = args
        return Heading(level=2, text=text)

    def put_paragraph(self, args):
        if len(args) == 2:
            class_name, text = args
            return Paragraph(text=text, class_name=class_name)
        (text,) = args
        return Paragraph(text=text)

    def put_hyperlink(self, args):
        url, label = args
        return Link(url=url, label=label)

    def put_image(self, args):
        (src,) = args
        return Image(src=src)

    def put_button(self, args):
        if len(args) == 2:
            class_name, text = args
            return Button(text=text, class_name=class_name)
        (text,) = args
        return Button(text=text)

    def item(self, args):
        (text,) = args
        return ListItem(text=text)

    def put_list(self, args):
        ordered = False
        items = args
        if args and str(args[0]).upper() in ["ORDERED", "UNORDERED"]:
            ordered = str(args[0]).upper() == "ORDERED"
            items = args[1:]
        return ListBlock(ordered=ordered, items=list(items))

    def put_div(self, args):
        class_name = None
        children = args
        if args and isinstance(args[0], str):
            class_name = args[0]
            children = args[1:]
        return Div(class_name=class_name, children=list(children))

    def put_section(self, args):
        class_name = None
        children = args
        if args and isinstance(args[0], str):
            class_name = args[0]
            children = args[1:]
        return Section(class_name=class_name, children=list(children))

    # ---- CSS properties ----
    def bg_color(self, _): return "background-color"
    def text_color(self, _): return "color"
    def font_size(self, _): return "font-size"
    def font_weight(self, _): return "font-weight"
    def text_align(self, _): return "text-align"

    def margin_top(self, _): return "margin-top"
    def margin_bottom(self, _): return "margin-bottom"
    def margin_left(self, _): return "margin-left"
    def margin_right(self, _): return "margin-right"

    def padding_top(self, _): return "padding-top"
    def padding_bottom(self, _): return "padding-bottom"
    def padding_left(self, _): return "padding-left"
    def padding_right(self, _): return "padding-right"

    def width(self, _): return "width"
    def height(self, _): return "height"

    def border_radius(self, _): return "border-radius"
    def border_width(self, _): return "border-width"
    def border_style(self, _): return "border-style"
    def border_color(self, _): return "border-color"

    def display(self, _): return "display"
    def justify_content(self, _): return "justify-content"
    def align_items(self, _): return "align-items"
    def opacity(self, _): return "opacity"
    def cursor(self, _): return "cursor"
    def position(self, _): return "position"
    def top(self, _): return "top"
    def z_index(self, _): return "z-index"

    def style_declaration(self, args):
        prop, value = args
        return CssDeclaration(property_name=prop, value=value)

    def block_style(self, args):
        style_name, *decls = args
        return StyleRule(selector=f".{style_name}", declarations=decls)

    def hover_style(self, args):
        style_name, *decls = args
        return StyleRule(selector=f".{style_name}:hover", declarations=decls)

    def hover_child_style(self, args):
        parent_class, child_class, *decls = args
        return StyleRule(selector=f".{parent_class}:hover .{child_class}", declarations=decls)

    # ---- document root ----
    def start(self, children):
        styles: list[StyleRule] = []
        body = []
        for node in children:
            if isinstance(node, StyleRule):
                styles.append(node)
            else:
                body.append(node)
        return Document(head=Head(styles=styles), body=body)

