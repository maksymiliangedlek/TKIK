class StyleMixin:
    def bg_color(self, _): return "background-color"

    def text_color(self, _): return "color"
    def font_weight(self, _): return "font-weight"
    def text_align(self, _): return "text-align"
    def font_size(self, _): return "font-size"

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
        property_name, value = args
        return f"{property_name}: {value};"

    def block_style(self, args):
        style_name, *declarations = args
        content = "\n  ".join(declarations)
        return f"<style>\n.{style_name} {{\n  {content}\n}}\n</style>"

    def hover_style(self, args):
        style_name, *declarations = args
        content = "\n  ".join(declarations)
        return f"<style>\n.{style_name}:hover {{\n  {content}\n}}\n</style>"

    def hover_child_style(self, args):
        parent_class, child_class, *declarations = args
        content = "\n  ".join(declarations)
        return f"<style>\n.{parent_class}:hover .{child_class} {{\n  {content}\n}}\n</style>"