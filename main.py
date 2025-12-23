import argparse
from parser.ParseXMI import XmiParser
from renderer.RenderGerman import GermanRenderer

if __name__ == "__main__":
    """Main function"""
    print('START TEST')
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
    # Parse
    relationships = xmi_parser.get_all_relationships()
    classes = xmi_parser.get_all_classes()
    # Render
    german_renderer = GermanRenderer()
    for class_object in classes.values():
        print(german_renderer.render_class(class_object))

    print('END TEST')
