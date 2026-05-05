from pathlib import Path

from src.backend.html_emitter import HtmlEmitter
from src.frontend.ast_builder import AstBuilder
from src.frontend.parser import build_parser


def main():
    root = Path(__file__).resolve().parent
    grammar_path = root / "frontend" / "grammar.lark"
    input_path = root / "in.txt"
    output_path_html = root / "out.html"
    output_path_css = root / "out.css"

    parser = build_parser(grammar_path)
    source_code = input_path.read_text(encoding="utf-8")

    try:
        tree = parser.parse(source_code)
        ast = AstBuilder().transform(tree)
        html_output, css_output = HtmlEmitter().emit(ast)
        output_path_html.write_text(html_output, encoding="utf-8")
        output_path_css.write_text(css_output, encoding="utf-8")
    except Exception as e:
        print(f"Compilation error:\n{e}")


if __name__ == "__main__":
    main()