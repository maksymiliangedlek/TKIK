from lark import Lark
from translator import HtmlTranslator


def main():
    with open("grammar.lark", "r", encoding="utf-8") as f:
        grammar_text = f.read()

    parser = Lark(grammar_text, parser='lalr')

    with open("in.txt", "r", encoding="utf-8") as f:
        source_code = f.read()

    try:
        tree = parser.parse(source_code)
        translator = HtmlTranslator()
        html_output = translator.transform(tree)

        with open("out.html", "w", encoding="utf-8") as f:
            f.write(html_output)
    except Exception as e:
        print(f"Compilation error:\n{e}")


if __name__ == "__main__":
    main()