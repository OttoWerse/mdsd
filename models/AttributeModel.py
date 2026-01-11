from typing import Optional, Dict, TypedDict
from models import TypeModel
from models.VisibilityType import VisibilityType


class AttributeDict(TypedDict):
    name: str
    type: Optional[TypeModel]
    visibility: Optional[VisibilityType]
    multiplicity: Optional[str]
    default_value: Optional[str]
    is_static: bool
    is_final: bool


class AttributeModel:
    def __init__(
            self,
            name: str,
            type: Optional[TypeModel] = None,
            visibility: Optional[VisibilityType] = None,
            multiplicity: Optional[str] = None,
            default_value: Optional[str] = None,
            is_static: bool = False,
            is_final: bool = False,
    ):
        self.name = name
        self.type = type
        self.visibility = visibility
        self.multiplicity = multiplicity
        self.default_value = default_value
        self.is_static = is_static
        self.is_final = is_final

    def to_dict(self) -> AttributeDict:
        return {
            "name": self.name,
            "type": self.type.to_dict() if self.type else None,
            "visibility": self.visibility.value if self.visibility else None,
            "multiplicity": self.multiplicity,
            "default_value": self.default_value,
            "is_static": self.is_static,
            "is_final": self.is_final,
        }

    @staticmethod
    def from_dict(d: AttributeDict) -> "AttributeModel":
        t = d.get("type")
        return AttributeModel(
            name=d.get("name", "<attr>"),
            type=TypeModel.from_dict(t) if t else None,
            visibility=VisibilityType.from_string(d.get("visibility")),
            multiplicity=d.get("multiplicity"),
            default_value=d.get("default_value"),
            is_static=d.get("is_static", False),
            is_final=d.get("is_final", False),
        )
