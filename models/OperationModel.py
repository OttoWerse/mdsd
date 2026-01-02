from typing import Optional, Dict, TypedDict

from models import ParameterModel, TypeModel
from models.VisibilityType import VisibilityType


class OperationDict(TypedDict):
    name: str
    return_type: Optional[Dict[str, object]]
    parameters: Dict[str, Dict[str, object]]
    return_type: str
    visibility: Optional[str]
    is_static: bool
    is_abstract: bool


class OperationModel:
    def __init__(
            self,
            name: str,
            return_type: Optional[TypeModel] = None,
            parameters: Optional[Dict[str, ParameterModel]] = None,
            visibility: Optional[VisibilityType] = None,
            is_static: bool = False,
            is_abstract: bool = False
    ):
        self.name = name
        self.return_type = return_type
        # TODO: Check for a single parameter of type "return" and add to OperationModel as attribute return type
        return_parameter = None
        for parameter in parameters:
            if parameters[parameter].direction == 'return':
                return_parameter = parameter
                return_type = parameters[parameter].type
        if return_parameter is not None:
            del parameters[return_parameter]
        self.parameters: Dict[str, ParameterModel] = parameters or {}
        self.return_type = return_type
        self.visibility = visibility
        self.is_static = is_static
        self.is_abstract = is_abstract

    def signature(self) -> str:
        params = ", ".join(
            f"{p.name}: {p.type.name if p.type else 'Any'}"
            for p in self.parameters.values()
        )
        ret = self.return_type.name if self.return_type else "void"
        return f"{self.name}({params}) -> {ret}"

    def to_dict(self) -> OperationDict:
        return {
            "name": self.name,
            "return_type": self.return_type.to_dict() if self.return_type else None,
            "parameters": {
                name: p.to_dict()
                for name, p in self.parameters.items()
            },
            "visibility": self.visibility.value if self.visibility else None,
            "is_static": self.is_static,
            "is_abstract": self.is_abstract,
        }

    @staticmethod
    def from_dict(d: OperationDict) -> "OperationModel":
        rt = d.get("return_type")

        op = OperationModel(
            name=d.get("name", "<op>"),
            return_type=TypeModel.from_dict(rt) if rt else None,
            visibility=Visibility.from_string(d.get("visibility")),
            is_static=d.get("is_static", False),
            is_abstract=d.get("is_abstract", False),
        )

        for name, p in d.get("parameters", {}).items():
            op.parameters[name] = ParameterModel.from_dict(p)

        return op
