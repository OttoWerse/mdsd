from bs4 import BeautifulSoup
import lxml


class XmiParser:
    def __init__(self, file_path):
        try:
            # TODO: Check if file is actually an XML file!
            file_object = open(file_path, 'r')
            file_content = file_object.read()
            # TODO: Check for lxml installed! (required by BS4 but not correctly enforced)
            self.xmi_tree = BeautifulSoup(file_content, 'xml')
        except Exception as e:
            print(f'{e}')

    def find_all_elements_by_name(self, name):
        """Finds elements of a given name in entire tree"""
        #
        if self.xmi_tree is None:
            pass
        result = self.xmi_tree.find_all(name)
        # TODO: Check if result is None or nah?
        return result


if __name__ == '__main__':
    """Main function"""
    parser = XmiParser(r'H:\Users\Otto\Documents\VPProjects\facade_mikrowelle.xmi')
    classes = []
    associations = []
    nodes = parser.find_all_elements_by_name('ownedMember')
    for node in nodes:
        try:
            # node_namespace = node.namespace
            # node_name = node.name
            # node_value = node.value
            node_type = node['xmi:type']
            match node_type:
                case 'uml:Class':
                    classes.append(node)
                case 'uml:Association':
                    associations.append(node)
        except Exception as e:
            print(f'{e}')
    # Handle associations
    for association in associations:
        try:
            association_name = association['name']
        except Exception as e:
            try:
                # TODO: Remove namespace and translate
                association_name = association['xmi:type']
            except Exception as e:
                association_name = 'uses'
                print(f'{e}')
        input(association_name)
