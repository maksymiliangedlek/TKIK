class TextMixin:
    def put_heading(self, args):
        if len(args) == 2:
            return f"<h1 class={args[0]}>{args[1]}</h1>"
        return f"<h1>{args[0]}</h1>"

    def put_subtitle(self, args):
        if len(args) == 2:
            return f"<h2 class={args[0]}>{args[1]}</h2>"
        return f"<h2>{args[0]}</h2>"

    def put_paragraph(self, args):
        if len(args) == 2:
            return f"<p class={args[0]}>{args[1]}</p>"
        return f"<p>{args[0]}</p>"

    def put_hyperlink(self, args):
        url, label = args
        return f'<a href="{url}">{label}</a>'