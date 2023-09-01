def check_var_scope(tokens):
    #Removendo nome do programa
    if len(tokens) >= 3 and tokens[0][0] == 'KEYWORD' and tokens[0][1] == 'program' and \
            tokens[1][0] == 'ID' and tokens[2][0] == 'DELIMITER' and tokens[2][1] == ';':
        tokens = tokens[3:]

    global_var = []
    scope_func = []
    i=0
    # Percorrer o código
    while i < len(tokens):
        if i == len(tokens)-1:
            #print("END")
            return
        scope_var = []
        
        #print(i)
        if tokens[i][0] == 'KEYWORD' and (tokens[i][1] == 'function' or tokens[i][1] == 'procedure'):
            if tokens[i+1][0] == 'ID' and tokens[i+2][1] == '(':
                scope_func.append(tokens[i+1][1])
                i = i + 2
                while tokens[i][1] != 'begin':
                    if tokens[i+1][0] == 'ID' and tokens[i+2][1] == ':' and tokens[i+3][0] == 'KEYWORD' and tokens[i+4][1] == ',':
                        scope_var.append(tokens[i+1][1])
                        i = i+4
                    elif tokens[i+1][0] == 'ID' and tokens[i+2][1] == ':' and tokens[i+3][0] == 'KEYWORD':
                        scope_var.append(tokens[i+1][1])
                        i = i+3
                    else:
                        i = i+1
                i = check_in_scope(tokens, i+1, global_var, scope_var, scope_func)
            else:
                print("ERRO: FUNÇÃO INVÁLIDA NA LINHA:", tokens[i][2])
                exit(1)
        elif tokens[i][0] == 'KEYWORD' and tokens[i][1] == 'begin':
            i = check_in_scope(tokens, i+1, global_var, scope_var, scope_func)
        elif tokens[i][0] == 'KEYWORD' and tokens[i][1] == 'var':
            i, global_var = check_in_global(tokens, i, global_var)
        i = i+1
        #print(global_var)
    return True

def check_in_scope(tokens, j, global_var, scope_var, scope_func):
    #print(scope_func, scope_var)
    # Percorrer até o fim do escopo
    while j < len(tokens):
        # Se encontrar um fim de escopo, para
        if tokens[j][0] == 'KEYWORD' and (tokens[j][1] == 'end' or tokens[j][1] == 'end.'):
            #print("END")
            return j+1
        # Se encontrar uma declaração de variável, adiciona na lista de variáveis do escopo 
        if tokens[j][0] == 'KEYWORD' and tokens[j][1] == 'var':
            k = j+1
            if tokens[k][0] != 'ID':
                print("ERRO: FALTOU ID DA VARIAVEL LINHA:", tokens[k][2])
                exit(1)

            while tokens[k][1] != ';':
                if tokens[k][0] == 'ID':
                    scope_var.append(tokens[k][1])
                    if tokens[k+1][1] == ':':
                        if tokens[k+2][0] == 'KEYWORD' and tokens[k+3][1] == ';':
                            #print("VARIAVEL OK")
                            j = k+3
                            break
                        else:
                            print("ERRO: DECLARAÇÃO DE VARIÁVEL MAL FORMATADA, LINHA:", tokens[k][2])
                            exit(1)
                    elif tokens[k+1][1] == ',':
                        k = k+2
                        continue
                    else:
                        print("ERRO: DECLARAÇÃO DE VARIÁVEL MAL FORMATADA, LINHA:", tokens[k][2])
                        exit(1)
                else:
                    print("ERRO: DECLARAÇÃO DE VARIÁVEL INVÁLIDA LINHA:", tokens[k][2])
                    exit(1)
        # Verifica se a variável foi declarada e não é uma função ou procedimento
        elif tokens[j][0] == 'ID':
            if tokens[j][1] not in global_var and tokens[j][1] not in scope_var and tokens[j][1] not in scope_func:
                print("ERRO: PROBLEMA DE DECLARAÇÃO NA LINHA:", tokens[j][2])
                exit(1)
        j = j+1

def check_in_global(tokens, j, global_var):
    k = j+1
    if tokens[k][0] != 'ID':
        print("ERRO: FALTOU ID DA VARIAVEL LINHA:", tokens[k][2])
        exit(1)

    while tokens[k][1] != ';':
        if tokens[k][0] == 'ID':
            global_var.append(tokens[k][1])
            if tokens[k+1][1] == ':':
                if tokens[k+2][0] == 'KEYWORD' and tokens[k+3][1] == ';':
                    #print("VARIAVEL OK")
                    j = k+3
                    break
                else:
                    print("ERRO: DECLARAÇÃO DE VARIÁVEL MAL FORMATADA, LINHA:", tokens[k][2])
                    exit(1)
            elif tokens[k+1][1] == ',':
                k = k+2
                continue
            else:
                print("ERRO: DECLARAÇÃO DE VARIÁVEL MAL FORMATADA, LINHA:", tokens[k][2])
                exit(1)
        else:
            print("ERRO: DECLARAÇÃO DE VARIÁVEL INVÁLIDA LINHA:", tokens[k][2])
            exit(1)
    return k, global_var