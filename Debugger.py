import re


def debugger(filename, withdict):
    source_dict = {}
    source = ''
    f = open(filename, "r")
    source = f.read()

    def remove_comments(string):
        pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|#[^\r\n]*$)"
        # primer grupo del patrón captura strings en comillas (dobles o simples)
        # segundo grupo captura comentarios (#una sola linea o /* multilineas*/
        regex = re.compile(pattern, re.MULTILINE | re.DOTALL) # compilamos la expresion
                                                              # regular retornando
                                                              # un patron en forma de obj.

        def _replacer(match):
            # si el segundo grupo es no None
            # significa que hemos capturano una strings que no esta entre comillas
            if match.group(2) is not None:
                return ""  # por lo tanto retornaremos una cadena vacia para borrar comentarios
            else:  # sinó, retornaremos el primer grupo
                return match.group(1)  # cadena entre comillas capturada

        return regex.sub(_replacer, string)

    # removeremos las lineas vacias y espacios
    def remove_lines(dic):
        for k in range(len(dic)):
            if not dic[k + 1]:
                dic.pop(k + 1)
        return dic

    source = remove_comments(source)
    dict_source = {}
    count = 1

    for line in source.split("\n"):
        dict_source[count] = line.lstrip(' ')
        dict_source[count] = " ".join(dict_source[count].split())
        count += 1
        # Quitar espacios entre lineas como
        # 2   hola     ejemplo
        # dict_source[count] = dict_source[count].re

    dict_source = remove_lines(dict_source)
    string_out = ''
    for k in dict_source:
        string_out += str(k) + ': ' + dict_source[k] + '\n'
        print(k, ' ', dict_source[k])

    if withdict:
        string_out = ''
        for k in dict_source:
            string_out += dict_source[k] + '\n'
    f = open(filename + 'd', 'w')
    f.write(string_out)
    f.close()
