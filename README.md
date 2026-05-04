# Język do budowania komponentów HTML i CSS

### Zespół i dane kontaktowe:
1.Maksymilian Gędłek - maksgedlek@student.agh.edu.pl

2.Kamil Maślanka - maslanka@student.agh.edu.pl

# Założenia

### Cel programu:
-Program ma na celu pisaniu w języku HTML i CSS za pomocą prostych poleceń

### Rodzaj translatora:
-Interpreter

### Planowany wynik działania programu:
-Interpreter HTML i CSS

### Planowany język implementacji:
-Python, parser LARK

### Opis tokenów (Lekser)

| Kod Tokena | Reguła / Wartość | Opis |
| :--- | :--- | :--- |
| `BEGIN` | `BEGIN` | Otwarcie bloku dokumentu |
| `END` | `END` | Zamknięcie bloku dokumentu |
| `TITLE_KW` | `TITLE` | Nagłówek główny (`<h1>`) |
| `SUBTITLE_KW` | `SUBTITLE` | Podtytuł (`<h2>`) |
| `TEXT_KW` | `TEXT` \| `PARAGRAPH` | Akapit tekstu (`<p>`) |
| `LINK_KW` | `LINK` | Hiperłącze (`<a>`) |
| `IMG_KW` | `IMAGE` | Obrazek (`<img>`) |
| `LIST_KW` | `LIST` | Definicja listy wyliczanej (`<ul>`/`<ol>`) |
| `ITEM_KW` | `ITEM` | Element listy (`<li>`) |
| `SECTION_KW` | `SECTION` | Kontener strukturalny (`<section>`) |
| `STYLE_KW` | `STYLE` | Otwarcie bloku definicji stylów |
| `BG_COLOR_KW` | `BG_COLOR` | Właściwość: kolor tła |
| `TEXT_COLOR_KW`| `TEXT_COLOR` | Właściwość: kolor tekstu |
| `FONT_SIZE_KW` | `FONT_SIZE` | Właściwość: rozmiar czcionki |
| `MARGIN_KW` | `MARGIN` | Właściwość: marginesy zewnętrzne |
| `PADDING_KW` | `PADDING` | Właściwość: odstępy wewnętrzne |
| `BORDER_KW` | `BORDER` | Właściwość: obramowanie |
| `IDENTIFIER` | `[a-zA-Z_][a-zA-Z0-9_]*` | Nazwy własne / identyfikatory klas |
| `STRING` | `"[^"]*"` | Napis w cudzysłowie |
| `INTEGER` | `[0-9]+` | Liczby całkowite |
| `HEX_COLOR` | `#[0-9a-fA-F]{3,6}` | Kod koloru HEX |
| `ASSIGN` | `=` \| `:=` | Operator przypisania |
| `LPAREN` | `(` | Nawias otwierający |
| `RPAREN` | `)` | Nawias zamykający |
| `LBRACE` | `{` | Klamra otwierająca blok |
| `RBRACE` | `}` | Klamra zamykająca blok |
| `SEMICOLON` | `;` | Koniec instrukcji |
| `COMMA` | `,` | Separator argumentów |

---

### Gramatyka (Parser)

```antlr
program
    : BEGIN instrukcja* END EOF
    ;

instrukcja
    : wstaw_naglowek
    | wstaw_podtytul
    | wstaw_akapit
    | wstaw_link
    | wstaw_obrazek
    | wstaw_liste
    | blok_sekcji
    | blok_stylu
    ;

wstaw_naglowek
    : TITLE_KW STRING SEMICOLON
    ;

wstaw_podtytul
    : SUBTITLE_KW STRING SEMICOLON
    ;

wstaw_akapit
    : TEXT_KW STRING SEMICOLON
    ;

wstaw_link
    : LINK_KW LPAREN STRING COMMA STRING RPAREN SEMICOLON
    ;

wstaw_obrazek
    : IMG_KW LPAREN STRING RPAREN SEMICOLON
    ;

wstaw_liste
    : LIST_KW IDENTIFIER? LBRACE element_listy+ RBRACE
    ;

element_listy
    : ITEM_KW STRING SEMICOLON
    ;

blok_sekcji
    : SECTION_KW IDENTIFIER LBRACE instrukcja* RBRACE
    ;

blok_stylu
    : STYLE_KW IDENTIFIER? LBRACE deklaracja_stylu* RBRACE
    ;

deklaracja_stylu
    : wlasciwosc_css ASSIGN wartosc SEMICOLON
    ;

wlasciwosc_css
    : BG_COLOR_KW
    | TEXT_COLOR_KW
    | FONT_SIZE_KW
    | MARGIN_KW
    | PADDING_KW
    | BORDER_KW
    ;

wartosc
    : STRING
    | INTEGER
    | HEX_COLOR
    | IDENTIFIER
    ;
