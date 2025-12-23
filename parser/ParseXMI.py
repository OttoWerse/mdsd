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

    def parse_class_attributes(self, class_node):
        attributes = {}
        try:
            attribute_nodes = [node for node in class_node.children if
                               node.name == FieldNames.OWNED_ATTRIBUTE]
        except Exception as e:
            logger.exception(f'EXCEPTION getting attribute nodes: {e}')
            sys.exit()
        for attribute_node in attribute_nodes:
            try:
                try:
                    attribute_name = attribute_node[FieldNames.NAME]
                # handle no name
                except Exception as e:
                    attribute_name = Placeholders.EMPTY_ATTRIBUTE_NAME
                attribute_id = attribute_node[FieldNames.XMI_ID]  # TODO: try-except around this?
            except Exception as e:
                logger.exception(f'EXCEPTION parsing attribute: {e}')
                sys.exit()
            attribute = AttributeModel(name=attribute_name)
            attributes[attribute_id] = attribute

    def parse_class_operations(self, class_node):
        operations = {}
        try:
            operation_nodes = [node for node in class_node.children if
                               node.name == FieldNames.OWNED_OPERATION]
        except Exception as e:
            logger.exception(f'EXCEPTION getting operation nodes: {e}')
            sys.exit()
        for operation_node in operation_nodes:
            try:
                try:
                    operation_name = operation_node[FieldNames.NAME]
                # handle no name
                except Exception as e:
                    operation_name = Placeholders.EMPTY_OPERATION_NAME
                operation_id = operation_node[FieldNames.XMI_ID]
            except Exception as e:
                logger.exception(f'EXCEPTION parsing operation: {e}')
                sys.exit()
            try:
                parameter_nodes = [node for node in operation_node.children if
                                   node.name == FieldNames.OWNED_PARAMETER]
            except Exception as e:
                logger.exception(f'EXCEPTION getting parameter nodes: {e}')
                sys.exit()
            for parameter_node in parameter_nodes:
                try:
                    try:
                        parameter_name = parameter_node[FieldNames.NAME]
                    # handle no name
                    except Exception as e:
                        parameter_name = Placeholders.EMPTY_PARAMETER_NAME
                    # TODO: Check parameter type = "return" and add to OperationModel return type
                except Exception as e:
                    logger.exception(f'EXCEPTION parsing parameter: {e}')
                    sys.exit()
                parameter = ParameterModel(name=parameter_name)
            operation = OperationModel(name=operation_name)
            operations[operation_id] = operation

    def parse_class(self, class_node):
        try:
            try:
                class_name = class_node[FieldNames.NAME]
            # handle no name
            except Exception as e:
                class_name = Placeholders.EMPTY_CLASS_NAME
            class_attributes = self.parse_class_attributes(class_node)
            class_operations = self.parse_class_operations(class_node)
        except Exception as e:
            logger.exception(f'EXCEPTION parsing class: {e}')
            sys.exit()
        # Create ClassModel Object and add to dict
        try:
            return ClassModel(class_name, )
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
            class_id = class_node[FieldNames.XMI_ID]  # TODO: try-except around this?
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
                # Get name of relationship from XMI file or set it based on relationship type
                relationship_name = ''
                try:
                    relationship_name = relationship_node[FieldNames.NAME]
                except Exception as e:
                    try:
                        match relationship_node[FieldNames.XMI_TYPE]:
                            # TODO: Add cases for known relationships, use constants and translate later in renderGerman
                            case _:
                                relationship_name = relationship_node[FieldNames.XMI_TYPE]
                    except Exception as e:
                        logger.exception(f'ERROR: no relationship name or type found for {relationship_node}')
                        sys.exit()
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

    for relationship in relationships.values():
        print(f'{relationship.name}: {relationship.source} -> {relationship.target}')
        print(f'{relationship.name}: {classes[relationship.source].name} -> {classes[relationship.target].name}')
