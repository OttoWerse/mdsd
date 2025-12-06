from dataclasses import field
from typing import Optional, List, Dict, Any

from models import AttributeModel, OperationModel


class ClassModel:
    name: str
    package: Optional[str] = None
    attributes: List["AttributeModel"] = field(default_factory=list)
    operations: List["OperationModel"] = field(default_factory=list)
    visibility: "Visibility" = Visibility.PUBLIC
    is_abstract: bool = False
    super_classes: List[str] = field(default_factory=list)
    interfaces: List[str] = field(default_factory=list)

    def add_attribute(self, attr: "AttributeModel") -> None:
        self.attributes.append(attr)

    def add_operation(self, op: "OperationModel") -> None:
        self.operations.append(op)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "package": self.package,
            "attributes": [a.to_dict() for a in self.attributes],
            "operations": [o.to_dict() for o in self.operations],
            "visibility": self.visibility.value,
            "is_abstract": self.is_abstract,
            "super_classes": list(self.super_classes),
            "interfaces": list(self.interfaces),
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ClassModel":
        cm = ClassModel(
            name=d.get("name", "<class>"),
            package=d.get("package"),
            visibility=Visibility.from_string(d.get("visibility")),
            is_abstract=bool(d.get("is_abstract", False)),
            super_classes=d.get("super_classes", []),
            interfaces=d.get("interfaces", []),
        )
        for a in d.get("attributes", []):
            cm.add_attribute(AttributeModel.from_dict(a))
        for o in d.get("operations", []):
            cm.add_operation(OperationModel.from_dict(o))
        return cm
