import subprocess
import os
import shutil
import re

def substituir_operadores(codigo):
    def substituicao(match):
        operador = match.group(1)
        valor1 = match.group(2)
        valor2 = match.group(3)
        if operador == '*':
            return f'{valor1} * {valor2}'
        elif operador == '+':
            return f'{valor1} + {valor2}'
        elif operador == '-':
            return f'{valor1} - {valor2}'
        elif operador == '>':
            return f'{valor1} > {valor2}'
        elif operador == '<':
            return f'{valor1} < {valor2}'
        else:
            return match.group(0)  # Retorna a correspondência original se o operador não for reconhecido

    new_content = re.sub(r'([*+\-><])\(([^,]+),([^)]+)\)', substituicao, codigo)
    return new_content

def detectar_recursao(codigo, nome_funcao):
    padrao = re.compile(r'\b' + nome_funcao + r'\(')
    if padrao.search(codigo):
        return True
    else:
        return False

def procurar_func(codigo):
    # Procurando pelo nome da função/procedimento
    match = re.search(r'\bprocedure\b (\w+)', codigo)
    if match:
        nome_funcao = match.group(1)
        if detectar_recursao(codigo, nome_funcao):
            print(f"A função '{nome_funcao}' é recursiva.")
        else:
            print(f"A função '{nome_funcao}' não é recursiva.")

def transpile(arquivo):
    with open(arquivo, 'r') as arquivo_txt:
        codigo = arquivo_txt.read()
        codigo = substituir_operadores(codigo)
        codigo = codigo.replace('read(', 'readln(')
        codigo = codigo.replace('write(', 'writeln(')
        codigo = codigo.replace('return', 'Exit')

        with open('a_temp.pas', 'w') as arquivo_pascal:
            arquivo_pascal.write(codigo)
        shutil.move('a_temp.pas', 'a.pas')

    executar_codigo_pascal()

def executar_codigo_pascal():
    result = subprocess.run(['fpc', 'a.pas'], capture_output=True, text=True)

    with open('output.txt', 'w') as f:
        subprocess.run(['./a'], stdout=f)

    filename = "output.txt"
    file = open(filename, 'r')

    for linha in file:
        print(linha)
    
    # linhas_saida = result.stdout.split('\n')
    # linhas_desejadas = [linha for linha in linhas_saida if linha.startswith(('2', 'doug'))]
    # for linha in linhas_desejadas:
    #     print(linha)