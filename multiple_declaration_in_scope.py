def multiple_declaration_of_variable_in_a_scope(symbol_table):
    variables = get_variables_in_symbol_table(symbol_table)
    check_for_duplicates(variables)


def get_variables_in_symbol_table(symbol_table):
    # create a list to store the variable names
    variables = []

    # add the symbols in the current scope to the list
    if hasattr(symbol_table, 'symbols'):
        for symbol in symbol_table.symbols:
            variables.append({symbol: symbol_table.scope_name})

    # if the current scope has child scopes, recursively call this function on each child
    if hasattr(symbol_table, 'child_scopes'):
        for child_scope in symbol_table.child_scopes:
            variables.extend(get_variables_in_symbol_table(child_scope))

    return variables


def check_for_duplicates(variables):
    # convert list of dictionaries to list of tuples for comparison
    variable_tuples = [tuple(d.items())[0] for d in variables]

    # create a set for unique tuples and a list for duplicates
    seen = set()
    duplicates = []

    # go through the list of tuples
    for var in variable_tuples:
        # if a tuple is already in the set, it's a duplicate
        if var in seen:
            duplicates.append(var)
        # if it's not in the set, add it to the set
        else:
            seen.add(var)

    # if there are duplicates, print them
    if duplicates:
        print("ERRO: CÓDIGO POSSUI VARIÁVEIS DUPLICADAS NO MESMO ESCOPO")
        for dup in duplicates:
            print("DUPLICADA:", dup)
        exit(1)