bnf = [
    "<programa> ::= program <id>; <corpo>",
    "<corpo> ::= <declara> <rotina> begin <sentencas> end",
    "<declara> ::= var <dvar> <mais_dc> | <empty>",
    "<mais_dc> ::= ; <cont_dc>",
    "<cont_dc> ::= <dvar> <mais_dc> | <empty>",
    "<dvar> ::= <variaveis> : <tipo_var>",
    "<tipo_var> ::= integer |real | pilha of integer | pilha of real",
    "<variaveis> ::= <id> <mais_var>",
    "<mais_var> ::= , <variaveis> | <empty>",
    "<rotina> ::= <procedimento> | <funcao> | <empty>",
    "<procedimento> ::= procedure <id> <parametros> ; <corpo> ; <rotina>",
    "<funcao> ::= function <id> <parametros> : <tipo_funcao> ; <corpo> ; <rotina>",
    "<parametros> ::= ( <lista_parametros> ) | <empty>",
    "<lista_parametros> ::= <lista_id> : <tipo_var> <cont_lista_par>",
    "<cont_lista_par> ::= ; <lista_parametros> | <empty>",
    "<lista_id> ::= <id> <cont_lista_id>",
    "<cont_lista_id> ::= , <lista_id> | <empty>",
    "<tipo_funcao> ::= integer |real | pilha of integer | pilha of real",
    "<sentencas> ::= <comando> <mais_sentencas>",
    "<mais_sentencas> ::= ; <cont_sentencas>",
    "<cont_sentencas> ::= <sentencas> | <empty>",
    "<var_read> ::= <id> <mais_var_read>",
    "<mais_var_read> ::= , <var_read> | <empty>",
    "<var_write> ::= <id> <mais_var_write>",
    "<mais_var_write> ::= , <var_write> | <empty>",
    "<comando> ::= read ( <var_read> ) | write ( <var_write> ) | for <id> := <expressao> to <expressao> do begin",
    "<sentencas> end | repeat <sentencas> until ( <condicao> ) | while ( <condicao> ) do begin <sentencas> end | if",
    "( <condicao> ) then begin <sentencas> end <pfalsa> | <id> := <expressao> | <chamada_procedimento>",
    "<chamada_procedimento> ::= <id> <argumentos>",
    "<argumentos> ::= ( <lista_arg> ) | <empty>",
    "<lista_arg> ::= <expressao> <cont_lista_arg>",
    "<cont_lista_arg> ::= , <lista_arg> | <empty>",
    "<condicao> ::= <relacao>(<expressao_num> ,<expressao_num>) |",
    "<relacao>(<expressao_pilha> ,<expressao_pilha>)",
    "<pfalsa> ::= else begin <sentencas> end | <empty>",
    "<relacao> ::= = | > | < | >= | <= | <>",
    "<expressao> ::= <expressao_num> | <expressao_pilha>",
    "<expressao_num> ::=<termo> | <id><argumentos>",
    "<operando> ::= <id> | <integer_num> | <real_num> | <operador> ( <operando> , <operando> )",
    "<operador> ::= + | - | * | / | //",
    "<termo> ::= <operador> ( <operando> , <operando> ) | <id> | <integer_num> | <real_num>",
    "<expressao_pilha> ::= <opPilha>(<conteudo>) | concatena(<conteudo> , <coneudo>) | inverte(<conteudo>)",
    "<conteudo> ::= ## | #<integer_num><integer_num_cont># | #<real_num><real_num_cont>#",
    "<integer_num_cont> ::= ,<integer_num><integer_num_cont>|<empty>",
    "<real_num_cont> ::= ,<real_num><real_num_cont>|<empty>",
    "<opPilha> ::= input | output | length",
    "<id> ::= <letra> <id_cont>",
    "<id_cont> ::= <letra><id_cont> | <digito><id_cont> | <empty>",
    "<num> ::= <digit><num_cont>",
    "<num_cont> ::= <digito><num_cont> |<empty>",
    "<integer_num> ::= +<num> | -<num> | <num> | 0",
    "<real_num> ::= +<num>,<num> | - <num>,<num> | +0,<num> | -0,<num> | <num>,<num> | 0,<num>",
    "<letra> ::= a | b |...| z",
    "<digito> ::= 0|1|...|9",
    "<digit> ::= 1|...|9"
]
