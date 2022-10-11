import re


variables = re.compile(r'^[a-zA-Z]+')
declaraciones = [re.compile(r'(^str)\s*([a-zA-Z]+[0-9]*)\s*(;$)'),  # Strings
                 re.compile(r'(^int)\s*([a-zA-Z]+[0-9]*)\s*(;$)'),  # Integers
                 re.compile(r'(^boolean)\s*([a-zA-Z]+[0-9]*)\s*(;$)')]  #Booleanos
declaraAsigna = [re.compile(r'(^str)\s*([a-zA-Z]+[0-9]*)\s*=\s*(\"[^\"]*\")\s*(;$)'),  # Strings
                 re.compile(r'(^int)\s*([a-zA-Z]+[0-9]*)\s*=\s*([0-9]+)\s*(;$)'),  # Integers
                 re.compile(r'(^boolean)\s*([a-zA-Z]+[0-9]*)\s*=\s*(True|False)\s*(;$)')]  #Booleanos
declaraAsignaVar = [re.compile(r'(^str)\s*([a-zA-Z]+[0-9]*)\s*=\s*([a-zA-Z]+[0-9]*)\s*(;$)'),
                    re.compile(r'(^int)\s*([a-zA-Z]+[0-9]*)\s*=\s*([a-zA-Z]+[0-9]*)\s*(;$)'),
                    re.compile(r'(^boolean)\s*([a-zA-Z]+[0-9]*)\s*=\s*([a-zA-Z]+[0-9]*)\s*(;$)')]

asignaciones = [re.compile(r'^([a-zA-Z]+[0-9]*)\s*=\s*(True|False)\s*(;$)'),  # Para boolean
                re.compile(r'^([a-zA-Z]+[0-9]*)\s*=\s*([a-zA-Z]+[0-9]*)\s*(;$)'),  # Para variables
                re.compile(r'^([a-zA-Z]+[0-9]*)\s*=\s*([0-9]+)\s*(;$)'),  # Para int
                re.compile(r'^([a-zA-Z]+[0-9]*)\s*=\s*(\"[^\"]*\")\s*(;$)'),  # Para str
                ]


tabsim = []

palabras = ['main', 'int', 'boolean', 'str', 'readin', 'print', 'for', 'if', 'while', 'else']
declar = ['int', 'str', 'boolean']


def ispalres(pal, declarar):
    if declarar:
        return pal in declar
    return pal in palabras


def lexan(linea):
    for a in range(0, len(declaraciones)):
        m = declaraciones[a].match(linea[0])
        if m:
            if m.group(2) in palabras:
                print('No puede declarar variables con palabras reservadas, error en la línea ', linea[1])
                return
            else:
                addTabSim(linea, m)
                return

    for a in range(0, len(asignaciones)):
        m = asignaciones[a].match(linea[0])
        if m:
            if (m.group(1) in palabras) or (m.group(2) in palabras):
                print('No puede asignar el valor a las palabras reservadas, error en la linea', linea[1])
                return
            else:
                asigTabSim(linea, m, a)
                return

    for a in range(0, len(declaraAsigna)):
        m = declaraAsigna[a].match(linea[0])
        if m:
            if (m.group(2) in palabras) or (m.group(3) in palabras):
                print('No puede declarar variables con palabras reservadas, error en la línea', linea[1])
                return
            else:
                asDeTabSim(linea, m)
                return
    for a in range(0, len(declaraAsignaVar)):
        m = declaraAsignaVar[a].match(linea[0])
        if m:
            if (m.group(2) in palabras) or (m.group(3) in palabras):
                print('No puede declarar variables con palabras reservadas, error en la línea', linea[1])
                return
            else:
                asDeVarTabSim(linea, m)
                return

    for _ in range(0,1):
        m = re.match(r'^(int)\s+([a-zA-Z]+[0-9]*)\s*=.*([+|\-|*|\/|\(|\)])+.*(;$)', linea[0])
        if m is not None:
            if (m.group(2) in palabras) or (
            re.match(r'=.*(int|main|boolean|str|readin|print|for|if|while|else).*', linea[0])):
                print('No puede declarar variables con palabras reservadas, error en la línea ', linea[1])
                return
            declarada = False
            for simb in tabsim:
                if m.group(2) == simb[0]:
                    declarada = True
                    break
            if declarada:
                print('Error, variable ya declarada, en la línea', linea[1])
                return False
            if (syntactic_analyzer(linea, tabsim)):
                tabsim.append([m.group(2), 'int', 'todavianocalculo :C', 'id' + str(len(tabsim))])
                return

    for _ in range(0, 1):
        m = re.match(r'^([a-zA-Z]+[0-9]*)\s*=.*([+|\-|*|\/|\(|\)])+.*(;$)', linea[0])
        if m is not None:
            if(m.group(1) in palabras) or (
            re.match(r'=.*(int|main|boolean|str|readin|print|for|if|while|else).*', linea[0])):
                print('No puede declarar variables con palabras reservadas, error en la línea ', linea[1])
                return
            declarada = False
            for simb in tabsim:
                if m.group(1) == simb[0]:
                    declarada = True
                    break
            if not declarada:
                print('Error, variable no declarada, en la línea', linea[1])
                return False
            if (syntactic_analyzer(linea, tabsim)):
                for variable in tabsim:
                    if m.group(1) == variable[0]:
                        variable[2] = 'todavianocalculo :C'
                return
            else:
                return

    for _ in range(0, 1):
        m = re.match(r'^if\(.*\);$', linea[0])
        if m is not None:
            logic_analyzer(linea, tabsim)
            return
    print("Error, revise la línea", linea[1], "ya que existe un error de sintaxis en la declaración o asignación")



def addTabSim(linea, m):
    declarada = False
    for simb in tabsim:
        if m.group(2) == simb[0]:
            declarada = True
            break
    if declarada:
        print('Error, variable ya declarada, en la línea', linea[1])
        return False
    else:
        add = [m.group(2), m.group(1)]
        if m.group(1) == 'int':
            add.append(0)
        elif m.group(1) == 'str':
            add.append("")
        elif m.group(1) == 'boolean':
            add.append(False)
        add.append('id' + str(len(tabsim)))
        tabsim.append(add)
        return True


def asigTabSim(linea, m, it):
    declarada = False
    for simb in tabsim:
        if m.group(1) == simb[0]:
            declarada = True
            if it == 0:
                if simb[1] == 'boolean':
                    if m.group(2) == 'False':
                        simb[2] = False
                    else:
                        simb[2] = True
                else:
                    print("Error, está intentando introducir una bandera a una variable de otro tipo en la línea",
                          linea[1])
                    return False
            elif it == 1:
                for simb1 in tabsim:
                    if m.group(2) == simb1[0]:
                        simb[2] = simb1[1]
                    else:
                        print("Error, variable no declarada en la linea",
                              linea[1])
                        return
            elif it == 2:
                if simb[1] == 'int':
                    simb[2] = int(m.group(2))
                else:
                    print("Error, está intentando introducir un entero a una variable de otro tipo en la línea",
                          linea[1])
                    return False
            elif it == 3:
                if simb[1] == 'str':
                    simb[2] = m.group(2)
                else:
                    print("Error, está intentando introducir una cadena a una variable de otro tipo en la línea",
                          linea[1])
                    return False


def asDeTabSim(linea, m):
    declarada = False
    for simb in tabsim:
        if m.group(2) == simb[0]:
            declarada = True
            break
    if declarada:
        print('Error, variable ya declarada, en la línea', linea[1])
        return False
    else:
        add = []
        add.append(m.group(2))
        add.append(m.group(1))
        if m.group(1) == 'int':
            add.append(int(m.group(3)))
        elif m.group(1) == 'str':
            add.append(m.group(3))
        elif m.group(1) == 'boolean':
            if m.group(3) == "False":
                add.append(False)
            else:
                add.append(True)

        add.append('id' + str(len(tabsim)))
        tabsim.append(add)
        return True


def asDeVarTabSim(linea, m):
    declarada, encontrada = False, False
    tipo = ""
    for simb in tabsim:
        if m.group(2) == simb[0]:
            declarada = True
        if m.group(3) == simb[0]:
            encontrada = True
            tipo = simb[1]
    if declarada:
        print('Error, variable ya declarada, en la línea', linea[1])
        return
    if not encontrada:
        print('Error, variable a asignar no ha sido declarada, en la línea', linea[1])
        return
    else:
        if m.group(1) != tipo:
            print("Error, tipo de dato de la variable a asignar es distinto a la que se va a declarar en la línea",
                  linea[1])
            return
        add = [m.group(2), m.group(1)]
        for simb in tabsim:
            if m.group(3) == simb[0]:
                add.append(simb[2])
                break
        add.append('id' + str(len(tabsim)))
        tabsim.append(add)
        return True


def syntactic_analyzer(linea, tabsim):
    # Recibe array ['linea tipo string', numero de linea int]
    numero_linea = linea[1]
    # elimina lo que viene antes del igual, el punto y coma, y los espacios
    expresion = re.sub(r'.*= *', '', linea[0]).replace(" ", "")
    expresion = re.sub(r';$','',expresion)
    # variables en linea almacena todas las variables presentes en la linea
    variables_en_linea = re.findall(r'[a-zA-Z]+\d*', expresion)
    if buscar_tokens(variables_en_linea, tabsim, numero_linea, expresion):
        # variables del algoritmo LR
        pila = [0]
        contador = 0
        # Almacena la expresion con 0s en lugar de ids, para que el analizador los tome como tal '0+0*0'
        expresion_procesada = reemplazar_variables(expresion)
        longitudExpresion = len(expresion_procesada) - 1
        # se llena tabla de acciones, ir a y todas las relacionadas
        ACCION = [
            [("D", 5), "E", "E", "E", "E", ("D", 4), "E", "E"],  # 0
            ["E", ("D", 6), ("D", 7), "E", "E", "E", "E", "A"],  # 1
            ["E", ("R", 3), ("R", 3), ("D", 8), ("D", 9), "E", ("R", 3), ("R", 3)],  # 2
            ["E", ("R", 6), ("R", 6), ("R", 6), ("R", 6), "E", ("R", 6), ("R", 6)],  # 3
            [("D", 5), "E", "E", "E", "E", ("D", 4), "E", "E"],  # 4
            ["E", ("R", 8), ("R", 8), ("R", 8), ("R", 8), "E", ("R", 8), ("R", 8)],  # 5
            [("D", 5), "E", "E", "E", "E", ("D", 4), "E", "E"],  # 6
            [("D", 5), "E", "E", "E", "E", ("D", 4), "E", "E"],  # 7
            [("D", 5), "E", "E", "E", "E", ("D", 4), "E", "E"],  # 8
            [("D", 5), "E", "E", "E", "E", ("D", 4), "E", "E"],  # 9
            ["E", ("D", 6), ("D", 7), "E", "E", "E", ("D", 15), "E"],  # 10
            ["E", ("R", 1), ("R", 1), ("D", 8), ("D", 9), "E", ("R", 1), ("R", 1)],  # 11
            ["E", ("R", 2), ("R", 2), ("D", 8), ("D", 9), "E", ("R", 2), ("R", 2)],  # 12
            ["E", ("R", 4), ("R", 4), ("R", 4), ("R", 4), "E", ("R", 4), ("R", 4)],  # 13
            ["E", ("R", 5), ("R", 5), ("R", 5), ("R", 5), "E", ("R", 5), ("R", 5)],  # 14
            ["E", ("R", 7), ("R", 7), ("R", 7), ("R", 7), "E", ("R", 7), ("R", 7)]]  # 15
        IR_A = [
            [1, 2, 3],  # 1
            "E",  # 2
            "E",  # 3
            "E",  # 4
            [10, 2, 3],  # 5
            "E",  # 6
            ["E", 11, 3],  # 7
            ["E", 12, 3],  # 8
            ["E", "E", 13],  # 9
            ["E", "E", 14],  # 10
            "E",  # 11
            "E",  # 12
            "E",  # 13
            "E",  # 14
            "E"]  # 15
        sacarsimbolos = {1: 3, 2: 3, 3: 1, 4: 3, 5: 3, 6: 1, 7: 3, 8: 1}
        producciones_primer_simbolo = {1: 0, 2: 0, 3: 0, 4: 1, 5: 1, 6: 1, 7: 2, 8: 2}
        simbolos = {"+": 1, "-": 2, "*": 3, "/": 4, "(": 5, ")": 6, "$": 7}
        #Algoritmo
        while True:
            # Si el contador es más grande que la expresión le marcamos el final de cadena de lo contrario a es igual
            # al símbolo que estamos analizando
            if contador > longitudExpresion:
                a = "$"
            else:
                a = expresion_procesada[contador]
            # Estado
            x = pila[len(pila) - 1]
            # Accion
            y = 0
            # Si a esta dentro de los simbolos y toma su valor en la tabla
            if a in simbolos:
                y = simbolos[a]
            # Si es estado de aceptación
            if ACCION[x][y] == "A":
                print("Analisis sintáctico linea " + str(numero_linea) + ": Correcto")
                return True
            # Si es estado de error
            elif ACCION[x][y] == "E":
                print("Analisis sintáctico linea " + str(numero_linea) + ": Incorrecto")
                return False
            else:
                # Si hay que ejecutar el algoritmo
                siguenteAccion = ACCION[x][y][0]
                numeroAccion = ACCION[x][y][1]
                # Si hay que desplazar
                if siguenteAccion == "D":
                    pila.append(numeroAccion)
                    contador += 1
                # Si hay que reducir
                elif siguenteAccion == "R":
                    for x in range(sacarsimbolos[numeroAccion]):
                        pila.pop()
                    t = pila[len(pila) - 1]
                    pila.append(IR_A[t][producciones_primer_simbolo[numeroAccion]])


def logic_analyzer(linea, tabsim):
    numero_linea = linea[1]
    expresion = re.sub(r'^if\(', '', linea[0])
    expresion = re.sub(r'\);$', '', expresion)
    expresion = reemplazar_operadores_logicos(expresion)
    variables_en_linea = re.findall(r'[a-zA-Z]+\d*', expresion)
    expresion = expresion.replace(" ", "")
    expresion_procesada = reemplazar_variables(expresion)
    if buscar_tokens(variables_en_linea, tabsim, numero_linea, expresion):
        pila = [0]
        contador = 0
        longitudExpresion = len(expresion_procesada) - 1
        ACCION = [
            [("D", 7), "E", "E", "E", "E", "E", "E", ("D", 5), ("D", 6), "E", "E"],  # 0
            ["E", ("D", 8), ("D", 9), "E", "E", "E", "E", "E", "E", "E", "A"],  # 1
            ["E", ("R", 3), ("R", 3), ("D", 10), ("D", 11), "E", "E", "E", "E", ("R", 3), ("R", 3)],  # 2
            ["E", ("R", 6), ("R", 6), ("R", 6), ("R", 6), ("D", 12), ("D", 13), "E", "E", ("R", 6), ("R", 6)],  # 3
            ["E", ("R", 9), ("R", 9), ("R", 9), ("R", 9), ("R", 9), ("R", 9), "E", "E", ("R", 9), ("R", 9)],  # 4
            [("D", 7), "E", "E", "E", "E", "E", "E", ("D", 5), ("D", 6), "E", "E"],  # 5
            [("D", 7), "E", "E", "E", "E", "E", "E", ("D", 5), ("D", 6), "E", "E"],  # 6
            ["E", ("R", 12), ("R", 12), ("R", 12), ("R", 12), ("R", 12), ("R", 12), "E", "E", ("R", 12), ("R", 12)],  # 7
            [("D", 7), "E", "E", "E", "E", "E", "E", ("D", 5), ("D", 6), "E", "E"],  # 8
            [("D", 7), "E", "E", "E", "E", "E", "E", ("D", 5), ("D", 6), "E", "E"],  # 9
            [("D", 7), "E", "E", "E", "E", "E", "E", ("D", 5), ("D", 6), "E", "E"],  # 10
            [("D", 7), "E", "E", "E", "E", "E", "E", ("D", 5), ("D", 7), "E", "E"],  # 11
            [("D", 7), "E", "E", "E", "E", "E", "E", ("D", 5), ("D", 7), "E", "E"],  # 12
            [("D", 7), "E", "E", "E", "E", "E", "E", ("D", 5), ("D", 7), "E", "E"],  # 13
            ["E", ("R", 10), ("R", 10), ("R", 10), ("R", 10), ("R", 10), ("R", 10), "E", "E", ("R", 10), ("R", 10)],  # 14
            ["E", ("D", 8), ("D", 9), "E", "E", "E", "E", "E", "E", ("D", 22), "E"],  # 15
            ["E", ("R", 1), ("R", 1), ("D", 10), ("D", 11), "E", "E", "E", "E", ("R", 1), ("R", 1)],  # 16
            ["E", ("R", 2), ("R", 2), ("D", 10), ("D", 11), "E", "E", "E", "E", ("R", 2), ("R", 2)],  # 17
            ["E", ("R", 4), ("R", 4), ("R", 4), ("R", 4), ("D", 12), ("D", 13), "E", "E", ("R", 4), ("R", 4)],  # 18
            ["E", ("R", 5), ("R", 5), ("R", 5), ("R", 5), ("D", 12), ("D", 13), "E", "E", ("R", 5), ("R", 5)],  # 19
            ["E", ("R", 7), ("R", 7), ("R", 7), ("R", 7), ("R", 7), ("R", 7), "E", "E", ("R", 7), ("R", 7)],  # 20
            ["E", ("R", 8), ("R", 8), ("R", 8), ("R", 8), ("R", 8), ("R", 8), "E", "E", ("R", 8), ("R", 8)],  # 21
            ["E", ("R", 11), ("R", 11), ("R", 11), ("R", 11), ("R", 11), ("R", 11), "E", "E", ("R", 11), ("R", 11)]]  # 22
        IR_A = [
            [1, 2, 3, 4],  # 0
            ["E", "E", "E", "E"],  # 1
            ["E", "E", "E", "E"],  # 2
            ["E", "E", "E", "E"],  # 3
            ["E", "E", "E", "E"],  # 4
            ["E", "E", "E", 14],  # 5
            [15, 2, 3, 4],  # 6
            ["E", "E", "E", "E"],  # 7
            ["E", 16, 3, 4],  # 8
            ["E", 17, 3, 4],  # 9
            ["E", "E", 18, 4],  # 10
            ["E", "E", 19, 4],  # 11
            ["E", "E", "E", 20],  # 12
            ["E", "E", "E", 21],  # 13
            ["E", "E", "E", "E"],  # 14
            ["E", "E", "E", "E"],  # 15
            ["E", "E", "E", "E"],  # 16
            ["E", "E", "E", "E"],  # 17
            ["E", "E", "E", "E"],  # 18
            ["E", "E", "E", "E"],  # 19
            ["E", "E", "E", "E"],  # 20
            ["E", "E", "E", "E"],  # 21
            ["E", "E", "E", "E"]]    # 22

        sacarsimbolos = {1: 3, 2: 3, 3: 1, 4: 3, 5: 3, 6: 1, 7: 3, 8: 3, 9: 1, 10: 2, 11: 3, 12: 1}
        producciones_primer_simbolo = {1: 0, 2: 0, 3: 0, 4: 1, 5: 1, 6: 1, 7: 2, 8: 2, 9: 2, 10: 3, 11: 3, 12: 3}
        simbolos = {"?": 1, "¿": 2, "¡": 3, ".": 4, ">": 5, "<": 6, "!": 7, "(": 8, ")": 9, "$": 10}
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
                print("Analisis lógico linea " + str(numero_linea) + ": Correcto")
                break
            elif ACCION[x][y] == "E":
                print("Analisis lógico linea " + str(numero_linea) + ": Incorrecto")
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
                    pila.append(IR_A[t][producciones_primer_simbolo[numeroAccion]])


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
    varinex = re.findall(r'[a-zA-Z]+[0-9]*', expresion)
    varinex.sort(key=len)
    varinex.reverse()
    for variable in varinex:
        expresion = expresion.replace(variable, '0')
    for variable in re.findall(r'[0-9]+', expresion):
        expresion = expresion.replace(variable, '0')
    return expresion


def reemplazar_operadores_logicos(expresion):
    for variable in re.findall(r'\/&', expresion):
        expresion = expresion.replace(variable, '?')
    for variable in re.findall(r'&&', expresion):
        expresion = expresion.replace(variable, '¿')
    for variable in re.findall(r'==', expresion):
        expresion = expresion.replace(variable, '¡')
    for variable in re.findall(r'!=', expresion):
        expresion = expresion.replace(variable, '.')
    return expresion