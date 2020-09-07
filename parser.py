import ply.yacc as yacc


from lex import tokens
from expression import Lam, App, Var



def p_lam_expr(p):
    'expr : LAM VAR DOT expr'
    p[0] = Lam(p[2], p[4])

def p_spine_expr(p):
    'expr : spine'
    p[0] = p[1]

def p_spine_comp(p):
    'spine : spine atom'
    p[0] = App(p[1], p[2])

def p_spine_sing(p):
    'spine : atom'
    p[0] = p[1]

def p_atom_expr(p):
    'atom : LPAR expr RPAR'
    p[0] = p[2]

def p_atom_var(p):
    'atom : VAR'
    p[0] = Var(p[1])


parser = yacc.yacc()

while True:
    try:
        s = input('lam > ')
    except EOFError:
        break
    if not s: continue
    result = parser.parse(s)
    print(result)
