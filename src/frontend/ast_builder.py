from __future__ import annotations

from lark import Transformer

from src.ast.nodes import *


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
        if len(args) == 2:
            class_name, src = args
            return Image(src=src, class_name=class_name)
        (src,) = args
        return Image(src=src)

    def put_button(self, args):
        if len(args) == 2:
            class_name, text = args
            return Button(text=text, class_name=class_name)
        (text,) = args
        return Button(text=text)

    def put_font(self, args):
        (family,) = args
        return Font(family=family)

    def put_icon(self, args):
        if len(args) == 2:
            icon_class, class_name = args
            return Icon(icon_class=icon_class, class_name=class_name)
        (icon_class,) = args
        return Icon(icon_class=icon_class)

    def define_var(self, args):
        name, value = args
        return VariableDefinition(name=name, value=str(value))

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

    def put_input(self, args):
        if len(args) == 2:
            class_name, text = args
            return Input(text=text, class_name=class_name)
        (text,) = args
        return Input(text=text)

    def put_form(self, args):
        class_name = None
        children = args
        if args and isinstance(args[0], str):
            class_name = args[0]
            children = args[1:]
        return Form(class_name=class_name, children=list(children))

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
    def font_family(self, _): return "font-family"
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
    def max_width(self, _): return "max-width"

    def border_radius(self, _): return "border-radius"
    def border_width(self, _): return "border-width"
    def border_style(self, _): return "border-style"
    def border_color(self, _): return "border-color"

    def display(self, _): return "display"
    def flex_direction(self, _): return "flex-direction"
    def justify_content(self, _): return "justify-content"
    def align_items(self, _): return "align-items"
    def gap(self, _): return "gap"
    def opacity(self, _): return "opacity"
    def cursor(self, _): return "cursor"
    def position(self, _): return "position"
    def top(self, _): return "top"
    def bottom(self, _): return "bottom"
    def left(self, _): return "left"
    def right(self, _): return "right"
    def z_index(self, _): return "z-index"
    def overflow(self, _): return "overflow"
    def box_shadow(self, _): return "box-shadow"
    def transition(self, _): return "transition"

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
        body: list[Node] = []
        variables: dict[str, str] = {}

        for node in children:
            if isinstance(node, VariableDefinition):
                variables[node.name] = node.value
            elif isinstance(node, StyleRule):
                styles.append(node)
            else:
                body.append(node)

        return Document(head=Head(styles=styles), body=body, variables=variables)
