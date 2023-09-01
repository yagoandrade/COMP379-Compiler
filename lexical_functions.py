import re

keywords = [
    "program", "begin", "end", "var", "integer", "real", "pilha", "of", "procedure",
    "function", "read", "write", "for", "to", "do", "repeat", "until", "while", "if",
    "then", "else", "concatena", "pilha_of_integer", "pilha_of_real", "length", "inverte",
    "input", "output", "return"
]

operators = [
    ":=", ">=", "<=", "<>", "//", ">", "<", "+", "-", "*", "/"
]

delimiters = [
    "(", ")", "[", "]", "{", "}", ";", ",", "#", ":", "."
]

patterns = [
    ('WHITESPACE', r'\s+', 'whitespace'),
    ('REAL_NUM', r'[+-]?\d+\.\d+', 'real'),
    ('INTEGER_NUM', r'[+-]?\d+', 'integer')
]

# Add keywords to patterns
for keyword in keywords:
    # patterns.append((keyword.upper(), r'\b' + re.escape(keyword) + r'\b', 'keyword'))
    patterns.append(('KEYWORD', r'\b' + re.escape(keyword) + r'\b', 'keyword'))

# Add operators to patterns
for operator in operators:
    patterns.append(('OPERATOR', re.escape(operator), 'operator'))

# Add delimiters to patterns
for delimiter in delimiters:
    patterns.append(('DELIMITER', re.escape(delimiter), 'delimiter'))


# Função para realizar a análise léxica
def lexer(program):
    tokens = []
    position = 0
    line_number = 1

    while position < len(program):
        match = None
        for token_type, pattern, _ in patterns:
            regex = re.compile(pattern)
            match = regex.match(program, position)
            if match:
                value = match.group(0)
                if token_type != 'WHITESPACE':
                    tokens.append((token_type, value, line_number))
                break

        if not match:
            regex = re.compile(r'([a-zA-Z_][a-zA-Z_0-9]*)')
            match = regex.match(program, position)
            if match:
                value = match.group(0)
                tokens.append(('ID', value, line_number))
            else:
                if position != len(program):
                    invalid_token = program[position]
                    raise SyntaxError(f'Invalid token: {invalid_token} at position {position}, line {line_number}')
                else:
                    break

        position = match.end()

        if '\n' in program[position:position + 1]:
            line_number += 1

    return tokens
