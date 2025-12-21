from models.ClassModel import ClassModel
from templates.German import CLASS_DESCRIPTION

if __name__ == "__main__":
    print('START TEST')
    Class = ClassModel(name='Mikrowelle', )
    print(CLASS_DESCRIPTION.substitute(class_name=Class.name,
                                       attribute_count=0,
                                       attribute_list='''''',
                                       method_count=0,
                                       method_list='''''',
                                       ))
    print('END TEST')
