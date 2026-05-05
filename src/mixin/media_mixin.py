class MediaMixin:
    def put_image(self, args):
        path = args[0]
        return f'<img src="{path}" alt="image">'