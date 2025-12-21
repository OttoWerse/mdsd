from models.TypeModel import TypeModel
from templates.German import TYPE_DESCRIPTION

if __name__ == "__main__":
    print("START TEST")

    type_model = TypeModel(name="String")

    print(TYPE_DESCRIPTION.substitute(
        type_name=type_model.name
    ))

    print("END TEST")
