from string import Template

"""TEMPLATES"""
CLASS_DESCRIPTION = Template("""Eine Klasse mit dem Namen $class_name. 
Sie hat die folgenden $attribute_count Attrbitue: 
$attribute_list
Sie hat die folgenden $method_count Methoden: 
$method_list""")
TYPE_DESCRIPTION = Template("""Typ: $type_name""")
VISIBILITY_DESCRIPTION = Template("""Sichtbarkeit: $visibility""")
ATTRIBUTE_DESCRIPTION = Template("""Ein $attribute_visibility Attribut mit dem Namen "$attribute_name" vom Typ $attribute_type""")
FIELD_DESCRIPTION = Template("""$field_visibility $field_name : $field_type""")
PARAMETER_DESCRIPTION = Template("""$parameter_type $parameter_name""")
METHOD_DESCRIPTION = Template("""$method_visibility $method_name($parameters_list) : $return_type""")
OPERATION_DESCRIPTION = Template("""$visibility $operation_name($parameters_list) : $return_type""")
RELATIONSHIP_DESCRIPTION = Template("""Beziehung: $source --[$relation_type]--> $target""")