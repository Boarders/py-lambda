def app(set1,set2):
    s = set1
    s.union(set2)
    return s

class Expr:
    pass

class Lam (Expr):
    def __init__(self, var, body):
        self.var = var
        self.body = body

    def __str__(self):
        return ("(\\" + str(self.var) + " . " + str(self.body) + ")")

    def fvs(self):
        body_fvs = self.body.fvs()
        if self.var in body_fvs:
            body_fvs.remove(self.var)
        return body_fvs

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
            head = stack[0]
            tail = stack[1:]
            return (body.subst(var,head).spine(tail))


class App (Expr):
    def __init__(self, fun, arg):
        self.fun = fun
        self.arg = arg

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
        return fun.spine([arg] + stack)


class Var (Expr):
    def __init__(self, var):
        self.var = var

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
        var = self.var
        acc = Var(var)
        for arg in stack:
            acc = App(acc, nf(arg))
        return acc


def nf(lam):
    return lam.spine([])

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
print(eight)
