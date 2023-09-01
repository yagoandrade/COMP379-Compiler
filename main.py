from abstract_syntax_tree import print_abstract_syntax_tree
from check_scope_var import check_var_scope
from lexical_functions import lexer
from multiple_declaration_in_scope import multiple_declaration_of_variable_in_a_scope
from syntactic import Parser
from transpiler import transpile
from symbol_table import SymbolTable, print_symbol_table, create_symbol_table
from misuse_type import checkFunctionAndValueType as checkMisuse
from check_scope_var import check_var_scope

def lexical_analysis(file):
    pass


def syntactic_analysis():
    print("Análise Sintatica")
    print_abstract_syntax_tree()

if __name__ == '__main__':
    #Arquivos
    filename = "example2.txt"
    file = open(filename, 'r')

    #Léxico
    tokens = lexer(file.read())

    # for token in tokens:
    #     print(token)

    #Sintático
    # Parser(tokens).programa()
    symbol_table = create_symbol_table(tokens)
    print("-"*50)
    print_symbol_table(symbol_table)
    print("\nSaída do código")
    print("-"*50)

    #Semantico
    
    transpile(filename)
    
