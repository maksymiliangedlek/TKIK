"""Small compile function shared by CLI and web UI."""

from pathlib import Path

from lark.exceptions import UnexpectedCharacters, UnexpectedEOF, UnexpectedInput, UnexpectedToken

from src.backend.html_emitter import HtmlEmitter
from src.frontend.ast_builder import AstBuilder
from src.frontend.parser import build_parser

GRAMMAR_PATH = Path(__file__).resolve().parent.parent / "frontend" / "grammar.lark"
_parser = None


def compile_source(source: str) -> dict:
    """Compile DSL text.

    Returns: {"success": bool, "html": str, "css": str, "errors": list[dict]}
    Error item: {"line": int, "column": int, "message": str}
    """
    global _parser
    if _parser is None:
        _parser = build_parser(GRAMMAR_PATH)

    try:
        tree = _parser.parse(source)
        ast = AstBuilder().transform(tree)
        html, css = HtmlEmitter().emit(ast)
        return {"success": True, "html": html, "css": css, "errors": []}
    except UnexpectedInput as err:
        return {"success": False, "html": "", "css": "", "errors": [_lark_error(err)]}
    except Exception as err:
        return {"success": False, "html": "", "css": "", "errors": [{"line": 0, "column": 0, "message": str(err)}]}


def _lark_error(err: UnexpectedInput) -> dict:
    line = int(getattr(err, "line", 0) or 0)
    column = int(getattr(err, "column", 0) or 0)

    if isinstance(err, UnexpectedToken):
        token = getattr(err, "token", None)
        got = repr(getattr(token, "value", token))
        expected = ", ".join(sorted(getattr(err, "expected", []) or [])) or "?"
        message = f"Unexpected token {got}. Expected one of: {expected}"
    elif isinstance(err, UnexpectedCharacters):
        message = "Unexpected character"
    elif isinstance(err, UnexpectedEOF):
        expected = ", ".join(sorted(getattr(err, "expected", []) or [])) or "?"
        message = f"Unexpected end of input. Expected one of: {expected}"
    else:
        message = str(err).split("\n", 1)[0]

    return {"line": line, "column": column, "message": message}
