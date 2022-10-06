import re


def syntactic_analyzer(linea, tabsim):
    numero_linea = linea[1]
    expresion = re.sub(r'.*= *', '', linea[0]).replace(" ", "")
    variables_en_linea = re.findall(r'[a-zA-Z]+\d*', expresion)

    if buscar_tokens(variables_en_linea, tabsim, numero_linea, expresion):
        pila_resultado = []
        pila = [0]
        contador = 0
        expresion_procesada = reemplazar_variables(expresion)
        longitudExpresion = len(expresion_procesada) - 1
        # print(linea[0] + " : " + expresion + " : " + expresion_procesada)
        ACCION = [
            [("D", 5), "E", "E", ("D", 4), "E", "E"],
            ["E", ("D", 6), "E", "E", "E", "A"],
            ["E", ("R", 2), ("D", 7), "E", ("R", 2), ("R", 2)],
            ["E", ("R", 4), ("R", 4), "E", ("R", 4), ("R", 4)],
            [("D", 5), "E", "E", ("D", 4), "E", "E"],
            ["E", ("R", 6), ("R", 6), "E", ("R", 6), ("R", 6)],
            [("D", 5), "E", "E", ("D", 4), "E", "E"],
            [("D", 5), "E", "E", ("D", 4), "E", "E"],
            ["E", ("D", 6), "E", "E", ("D", 11), "E"],
            ["E", ("R", 1), ("D", 7), "E", ("R", 1), ("R", 1)],
            ["E", ("R", 3), ("R", 3), "E", ("R", 3), ("R", 3)],
            ["E", ("R", 5), ("R", 5), "E", ("R", 5), ("R", 5)]]
        IR_A = [
            [1, 2, 3],
            "E",
            "E",
            "E",
            [8, 2, 3],
            "E",
            ["E", 9, 3],
            ["E", "E", 10],
            "E",
            "E",
            "E",
            "E"]
        # Número de Producción: regresa simbolos a retirar de la pila
        sacarsimbolos = {1: 3, 2: 1, 3: 3, 4: 1, 5: 3, 6: 1}
        producciones_ps = {1: 0, 2: 0, 3: 1, 4: 1, 5: 2, 6: 2}
        simbolos = {"+": 1, "*": 2, "(": 3, ")": 4, "$": 5}
        while True:
            if contador > longitudExpresion:
                a = "$"
            else:
                a = expresion_procesada[contador]
            # Estado
            x = pila[len(pila) - 1]
            # Accion
            y = 0
            if a in simbolos:
                y = simbolos[a]
            if ACCION[x][y] == "A":
                print("Analisis sintáctico linea " + str(numero_linea) + ": Correcto")
                break
            elif ACCION[x][y] == "E":
                print("Analisis sintáctico linea " + str(numero_linea) + ": Incorrecto")
                break
            else:
                siguenteAccion = ACCION[x][y][0]
                numeroAccion = ACCION[x][y][1]
                if siguenteAccion == "D":
                    pila.append(numeroAccion)
                    contador += 1
                elif siguenteAccion == "R":
                    for x in range(sacarsimbolos[numeroAccion]):
                        pila.pop()
                    t = pila[len(pila) - 1]
                    pila.append(IR_A[t][producciones_ps[numeroAccion]])


def buscar_tokens(variables_en_linea, tabsim, numero_linea, expresion):
    variable_no_declarada = False
    contador_no_declaradas = 0
    for nombre_variable in variables_en_linea:
        for _ in range(0, len(tabsim)):
            if nombre_variable in tabsim[_][0]:
                variable_no_declarada = False
                break
            else:
                variable_no_declarada = True
        if variable_no_declarada:
            contador_no_declaradas += 1
    if contador_no_declaradas <= 0:
        if len(re.sub('[^(]', '', expresion)) != len(re.sub('[^)]', '', expresion)):
            print("Error en linea " + str(numero_linea) + ": paréntesis no balanceados")
            return False
        else:
            return True
    else:
        print("Error en linea " + str(numero_linea) + ": existen " + str(contador_no_declaradas)
              + " variables sin declarar")
        return False


def reemplazar_variables(expresion):
    for variable in re.findall(r'[a-zA-Z]+[0-9]*', expresion):
        expresion = expresion.replace(variable, '0')
    for variable in re.findall(r'[0-9]+', expresion):
        expresion = expresion.replace(variable, '0')
    return expresion

if __name__ == '__main__':
    tabsim = [['a', 'int', 0, 'id0'], ['z', 'int', 0, 'id1'],
              ['id', 'int', 0, 'id2'], ['q', 'int', 0, 'id3'],
              ['id77', 'str', 0, 'id4']]
    linea = [['int x = 7 + 1', 1]]

    for _ in range(0, len(linea)-1):
        syntactic_analyzer(linea[_], tabsim)
