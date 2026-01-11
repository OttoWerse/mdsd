from typing import Optional, TypedDict, Dict

from models import TypeModel


class ParameterDict(TypedDict):
    name: str
    type: Optional[TypeModel]
    default: Optional[str]
    direction: Optional[str]


class ParameterModel:
    def __init__(
            self,
            name: str,
            type: Optional[TypeModel] = None,
            default: Optional[str] = None,
            direction: Optional[str] = None,
    ):
        self.name = name
        self.type = type
        self.default = default
        self.direction = direction

    def to_dict(self) -> ParameterDict:
        return {
            "name": self.name,
            "type": self.type.to_dict() if self.type else None,
            "default": self.default,
            "direction": self.direction,
        }

    @staticmethod
    def from_dict(d: ParameterDict) -> "ParameterModel":
        t = d.get("type")
        return ParameterModel(
            name=d.get("name", "arg"),
            type=TypeModel.from_dict(t) if t else None,
            default=d.get("default"),
            direction=d.get("direction"),
        )
