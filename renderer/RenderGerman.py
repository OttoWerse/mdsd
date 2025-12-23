from models.ClassModel import ClassModel
from templates.German import CLASS_DESCRIPTION


class GermanRenderer:
    def __init__(self):
        pass

    def render_class(self, Class):
        name = Class.name
        attribute_count = len(Class.attributes)
        attribute_list = Class.attributes  # TODO: Format using loop and such BS
        method_count = len(Class.operations)
        method_list = Class.operations  # TODO: Format using loop and such BS

        return CLASS_DESCRIPTION.substitute(
            class_name=name,
            attribute_count=attribute_count,
            attribute_list=attribute_list,
            method_count=method_count,
            method_list=method_list,
        )
