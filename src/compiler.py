from lark import Lark, Transformer

my_grammar = r"""
    start: "BEGIN" instrukcja* "END"

    ?instrukcja: wstaw_naglowek
              | wstaw_podtytul
              | wstaw_akapit
              | wstaw_link
              | blok_stylu

    wstaw_naglowek: "TITLE" STRING ";"
    wstaw_podtytul: "SUBTITLE" STRING ";"
    wstaw_akapit: "TEXT" STRING ";"
    wstaw_link: "LINK" STRING STRING ";"

    blok_stylu: "STYLE" IDENTIFIER "{" deklaracja_stylu* "}"
    deklaracja_stylu: wlasciwosc_css "=" wartosc ";"

    wlasciwosc_css: "BG_COLOR" -> bg_color
                  | "TEXT_COLOR" -> text_color
                  | "FONT_SIZE" -> font_size

    ?wartosc: STRING | INTEGER | HEX_COLOR | IDENTIFIER

    # Definicje tokenów
    IDENTIFIER: /[a-zA-Z_][a-zA-Z0-9_]*/
    STRING: /"[^"]*"/
    INTEGER: /[0-9]+/
    HEX_COLOR: /#[0-9a-fA-F]{3,6}/

    %import common.WS
    %ignore WS
"""


class HtmlTranslator(Transformer):
    def STRING(self, s):
        return s.strip('"')

    def INTEGER(self, i):
        return str(i)

    def IDENTIFIER(self, id):
        return str(id)

    def HEX_COLOR(self, h):
        return str(h)

    # Metody transformujące reguły
    def wstaw_naglowek(self, args):
        return f"<h1>{args[0]}</h1>"

    def wstaw_podtytul(self, args):
        return f"<h2>{args[0]}</h2>"

    def wstaw_akapit(self, args):
        return f"<p>{args[0]}</p>"

    def wstaw_link(self, args):
        url, label = args
        return f'<a href="{url}">{label}</a>'

    def bg_color(self, _): return "background-color"

    def text_color(self, _): return "color"

    def font_size(self, _): return "font-size"

    def deklaracja_stylu(self, args):
        wlasciwosc, wartosc = args
        return f"{wlasciwosc}: {wartosc};"

    def blok_stylu(self, args):
        nazwa_stylu, *deklaracje = args
        content = "\n  ".join(deklaracje)
        return f"<style>\n.{nazwa_stylu} {{\n  {content}\n}}\n</style>"

    def start(self, children):
        return "\n".join(children)


code = """
BEGIN
    TITLE "Moja Strona";
    STYLE MojaKlasa {
        BG_COLOR = #ff0000;
        FONT_SIZE = 18;
    }
    TEXT "Witaj w moim generatorze!";
    LINK "https://google.com" "Kliknij tutaj";
END
"""

parser = Lark(my_grammar, parser='lalr')

try:
    tree = parser.parse(code)
    result = HtmlTranslator().transform(tree)
    print(result)

    with open('test.html', 'w') as f:
        f.write(result)
except Exception as e:
    print(f"Błąd: {e}")