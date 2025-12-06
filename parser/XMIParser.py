from bs4 import BeautifulSoup
# This is only here to make PyCharm check for this package!
import lxml


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
            print(f'EXCEPTION: {e}')

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
        classes = []
        for node in self.nodes:
            try:
                node_type = node['xmi:type']
                if node_type == 'uml:Class':
                    # TODO: Create ClassModel Object and append those instead
                    class_name = node['name']
                    classes.append(node)
            except Exception as e:
                print(f'EXCEPTION: {e}')
                return []
        return classes

    def get_all_associations(self):
        """Returns all associations in the parsers xml tree"""
        associations = []
        for node in self.nodes:
            try:
                node_type = node['xmi:type']
                if node_type == 'uml:Association':
                    # TODO: Create AssociationModel Object and append those instead
                    try:
                        association_name = node['name']
                    except Exception as e:
                        association_name = node['xmi:type']
                    ends = []
                    # TODO: Check for exactly 2 children!
                    for child in node.children:
                        match child.name:
                            case 'ownedEnd':
                                end_id = child['type']
                                ends.append(end_id)
                    left_end = ends[0]
                    right_end = ends[1]
                    print(f'{association_name} -> {left_end} -> {right_end}')
                    associations.append(node)
            except Exception as e:
                print(f'EXCEPTION: {e}')
                return []
        return associations


if __name__ == '__main__':
    """Main function"""
    parser = XmiParser(r'H:\Users\Otto\Documents\VPProjects\facade_mikrowelle.xmi')
    classes = parser.get_all_classes()
    associations = parser.get_all_associations()
