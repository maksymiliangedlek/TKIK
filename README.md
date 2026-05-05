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

### Planowany język implementacji:
-Python, parser LARK

### Opis tokenów (Lekser)

| Kod Tokena | Reguła / Wartość | Opis |
| :--- | :--- | :--- |
| BEGIN | BEGIN | Otwarcie bloku dokumentu |
| END | END | Zamknięcie bloku dokumentu |
| TITLE | TITLE | Nagłówek główny (```<h1>```) |
| SUBTITLE | SUBTITLE | Podtytuł (```<h2>```) |
| TEXT | TEXT | Akapit tekstu (```<p>```) |
| LINK | LINK | Hiperłącze (```<a>```) |
| IMAGE | IMAGE | Obrazek (```<img>```) |
| BUTTON | BUTTON | Przycisk akcji (```<button>```) |
| INPUT | INPUT | Pole tekstowe (```<input type="text">```) |
| LIST | LIST | Definicja listy wyliczanej (```<ul>/<ol>```) |
| ITEM | ITEM | Element listy (```<li>```) |
| SECTION | SECTION | Kontener strukturalny (```<section>```) |
| DIV | DIV | Pusty kontener blokowy (```<div>```) |
| FORM | FORM | Kontener formularza (```<form>```) |
| STYLE | STYLE | Otwarcie bloku definicji stylów |
| HOVER | HOVER | Styl pseudo-klasy (efekt po najechaniu) |
| HOVER_CHILD | HOVER_CHILD | Styl zagnieżdżony (zmiana dziecka po najechaniu na rodzica) |
| CSS_PROP | BG_COLOR, MARGIN_TOP, DISPLAY, BOX_SHADOW... | Właściwości CSS |
| IDENTIFIER | [a-zA-Z_][a-zA-Z0-9_]* | Nazwy własne / identyfikatory klas |
| STRING | "[^"]*" | Napis w cudzysłowie |
| INTEGER | [0-9]+ | Liczby całkowite |
| HEX_COLOR | #[0-9a-fA-F]{3,6} | Kod koloru HEX |
| DIMENSION | INTEGER UNIT? | Wartość z jednostką (np. 15px, 100%) |
| UNIT | px \| em \| rem \| % \| pt \| vh \| vw | Obsługiwane jednostki CSS |
| LIST_TYPE | ORDERED \| UNORDERED | Modyfikatory typu listy |
| ASSIGN | = | Operator przypisania |
| LBRACE | { | Klamra otwierająca blok |
| RBRACE | } | Klamra zamykająca blok |
| SEMICOLON | ; | Koniec instrukcji |

### Gramatyka (Parser)
```
start
    : "BEGIN" instruction* "END"
    ;

?instruction
    : put_heading
    | put_subtitle
    | put_paragraph
    | put_hyperlink
    | put_image
    | put_list
    | put_button
    | put_input
    | put_div
    | put_section
    | put_form
    | block_style
    ;

put_heading   : "TITLE" [IDENTIFIER] STRING ";" ;
put_subtitle  : "SUBTITLE" [IDENTIFIER] STRING ";" ;
put_paragraph : "TEXT" [IDENTIFIER] STRING ";" ;
put_hyperlink : "LINK" STRING STRING ";" ;
put_image     : "IMAGE" STRING ";" ;
put_button    : "BUTTON" [IDENTIFIER] STRING ";" ;
put_input     : "INPUT" [IDENTIFIER] STRING ";" ;

put_list      : "LIST" [(ORDERED | UNORDERED)] "{" item* "}" ";" ;
item          : "ITEM" STRING ";" ;

put_div       : "DIV" [IDENTIFIER] "{" instruction* "}" ";" ;
put_section   : "SECTION" [IDENTIFIER] "{" instruction* "}" ";" ;
put_form      : "FORM" [IDENTIFIER] "{" instruction* "}" ";" ;

block_style
    : "STYLE" IDENTIFIER "{" style_declaration* "}"
    | "HOVER" IDENTIFIER "{" style_declaration* "}"
    | "HOVER_CHILD" IDENTIFIER IDENTIFIER "{" style_declaration* "}"
    ;

style_declaration
    : css_property "=" value ";"
    ;

css_property
    : "BG_COLOR" | "TEXT_COLOR" | "FONT_SIZE" | "FONT_WEIGHT" | "TEXT_ALIGN"
    | "MARGIN_TOP" | "MARGIN_BOTTOM" | "MARGIN_LEFT" | "MARGIN_RIGHT"
    | "PADDING_TOP" | "PADDING_BOTTOM" | "PADDING_LEFT" | "PADDING_RIGHT"
    | "WIDTH" | "HEIGHT" | "BORDER_RADIUS" | "BORDER_WIDTH" | "BORDER_STYLE" | "BORDER_COLOR"
    | "DISPLAY" | "JUSTIFY_CONTENT" | "ALIGN_ITEMS" | "OPACITY" | "CURSOR"
    | "POSITION" | "TOP" | "Z_INDEX" | "BOX_SHADOW" | "TRANSITION"
    ;

?value
    : STRING 
    | INTEGER 
    | HEX_COLOR 
    | IDENTIFIER 
    | DIMENSION
    ;
```
