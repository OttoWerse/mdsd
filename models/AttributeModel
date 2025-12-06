
class AttributeModel:
    name: str
    type: Optional["TypeModel"] = None
    visibility: "Visibility" = None
    multiplicity: Optional[str] = None
    default_value: Optional[str] = None
    is_static: bool = False
    is_final: bool = False

    def to_dict(self) -> Dict[str, Any]:
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
    def from_dict(d: Dict[str, Any]) -> "AttributeModel":
        t = d.get("type")
        return AttributeModel(
            name=d.get("name", "<attr>"),
            type=TypeModel.from_dict(t) if t else None,
            visibility=Visibility.from_string(d.get("visibility")),
            multiplicity=d.get("multiplicity"),
            default_value=d.get("default_value"),
            is_static=bool(d.get("is_static", False)),
            is_final=bool(d.get("is_final", False)),
        )
