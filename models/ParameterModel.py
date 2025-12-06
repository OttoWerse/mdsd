import self


class ParameterModel:
    name: str
    type: Optional["TypeModel"] = None
    default: Optional[str] = None
    direction: str = "in"  # UML: in, out, inout

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "type": self.type.to_dict() if self.type else None,
            "default": self.default,
            "direction": self.direction,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ParameterModel":
        t = d.get("type")
        return ParameterModel(
            name=d.get("name", "arg"),
            type=TypeModel.from_dict(t) if t else None,
            default=d.get("default"),
            direction=d.get("direction", "in"),
        )
