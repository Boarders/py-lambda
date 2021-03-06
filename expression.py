from functools import reduce
from dataclasses import dataclass
from collections import deque

def app(set1,set2):
    s = set1
    s.union(set2)
    return s

class Expr:
    pass

@dataclass
class Lam (Expr):
    var : str
    body : Expr

    def __str__(self):
        return ("(\\" + str(self.var) + " . " + str(self.body) + ")")

    def fvs(self):
        fvs = { fv for fv in self.body.fvs() if fv != self.var}
        return fvs

    def subst(self, v, arg):
        body = self.body
        free_vars = arg.fvs()
        vrs = app(free_vars,body.fvs())
        var = self.var

        def fresh(v):
            if v in vrs:
                return (fresh (v + "'"))
            else:
                return v
        if v == var:
            return self
        elif var in free_vars:
            v_new = fresh(var)
            body_new = body.subst(var, Var(v_new))
            return Lam(v_new, body_new.subst(v, arg))
        else:
            return Lam(self.var, body.subst(v, arg))

    def spine(self, stack):
        var  = self.var
        body = self.body
        if len(stack) == 0:
            return (Lam (var, nf(body)))
        else:
            head = stack.pop()
            tail = stack
            return (body.subst(var,head).spine(tail))

@dataclass
class App (Expr):
    fun : Expr
    arg : Expr

    def __str__(self):
        return (str(self.fun) + " " + str(self.arg))

    def fvs(self):
        fun_vs = (self.fun).fvs()
        arg_vs = (self.arg).fvs()
        return (app(fun_vs, arg_vs))

    def subst(self, v, arg):
        return App(self.fun.subst(v, arg), self.arg.subst(v, arg))

    def spine(self,stack):
        fun = self.fun
        arg = self.arg
        stack.append(arg)
        return fun.spine(stack)

@dataclass
class Var (Expr):
    var : str

    def __str__(self):
         return self.var

    def fvs(self):
        return {self.var}

    def subst(self, v, arg):
        if self.var == v:
            return arg
        else:
            return(Var(self.var))

    def spine(self, stack):
        unf = lambda acc, x : App (acc, nf(x))
        return reduce (unf, stack, Var(self.var))


def nf(lam):
    d = deque()
    return lam.spine(d)

z = Var("z")
s = Var("s")
n = Var("n")
m = Var("m")
zero = Lam("s", Lam("z", z))
succ = Lam("n", Lam("s", Lam("z", App(s, (App(App(n, s), z))))))
one = nf(App(succ, zero))
two = nf(App(succ, one))
msz = App (App(m,s), z)
add = Lam ("n", (Lam("m", Lam("s", (Lam("z", App(App(n, s), msz)))))))
four = nf(App(App(add, two), two))
eight = nf(App(App(add, four), four))
# test expression
# print(eight)
