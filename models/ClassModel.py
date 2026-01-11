from typing import Optional, List, Dict, TypedDict

from models import AttributeModel, OperationModel
from models.VisibilityType import VisibilityType


class ClassDict(TypedDict):
    name: str
    package: Optional[str]
    attributes: Dict[str, Dict[str, AttributeModel]]
    operations: Dict[str, Dict[str, OperationModel]]
    visibility: str
    is_abstract: bool
    super_classes: List[str]
    interfaces: List[str]


class ClassModel:
    def __init__(
            self,
            name: Optional[str] = None,
            package: Optional[str] = None,
            attributes: Optional[Dict[str, AttributeModel]] = None,
            operations: Optional[Dict[str, OperationModel]] = None,
            visibility: Optional[VisibilityType] = None,
            is_abstract: bool = False,
            super_classes: Optional[List[str]] = None,
            interfaces: Optional[List[str]] = None
    ):
        self.name = name or "<class>"
        self.package = package
        self.attributes: Dict[str, AttributeModel] = attributes or {}
        self.operations: Dict[str, OperationModel] = operations or {}
        self.visibility = visibility or VisibilityType.PUBLIC
        self.is_abstract = is_abstract
        self.super_classes = super_classes or []
        self.interfaces = interfaces or []

    def add_attribute(self, attr: AttributeModel) -> None:
        self.attributes[attr.name] = attr

    def add_operation(self, op: OperationModel) -> None:
        self.operations[op.name] = op

    def to_dict(self) -> ClassDict:
        return {
            "name": self.name,
            "package": self.package,
            "attributes": {
                name: attr.to_dict()
                for name, attr in self.attributes.items()
            },
            "operations": {
                name: op.to_dict()
                for name, op in self.operations.items()
            },
            "visibility": self.visibility.value,
            "is_abstract": self.is_abstract,
            "super_classes": list(self.super_classes),
            "interfaces": list(self.interfaces),
        }

    @staticmethod
    def from_dict(d: ClassDict) -> "ClassModel":
        cm = ClassModel(
            name=d.get("name", "<class>"),
            package=d.get("package"),
            visibility=Visibility.from_string(d.get("visibility")),
            is_abstract=d.get("is_abstract", False),
            super_classes=d.get("super_classes", []),
            interfaces=d.get("interfaces", []),
        )

        for name, a in d.get("attributes", {}).items():
            cm.attributes[name] = AttributeModel.from_dict(a)

        for name, o in d.get("operations", {}).items():
            cm.operations[name] = OperationModel.from_dict(o)

        return cm
