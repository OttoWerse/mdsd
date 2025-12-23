from constants import FieldNames, Placeholders
from models.AttributeModel import AttributeModel
from models.ClassModel import ClassModel
from models.OperationModel import OperationModel
from models.ParameterModel import ParameterModel
from models.RelationshipModel import RelationshipModel
from bs4 import BeautifulSoup
import argparse
import sys
import lxml
import logging

logger = logging.getLogger(__name__)


class XmiParser:
    def __init__(self, file_path):
        try:
            # Check if file is actually an XML file!
            if not file_path.endswith(".xmi"):
                logger.exception(f'ERROR not an XMI file: {file_path}')
                sys.exit()
            file_object = open(file_path, 'r')
            file_content = file_object.read()
            # Check for lxml installed! (required by BS4 but not correctly enforced)
            lxml.get_include()
            self.xmi_soup = BeautifulSoup(file_content, 'xml')
            self.nodes = self.find_all_elements_by_name('ownedMember')
        except Exception as e:
            logger.exception(f'EXCEPTION initialising parser: {e}')
            sys.exit()

    def find_all_elements_by_name(self, name):
        """Finds elements of a given name in entire tree"""
        #
        if self.xmi_soup is None:
            pass
        result = self.xmi_soup.find_all(name)
        # TODO: Check if result is None or nah?
        return result

    def parse_attribute(self, attribute_node):
        try:
            try:
                attribute_name = attribute_node[FieldNames.NAME]
            except Exception as e:  # handle no name
                attribute_name = Placeholders.EMPTY_ATTRIBUTE_NAME
        except Exception as e:
            logger.exception(f'EXCEPTION parsing attribute: {e}')
            sys.exit()
        return AttributeModel(name=attribute_name)

    def parse_class_attributes(self, class_node):
        try:
            attributes = {}
            attribute_nodes = [node for node in class_node.children if
                               node.name == FieldNames.OWNED_ATTRIBUTE]
        except Exception as e:
            logger.exception(f'EXCEPTION getting attribute nodes: {e}')
            sys.exit()
        for attribute_node in attribute_nodes:
            attribute_id = attribute_node[FieldNames.XMI_ID]
            attribute = self.parse_attribute(attribute_node)
            attributes[attribute_id] = attribute
        return attributes

    def parse_parameter(self, parameter_node):
        try:
            try:
                parameter_name = parameter_node[FieldNames.NAME]
            except Exception as e:  # handle no name
                parameter_name = Placeholders.EMPTY_PARAMETER_NAME
            # TODO: Check parameter type = "return" and add to OperationModel return type
        except Exception as e:
            logger.exception(f'EXCEPTION parsing parameter: {e}')
            sys.exit()
        return ParameterModel(name=parameter_name)

    def parse_operation(self, operation_node):
        try:
            try:
                operation_name = operation_node[FieldNames.NAME]
            except Exception as e:  # handle no name
                operation_name = Placeholders.EMPTY_OPERATION_NAME
        except Exception as e:
            logger.exception(f'EXCEPTION parsing operation: {e}')
            sys.exit()
        try:
            parameters = {}
            parameter_nodes = [node for node in operation_node.children if
                               node.name == FieldNames.OWNED_PARAMETER]
        except Exception as e:
            logger.exception(f'EXCEPTION getting parameter nodes: {e}')
            sys.exit()
        for parameter_node in parameter_nodes:
            parameter_id = parameter_node[FieldNames.XMI_ID]
            parameter = self.parse_parameter(parameter_node)
            parameters[parameter_id] = parameter
        return OperationModel(name=operation_name,
                              parameters=parameters, )

    def parse_class_operations(self, class_node):
        try:
            operations = {}
            operation_nodes = [node for node in class_node.children if
                               node.name == FieldNames.OWNED_OPERATION]
        except Exception as e:
            logger.exception(f'EXCEPTION getting operation nodes: {e}')
            sys.exit()
        for operation_node in operation_nodes:
            operation_id = operation_node[FieldNames.XMI_ID]
            operation = self.parse_operation(operation_node)
            operations[operation_id] = operation
        return operations

    def parse_class(self, class_node):
        try:
            try:
                class_name = class_node[FieldNames.NAME]
            except Exception as e:  # handle no name
                class_name = Placeholders.EMPTY_CLASS_NAME
            # TODO: Add these fields properly
            #  class_package = class_node[FieldNames.PACKAGE]
            #  class_visibility = class_node[FieldNames.VISIBILITY]
            #  class_is_abstract = class_node[FieldNames.ABSTRACT]
            # Parse children nodes
            # TODO: how exactly are these stored im XMI?
            #  class_supers =
            #  class_interfaces =
            class_attributes = self.parse_class_attributes(class_node)
            class_operations = self.parse_class_operations(class_node)
        except Exception as e:
            logger.exception(f'EXCEPTION parsing class: {e}')
            sys.exit()
        # Create ClassModel Object and add to dict
        try:
            return ClassModel(name=class_name,
                              attributes=class_attributes,
                              operations=class_operations, )
        except Exception as e:
            logger.exception(f'EXCEPTION creating class model: {e}')
            sys.exit()

    def get_all_classes(self):
        """Returns all classes in the parsers xml tree"""
        return_classes = {}
        try:
            class_nodes = [node for node in self.nodes if
                           node[FieldNames.XMI_TYPE] == FieldNames.UML_CLASS]
        except Exception as e:
            logger.exception(f'EXCEPTION getting class nodes: {e}')
            sys.exit()
        for class_node in class_nodes:
            class_id = class_node[FieldNames.XMI_ID]
            class_model = self.parse_class(class_node)
            return_classes[class_id] = class_model
        return return_classes

    def get_all_relationships(self):
        """Returns all relationships in the parsers xml tree"""
        return_relationships = {}
        try:
            relationship_nodes = [node for node in self.nodes if
                                  node[FieldNames.XMI_TYPE] == FieldNames.UML_ASSOCIATION]
        except Exception as e:
            logger.exception(f'EXCEPTION getting relationship nodes: {e}')
            sys.exit()
        for relationship_node in relationship_nodes:
            # Get id of relationship node
            try:
                relationship_id = relationship_node[FieldNames.XMI_ID]
                relationship_type = relationship_node[FieldNames.XMI_TYPE]
                # Get name of relationship from XMI file or set it based on relationship type
                try:
                    relationship_name = relationship_node[FieldNames.NAME]
                except Exception as e:
                    match relationship_type:
                        # TODO: Add cases for known relationships, use constants and translate later in renderGerman
                        case 'uml:Association':
                            relationship_name = Placeholders.ASSOCIATION_NAME
                        case _:
                            relationship_name = Placeholders.EMPTY_RELATIONSHIP_NAME
                # Get ends of relationship from XMI
                ends = [child[FieldNames.TYPE] for child in relationship_node.children if
                        child.name == FieldNames.OWNED_END]
                # Check for exactly two ends
                if len(ends) != 2:
                    logger.exception(f'ERROR: more than two ends found for {relationship_name}')
                    sys.exit()
                # Set left and right end of relationship
                left_end = ends[0]
                right_end = ends[1]
                # Create RelationshipModel Object and add to dict
                return_relationships[relationship_id] = RelationshipModel(relationship_name, left_end, right_end)
            except Exception as e:
                logger.exception(f'EXCEPTION parsing relationship: {e}')
                sys.exit()
        return return_relationships


if __name__ == '__main__':
    """Main function"""
    argument_parser = argparse.ArgumentParser("ParseXMI")
    argument_parser.add_argument("--xmi_path",
                                 type=str,
                                 help="Speicherpfad der XMI Datei",
                                 nargs='?',
                                 const=0,
                                 required=False, )
    args = argument_parser.parse_args()
    xmi_file_path = args.xmi_path or r'examples/facade_mikrowelle.xmi'
    xmi_parser = XmiParser(xmi_file_path)

    relationships = xmi_parser.get_all_relationships()
    classes = xmi_parser.get_all_classes()
    print('Klassen:')
    for class_object in classes.values():
        print(f' -{class_object.name}')
        print(f'  Attribute:')
        for attribute_object in class_object.attributes.values():
            print(f'   -{attribute_object.name}')
        print(f'  Methoden:')
        for operation_object in class_object.operations.values():
            print(f'   -{operation_object.name}')
            print(f'    Parameter:')
            for parameter_object in operation_object.parameters.values():
                print(f'     -({parameter_object.direction}) {parameter_object.name} : {parameter_object.type}')
    print('Beziehungen:')
    for relationship_object in relationships.values():
        print(f' -{classes[relationship_object.source].name} '
              f'--({relationship_object.name})-> '
              f'{classes[relationship_object.target].name}')
