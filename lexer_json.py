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
t_STRING    = r'"[A-ÿ0-9;, \._@#$!%&*()_-]*"' 
t_NUMBER    = r'[0-9]+' 
t_ignore    = ' \t\n\r'  # ignorar espacios y tabs


def t_error(t):
    print("Illegal character ", t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()