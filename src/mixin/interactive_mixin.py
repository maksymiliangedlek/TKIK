class InteractiveMixin:
    def put_button(self, args):
        return f"<button class={args[0]}>{args[1]}</button>"
