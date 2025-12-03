import ply.lex as lex

# tokens
tokens = (
    'LBRACE', 'RBRACE',     # { }
    'LBRACKET', 'RBRACKET', # [ ]
    'COMMA', 'COLON',       # , :
    'STRING', 'NUMBER'      # "texto", 123
)

# reglas de expresiones regulares 
t_LBRACE    = r'\{'
t_RBRACE    = r'\}'
t_LBRACKET  = r'\['
t_RBRACKET  = r'\]'
t_COMMA     = r','
t_COLON     = r':'

# regla para Strings (incluyendo comillas)
def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'

    return t

# regla para Números
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# ignorar espacios y tabs
t_ignore = ' \t\n\r'

def t_error(t):
    print("Caracter ilegal '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()