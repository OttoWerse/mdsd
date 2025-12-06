from dataclasses import field
from typing import List, Optional, Dict, Any


class TypeModel:
    name: str
    package: Optional[str] = None
    generic_parameters: List["TypeModel"] = field(default_factory=list)
    is_primitive: bool = False

    def __repr__(self) -> str:
        if self.generic_parameters:
            gens = ", ".join(repr(g) for g in self.generic_parameters)
            return f"{self.name}[{gens}]"
        return self.name

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "package": self.package,
            "generic_parameters": [g.to_dict() for g in self.generic_parameters],
            "is_primitive": self.is_primitive,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "TypeModel":
        return TypeModel(
            name=d.get("name", "<unknown>"),
            package=d.get("package"),
            generic_parameters=[TypeModel.from_dict(g) for g in d.get("generic_parameters", [])],
            is_primitive=d.get("is_primitive", False),
        )
