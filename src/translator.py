from lark import Transformer

class HtmlTranslator(Transformer):
    def STRING(self, s):
        return s.strip('"')

    def INTEGER(self, i):
        return str(i)

    def IDENTIFIER(self, id):
        return str(id)

    def HEX_COLOR(self, h):
        return str(h)

    def put_heading(self, args):
        return f"<h1>{args[0]}</h1>"

    def put_subtitle(self, args):
        return f"<h2>{args[0]}</h2>"

    def put_paragraph(self, args):
        return f"<p>{args[0]}</p>"

    def put_image(self, args):
        path = args[0]
        return f'<img src="{path}" alt="image">'

    def item(self, args):
        content = args[0]
        return f"  <li>{content}</li>"

    def put_list(self, args):
        if args and str(args[0]).upper() in ["ORDERED", "UNORDERED"]:
            list_type = str(args[0]).upper()
            items = args[1:]
        else:
            list_type = "UNORDERED"
            items = args

        content = "\n".join(items)

        if list_type == "ORDERED":
            return f"<ol>\n{content}\n</ol>"
        else:
            return f"<ul>\n{content}\n</ul>"

    def put_hyperlink(self, args):
        url, label = args
        return f'<a href="{url}">{label}</a>'

    def bg_color(self, _): return "background-color"

    def text_color(self, _): return "color"

    def font_size(self, _): return "font-size"

    def style_declaration(self, args):
        property_name, value = args
        return f"{property_name}: {value};"

    def block_style(self, args):
        style_name, *declarations = args
        content = "\n  ".join(declarations)
        return f"<style>\n.{style_name} {{\n  {content}\n}}\n</style>"

    def start(self, children):
        return "\n".join(children)