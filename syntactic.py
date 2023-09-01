class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def programa(self):
        self.match('KEYWORD', 'program')
        self.match('ID')
        self.match('DELIMITER', ';')
        self.corpo()
        self.match('DELIMITER', '.')
        if self.tokens[self.current][0] == 'DELIMITER' and self.tokens[self.current][1] == '.':
            return
        else:
            self.error("Não é possível declarar nada fora do escopo principal!")

    def corpo(self):
        self.declara()
        self.match('KEYWORD', 'begin')
        self.comandos()
        self.match('KEYWORD', 'end')

    def corpo_funcao(self):
        self.declara()
        self.match('KEYWORD', 'begin')
        self.comandos()
        self.match('KEYWORD', 'end')
        self.match('DELIMITER', ';')

    def comandos(self):
        self.comando()
        self.mais_comandos()
    
    def chamada_procedimento(self):
        if self.tokens[self.current][0] == 'DELIMITER' and self.tokens[self.current][1] == '(':
            self.match('DELIMITER', '(')
            self.var()
            self.match('DELIMITER', ')')

    def comando(self):
        if self.tokens[self.current][0] == 'KEYWORD' and self.tokens[self.current][1] == 'read':
            self.match('KEYWORD', 'read')
            self.match('DELIMITER', '(')
            self.var()
            self.match('DELIMITER', ')')
            self.match('DELIMITER', ';')
            self.comando()

        elif self.tokens[self.current][0] == 'ID':
            self.expressao()
            self.comando()

        elif self.tokens[self.current][0] == 'KEYWORD' and self.tokens[self.current][1] == 'return':
            self.match('KEYWORD', 'return')
            self.match('DELIMITER', ';')
            self.comando()
            
        elif self.tokens[self.current][0] == 'KEYWORD' and self.tokens[self.current][1] == 'write':
            self.match('KEYWORD', 'write')
            self.match('DELIMITER', '(')
            self.var()
            self.match('DELIMITER', ')')
            self.match('DELIMITER', ';')
            self.comando()

        elif self.tokens[self.current][0] == 'KEYWORD' and self.tokens[self.current][1] == 'for':
            self.match('KEYWORD', 'for')
            self.match('ID')
            self.match('OPERATOR', ':=')
            self.var()
            self.match('KEYWORD', 'to')
            self.var()
            self.match('KEYWORD', 'do')
            self.match('KEYWORD', 'begin')
            self.comando()
            self.match('KEYWORD', 'end')
            self.comando()

        elif self.tokens[self.current][0] == 'KEYWORD' and self.tokens[self.current][1] == 'repeat':
            self.match('KEYWORD', 'repeat')
            self.comando()
            self.match('KEYWORD', 'until')
            self.match('DELIMITER', '(')
            self.termo()
            self.match('DELIMITER', ')')
            self.comando()

        elif self.tokens[self.current][0] == 'KEYWORD' and self.tokens[self.current][1] == 'while':
            self.match('KEYWORD', 'while')
            self.match('DELIMITER', '(')
            self.termo()
            self.match('DELIMITER', ')')
            self.match('KEYWORD', 'do')
            self.match('KEYWORD', 'begin')
            self.comando()
            self.match('KEYWORD', 'end')
            self.comando()

        elif self.tokens[self.current][0] == 'KEYWORD' and self.tokens[self.current][1] == 'if':
            self.match('KEYWORD', 'if')
            self.match('DELIMITER', '(')
            self.termo()
            self.match('DELIMITER', ')')
            self.match('KEYWORD', 'then')
            #self.match('KEYWORD', 'begin')
            self.comando()
            #self.match('KEYWORD', 'end')
            #self.pfalsa()
            #self.comando()

    def pfalsa(self):
        if self.tokens[self.current][0] == 'KEYWORD' and self.tokens[self.current][1] == 'else':
            self.match('KEYWORD', 'else')
            self.match('KEYWORD', 'begin')
            self.comando()
            self.match('KEYWORD', 'end')

    def expressao(self):
        self.match('ID')
        if self.tokens[self.current][0] == 'OPERATOR' and self.tokens[self.current][1] == ':=':
            self.match('OPERATOR', ':=')
            self.var()
            self.match('DELIMITER', ';')
        elif self.tokens[self.current][0] == 'DELIMITER' and self.tokens[self.current][1] == '(':
            self.match('DELIMITER', '(')
            self.var()
            self.match('DELIMITER', ')')
            self.match('DELIMITER', ';')
        else:
            self.match(':= ou ()')

    def mais_comandos(self):
        if self.tokens[self.current][1] in ('read', 'write', 'for', 'while', 'if', 'repeat') or self.tokens[self.current][0] == 'ID':
            self.comandos()

    def var(self):
        if self.tokens[self.current][0] in ['INTEGER_NUM', 'REAL_NUM']:
            self.match(self.tokens[self.current][0])
        elif self.tokens[self.current][0] == 'ID':
            self.match('ID')
            self.chamada_procedimento()
        else:
            self.termo()

        self.mais_var_comando()

    def mais_var_comando(self):
        if self.tokens[self.current][0] == 'DELIMITER' and self.tokens[self.current][1] == ',':
            self.match('DELIMITER', ',')
            if self.tokens[self.current][0] == 'DELIMITER' and self.tokens[self.current][1] == ')':
                self.match("IDENTIFICADOR OU NUM OU CHAMADA PROCEDIMENTO")
            else:
                self.var()

    def corpo_procedimento(self):
        self.declara()
        self.match('KEYWORD', 'begin')
        self.comandos()
        self.match('KEYWORD', 'end')
        self.match('DELIMITER', ';')

    def funcao(self):
        self.match('KEYWORD', 'function')
        self.match('ID')
        self.parametros()
        self.match('DELIMITER', ':')    
        self.tipo_var()
        self.match('DELIMITER', ';')
        self.corpo_funcao()

    def procedimento(self):
        self.match('KEYWORD','procedure')
        self.match('ID')
        self.parametros()
        self.match('DELIMITER', ';')
        self.corpo_procedimento()

    def parametros(self):
        self.match('DELIMITER', '(')
        self.lista_parametros()
        self.match('DELIMITER', ')')

    def termo(self):
        if self.tokens[self.current][0] == 'ID' or self.tokens[self.current][0] in ['INTEGER_NUM', 'REAL_NUM']:
            self.match(self.tokens[self.current][0])
        elif self.tokens[self.current][0] == 'OPERATOR' and self.tokens[self.current][1] in ['+', '-', '*', '/', '>', '<', '>=', '<=', '=', '<>']:
            self.match('OPERATOR', self.tokens[self.current][1])
            self.match('DELIMITER', '(')
            self.termo()
            self.match('DELIMITER', ',')
            if self.tokens[self.current][0] == 'DELIMITER' and self.tokens[self.current][1] == ')':
                self.match('IDENTIFICADOR OU NUMERO OU CHAMADA PROCEDIMENTO')
            else:
                self.termo()
                self.match('DELIMITER', ')')
        elif self.tokens[self.current][0] == 'KEYWORD' and self.tokens[self.current][1] in ('input', 'output', 'length','inverte'):
            self.match('KEYWORD', self.tokens[self.current][1])
            self.match('DELIMITER', '(')
            self.um_conteudo()
            self.match('DELIMITER', ')')
        elif self.tokens[self.current][0] == 'KEYWORD' and self.tokens[self.current][1] == 'concatena':
            self.match('KEYWORD', self.tokens[self.current][1])
            self.match('DELIMITER', '(')
            self.dois_conteudo()
            self.match('DELIMITER', ')')
        elif self.tokens[self.current][0] == 'DELIMITER' and self.tokens[self.current][1] == ')':
            return
        else:
            self.match('IDENTIFICADOR OU NUMERO OU OPERADOR')

    def um_conteudo(self):
        self.match('DELIMITER', '#')
        self.valor_conteudo()
        self.match('DELIMITER', '#')
    
    def dois_conteudo(self):
        self.match('DELIMITER', '#')
        self.valor_conteudo()
        self.match('DELIMITER', '#')
        self.match('DELIMITER', ',')
        self.match('DELIMITER', '#')
        self.valor_conteudo()
        self.match('DELIMITER', '#')

    def valor_conteudo(self):
        if self.tokens[self.current][0] in ['INTEGER_NUM', 'REAL_NUM']:
            self.match(self.tokens[self.current][0])

        self.mais_valor_conteudo()

    def mais_valor_conteudo(self):
        if self.tokens[self.current][0] == 'DELIMITER' and self.tokens[self.current][1] == ',':
           self.match('DELIMITER', ',')
           self.valor_conteudo()

    def lista_parametros(self):
        self.declaracao_param()
        self.mais_param()

    def declaracao_param(self):
        if self.tokens[self.current][0] == 'ID':
            self.match('ID')
            self.match('DELIMITER', ':')
            self.tipo_var()

    def mais_param(self):
        if self.tokens[self.current][0] == 'DELIMITER' and self.tokens[self.current][1] == ';':
            self.match('DELIMITER', ';')
            if self.tokens[self.current][0] == 'ID':
                self.declaracao_param()
                self.mais_param()
            else:
                self.match('ID')

    def declara(self):
        if self.tokens[self.current][0] == 'KEYWORD' and self.tokens[self.current][1] == 'var':
            self.match('KEYWORD', 'var')
            self.dvar()
            self.match('DELIMITER', ';')
            self.mais_dc()
            self.declara()
        
        elif self.tokens[self.current][0] == 'KEYWORD' and self.tokens[self.current][1] in ('function'):
            self.funcao()
            self.declara()

        elif self.tokens[self.current][0] == 'KEYWORD' and self.tokens[self.current][1] in ('procedure'):
            self.procedimento()
            self.declara()
    
    def mais_dc(self):
        if self.tokens[self.current][0] == 'DELIMITER' and self.tokens[self.current][1] == ';':
            self.match('DELIMITER', ';')
            self.cont_dc()
  
    def dvar(self):
        self.variaveis()
        self.match('DELIMITER', ':')
        self.tipo_var()
        
    def tipo_var(self):
        if self.tokens[self.current][0] == 'KEYWORD' and self.tokens[self.current][1] in ['integer', 'real', 'pilha_of_integer', 'pilha_of_real']:
            self.match('KEYWORD', self.tokens[self.current][1])
        else:
            self.error("Tipo de variável inválido.")

    def variaveis(self):
        self.match('ID')
        self.mais_var()

    def mais_var(self):
        if self.tokens[self.current][0] == 'DELIMITER' and self.tokens[self.current][1] == ',':
            self.match('DELIMITER', ',')
            self.variaveis()

    def match(self, expected_type, expected_value=None):
        if self.current >= len(self.tokens):
            self.error("Fim inesperado do arquivo.")
            
        token_type, token_value, _ = self.tokens[self.current]
        if token_type != expected_type or (expected_value is not None and token_value != expected_value):
            self.error(f"Token inesperado: {token_type} '{token_value}', esperava-se: {expected_type} '{expected_value if expected_value else ''}'.")

        if self.current == len(self.tokens)-1:
            return
        else:
            self.current += 1

    def error(self, message):
        _, _, line = self.tokens[self.current]
        raise SyntaxError(f"Linha {line}: {message}")
