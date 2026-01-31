from constants import FieldNames
from models.AttributeModel import AttributeModel
from models.ClassModel import ClassModel
from models.OperationModel import OperationModel
from models.ParameterModel import ParameterModel
from models.RelationshipModel import RelationshipModel
from bs4 import BeautifulSoup
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
                attribute_name = None
            try:
                attribute_type = attribute_node[FieldNames.TYPE]
            except Exception as e:  # Handle no type
                attribute_type = None  # TODO: This specific scenario needs to be rendered explicitly as "no type given"!
            attribute_visibility = attribute_node[FieldNames.VISIBILITY]
        except Exception as e:
            logger.exception(f'EXCEPTION parsing attribute: {e}')
            sys.exit()
        return AttributeModel(name=attribute_name,
                              type=attribute_type,
                              visibility=attribute_visibility, )

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
            except Exception as e:  # Handle no name
                parameter_name = None
            try:
                parameter_type = parameter_node[FieldNames.TYPE]
            except Exception as e:  # Handle no type
                parameter_type = None  # TODO: This specific scenario needs to be rendered explicitly as "no type given"!
            parameter_direction = parameter_node[FieldNames.KIND]
        except Exception as e:
            logger.exception(f'EXCEPTION parsing parameter: {e}')
            sys.exit()
        return ParameterModel(name=parameter_name,
                              type=parameter_type,
                              direction=parameter_direction, )

    def parse_operation(self, operation_node):
        try:
            try:
                operation_name = operation_node[FieldNames.NAME]
            except Exception as e:  # handle no name
                operation_name = None
            operation_visibility = operation_node[FieldNames.VISIBILITY]
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
                              parameters=parameters,
                              visibility=operation_visibility, )

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
                class_name = None
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
                # Get ends of relationship from XMI
                ends = [child for child in relationship_node.children if
                        child.name == FieldNames.OWNED_END]
                # Check for exactly two ends
                if len(ends) != 2:
                    logger.exception(f'ERROR: more than two ends found for {relationship_id}')
                    sys.exit()
                # Set left and right end of relationship
                left_end = ends[0]
                right_end = ends[1]
                # Get special relationship kinds
                relationship_aggregation = right_end[FieldNames.AGGREGATION]
                # Get name of relationship from XMI file or set it based on relationship type
                try:
                    relationship_name = relationship_node[FieldNames.NAME]
                except Exception as e:
                    relationship_name = relationship_aggregation
                # Create RelationshipModel Object and add to dict
                return_relationships[relationship_id] = RelationshipModel(relationship_name,
                                                                          left_end[FieldNames.TYPE],
                                                                          right_end[FieldNames.TYPE])
            except Exception as e:
                logger.exception(f'EXCEPTION parsing relationship: {e}')
                sys.exit()
        return return_relationships


if __name__ == '__main__':
    """Main function for testing class"""
    xmi_parser = XmiParser(r'examples/facade_mikrowelle.xmi')

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
