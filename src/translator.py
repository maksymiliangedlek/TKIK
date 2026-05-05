from lark import Transformer
from src.mixin.style_mixin import StyleMixin
from src.mixin.values_mixin import ValuesMixin
from src.mixin.text_mixin import TextMixin
from src.mixin.container_mixin import ContainerMixin
from src.mixin.media_mixin import MediaMixin
from src.mixin.list_mixin import ListMixin
from src.mixin.interactive_mixin import InteractiveMixin

class HtmlTranslator(Transformer, StyleMixin, ValuesMixin, TextMixin, ContainerMixin, MediaMixin, ListMixin, InteractiveMixin):
    def start(self, children):
        head_elements = []
        body_elements = []

        for element in children:
            if element.startswith("<style>"):
                head_elements.append(element)
            else:
                body_elements.append(element)

        head_content = "\n  ".join(head_elements)
        body_content = "\n  ".join(body_elements)

        html_template = f"""<!DOCTYPE html>
<html lang="pl">
<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
{head_content}

</head>

<body>

{body_content}

</body>

</html>"""

        return html_template