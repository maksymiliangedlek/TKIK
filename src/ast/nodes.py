from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Sequence, TypeAlias


@dataclass(frozen=True, slots=True)
class Document:
    head: Head = field(default_factory=lambda: Head())
    body: list[Node] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class Head:
    styles: list[StyleRule] = field(default_factory=list)


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



Node: TypeAlias = Heading | Paragraph | Div | Section | ListBlock | Image | Button | Link



@dataclass(frozen=True, slots=True)
class CssDeclaration:
    property_name: str
    value: str


@dataclass(frozen=True, slots=True)
class StyleRule:
    selector: str
    declarations: Sequence[CssDeclaration]

