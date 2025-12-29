from typing import TypedDict, List, Optional, Dict


class TypeDict(TypedDict):
    name: str
    package: Optional[str]
    generic_parameters: List[Dict[str, object]]
    is_primitive: bool


class TypeModel:
    name: str
    package: Optional[str]
    generic_parameters: List["TypeModel"]
    is_primitive: bool

    def __init__(
        self,
        name: str,
        package: Optional[str] = None,
        generic_parameters: Optional[List["TypeModel"]] = None,
        is_primitive: bool = False,
    ):
        self.name = name
        self.package = package
        self.generic_parameters = generic_parameters if generic_parameters is not None else []
        self.is_primitive = is_primitive

    def __repr__(self) -> str:
        if self.generic_parameters:
            gens = ", ".join(repr(g) for g in self.generic_parameters)
            return f"{self.name}[{gens}]"
        return self.name

    def to_dict(self) -> TypeDict:
        return {
            "name": self.name,
            "package": self.package,
            "generic_parameters": [
                g.to_dict() for g in self.generic_parameters
            ],
            "is_primitive": self.is_primitive,
        }

    @staticmethod
    def from_dict(d: TypeDict) -> "TypeModel":
        return TypeModel(
            name=d.get("name", "<unknown>"),
            package=d.get("package"),
            generic_parameters=[
                TypeModel.from_dict(g)
                for g in d.get("generic_parameters", [])
            ],
            is_primitive=d.get("is_primitive", False),
        )
