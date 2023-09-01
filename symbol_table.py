import math

class SymbolTable:
    """Classe para representar uma tabela de símbolos com escopos hierárquicos."""

    def __init__(self, scope_name='global', parent=None):
        """Inicializa uma nova tabela de símbolos."""
        self.scope_name = scope_name
        self.symbols = {}
        self.parent = parent
        self.child_scopes = []

    def add_function(self, function_name, function_type, parameters=None):
        """Adiciona uma nova função ou procedimento à tabela de símbolos."""
        if function_name in self.symbols:
            raise ValueError(f"A função '{function_name}' já está definida no escopo atual.")
        self.symbols[function_name] = {'symbol': function_name, 'type': function_type, 'value': parameters}

    def get_function(self, function_name):
        """Recupera uma função ou procedimento da tabela de símbolos."""
        if function_name in self.symbols and self.symbols[function_name]['type'] in ['procedure', 'function']:
            return self.symbols[function_name]
        elif self.parent:
            return self.parent.get_function(function_name)
        else:
            raise ValueError(f"A função '{function_name}' não está definida em nenhum escopo.")

    def add_symbol(self, symbol, symbol_type, symbol_value=0, line=None):
        """Adiciona um novo símbolo à tabela."""
        if symbol in self.symbols:
            raise ValueError(f"O símbolo '{symbol}' já está definido no escopo atual.")
        self.symbols[symbol] = {'symbol': symbol, 'type': symbol_type, 'values': [(symbol_value, line)]}

    def get_symbol(self, symbol):
        """Recupera um símbolo da tabela de símbolos."""
        if is_number(symbol):
            return symbol  # Retorna None quando o símbolo é um número
        if symbol in self.symbols:
            return self.symbols[symbol]
        elif self.parent and self.scope_name != "global":
            return self.parent.get_symbol(symbol)
        else:
            raise ValueError(f"O símbolo '{symbol}' não está definido em nenhum escopo.")

    def update_symbol(self, symbol, value, line, add_start=False):
        """Atualiza o valor de um símbolo na tabela de símbolos."""
        if symbol in self.symbols:
            if not add_start:
                self.symbols[symbol]['values'].append((value, line))
            else:
                self.symbols[symbol]['values'][0] = (value,line)
        elif self.parent and self.scope_name != "global":
            self.parent.update_symbol(symbol, value, line)
        else:
            raise ValueError(f"O símbolo '{symbol}' não está definido em nenhum escopo.")

    def add_child_scope(self, child_scope):
        """Adiciona um escopo filho à tabela de símbolos."""
        self.child_scopes.append(child_scope)

    def enter_scope(self, scope_name):
        """Entra em um escopo filho."""
        for child_scope in self.child_scopes:
            if child_scope.scope_name == scope_name:
                return child_scope
        raise ValueError(f"O escopo '{scope_name}' não foi encontrado.")

    def exit_scope(self):
        """Sai do escopo atual."""
        if self.parent is None:
            raise ValueError("Não é possível sair do escopo atual, pois não há escopo pai.")
        return self.parent

    def update_function_parameters(self, function_name, parameters):
        function_scope = self.enter_scope(function_name)
        for param_name, param_value in parameters.items():
            function_scope.update_symbol(param_name, param_value, None)  # assuming line number is not important here

    def print_selected_scope(self, scope_name):
        scope = self.enter_scope(scope_name)
        scope.print_symbols()

    def print_symbols(self, indentation=''):
        print(f"Escopo '{self.scope_name}':")
        for symbol, data in self.symbols.items():
            print(f"{indentation}Símbolo: {symbol} | Tipo: {data['type']}")
            for value, line in data['values']:
                print(f"{indentation}\tValor: {value} | Linha: {line}")
        print("-------------------")
        # Para cada escopo filho, chama esta função recursivamente
        for child_scope in self.child_scopes:
            child_scope.print_symbols(indentation + '\t')

    def update_symbol_recursive(self, symbol, value, line):
        """Atualiza o valor de um símbolo na tabela de símbolos, exibindo também os valores vindos da recursão."""
        if symbol in self.symbols:
            if self.symbols[symbol]['values'][-1][0] != value:
                self.symbols[symbol]['values'].append((value, line))
                print(f"Valor atualizado de '{symbol}' para '{value}' na linha {line}")
        elif self.parent and self.scope_name != "global":
            self.parent.update_symbol_recursive(symbol, value, line)
        else:
            raise ValueError(f"O símbolo '{symbol}' não está definido em nenhum escopo.")
    
    def get_first_function_parameter(self, function_name):
        """Obtém o primeiro parâmetro de uma função."""
        function_data = self.get_function(function_name)
        parameters = function_data['value']
        if parameters:
            first_parameter_name = parameters[0]
            return self.get_symbol(first_parameter_name)['values'][-1][0]
        else:
            return None

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def create_symbol_table(tokens):
    # Cria uma tabela de símbolos global
    global_symbol_table = SymbolTable()
    current_symbol_table = global_symbol_table
    current = 0

    while current < len(tokens):
        token_type, token_value, token_line = tokens[current]

        if token_type == 'KEYWORD' and token_value == 'end':
            # Verifica se é o fim de um escopo e muda para o escopo pai
            if current_symbol_table.scope_name != 'global':
                current_symbol_table = global_symbol_table
            else:
                current_symbol_table = current_symbol_table.parent
            current += 1
            continue

        if token_type == 'KEYWORD' and token_value in ['procedure', 'function']:
            # Verifica se é a definição de uma função ou procedimento
            current += 1
            procedure_name = tokens[current][1]
            # Cria um novo escopo para a função ou procedimento
            new_symbol_table = SymbolTable(scope_name=procedure_name, parent=current_symbol_table)
            current_symbol_table.add_child_scope(new_symbol_table)
            current_symbol_table = new_symbol_table
            current += 2
            while tokens[current][1] != ')':
                if tokens[current][0] == 'ID':
                    # Processa os parâmetros da função ou procedimento
                    param_name = tokens[current][1]
                    current += 2
                    param_type = tokens[current][1]
                    current_symbol_table.add_symbol(param_name, param_type, 0, tokens[current][2])
                current += 1
            current += 1
            continue

        if token_type == 'KEYWORD' and token_value == 'var':
            # Verifica se é a definição de variáveis
            current += 1
            symbol_names = []
            while tokens[current][0] != 'DELIMITER' or tokens[current][1] != ';':
                if tokens[current][0] == 'ID':
                    # Processa os nomes das variáveis
                    symbol_names.append(tokens[current][1])
                elif tokens[current][0] == 'DELIMITER' and tokens[current][1] == ':':
                    current += 1
                    if tokens[current][0] == 'KEYWORD':
                        # Processa o tipo das variáveis
                        symbol_type = tokens[current][1]
                        symbol_line = tokens[current][2]
                        for symbol_name in symbol_names:
                            # Adiciona as variáveis à tabela de símbolos
                            current_symbol_table.add_symbol(symbol_name, symbol_type, 0, symbol_line)
                        symbol_names = []
                current += 1

        elif token_type == 'ID':
            symbol_name = token_value
            current += 1
            if current_symbol_table.scope_name == "global" and token_type == "ID" and tokens[current][1] == "(":
                # Verifica se é uma chamada de função no escopo global
                function_name = token_value
                current += 1
                while ')' not in [tokens[current][1]]:
                    param_value = tokens[current][1]
                    if not is_number(param_value):
                        param_value = current_symbol_table.get_symbol(param_value)['values'][-1][0]
                    # Atualiza os valores dos parâmetros da função
                    function_symbol_tables = [child for child in current_symbol_table.child_scopes if child.scope_name == function_name]
                    if len(function_symbol_tables) > 0:
                        function_symbol_table = function_symbol_tables[0]
                        for param_name in function_symbol_table.symbols.keys():
                            function_symbol_table.update_symbol(param_name, param_value, token_line)
                            break
                    else:
                        raise ValueError(f"A função '{function_name}' não foi encontrada.")
                    current += 1
                current += 1
                continue

            if current_symbol_table.scope_name == "global":
                if tokens[current][0] == 'OPERATOR' and tokens[current][1] == ':=':
                    # Verifica se é uma atribuição no escopo global
                    current += 1
                    handle_assignment_operation(current_symbol_table, tokens[current], symbol_name, tokens[current:])

        current += 1

    # Processa os escopos filhos da tabela de símbolos global
    current = 0
    for child_scope in global_symbol_table.child_scopes:
        child_symbol_table = global_symbol_table.enter_scope(child_scope.scope_name)
        process_scope(tokens, child_symbol_table)
    return global_symbol_table

def handle_assignment_operation(symbol_table, current_token, symbol_name, tokens):
    """Lida com a operação de atribuição."""
    symbol_value = None
    if current_token[0] in ['REAL_NUM', 'INTEGER_NUM']:
        symbol_value = float(current_token[1])
        symbol_table.update_symbol(symbol_name, symbol_value, current_token[2])

    elif current_token[0] == 'OPERATOR':
        operator1 = tokens[2][1]
        operator1 = int(operator1) if is_number(operator1) else \
        symbol_table.get_symbol(operator1)['values'][-1][0]
        operator2 = tokens[4][1]
        operator2 = int(operator2) if is_number(operator2) else \
        symbol_table.get_symbol(operator2)['values'][-1][0]

        if current_token[1] == '+':
            symbol_value = int(operator1) + int(operator2)
        elif current_token[1] == '-':
            symbol_value = int(operator1) - int(operator2)
        elif current_token[1] == '*':
            symbol_value = int(operator1) * int(operator2)
        elif current_token[1] == '/':
            symbol_value = int(operator1) / int(operator2)
        else:
            raise ValueError(f"Operador inválido: {current_token[0]}")

        symbol_table.update_symbol(symbol_name, symbol_value, current_token[2])
    return symbol_value


def process_scope(tokens, symbol_table: SymbolTable):
    """Processa um escopo que não seja o global (funções ou procedimentos)."""
    current = 0
    with open('output.txt', 'r') as f:
        resultado = f.read()
    while current < len(tokens):
        token_type, token_value, _ = tokens[current]

        if token_type == 'ID':
            symbol_name = token_value
            current += 1
            if token_value == "fact" and tokens[current][1] == "(": 
            
                for result in resultado.split():
                    print(result, ' result')
                    symbol_table.update_symbol("count", result, tokens[current][2])
                break
                    
            elif tokens[current][0] == 'OPERATOR' and tokens[current][1] == ':=':
                # Verifica se é uma atribuição
                current += 1
                handle_assignment_operation(symbol_table, tokens[current], symbol_name, tokens[current:])

        current += 1
def print_symbol_table(symbol_table: SymbolTable):
    """Imprime a tabela de símbolos."""
    symbol_table.print_symbols()