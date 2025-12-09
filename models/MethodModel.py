from dataclasses import dataclass, field
from typing import List

from models import ParameterModel, TypeModel


class MethodModel:

    def __init__(
        self,
        name: str,
        return_type: TypeModel,
        parameters: List[ParameterModel] = None,
        visibility: VisibilityModel = VisibilityModel.PUBLIC,
        is_static: bool = False,
        is_abstract: bool = False
    ):
        self.name = name
        self.return_type = return_type
        self.parameters = parameters if parameters is not None else []
        self.visibility = visibility
        self.is_static = is_static
        self.is_abstract = is_abstract

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
