import html
import re
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs

from src.webapp.compiler import compile_source

WEBAPP_DIR = Path(__file__).resolve().parent
STATIC_DIR = WEBAPP_DIR / "static"
TEMPLATE = (WEBAPP_DIR / "template.html").read_text(encoding="utf-8")

DEFAULT_SOURCE = "BEGIN\n\nEND\n"


def make_preview(html_out: str, css_out: str) -> str:
    if not html_out:
        return ""
    style = f"<style>{css_out}</style>"
    preview = re.sub(
        r'<link\s+rel=["\']stylesheet["\']\s+href=["\']out\.css["\']\s*/?>',
        style,
        html_out,
        flags=re.I,
    )
    if preview == html_out and "</head>" in html_out:
        preview = html_out.replace("</head>", style + "</head>", 1)
    return preview


def render_page(source: str, result: dict | None = None) -> str:
    if result is None:
        result = {"success": False, "html": "", "css": "", "errors": []}
    error_lines = sorted({e["line"] for e in result["errors"] if e["line"] > 0})

    if result["errors"]:
        errors_html = ""
        for err in result["errors"]:
            if err["line"] > 0:
                loc = f"Line {err['line']}, column {err['column']}: "
            else:
                loc = ""
            errors_html += (
                f'<p class="error" data-line="{err["line"]}">'
                f"{html.escape(loc + err['message'])}</p>\n"
            )
    else:
        if result["success"]:
            errors_html = '<p class="ok">Poprawnie skompilowano.</p>'
        else:
            errors_html = '<p class="muted">Kliknij Kompiluj, aby sprawdzić swój kod.</p>'

    preview = make_preview(result["html"], result["css"])

    return (
        TEMPLATE.replace("{{SOURCE}}", html.escape(source))
        .replace("{{HTML}}", html.escape(result["html"]))
        .replace("{{CSS}}", html.escape(result["css"]))
        .replace("{{PREVIEW}}", html.escape(preview))
        .replace("{{ERRORS}}", errors_html)
        .replace("{{ERROR_LINES}}", ",".join(str(n) for n in error_lines))
    )


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path.startswith("/static/"):
            self._send_file(STATIC_DIR / path[len("/static/") :])
        elif path in ("/", "/index.html"):
            self._send_html(render_page(DEFAULT_SOURCE))
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path.split("?", 1)[0] not in ("/", "/index.html"):
            self.send_error(404)
            return

        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length).decode("utf-8") if length else ""
        params = parse_qs(body, keep_blank_values=True)
        source = params.get("source", [DEFAULT_SOURCE])[0]

        result = compile_source(source)
        self._send_html(render_page(source, result))

    def _send_html(self, text: str):
        data = text.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _send_file(self, path: Path):
        if not path.is_file():
            self.send_error(404)
            return
        data = path.read_bytes()
        if path.suffix == ".css":
            ctype = "text/css"
        elif path.suffix == ".js":
            ctype = "text/javascript"
        else:
            ctype = "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def run(host: str = "127.0.0.1", port: int = 8000):
    url = f"http://{host}:{port}/"
    print(f"Web UI: {url}")
    print("Press Ctrl+C to stop.")
    try:
        HTTPServer((host, port), Handler).serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
