import sys

from bs4 import BeautifulSoup
# This is only here to make PyCharm check for this package!
import lxml

from constants import FieldNames
from models.ClassModel import ClassModel
from models.RelationshipModel import RelationshipModel


class XmiParser:
    def __init__(self, file_path):
        try:
            # TODO: Check if file is actually an XML file!
            file_object = open(file_path, 'r')
            file_content = file_object.read()
            # TODO: Check for lxml installed! (required by BS4 but not correctly enforced)
            self.xmi_tree = BeautifulSoup(file_content, 'xml')
            # TODO: Is this all we really need?
            self.nodes = self.find_all_elements_by_name('ownedMember')
        except Exception as e:
            print(f'EXCEPTION initialising parser: {e}')
            sys.exit()

    def find_all_elements_by_name(self, name):
        """Finds elements of a given name in entire tree"""
        #
        if self.xmi_tree is None:
            pass
        result = self.xmi_tree.find_all(name)
        # TODO: Check if result is None or nah?
        return result

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
            try:
                class_id = class_node[FieldNames.XMI_ID]
                class_name = class_node[FieldNames.NAME]
                # Create ClassModel Object and add to dict
                return_classes[class_id] = ClassModel(class_name, )
            except Exception as e:
                print(f'EXCEPTION parsing class: {e}')
                sys.exit()
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
    parser = XmiParser(r'H:\Users\Otto\Documents\VPProjects\facade_mikrowelle.xmi')
    relationships = parser.get_all_relationships()
    classes = parser.get_all_classes()

    for relationship in relationships.values():
        print(f'{relationship.name}: {relationship.source} -> {relationship.target}')
        print(f'{relationship.name}: {classes[relationship.source].name} -> {classes[relationship.target].name}')
