from constants import DataTypesUML, VisiblityUML, RelationshipsUML
from templates import German


class GermanRenderer:
    def __init__(self, classes, relationships):
        self.classes = classes
        self.relationships = relationships

    def render_class_diagram(self):
        return_text = ''
        for class_object in self.classes.values():
            return_text += f'{self.render_class(class_object)} \n'
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

    def get_type_string(self, attribute_type):
        match attribute_type:
            case DataTypesUML.STRING:
                return German.DATATYPE_STRING
            case DataTypesUML.FLOAT:
                return German.DATATYPE_FLOAT
            case DataTypesUML.INT:
                return German.DATATYPE_INTEGER
            case DataTypesUML.VOID:
                return German.DATATYPE_VOID
            case _:
                input(attribute_type)

    def get_visibility_string(self, visibility):
        match visibility:
            case VisiblityUML.PUBLIC:
                return German.VISIBILITY_PUBLIC
            case VisiblityUML.PACKAGE:
                return German.VISIBILITY_PACKAGE
            case VisiblityUML.PROTECTED:
                return German.VISIBILITY_PROTECTED
            case VisiblityUML.PRIVATE:
                return German.VISIBILITY_PRIVATE
            case _:
                return German.VISIBILITY_UNKNOWN

    def render_attribute_list(self, attributes):
        return_text = ''
        for attribute_object in attributes:
            attribute_visibility = self.get_visibility_string(attribute_object.visibility)
            attribute_name = attribute_object.name or German.EMPTY_ATTRIBUTE_NAME
            attribute_type = self.get_type_string(attribute_object.type)
            # Use Template to create formatted text and append to return_text
            return_text += f'{German.ATTRIBUTE_DESCRIPTION.substitute(attribute_visibility=attribute_visibility,
                                                                      attribute_name=attribute_name,
                                                                      attribute_type=attribute_type)}'
        return return_text[:-1]  # Remove trailing "\n" gracefully

    def render_operation_list(self, operations):
        return_text = ''
        for operation_object in operations:
            operation_name = operation_object.name or German.EMPTY_OPERATION_NAME
            operation_visibility = German.VISIBILITY_UNKNOWN
            operation_visibility = self.get_visibility_string(operation_object.visibility)
            operation_return_type = operation_object.return_type
            parameter_count = len(operation_object.parameters)
            if parameter_count == 1:
                for parameter_object in operation_object.parameters.values():
                    parameter_name = parameter_object.name or German.EMPTY_PARAMETER_NAME
                    # TODO: Test & rename
                    parameter_type = self.get_type_string(parameter_object.type)
                    parameter_text = German.PARAMETER_DESCRIPTION_SINGLE.substitute(parameter_type=parameter_type,
                                                                                    parameter_name=parameter_name)
                    if operation_object.return_type == DataTypesUML.VOID:
                        return_text += f'{German.OPERATION_DESCRIPTION_SINGLE_NO_RETURN.substitute(visibility=operation_visibility,
                                                                                                   operation_name=operation_name,
                                                                                                   parameters_count=parameter_count,
                                                                                                   parameters_text=parameter_text, )} \n'
                    else:
                        return_text += f'{German.OPERATION_DESCRIPTION_SINGLE_WITH_RETURN.substitute(visibility=operation_visibility,
                                                                                                     operation_name=operation_name,
                                                                                                     return_type=operation_return_type,
                                                                                                     parameters_count=parameter_count,
                                                                                                     parameters_text=parameter_text, )} \n'
            elif parameter_count > 1:
                parameter_list = self.render_parameter_list(operation_object.parameters.values())
                # Use Template to create formatted text and append to return_text
                if operation_object.return_type == DataTypesUML.VOID:
                    return_text += f'{German.OPERATION_DESCRIPTION_MULTIPLE_NO_RETURN.substitute(visibility=operation_visibility,
                                                                                                 operation_name=operation_name,
                                                                                                 parameters_count=parameter_count,
                                                                                                 parameters_list=parameter_list, )} \n'
                else:
                    return_text += f'{German.OPERATION_DESCRIPTION_MULTIPLE_WITH_RETURN.substitute(visibility=operation_visibility,
                                                                                                   operation_name=operation_name,
                                                                                                   return_type=operation_return_type,
                                                                                                   parameters_count=parameter_count,
                                                                                                   parameters_list=parameter_list, )} \n'
            else:
                pass  # TODO: Can this haappen unless the XMI file is broken?
        return return_text[:-1]  # Remove trailing "\n" gracefully

    def render_parameter_list(self, parameters):
        return_text = ''
        for parameter_object in parameters:
            parameter_direction = parameter_object.direction
            parameter_name = parameter_object.name or German.EMPTY_PARAMETER_NAME
            # TODO: Test & rename
            parameter_type = self.get_type_string(parameter_object.type)
            return_text += f'{German.PARAMETER_DESCRIPTION_MULTIPLE.substitute(parameter_type=parameter_type,
                                                                               parameter_name=parameter_name)}, '
        return return_text[:-2]  # Remove trailing ", " gracefully

    def render_relationship(self, relationship_object):
        return_text = ''
        relationship_name = relationship_object.name
        match relationship_name:
            case RelationshipsUML.ASSOCIATION:
                relationship_name = German.ASSOCIATION_NAME
            case '':
                relationship_name = German.EMPTY_RELATIONSHIP_NAME
            case _:
                relationship_name = German.RELATIONSHIP_NAME.substitute(relation_name=relationship_name)
        # Use Template to create formatted text into return_text
        return_text = German.RELATIONSHIP_DESCRIPTION.substitute(source=self.classes[relationship_object.source].name,
                                                                 relation_type=relationship_name,
                                                                 target=self.classes[relationship_object.target].name, )
        return return_text
