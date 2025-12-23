from models.RelationshipModel import RelationshipModel
from models.RelationshipType import RelationshipType
from templates.German import RELATIONSHIP_DESCRIPTION

if __name__ == "__main__":
    print("START TEST")

    relationship = RelationshipModel(
        source_class="Mikrowelle",
        target_class="Hersteller",
        relationship_type=RelationshipType.ASSOCIATION
    )

    print(RELATIONSHIP_DESCRIPTION.substitute(
        source=relationship.source_class,
        target=relationship.target_class,
        relation_type=relationship.relationship_type.name
    ))

    print("END TEST")
