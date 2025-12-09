from typing import Optional, Any, Dict
from models import TypeModel

class ParameterModel:
    def __init__(
        self,
        name: str,
        type: Optional[TypeModel] = None,
        default: Optional[str] = None,

    ):
        self.name = name
        self.type = type
        self.default = default

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "type": self.type.to_dict() if self.type else None,
            "default": self.default,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ParameterModel":
        t = d.get("type")
        return ParameterModel(
            name=d.get("name", "arg"),
            type=TypeModel.from_dict(t) if t else None,
            default=d.get("default"),
        )
