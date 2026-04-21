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
-Python


### Opis tokenów:

| Kod Tokena | Reguła / Wartość | Opis |
| :--- | :--- | :--- |
| `BEGIN` | `BEGIN` | Otwarcie bloku programu / dokumentu |
| `END` | `END` | Zamknięcie bloku programu / dokumentu |
| `TITLE_KW` | `TITLE` | Słowo kluczowe dla nagłówka głównego (generuje `<h1>`) |
| `SUBTITLE_KW` | `SUBTITLE` | Słowo kluczowe dla podtytułu (generuje `<h2>`) |
| `TEXT_KW` | `TEXT` lub `PARAGRAPH` | Słowo kluczowe dla akapitu tekstu (generuje `<p>`) |
| `LINK_KW` | `LINK` | Słowo kluczowe dla hiperłącza (generuje `<a>`) |
| `STYLE_KW` | `STYLE` | Otwarcie bloku definiowania stylów CSS |
| `BG_COLOR_KW` | `BG_COLOR` | Właściwość CSS: kolor tła (`background-color`) |
| `TEXT_COLOR_KW`| `TEXT_COLOR` | Właściwość CSS: kolor tekstu (`color`) |
| `FONT_SIZE_KW` | `FONT_SIZE` | Właściwość CSS: rozmiar czcionki (`font-size`) |
| `IDENTIFIER` | `[a-zA-Z_][a-zA-Z0-9_]*` | Nazwy zmiennych lub identyfikatory klas/ID |
| `STRING` | `"[^"]*"` | Ciąg znaków w cudzysłowach (np. `"Hello world"`) |
| `INTEGER` | `[0-9]+` | Liczby całkowite (np. do określania pikseli, np. `16`) |
| `HEX_COLOR` | `#[0-9a-fA-F]{3,6}` | Kolor w formacie heksadecymalnym (np. `#FF0000`) |
| `ASSIGN` | `=` lub `:=` | Operator przypisania wartości do atrybutu/stylu |
| `LPAREN` | `(` | Nawias otwierający (np. na parametry tagu) |
| `RPAREN` | `)` | Nawias zamykający |
| `LBRACE` | `{` | Klamra otwierająca blok (np. w stylach) |
| `RBRACE` | `}` | Klamra zamykająca blok |
| `SEMICOLON` | `;` | Separator instrukcji (koniec linii komendy) |
| `COMMA` | `,` | Separator argumentów |
