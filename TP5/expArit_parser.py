from expArit_lexer import lexer 

prox_symb = None 

#P1: EXP   -> TERMO EXP2
#P2: EXP2  -> OP_SOMA TERMO EXP2 
#P3:         | ε
#P4: TERMO -> FATOR TERMO2
#P5: TERMO2 -> OP_MULT FATOR TERMO2 
#P6:          | ε
#P7: FATOR -> INT 
#P8:          | PA EXP PF
# OP_SOMA -> + 
#           | -
# OP_MULT -> * 
#           | /

#EXP > TERMO > FATOR
def parserError(symb):
    print("Erro sintático, token inesperado: ", symb)

def rec_term(symb):
    global prox_symb
    if prox_symb.type == symb:
        prox_symb = lexer.token()
    else:
        parserError(prox_symb)
        prox_symb = ('erro', '', 0, 0)

def fator():
    global prox_symb
    if prox_symb.type == 'INT':
        print("DERIVAR INT DE P7: FATOR -> INT ")
        rec_term('INT')
        print("Reconheci INT DE P7: FATOR -> INT")
    if prox_symb.type == 'PA':
        print("DERIVAR PA DE P8: FATOR -> PA EXP PF")
        rec_term('PA')
        print("Reconheci PA DE P8: FATOR -> PA EXP PF")
    if prox_symb.type == 'PF': #acaba 
        print("DERIVAR PF DE P8: FATOR -> PA EXP PF")
        rec_term('PF')
        print("Reconheci PF DE P8: FATOR -> PA EXP PF")
def exp():
    global prox_symb
    if prox_symb.type == 'INT':

