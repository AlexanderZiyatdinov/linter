class Java:
    bracket_operators_and_calls = '()[]{}<>.;'
    quoates = r""""'"""
    common_classes = ['System', 'Math']
    operators = '()[]{}<>+-*/%=!&|^~?:;.'
    primitives = ['byte', 'short', 'int',
                  'long', 'char', 'float', 'double', 'boolean', 'String']
    control_structures = ['if', 'else', 'switch', 'case', 'default', 'while',
                          'do', 'break', 'continue', 'for']
    exceptions = ['try', 'catch', 'finally', 'throw', 'throws']
    scopes = ['private', 'protected', 'public']
    ads = ['import', 'package', 'class', 'interface', 'extends', 'implements',
           'static', 'final', 'void', 'abstract', 'native']
    calls = ['new', 'return', 'this', 'super']

    keywords = [*primitives, *control_structures, *exceptions,
                *scopes, *ads, *calls]


class Cpp:
    pass
