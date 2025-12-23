from models.OperationModel import OperationModel
from models.TypeModel import TypeModel
from models.VisibilityType import VisibilityType
from templates.German import OPERATION_DESCRIPTION

if __name__ == "__main__":
    print("START TEST")

    operation = OperationModel(
        name="stoppen",
        return_type=TypeModel("void"),
        visibility=VisibilityType.PUBLIC
    )

    print(OPERATION_DESCRIPTION.substitute(
        operation_name=operation.name,
        return_type=operation.return_type.name,
        visibility=operation.visibility.name
    ))

    print("END TEST")
