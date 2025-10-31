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
# OP_SOMA -> + | -
# OP_MULT -> * | /

def parserError(symb):
    print("Erro sintático, token inesperado:", symb)

def rec_term(symb):
    global prox_symb
    if prox_symb and prox_symb.type == symb:
        prox_symb = lexer.token()
    else:
        parserError(prox_symb)
        prox_symb = None

def fator():
    global prox_symb
    if prox_symb and prox_symb.type == 'INT':
        print("Derivar P7: FATOR -> INT")
        rec_term('INT')
        print("Reconheci P7: FATOR -> INT")
    elif prox_symb and prox_symb.type == 'PA':
        print("Derivar P8: FATOR -> PA EXP PF")
        rec_term('PA')
        exp()
        rec_term('PF')
        print("Reconheci P8: FATOR -> PA EXP PF")
    else:
        parserError(prox_symb)

def termo():
    global prox_symb
    if prox_symb and prox_symb.type in ['INT','PA']:
        print("Derivar P4: TERMO -> FATOR TERMO2")
        fator()
        termo2()
        print("Reconheci P4: TERMO -> FATOR TERMO2")
    else:
        parserError(prox_symb)

def op_mult():
    global prox_symb
    if prox_symb and prox_symb.type == 'OP' and prox_symb.value in ['*','/']:
        rec_term('OP')
    else:
        parserError(prox_symb)

def termo2():
    global prox_symb
    if prox_symb and prox_symb.type == 'OP' and prox_symb.value in ['*','/']:
        print("Derivar P5: TERMO2 -> OP_MULT FATOR TERMO2")
        op_mult()
        fator()
        termo2()
        print("Reconheci P5: TERMO2 -> OP_MULT FATOR TERMO2")
    else:
        print("Derivar P6: TERMO2 -> ε")
        return

def op_soma():
    global prox_symb
    if prox_symb and prox_symb.type == 'OP' and prox_symb.value in ['+','-']:
        rec_term('OP')
    else:
        parserError(prox_symb)

def exp2():
    global prox_symb
    if prox_symb and prox_symb.type == 'OP' and prox_symb.value in ['+','-']:
        print("Derivar P2: EXP2 -> OP_SOMA TERMO EXP2")
        op_soma()
        termo()
        exp2()
        print("Reconheci P2: EXP2 -> OP_SOMA TERMO EXP2")
    else:
        print("Derivar P3: EXP2 -> ε")
        return

def exp():
    global prox_symb
    if prox_symb and prox_symb.type in ['INT','PA']:
        print("Derivar P1: EXP -> TERMO EXP2")
        termo()
        exp2()
        print("Reconheci P1: EXP -> TERMO EXP2")
    else:
        parserError(prox_symb)


lexer.input("3 + 5 * (10 - 2)")
prox_symb = lexer.token()
exp()
