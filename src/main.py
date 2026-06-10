from pathlib import Path

from src.webapp.compiler import compile_source


def main():
    root = Path(__file__).resolve().parent
    source = (root / "in.txt").read_text(encoding="utf-8")
    result = compile_source(source)

    if result["success"]:
        (root / "out.html").write_text(result["html"], encoding="utf-8")
        (root / "out.css").write_text(result["css"], encoding="utf-8")
    else:
        message = "\n".join(e["message"] for e in result["errors"])
        print(f"Compilation error:\n{message}")


if __name__ == "__main__":
    main()