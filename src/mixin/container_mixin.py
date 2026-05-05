class ContainerMixin:
    def div_with_class(self,args):
        content_class = args[0]
        content = "".join(args[1:])
        return f"<div class={content_class}>\n{content}</div>"

    def div_no_class(self,args):
        content = "".join(args)
        return f"<div>\n{content}</div>"

    def section_with_class(self,args):
        content_class = args[0]
        content = "".join(args[1:])
        return f"<section class={content_class}>\n{content}</section>"

    def section_no_class(self,args):
        content = "".join(args)
        return f"<section>\n{content}</section>"