def checkFunctionAndValueType(tokens):
    symbolTable = {}
    checkEnum = {"integer": "integer", "real": "real"}
    hasErrors = False

    for i in range(len(tokens)):
        token = tokens[i]
        tokentype = token[0]
        content = token[1]
        line = token[2]

        if tokentype == "identifier" and i > 0 and tokens[i - 1][0] == "var":
            if i + 2 < len(tokens) and tokens[i + 2][0] == "integer":
                symbolTable[content] = "integer"
            elif i + 2 < len(tokens) and tokens[i + 2][0] == "real":
                symbolTable[content] = "real"
            else:
                symbolTable[content] = "variable"
        elif (tokentype == "integer" or tokentype == "real") and i >= 2 and tokens[i - 2][1] == "identifier" and tokens[i - 3][0] != "(":
            identifierContent = tokens[i - 2][0]
            idType = symbolTable[identifierContent]

            if idType == "integer" and tokentype == "real":
                print(f"Erro: Tipo de valor incorreto para '{identifierContent}' na linha {line}.")
                hasErrors = True
        elif tokentype == "operator" and (content == "+" or content == "-" or content == "*" or content == "/"):
            if i + 4 < len(tokens):
                firstParamContent = tokens[i + 2][0]
                firstParamIdType = symbolTable[firstParamContent]
                type1 = tokens[i + 2][1]

                secondParamContent = tokens[i + 4][0]
                secondParamIdType = symbolTable[secondParamContent]
                type2 = tokens[i + 4][1]

                if type1 == "identifier":
                    if type2 == "identifier":
                        if firstParamIdType != secondParamIdType:
                            print(f"Você está tentando operar com tipos inválidos na linha {line}...")
                            hasErrors = True
                    else:
                        currentType = checkEnum[firstParamIdType]
                        if currentType != type2:
                            print(f"Você está tentando operar com tipos inválidos na linha {line}...")
                            hasErrors = True
                else:
                    if type2 == "identifier":
                        currentType = checkEnum[secondParamIdType]
                        if type1 != currentType:
                            print(f"Você está tentando operar com tipos inválidos na linha {line}...")
                            hasErrors = True
                    else:
                        if type1 != type2:
                            print(f"Você está tentando operar com tipos inválidos na linha {line}...")
                            hasErrors = True

    return not hasErrors
