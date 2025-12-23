from models.FieldModel import FieldModel
from models.TypeModel import TypeModel
from models.VisibilityType import VisibilityType
from templates.German import FIELD_DESCRIPTION

if __name__ == "__main__":
    print("START TEST")

    field = FieldModel(
        name="hersteller",
        type=TypeModel("String"),
        visibility=VisibilityType.PRIVATE
    )

    print(FIELD_DESCRIPTION.substitute(
        field_name=field.name,
        field_type=field.type.name,
        field_visibility=field.visibility.name
    ))

    print("END TEST")
