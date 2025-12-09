from dataclasses import dataclass
from typing import Optional
from models import TypeModel


@dataclass
class FieldModel:
    name: str
    type: TypeModel
    visibility: VisibilityModel = VisibilityModel.PUBLIC
    is_static: bool = False
    is_final: bool = False

    def __init__(
        self,
        name: str,
        type: TypeModel,
        visibility: VisibilityModel = VisibilityModel.PUBLIC,
        is_static: bool = False,
        is_final: bool = False
    ):
        self.name = name
        self.type = type
        self.visibility = visibility
        self.is_static = is_static
        self.is_final = is_final

    def __str__(self):
        mods = []
        if self.is_static:
            mods.append("static")
        if self.is_final:
            mods.append("final")

        modifiers = " ".join(mods)
        return f"{self.visibility.value} {modifiers} {self.type.name} {self.name}".strip()
