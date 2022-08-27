import re


class LexicalAnalyzer:
    # Fila del token
    lin_num = 1

    def tokenize(self, code):
        rules = [
            ('MAIN', r'main'),  # main
            ('INT', r'int'),  # int
            ('FLOAT', r'float'),  # float
            ('IF', r'if'),  # if
            ('ELSE', r'else'),  # else
            ('WHILE', r'while'),  # while
            ('READ', r'read'),  # read
            ('PRINT', r'print'),  # print
            ('PARENTESIS_IZ', r'\('),  # (
            ('PARENTESIS_DER', r'\)'),  # )
            ('LLAVE_IZ', r'\{'),  # {
            ('LLAVE_DER', r'\}'),  # }
            ('COMA', r','),  # ,
            ('PUN_COMA', r';'),  # ;
            ('IGUAL', r'=='),  # ==
            ('NO_IGUAL', r'!='),  # !=
            ('MENOR_IG', r'<='),  # <=
            ('MAYOR_ig', r'>='),  # >=
            ('O', r'\|\|'),  # ||
            ('Y', r'&&'),  # &&
            ('ASIG', r'\='),  # =
            ('MENOR', r'<'),  # <
            ('MAYOR', r'>'),  # >
            ('SUMA', r'\+'),  # +
            ('RESTA', r'-'),  # -
            ('MULTI', r'\*'),  # *
            ('DIV', r'\/'),  # /
            ('ID', r'[a-zA-Z]\w*'),  # VARIABLES IDENTIFICADORAS
            ('CONSTANTE_FLOAT', r'\d(\d)*\.\d(\d)*'),  # FLOAT
            ('CONSTANTE_INT', r'\d(\d)*'),  # INT
            ('NUEVA_LINEA', r'\n'),  # SALTO DE LINEA
            ('SALTO', r'[ \t]+'),  # ESPACIOS y TABULACIONES
            ('OTRO_CARACTER', r'.'),  # OTRO CARACTER
        ]

        tokens_join = '|'.join('(?P<%s>%s)' % x for x in rules)
        lin_start = 0

        # Listas de la salida del programa
        token = []
        lexeme = []
        row = []
        column = []

        # Tabla de tokens, documentos

        # Analiza el código para encontrar los lexemas y sus respectivos Tokens
        for m in re.finditer(tokens_join, code): # Analiza con libreria re
                                                 # Si se encuentra el
            token_type = m.lastgroup
            token_lexeme = m.group(token_type)

            if token_type == 'NUEVA_LINEA':
                lin_start = m.end()
                self.lin_num += 1
            elif token_type == 'SALTO':
                continue
            elif token_type == 'OTRO_CARACTER':
                raise RuntimeError('%r error inesperado en línea %d' % (token_lexeme, self.lin_num))
            else:

                col = m.start() - lin_start
                column.append(col)
                token.append(token_type)
                lexeme.append(token_lexeme)
                row.append(self.lin_num)

                f = open('ejemplo.afn', 'r')
                string = f.read()
                f.close()
                f = open('ejemplo.afn', 'w')
                f.writelines(string + '{1},\'{0}\',{2},{3}\n'.format(token_lexeme,
                                                                     token_type,
                                                                     self.lin_num, col), )
                print('Token = {0}, Lexema encontrado = \'{1}\', Fila = {2}, Columna = {3}'.format(token_type,
                                                                                                   token_lexeme,
                                                                                                   self.lin_num, col))
        f.close()
        return token, lexeme, row, column
