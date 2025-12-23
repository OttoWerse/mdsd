from models.ClassModel import ClassModel
from templates.German import CLASS_DESCRIPTION


class GermanRenderer:
    def __init__(self):
        pass

    def render_class_diagram(self, classes, relationships):
        return_text = 'Klassen: \n'
        for class_object in classes.values():
            return_text += self.render_class(class_object)
        return_text += 'Beziehungen: \n'
        for relationship_object in relationships.values():
            return_text += self.render_relationship(relationship_object)
        return return_text

    def render_class(self, class_object):
        return_text = ''
        class_name = class_object.name
        attribute_count = len(class_object.attributes.values())
        attribute_list = self.render_attribute_list(class_object.attributes.values())
        operation_count = len(class_object.operations.values())
        operation_list = self.render_operation_list(class_object.operations.values())
        # Use Template to create formatted text into return_text
        return_text = CLASS_DESCRIPTION.substitute(
            class_name=class_name,
            attribute_count=attribute_count,
            attribute_list=attribute_list,
            method_count=operation_count,
            method_list=operation_list,
        )
        return return_text

    def render_attribute_list(self, attributes):
        return_text = ''
        for attribute_object in attributes:
            attribute_name = attribute_object.name
            # TODO: Use Template to create formatted text and append to return_text
        return return_text

    def render_operation_list(self, operations):
        return_text = ''
        for operation_object in operations:
            operation_name = operation_object.name
            parameter_count = len(operation_object.parameters)
            parameter_list = self.renbder_parameter_list(operation_object.parameters.values())
            # TODO: Use Template to create formatted text and append to return_text
        return return_text

    def renbder_parameter_list(self, parameters):
        return_text = ''
        for parameter_object in parameters:
            parameter_direction = parameter_object.direction
            parameter_name = parameter_object.name
            parameter_type = parameter_object.type
            # TODO: Use Template to create formatted text and append to return_text
        return return_text

    def render_relationship(self, relationship_object):
        return_text = ''
        relationship_name = relationship_object.name
        # TODO: Use Template to create formatted text into return_text
        return return_text
