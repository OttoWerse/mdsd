from templates import German


class GermanRenderer:
    def __init__(self, classes, relationships):
        self.classes = classes
        self.relationships = relationships

    def render_class_diagram(self):
        return_text = 'Klassen: \n'
        for class_object in self.classes.values():
            return_text += f'{self.render_class(class_object)} \n'
        return_text += 'Beziehungen: \n'
        for relationship_object in self.relationships.values():
            return_text += f'{self.render_relationship(relationship_object)} \n'
        return return_text

    def render_class(self, class_object):
        return_text = ''
        class_name = class_object.name or German.EMPTY_CLASS_NAME
        attribute_count = len(class_object.attributes.values())
        attribute_list = self.render_attribute_list(class_object.attributes.values())
        operation_count = len(class_object.operations.values())
        operation_list = self.render_operation_list(class_object.operations.values())
        # Use Template to create formatted text into return_text
        return_text = German.CLASS_DESCRIPTION.substitute(
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
            attribute_visibility = attribute_object.visibility
            attribute_name = attribute_object.name or German.EMPTY_ATTRIBUTE_NAME
            attribute_type = attribute_object.type
            # Use Template to create formatted text and append to return_text
            return_text += f'{German.ATTRIBUTE_DESCRIPTION.substitute(attribute_visibility=attribute_visibility,
                                                                      attribute_name=attribute_name,
                                                                      attribute_type=attribute_type)} \n'
        return return_text[:-1]  # Remove trailing "\n" gracefully

    def render_operation_list(self, operations):
        return_text = ''
        for operation_object in operations:
            operation_name = operation_object.name or German.EMPTY_OPERATION_NAME
            operation_visibility = operation_object.visibility
            operation_return_type = operation_object.return_type
            parameter_count = len(operation_object.parameters)
            parameter_list = self.render_parameter_list(operation_object.parameters.values())
            # Use Template to create formatted text and append to return_text
            return_text += f'{German.OPERATION_DESCRIPTION.substitute(visibility=operation_visibility,
                                                                      operation_name=operation_name,
                                                                      return_type=operation_return_type,
                                                                      parameters_count=parameter_count,
                                                                      parameters_list=parameter_list, )} \n'
        return return_text[:-1]  # Remove trailing "\n" gracefully

    def render_parameter_list(self, parameters):
        return_text = ''
        for parameter_object in parameters:
            parameter_direction = parameter_object.direction
            parameter_name = parameter_object.name or German.EMPTY_PARAMETER_NAME
            parameter_type = parameter_object.type
            return_text += f'{German.PARAMETER_DESCRIPTION.substitute(parameter_type=parameter_type,
                                                                      parameter_name=parameter_name)}, '
        return return_text[:-2]  # Remove trailing ", " gracefully

    def render_relationship(self, relationship_object):
        return_text = ''
        relationship_name = relationship_object.name
        match relationship_name:
            case 'uml:Association':
                relationship_name = German.ASSOCIATION_NAME
            # TODO: Add cases for known relationships, use constants and translate later in renderGerman
            case _:
                relationship_name = German.EMPTY_RELATIONSHIP_NAME
        # Use Template to create formatted text into return_text
        return_text = German.RELATIONSHIP_DESCRIPTION.substitute(source=self.classes[relationship_object.source].name,
                                                                 relation_type=relationship_name,
                                                                 target=self.classes[relationship_object.target].name, )
        return return_text
