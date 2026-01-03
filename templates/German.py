from string import Template

from constants.FieldNames import VISIBILITY

"""Placeholders for empty names"""
EMPTY_ATTRIBUTE_NAME = 'Namenloses Attribut'
EMPTY_OPERATION_NAME = 'Namenlose Methode'
EMPTY_PARAMETER_NAME = 'Namenloser Parameter'
EMPTY_CLASS_NAME = 'Namenlose Klasse'
EMPTY_RELATIONSHIP_NAME = 'Namenlose Beziehung'

"""Strings for known types"""
ASSOCIATION_NAME = 'Assoziation'

"""Strings for visibility"""
VISIBILITY_UNKNOWN = 'undefiniert sichtbare'
VISIBILITY_PRIVATE = 'privates'
VISIBILITY_PUBLIC = 'öffentliche'
VISIBILITY_PROTECTED = 'geschützte'
VISIBILITY_PACKAGE = 'paketweit sichtbare'

"""Templates"""
# TODO: separate template into it's sub parts to remove empty method and attribute sections from print
# TODO: remove count in case of 1
CLASS_DESCRIPTION = Template(
    '''Die Klasse "$class_name" repräsentiert eine Einheit im System. 
Sie besitzt $attribute_count Attribute. $attribute_list
Zusätzlich stellt sie $method_count Methoden bereit. $method_list
'''
)

TYPE_DESCRIPTION = Template(
    '''Der Typ von "$element_name" ist "$type_name". '''
)

VISIBILITY_DESCRIPTION = Template(
    '''Die Sichtbarkeit von "$element_name" ist "$visibility". '''
)

ATTRIBUTE_DESCRIPTION = Template(
    '''Ein $attribute_visibility Attribut "$attribute_name" vom Typ "$attribute_type". '''
)

"""Operations"""
OPERATION_DESCRIPTION_MULTIPLE = Template(
    '''Die $visibility Methode "$operation_name" mit Rückgabewert "$return_type" und $parameters_count Parametern. $parameters_list'''
)
OPERATION_DESCRIPTION_SINGLE = Template(
    '''Die $visibility Methode "$operation_name" liefert einen Wert vom Typ "$return_type" zurück und akzeptiert einen Parameter $parameters_text. '''
)
"""Parameters"""
PARAMETER_DESCRIPTION_SINGLE = Template(
    '''"$parameter_name" vom Typ "$parameter_type"'''
)
PARAMETER_DESCRIPTION_MULTIPLE = Template(
    '''Einen Parameter "$parameter_name" vom Typ "$parameter_type". '''
)

RELATIONSHIP_DESCRIPTION = Template(
    '''Zwischen "$source" und "$target" besteht eine Beziehung vom Typ "$relation_type".'''
)
