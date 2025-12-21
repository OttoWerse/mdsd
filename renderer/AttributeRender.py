from models.AttributeModel import AttributeModel
from models.TypeModel import TypeModel
from models.VisibilityType import VisibilityType
from templates.German import ATTRIBUTE_DESCRIPTION

if __name__ == "__main__":
    print("START TEST")

    attribute = AttributeModel(
        name="leistung",
        type=TypeModel("int"),
        visibility=VisibilityType.PRIVATE
    )

    print(ATTRIBUTE_DESCRIPTION.substitute(
        attribute_name=attribute.name,
        attribute_type=attribute.type.name,
        attribute_visibility=attribute.visibility.name
    ))

    print("END TEST")
