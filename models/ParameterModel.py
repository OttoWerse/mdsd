import self


class ParameterModel:

def __init__(self, name: str, type_: str):
self.name = name
self.type = type_


def __repr__(self):
return f"ParameterModel(name={self.name}, type={self.type})"
