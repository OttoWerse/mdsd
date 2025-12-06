import parameter
import return_type


class MethodModel:

def __init__(self, name: str, return_type: str = None):
self.name = name
self.return_type = return_type
self.parameters = [] # List[ParameterModel]


def add_parameter(self, parameter):
self.parameters.append(parameter)


def __repr__(self):
return f"MethodModel(name={self.name}, return_type={self.return_type}, parameters={self.parameters})"
