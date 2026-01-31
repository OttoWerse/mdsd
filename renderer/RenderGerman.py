from unittest import case

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
        attribute_count = self.get_number_string(number=len(class_object.attributes.values()), is_female=True)
        attribute_list = self.render_attribute_list(class_object.attributes.values())
        operation_count = self.get_number_string(number=len(class_object.operations.values()), is_female=True)
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

    def get_number_string(self, number, is_female=False):
        match number:
            case 0:
                if is_female:
                    return German.NO_0_FEMALE
                else:
                    return German.NO_0_MALE
            case 1:
                if is_female:
                    return German.NO_1_FEMALE
                else:
                    return German.NO_1_MALE
            case 2:
                return German.NO_2
            case 3:
                return German.NO_3
            case 4:
                return German.NO_4
            case 5:
                return German.NO_5
            case 6:
                return German.NO_6
            case 7:
                return German.NO_7
            case 8:
                return German.NO_7
            case 9:
                return German.NO_9
            case 10:
                return German.NO_10
            case 11:
                return German.NO_11
            case 12:
                return German.NO_12
            case _:
                return number

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
                    if operation_object.return_type == DataTypesUML.VOID or operation_object.return_type is None:
                        return_text += f'{German.OPERATION_DESCRIPTION_SINGLE_NO_RETURN.substitute(visibility=operation_visibility,
                                                                                                   operation_name=operation_name,
                                                                                                   parameters_text=parameter_text, )} \n'
                    else:
                        return_text += f'{German.OPERATION_DESCRIPTION_SINGLE_WITH_RETURN.substitute(visibility=operation_visibility,
                                                                                                     operation_name=operation_name,
                                                                                                     return_type=operation_return_type,
                                                                                                     parameters_text=parameter_text, )} \n'
            elif parameter_count > 1:
                parameter_count_text = self.get_number_string(number=parameter_count, is_female=False)
                parameter_list = self.render_parameter_list(operation_object.parameters.values())
                # Use Template to create formatted text and append to return_text
                if operation_object.return_type == DataTypesUML.VOID or operation_object.return_type is None:
                    return_text += f'{German.OPERATION_DESCRIPTION_MULTIPLE_NO_RETURN.substitute(visibility=operation_visibility,
                                                                                                 operation_name=operation_name,
                                                                                                 parameters_count=parameter_count_text,
                                                                                                 parameters_list=parameter_list, )} \n'
                else:
                    return_text += f'{German.OPERATION_DESCRIPTION_MULTIPLE_WITH_RETURN.substitute(visibility=operation_visibility,
                                                                                                   operation_name=operation_name,
                                                                                                   return_type=operation_return_type,
                                                                                                   parameters_count=parameter_count_text,
                                                                                                   parameters_list=parameter_list, )} \n'
            else:
                pass  # TODO: Can this haappen unless the XMI file is broken?
        return return_text[:-1]  # Remove trailing "\n" gracefully

    def render_parameter_list(self, parameters):
        return_text = ''
        current_count = 0
        total_count = len(parameters)
        for parameter_object in parameters:
            current_count += 1
            parameter_direction = parameter_object.direction
            parameter_name = parameter_object.name or German.EMPTY_PARAMETER_NAME
            # TODO: Test & rename
            parameter_type = self.get_type_string(parameter_object.type)
            if current_count == 1:
                return_text += German.PARAMETER_DESCRIPTION_MULTIPLE_START.substitute(parameter_type=parameter_type,
                                                                                         parameter_name=parameter_name)
            elif current_count == total_count:
                return_text += German.PARAMETER_DESCRIPTION_MULTIPLE_END.substitute(parameter_type=parameter_type,
                                                                                       parameter_name=parameter_name)
            else:
                return_text += German.PARAMETER_DESCRIPTION_MULTIPLE_MIDDLE.substitute(parameter_type=parameter_type,
                                                                                          parameter_name=parameter_name)
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
