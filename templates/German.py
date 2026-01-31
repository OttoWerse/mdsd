from string import Template

"""Placeholders for empty names"""
EMPTY_ATTRIBUTE_NAME = 'Namenloses Attribut'
EMPTY_OPERATION_NAME = 'Namenlose Methode'
EMPTY_PARAMETER_NAME = 'Namenloser Parameter'
EMPTY_CLASS_NAME = 'Namenlose Klasse'
EMPTY_RELATIONSHIP_NAME = 'Namenlose Beziehung'

"""Strings for known relationship types"""
ASSOCIATION_NAME = 'Assoziation'

"""Strings for known datatypes"""
DATATYPE_STRING = 'freitext'
DATATYPE_INTEGER = 'ganze Zahl'
DATATYPE_FLOAT = 'gleitkommazahl'
DATATYPE_VOID = 'Keine Wertübergabe'
# TODO: More advanced datatypes etc.

"""Strings for visibility"""
VISIBILITY_UNKNOWN = 'undefiniert sichtbare'
VISIBILITY_PRIVATE = 'privates'
VISIBILITY_PUBLIC = 'öffentliche'
VISIBILITY_PROTECTED = 'geschützte'
VISIBILITY_PACKAGE = 'paketweit sichtbare'

"""Templates"""
CLASSES_HEADING = 'Klassen: \n'
RELATIONSHIP_HEADING = 'Berechnungen: \n'

CLASS_DESCRIPTION = Template(
    '''Die Klasse "$class_name" repräsentiert eine Einheit im System. 
Sie besitzt $attribute_count Attribute; $attribute_list
Zusätzlich stellt sie $method_count Methoden bereit. $method_list
'''
)

TYPE_DESCRIPTION = Template('''Der Typ von "$element_name" ist "$type_name". ''')

VISIBILITY_DESCRIPTION = Template('''Die Sichtbarkeit von "$element_name" ist "$visibility". ''')

ATTRIBUTE_DESCRIPTION = Template(
    '''Ein $attribute_visibility Attribut namens "$attribute_name" vom Typ "$attribute_type". ''')

"""Operations"""
OPERATION_DESCRIPTION_MULTIPLE_WITH_RETURN = Template(
    '''Die $visibility Methode "$operation_name" mit Rückgabewert $return_type akzeptiert $parameters_count Parameter. $parameters_list'''
)
OPERATION_DESCRIPTION_MULTIPLE_NO_RETURN = Template(
    '''Die $visibility Methode "$operation_name" ohne Rückgabewert  akzeptiert $parameters_count Parameter. $parameters_list'''
)
OPERATION_DESCRIPTION_SINGLE_WITH_RETURN = Template(
    '''Die $visibility Methode "$operation_name" mit Rückgabewert $return_type akzeptiert einen Parameter $parameters_text. '''
)
OPERATION_DESCRIPTION_SINGLE_NO_RETURN = Template(
    '''Die $visibility Methode "$operation_name" ohne Rückgabewert akzeptiert einen Parameter $parameters_text. '''
)
"""Parameters"""
PARAMETER_DESCRIPTION_SINGLE = Template(
    '''"$parameter_name" vom Typ "$parameter_type"'''
)
PARAMETER_DESCRIPTION_MULTIPLE = Template(
    '''Einen Parameter "$parameter_name" vom Typ "$parameter_type". '''
)

RELATIONSHIP_NAME = Template(
    '''Beziehung namens "$relation_name"'''
)
RELATIONSHIP_DESCRIPTION = Template(
    '''Zwischen "$source" und "$target" besteht eine $relation_type.'''
)
