from string import Template

"""Placeholders for empty names"""
EMPTY_ATTRIBUTE_NAME = 'Namenloses Attribut'
EMPTY_OPERATION_NAME = 'Namenlose Methode'
EMPTY_PARAMETER_NAME = 'Namenloser Parameter'
EMPTY_CLASS_NAME = 'Namenlose Klasse'
EMPTY_RELATIONSHIP_NAME = 'Namenlose Beziehung'

"""Strings for known types"""
ASSOCIATION_NAME = 'Assoziation'

"""Templates"""
# TODO: separate template into it's sub parts to remove empty method and attribute sections from print
# TODO: remove count in case of 1
CLASS_DESCRIPTION = Template(
    '''Die Klasse "$class_name" repräsentiert eine Einheit im System. 
Sie besitzt die folgenden $attribute_count Attribute: 
$attribute_list
Zusätzlich stellt sie die folgenden $method_count Methoden bereit: 
$method_list
'''
)

TYPE_DESCRIPTION = Template(
    '''Der Typ von "$element_name" ist "$type_name".'''
)

VISIBILITY_DESCRIPTION = Template(
    '''Die Sichtbarkeit von "$element_name" ist "$visibility".'''
)

ATTRIBUTE_DESCRIPTION = Template(
    '''Das Attribut "$attribute_name" ist vom Typ "$attribute_type" und hat die Sichtbarkeit "$attribute_visibility".'''
)

PARAMETER_DESCRIPTION = Template(
    '''"$parameter_name" vom Typ $parameter_type'''
)

METHOD_DESCRIPTION = Template(
    '''"$method_name($parameters_list) : $return_type)" ($method_visibility)'''
)

OPERATION_DESCRIPTION = Template(
    '''Die Methode "$operation_name" ist "$visibility" sichtbar, akzeptiert die folgenden $parameters_count Parameter: 
$parameters_list 
und liefert einen Wert vom Typ "$return_type" zurück.'''
)

RELATIONSHIP_DESCRIPTION = Template(
    '''Zwischen "$source" und "$target" besteht eine Beziehung vom Typ "$relation_type".'''
)
