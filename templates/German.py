from string import Template

ATTRIBUTE_DESCRIPTION = Template("""$attribute_visibility $attribute_name""")
METHOD_DESCRIPTION = Template("""$method_visibility $method_name ($parameters_list)""")
CLASS_DESCRIPTION = Template("""Eine Klasse mit dem Namen $class_name. 
Sie hat die folgenden $attribute_count Attrbitue: 
$attribute_list
Sie hat die folgenden $method_count Methoden: 
$method_list""")
