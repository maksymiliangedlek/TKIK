# Język do budowania komponentów HTML i CSS

### Zespół i dane kontaktowe:
1.Maksymilian Gędłek - maksgedlek@student.agh.edu.pl

2.Kamil Maślanka - maslanka@student.agh.edu.pl

# Założenia

### Cel programu:
-Program ma na celu pisaniu w języku HTML i CSS za pomocą prostych poleceń

### Rodzaj translatora:
-Transpiler

### Planowany wynik działania programu:
-Generator plików statycznych HTML i CSS

### Język implementacji:
- Python, parser **Lark** 

### Architektura transpilera

```
DSL (in.txt) → Parser → AST (dataclasses) → HTML Emitter → out.html + out.css
```


### Opis tokenów (Lekser)

Poniższa tabela odpowiada aktualnej gramatyce w `src/frontend/grammar.lark`.

#### Słowa kluczowe — dokument

| Token | Wartość | Opis |
| :--- | :--- | :--- |
| `BEGIN` | `BEGIN` | Otwarcie bloku dokumentu |
| `END` | `END` | Zamknięcie bloku dokumentu |
| `DEFINE` | `DEFINE` | Definicja zmiennej CSS (np. `DEFINE KOLOR #598C32;`) |

#### Słowa kluczowe — elementy HTML

| Token | Wartość | Opis |
| :--- | :--- | :--- |
| `TITLE` | `TITLE` | Nagłówek główny (`<h1>`), opcjonalna klasa CSS |
| `SUBTITLE` | `SUBTITLE` | Podtytuł (`<h2>`), opcjonalna klasa CSS |
| `TEXT` | `TEXT` | Akapit (`<p>`), opcjonalna klasa CSS |
| `LINK` | `LINK` | Hiperłącze (`<a href="...">`) |
| `IMAGE` | `IMAGE` | Obrazek (`<img>`), opcjonalna klasa CSS |
| `LIST` | `LIST` | Lista (`<ul>` / `<ol>`), opcjonalnie `ORDERED` lub `UNORDERED` |
| `ITEM` | `ITEM` | Element listy (`<li>`) |
| `BUTTON` | `BUTTON` | Przycisk (`<button>`), opcjonalna klasa CSS |
| `INPUT` | `INPUT` | Pole tekstowe (`<input type="text">`), opcjonalna klasa CSS |
| `FORM` | `FORM` | Formularz (`<form>`) z blokiem instrukcji |
| `DIV` | `DIV` | Kontener (`<div>`), opcjonalna klasa CSS |
| `SECTION` | `SECTION` | Sekcja (`<section>`), opcjonalna klasa CSS |
| `FONT` | `FONT` | Import czcionki Google Fonts (np. `FONT "Roboto";`) |
| `ICON` | `ICON` | Ikona Font Awesome (np. `ICON "envelope" Klasa;`) |

#### Słowa kluczowe — style CSS

| Token | Wartość | Opis |
| :--- | :--- | :--- |
| `STYLE` | `STYLE` | Blok reguły CSS dla klasy (`.NazwaKlasy { ... }`) |
| `HOVER` | `HOVER` | Reguła `:hover` dla klasy |
| `HOVER_CHILD` | `HOVER_CHILD` | Reguła `:hover .dziecko` (dwa identyfikatory) |
| `ORDERED` | `ORDERED` (bez rozróżniania wielkości liter) | Lista numerowana (`<ol>`) |
| `UNORDERED` | `UNORDERED` (bez rozróżniania wielkości liter) | Lista punktowana (`<ul>`) |

#### Właściwości CSS (`css_property`)

| Token | Mapowanie CSS | Opis |
| :--- | :--- | :--- |
| `BG_COLOR` | `background-color` | Kolor tła |
| `TEXT_COLOR` | `color` | Kolor tekstu |
| `FONT_SIZE` | `font-size` | Rozmiar czcionki |
| `FONT_WEIGHT` | `font-weight` | Grubość czcionki |
| `FONT_FAMILY` | `font-family` | Rodzina czcionki |
| `TEXT_ALIGN` | `text-align` | Wyrównanie tekstu |
| `MARGIN_TOP` | `margin-top` | Górny margines |
| `MARGIN_BOTTOM` | `margin-bottom` | Dolny margines |
| `MARGIN_LEFT` | `margin-left` | Lewy margines |
| `MARGIN_RIGHT` | `margin-right` | Prawy margines |
| `PADDING_TOP` | `padding-top` | Górny padding |
| `PADDING_BOTTOM` | `padding-bottom` | Dolny padding |
| `PADDING_LEFT` | `padding-left` | Lewy padding |
| `PADDING_RIGHT` | `padding-right` | Prawy padding |
| `WIDTH` | `width` | Szerokość |
| `HEIGHT` | `height` | Wysokość |
| `MAX_WIDTH` | `max-width` | Maksymalna szerokość |
| `BORDER_RADIUS` | `border-radius` | Zaokrąglenie rogów |
| `BORDER_WIDTH` | `border-width` | Grubość obramowania |
| `BORDER_STYLE` | `border-style` | Styl obramowania |
| `BORDER_COLOR` | `border-color` | Kolor obramowania |
| `DISPLAY` | `display` | Typ wyświetlania (np. `flex`, `none`) |
| `FLEX_DIRECTION` | `flex-direction` | Kierunek flexbox |
| `JUSTIFY_CONTENT` | `justify-content` | Wyrównanie w osi głównej |
| `ALIGN_ITEMS` | `align-items` | Wyrównanie w osi poprzecznej |
| `GAP` | `gap` | Odstęp między elementami flex/grid |
| `OPACITY` | `opacity` | Przezroczystość |
| `CURSOR` | `cursor` | Kursor myszy |
| `POSITION` | `position` | Pozycjonowanie |
| `TOP` | `top` | Odległość od góry |
| `BOTTOM` | `bottom` | Odległość od dołu |
| `LEFT` | `left` | Odległość od lewej |
| `RIGHT` | `right` | Odległość od prawej |
| `Z_INDEX` | `z-index` | Warstwa (stacking) |
| `OVERFLOW` | `overflow` | Przepełnienie |
| `BOX_SHADOW` | `box-shadow` | Cień |
| `TRANSITION` | `transition` | Animacja przejścia |

#### Literały i typy wartości

| Token | Reguła / Wartość | Opis |
| :--- | :--- | :--- |
| `IDENTIFIER` | `/[a-zA-Z_][a-zA-Z0-9_]*/` | Nazwa klasy, zmiennej lub identyfikator |
| `STRING` | `/"[^"]*"/` | Napis w cudzysłowie |
| `INTEGER` | `/[0-9]+/` | Liczba całkowita |
| `HEX_COLOR` | `/#[0-9a-fA-F]{3,6}/` | Kolor w formacie HEX |
| `DIMENSION` | `INTEGER` + opcjonalnie `UNIT` | Wymiar z jednostką (np. `20px`, `5%`) |
| `UNIT` | `px` \| `em` \| `rem` \| `%` \| `pt` | Jednostka wymiaru |

Wartość właściwości CSS (`value`) może być: `STRING`, `INTEGER`, `HEX_COLOR`, `IDENTIFIER` (np. nazwa zmiennej z `DEFINE`) lub `DIMENSION`.

#### Symbole i komentarze

| Symbol | Opis |
| :--- | :--- |
| `{` `}` | Otwarcie / zamknięcie bloku instrukcji lub stylu |
| `;` | Koniec instrukcji |
| `=` | Przypisanie wartości właściwości CSS |
| `/* ... */` | Komentarz blokowy (ignorowany) |
| `// ...` | Komentarz liniowy (ignorowany) |
| białe znaki | Ignorowane (`WS`, `NEWLINE`) |

---

### Gramatyka (Parser)

Plik źródłowy: `src/frontend/grammar.lark`

```lark
start: "BEGIN" instruction* "END"

?instruction: put_heading
            | put_subtitle
            | put_paragraph
            | put_hyperlink
            | put_image
            | put_list
            | put_button
            | put_input
            | put_form
            | put_div
            | put_section
            | put_font
            | put_icon
            | define_var
            | block_style

put_heading: "TITLE" [IDENTIFIER] STRING ";"
put_subtitle: "SUBTITLE" [IDENTIFIER] STRING ";"
put_paragraph: "TEXT" [IDENTIFIER] STRING ";"
put_hyperlink: "LINK" STRING STRING ";"
put_image: "IMAGE" [IDENTIFIER] STRING ";"
put_list: "LIST" [(ORDERED | UNORDERED)] "{" item* "}" ";"
put_button: "BUTTON" [IDENTIFIER] STRING ";"
put_input: "INPUT" [IDENTIFIER] STRING ";"
put_form: "FORM" [IDENTIFIER] "{" instruction* "}" ";" -> put_form
put_font: "FONT" STRING ";"
put_icon: "ICON" STRING [IDENTIFIER] ";"

define_var: "DEFINE" IDENTIFIER value ";"

put_div: "DIV" [IDENTIFIER] "{" instruction* "}" ";" -> put_div
put_section: "SECTION" [IDENTIFIER] "{" instruction* "}" ";" -> put_section

item: "ITEM" STRING ";"

block_style: "STYLE" IDENTIFIER "{" style_declaration* "}"
           | "HOVER" IDENTIFIER "{" style_declaration* "}" -> hover_style
           | "HOVER_CHILD" IDENTIFIER IDENTIFIER "{" style_declaration* "}" -> hover_child_style
style_declaration: css_property "=" value ";"

css_property: "BG_COLOR" -> bg_color
            | "TEXT_COLOR" -> text_color
            | "FONT_SIZE" -> font_size
            | "FONT_WEIGHT" -> font_weight
            | "FONT_FAMILY" -> font_family
            | "TEXT_ALIGN" -> text_align
            | "MARGIN_TOP" -> margin_top
            | "MARGIN_BOTTOM" -> margin_bottom
            | "MARGIN_LEFT" -> margin_left
            | "MARGIN_RIGHT" -> margin_right
            | "PADDING_TOP" -> padding_top
            | "PADDING_BOTTOM" -> padding_bottom
            | "PADDING_LEFT" -> padding_left
            | "PADDING_RIGHT" -> padding_right
            | "WIDTH" -> width
            | "HEIGHT" -> height
            | "MAX_WIDTH" -> max_width
            | "BORDER_RADIUS" -> border_radius
            | "BORDER_WIDTH" -> border_width
            | "BORDER_STYLE" -> border_style
            | "BORDER_COLOR" -> border_color
            | "DISPLAY" -> display
            | "FLEX_DIRECTION" -> flex_direction
            | "JUSTIFY_CONTENT" -> justify_content
            | "ALIGN_ITEMS" -> align_items
            | "GAP" -> gap
            | "OPACITY" -> opacity
            | "CURSOR" -> cursor
            | "POSITION" -> position
            | "TOP" -> top
            | "BOTTOM" -> bottom
            | "LEFT" -> left
            | "RIGHT" -> right
            | "Z_INDEX" -> z_index
            | "OVERFLOW" -> overflow
            | "BOX_SHADOW" -> box_shadow
            | "TRANSITION" -> transition

?value: STRING | INTEGER | HEX_COLOR | IDENTIFIER | DIMENSION

IDENTIFIER: /[a-zA-Z_][a-zA-Z0-9_]*/
STRING: /"[^"]*"/
INTEGER: /[0-9]+/
HEX_COLOR: /#[0-9a-fA-F]{3,6}/
DIMENSION: INTEGER UNIT?
UNIT: "px" | "em" | "rem" | "%" | "pt"
ORDERED: /ORDERED/i
UNORDERED: /UNORDERED/i

%import common.WS
%import common.NEWLINE

%import common.C_COMMENT
%import common.CPP_COMMENT

%ignore WS
%ignore C_COMMENT
%ignore CPP_COMMENT

```
---

### Informacje o pakietach zewnętrznych i wymaganiach

Do uruchomienia transpilera wymagane jest środowisko **Python (wersja 3.10 lub nowsza)**. Projekt wykorzystuje następujące zależności zewnętrzne:
- **Lark**.

Instalacja wymaganych pakietów:
```bash
pip install lark
```
### Instrukcja obsługi
Wykonanie poniższej komendy odpala webapp na którym można live kompilować nasz język/
```bash
python3 -m src.webapp
```
### Przykład użycia
Znajduje się w pliku src.in.text



