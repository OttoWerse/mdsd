class FieldModel:

def __init__(self, name: str, type_: str):
self.name = name
self.type = type_


def __repr__(self):
return f"FieldModel(name={self.name}, type={self.type})"
