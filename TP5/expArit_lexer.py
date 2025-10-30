import ply.lex as lex 

tokens = ('PA','PF','INT','OP')

t_PA= r'\('
t_PF= r'\)'
t_INT = r'\d+'
t_OP = r'[+\-*/]'


# EXP   -> TERMO EXP2
# EXP2  -> OP_SOMA TERMO EXP2 
#         | ε
# TERMO -> FATOR TERMO2
# TERMO2 -> OP_MULT FATOR TERMO2 
#          | ε
# FATOR -> INT | PA EXP PF
#
# OP_SOMA -> + | -
# OP_MULT -> * | /

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
t_ignore = ' \t'

def t_error(t):
    print("Caracter desconhecido '%s'", t.value[0], 'Linha', t.lexer.lineno)
    t.lexer.skip(1)
lexer = lex.lex()

lexer.input("3 + 5 * (10 - 2)")
for token in lexer:
    print(token.type,token.value)