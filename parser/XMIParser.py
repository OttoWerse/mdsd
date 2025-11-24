import xml.etree.ElementTree as ET


class XmiParser:
    xmi_path_name = None

    def get_document_object(self):
        if self.xmi_path_name is None:
            # TODO: Log failure
            return None
        try:
            return ET.parse(self.xmi_path_name)  # TODO: Should this be root? .getRoot()

        except Exception as e:
            # TODO: Log failure
            print(e)
            return None

    def find_elements(self, parent_element, attr_name, attr_value, is_entire_document):
        if attr_name is None:
            return None
        if parent_element is None:
            # TODO: Log failure
            return None
        # TODO: use namespaces correctly
        # TODO: Constants and other such woke OOP nonsense
        if is_entire_document:
            xpath_expression = fr".//*[@{attr_name}='{attr_value}']"
        else:
            xpath_expression = fr"//*[@{attr_name}='%s']{attr_value}"
        parent_element.findall(xpath_expression)

    def get_elements_by_tag_name_namespace(self, param):
        # TODO
        pass

    def parse_models(self):
        root = self.get_document_object()
        root_node_list = self.get_elements_by_tag_name_namespace('uml')