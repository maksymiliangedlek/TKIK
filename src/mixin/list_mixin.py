class ListMixin:
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
