import cmd
from parser import parser
from expression import nf
import ply.yacc as yacc


class PyRepl(cmd.Cmd):
    intro = '''
                                   λλλ Py Lambda λλλ
    '''
    prompt = 'λ > '

    def do_EOF(self,line):
        return True
    def do_quit(self, arg):
        'Exit the repl'
        print('Thank your lambdas!')
        return True

    def default(self,line):
        parseExpr = parser.parse(line)
        print(nf(parseExpr))


if __name__ == '__main__':
    PyRepl().cmdloop()
