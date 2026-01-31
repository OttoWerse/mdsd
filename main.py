import argparse
from parser.ParseXMI import XmiParser
from renderer.RenderGerman import GermanRenderer

if __name__ == "__main__":
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
    # Parse
    relationships = xmi_parser.get_all_relationships()
    classes = xmi_parser.get_all_classes()
    # Render
    german_renderer = GermanRenderer(classes=classes,
                                     relationships=relationships, )
    output_string = german_renderer.render_class_diagram()
    save_file_input = input('Save output to file? (Y/N)')
    match save_file_input.lower():
        case 'y':
            with open('output.txt', 'w', encoding='utf-8') as file:
                file.write(output_string)
        case 'n':
            print(output_string)
