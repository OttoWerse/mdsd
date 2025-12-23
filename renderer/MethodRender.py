from models.MethodModel import MethodModel
from models.TypeModel import TypeModel
from models.VisibilityType import VisibilityType
from templates.German import METHOD_DESCRIPTION

if __name__ == "__main__":
    print("START TEST")

    method = MethodModel(
        name="starten",
        return_type=TypeModel("void"),
        visibility=VisibilityType.PUBLIC
    )

    print(METHOD_DESCRIPTION.substitute(
        method_name=method.name,
        return_type=method.return_type.name,
        visibility=method.visibility.name,
        parameter_count=0
    ))

    print("END TEST")
