import ply.lex as lex

tokens = [
      'LAM',
      'DOT',
      'VAR',
      'LPAR',
      'RPAR',     
      ]
  
class Lexer(object):
  tokens = tokens

  alpha = r'[a-z][A-Z]'
  var = r'alpha\w+'
  t_LAM = r'\\'
  t_VAR = r'[a-zA-Z]\w*'
  t_LPAR = r'\('
  t_RPAR = r'\)'

  t_DOT = r'\.'
  

  t_ignore = ' \t'
  t_ignore_COMMENT = r'--.*'

  def t_error(self,t):
      print("Illegal char '%s'" % t.value[0])
      t.lexer.skip(1)

  def t_newline(self,t):
      r'\n+'
      t.lexer.lineno += len(t.value)

  def build(self, **kwargs):
      self.lexer = lex.lex(module=self, **kwargs)

  def test(self,data):
      self.lexer.input(data)
      while True:
        tok = self.lexer.token()
        if not tok: 
            break      # No more input
        print(tok)

# quick test apparatus    
# data = '''
# -- comment
# \ b . ( b c d )
# '''
# 
# l = Lexer()
# l.build()
# l.test(data)



