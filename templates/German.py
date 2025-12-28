from string import Template

"""TEMPLATES"""
CLASS_DESCRIPTION = Template(
"""Die Klasse "$class_name" repräsentiert eine Einheit im System. 
Sie besitzt die Attribute: $attribute_list. 
Zusätzlich stellt sie die folgenden Methoden bereit: $method_list."""
)


TYPE_DESCRIPTION = Template(
"""Der Typ von "$element_name" ist "$type_name"."""
)


VISIBILITY_DESCRIPTION = Template(
"""Die Sichtbarkeit von "$element_name" ist "$visibility"."""
)

ATTRIBUTE_DESCRIPTION = Template(
"""$attribute_name" vom Typ "$attribute_type" mit Sichtbarkeit "$attribute_visibility"""
)

FIELD_DESCRIPTION = Template(
"""Das Feld "$field_name" ist vom Typ "$field_type" und hat die Sichtbarkeit "$field_visibility"."""
)


PARAMETER_DESCRIPTION = Template(
"""$parameter_name: $parameter_type"""
)



METHOD_DESCRIPTION = Template(
""""$method_name($parameters_list) : $return_type)" ($method_visibility)"""
)

OPERATION_DESCRIPTION = Template(
"""Die Operation "$operation_name" ist "$visibility" sichtbar, akzeptiert die Parameter ($parameters_list) und liefert einen Wert vom Typ "$return_type" zurück."""
)


RELATIONSHIP_DESCRIPTION = Template(
"""Zwischen "$source" und "$target" besteht eine Beziehung vom Typ "$relation_type"."""
)


