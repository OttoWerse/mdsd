from models.ParameterModel import ParameterModel
from models.TypeModel import TypeModel
from templates.German import PARAMETER_DESCRIPTION

if __name__ == "__main__":
    print("START TEST")

    parameter = ParameterModel(
        name="zeit",
        type=TypeModel("int")
    )

    print(PARAMETER_DESCRIPTION.substitute(
        parameter_name=parameter.name,
        parameter_type=parameter.type.name
    ))

    print("END TEST")
