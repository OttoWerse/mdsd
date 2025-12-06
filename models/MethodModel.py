from dataclasses import field
from typing import List

import parameter
import return_type

from models import TypeModel


class MethodModel:
    name: str
    return_type: TypeModel
    parameters: List[ParameterModel] = field(default_factory=list)
    visibility: VisibilityModel = VisibilityModel.PUBLIC
    is_static: bool = False
    is_abstract: bool = False

    def __str__(self):
        mods = []
        if self.is_static:
            mods.append("static")
        if self.is_abstract:
            mods.append("abstract")

        modifiers = " ".join(mods)
        params = ", ".join(str(p) for p in self.parameters)

        return (
            f"{self.visibility.value} {modifiers} "
            f"{self.return_type.name} {self.name}({params})"
        ).strip()
