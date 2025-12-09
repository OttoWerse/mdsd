from typing import Any

class RelationshipModel:
    def __init__(
        self,
        name: str,
        source: Any,
        target: Any,
        visibility: str = "public",
    ):
        self.name = name
        self.source = source
        self.target = target
        self.visibility = visibility

    def __repr__(self):
        return (
            f"RelationshipModel(name={self.name}, "
            f"source={self.source}, "
            f"target={self.target}, "
            f"visibility={self.visibility})"
        )
