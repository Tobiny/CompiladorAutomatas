import re


def debugger(filename):
    source_dict = {}
    source = ''
    f = open(filename, "r")
    source = f.read()
    pila_corchetes = []

    def remove_comments(string):
        pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|#[^\r\n]*$)"
        # primer grupo del patrón captura strings en comillas (dobles o simples)
        # segundo grupo captura comentarios (#una sola linea o /* multilineas*/
        regex = re.compile(pattern, re.MULTILINE | re.DOTALL)  # compilamos la expresion

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
        corchetes_entrada = re.findall(r'{', line)
        if len(corchetes_entrada) > 0:
            pila_corchetes.append(corchetes_entrada)
        if len(pila_corchetes) > 0 and "}" in line:
            for _ in range(len(re.findall(r'}', line))):
                try:
                    pila_corchetes.pop()
                except:
                    print("Error, corchetes no balanceados.")
                    quit()
        # dict_source[count] = dict_source[count].replace('(', ' ( ')
        # dict_source[count] = dict_source[count].replace(')', ' ) ')
        # dict_source[count] = dict_source[count].replace('<', ' < ')
        # dict_source[count] = dict_source[count].replace('>', ' > ')
        # dict_source[count] = dict_source[count].replace('=', ' = ')
        # dict_source[count] = dict_source[count].replace('+', ' + ')
        # dict_source[count] = dict_source[count].replace('-', ' - ')
        # dict_source[count] = dict_source[count].replace('*', ' * ')
        # dict_source[count] = dict_source[count].replace(';', '; ')

        count += 1
        # Quitar espacios entre lineas como
        # 2   hola     ejemplo
        # dict_source[count] = dict_source[count].re

    if len(pila_corchetes) > 0:
        print("Error, corchetes no balanceados.")
        quit()
    dict_source = remove_lines(dict_source)
    string_out = ''
    count = 0 #Contador para añadir saltos de linea

    for k in dict_source:

        if count != 0:
            string_out +='\n'+ str(k) + ': ' + dict_source[k]
        else:
            count = 1
            string_out += str(k) + ': ' + dict_source[k]

    f = open(filename + 'd', 'w')
    f.write(string_out)
    f.close()
