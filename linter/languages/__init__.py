round_brackets = '()'
square_brackets = '[]'
figure_brackets = '{}'
triangle_brackets = '<>'


class Java:
    primitives = ['byte', 'short', 'int',
                  'long', 'char', 'float', 'double', 'boolean']
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