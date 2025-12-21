import argparse
import sys
from bs4 import BeautifulSoup
from constants import FieldNames
from models.AttributeModel import AttributeModel
from models.ClassModel import ClassModel
from models.OperationModel import OperationModel
from models.ParameterModel import ParameterModel
from models.RelationshipModel import RelationshipModel


class XmiParser:
    def __init__(self, file_path):
        try:
            # TODO: Check if file is actually an XML file!
            file_object = open(file_path, 'r')
            file_content = file_object.read()
            # TODO: Check for lxml installed! (required by BS4 but not correctly enforced)
            self.xmi_soup = BeautifulSoup(file_content, 'xml')
            # TODO: Is this all we really need?
            self.nodes = self.find_all_elements_by_name('ownedMember')
        except Exception as e:
            print(f'EXCEPTION initialising parser: {e}')
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
            print(f'EXCEPTION getting attribute nodes: {e}')
            sys.exit()
        for attribute_node in attribute_nodes:
            try:
                attribute_name = attribute_node[FieldNames.NAME]  # TODO: handle no name
                attribute_id = attribute_node[FieldNames.XMI_ID]  # TODO: try-except around this?
            except Exception as e:
                print(f'EXCEPTION parsing attribute: {e}')
                sys.exit()
            attribute = AttributeModel(name=attribute_name)
            print(f'{attribute}')
            attributes[attribute_id] = attribute

    def parse_class_operations(self, class_node):
        operations = {}
        try:
            operation_nodes = [node for node in class_node.children if
                               node.name == FieldNames.OWNED_OPERATION]
        except Exception as e:
            print(f'EXCEPTION getting operation nodes: {e}')
            sys.exit()
        for operation_node in operation_nodes:
            try:
                operation_name = operation_node[FieldNames.NAME]  # TODO: handle no name
                operation_id = operation_node[FieldNames.XMI_ID]
            except Exception as e:
                print(f'EXCEPTION parsing operation: {e}')
                sys.exit()
            try:
                parameter_nodes = [node for node in operation_node.children if
                                   node.name == FieldNames.OWNED_PARAMETER]
            except Exception as e:
                print(f'EXCEPTION getting parameter nodes: {e}')
                sys.exit()
            for parameter_node in parameter_nodes:
                try:
                    parameter_name = parameter_node[FieldNames.NAME]  # TODO: handle no name
                    # TODO: Check parameter type = "return" and add to OperationModel return type
                except Exception as e:
                    print(f'EXCEPTION parsing parameter: {e}')
                    sys.exit()
                parameter = ParameterModel(name=parameter_name)
                print(f'{parameter}')
            operation = OperationModel(name=operation_name)
            print(f'{operation}')
            operations[operation_id] = operation

    def parse_class(self, class_node):
        try:
            class_name = class_node[FieldNames.NAME]  # TODO: handle no name
            class_attributes = self.parse_class_attributes(class_node)
            class_operations = self.parse_class_operations(class_node)
        except Exception as e:
            print(f'EXCEPTION parsing class: {e}')
            sys.exit()
        # Create ClassModel Object and add to dict
        try:
            return ClassModel(class_name, )
        except Exception as e:
            print(f'EXCEPTION creating class model: {e}')
            sys.exit()

    def get_all_classes(self):
        """Returns all classes in the parsers xml tree"""
        return_classes = {}
        try:
            class_nodes = [node for node in self.nodes if
                           node[FieldNames.XMI_TYPE] == FieldNames.UML_CLASS]
        except Exception as e:
            print(f'EXCEPTION getting class nodes: {e}')
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
            print(f'EXCEPTION getting relationship nodes: {e}')
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
                        print(f'ERROR: no relationship name or type found for {relationship_node}')
                        sys.exit()
                # Get ends of relationship from XMI
                ends = [child[FieldNames.TYPE] for child in relationship_node.children if
                        child.name == FieldNames.OWNED_END]
                # Check for exactly two ends
                if len(ends) != 2:
                    print(f'ERROR: more than two ends found for {relationship_name}')
                    sys.exit()
                # Set left and right end of relationship
                left_end = ends[0]
                right_end = ends[1]
                # Create RelationshipModel Object and add to dict
                return_relationships[relationship_id] = RelationshipModel(relationship_name, left_end, right_end)
            except Exception as e:
                print(f'EXCEPTION parsing relationship: {e}')
                sys.exit()
        return return_relationships


if __name__ == '__main__':
    """Main function"""
    argument_parser = argparse.ArgumentParser("ParseXMI")
    argument_parser.add_argument("--xmi_path",
                                 type=str,
                                 help="Speicherpfad der XMI Datei",
                                 nargs='?',
                                 const=0, )
    args = argument_parser.parse_args()
    xmi_parser = XmiParser(args.xmi_path)

    relationships = xmi_parser.get_all_relationships()
    classes = xmi_parser.get_all_classes()

    for relationship in relationships.values():
        print(f'{relationship.name}: {relationship.source} -> {relationship.target}')
        print(f'{relationship.name}: {classes[relationship.source].name} -> {classes[relationship.target].name}')
