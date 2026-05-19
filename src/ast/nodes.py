from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Sequence, TypeAlias


# -------- Core document model --------

@dataclass(frozen=True, slots=True)
class Document:
    head: Head = field(default_factory=lambda: Head())
    body: list[Node] = field(default_factory=list)
    variables: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class Head:
    styles: list[StyleRule] = field(default_factory=list)


# -------- Body nodes --------

@dataclass(frozen=True, slots=True)
class Heading:
    level: Literal[1, 2]
    text: str
    class_name: str | None = None


@dataclass(frozen=True, slots=True)
class Paragraph:
    text: str
    class_name: str | None = None


@dataclass(frozen=True, slots=True)
class Div:
    children: list[Node]
    class_name: str | None = None


@dataclass(frozen=True, slots=True)
class Section:
    children: list[Node]
    class_name: str | None = None


@dataclass(frozen=True, slots=True)
class ListItem:
    text: str


@dataclass(frozen=True, slots=True)
class ListBlock:
    ordered: bool
    items: list[ListItem]


@dataclass(frozen=True, slots=True)
class Image:
    src: str
    alt: str = "image"
    class_name: str | None = None


@dataclass(frozen=True, slots=True)
class Button:
    text: str
    class_name: str | None = None


@dataclass(frozen=True, slots=True)
class Link:
    url: str
    label: str


@dataclass(frozen=True, slots=True)
class Input:
    text: str
    class_name: str | None = None


@dataclass(frozen=True, slots=True)
class Form:
    children: list[Node]
    class_name: str | None = None


@dataclass(frozen=True, slots=True)
class Font:
    """Google Font family to load in <head>."""
    family: str


@dataclass(frozen=True, slots=True)
class Icon:
    """Font Awesome icon (class string, e.g. 'fa-solid fa-envelope')."""
    icon_class: str
    class_name: str | None = None


@dataclass(frozen=True, slots=True)
class VariableDefinition:
    """CSS variable: name -> value (substituted during emission)."""
    name: str
    value: str


Node: TypeAlias = (
    Heading
    | Paragraph
    | Div
    | Section
    | ListBlock
    | Image
    | Button
    | Link
    | Input
    | Form
    | Font
    | Icon
    | VariableDefinition
)


# -------- CSS model (head) --------

@dataclass(frozen=True, slots=True)
class CssDeclaration:
    property_name: str
    value: str


@dataclass(frozen=True, slots=True)
class StyleRule:
    selector: str
    declarations: Sequence[CssDeclaration]
