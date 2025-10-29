import ply.lex as lex 

tokens = ('PA','PF','INT','OP')

t_PA= r'\('
t_PF= r'\)'
t_INT = r'[+\-]?\d+'
t_OP = r'[+\-*/]'


# 3 + 5 * (10 - 2)
# (8 / 4) + 7 - 2
# 
# P1: EXP -> INT OP EXP
#          | PRIORIDADE OP EXP 
#          | INT
# P2: PRIORIDADE -> PA EXP PF
#                  | ε


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