import re


variables = re.compile(r'^[a-zA-Z]+')
declaraciones = [re.compile(r'(^str)\s*([a-zA-Z]+[0-9]*)\s*(;$)'), re.compile(r'(^int)\s*([a-zA-Z]+[0-9]*)\s*(;$)'),
                 re.compile(r'(^boolean)\s*([a-zA-Z]+[0-9]*)\s*(;$)')]
declaraAsigna = [re.compile(r'(^str)\s*([a-zA-Z]+[0-9]*)\s*=\s*(\"[^\"]*\")\s*(;$)'),
                 re.compile(r'(^int)\s*([a-zA-Z]+[0-9]*)\s*=\s*([0-9]+)\s*(;$)'),
                 re.compile(r'(^boolean)\s*([a-zA-Z]+[0-9]*)\s*=\s*(True|False)\s*(;$)')]
declaraAsignaVar = [re.compile(r'(^str)\s*([a-zA-Z]+[0-9]*)\s*=\s*([a-zA-Z]+[0-9]*)\s*(;$)'),
                    re.compile(r'(^int)\s*([a-zA-Z]+[0-9]*)\s*=\s*([a-zA-Z]+[0-9]*)\s*(;$)'),
                    re.compile(r'(^boolean)\s*([a-zA-Z]+[0-9]*)\s*=\s*([a-zA-Z]+[0-9]*)\s*(;$)')]

asignaciones = [re.compile(r'^([a-zA-Z]+[0-9]*)\s*=\s*(True|False)\s*(;$)'),
                re.compile(r'^([a-zA-Z]+[0-9]*)\s*=\s*([a-zA-Z]+[0-9]*)\s*(;$)'),  # Para variables
                re.compile(r'^([a-zA-Z]+[0-9]*)\s*=\s*([0-9]+)\s*(;$)'),  # Para int
                re.compile(r'^([a-zA-Z]+[0-9]*)\s*=\s*(\"[^\"]*\")\s*(;$)'),  # Para str
                ]  # Para boolean
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
    syntactic_analyzer(linea, tabsim)
    # print("Error, revise la línea", linea[1], "ya que existe un error de sintaxis en la declaración o asignación")



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
    numero_linea = linea[1]
    expresion = re.sub(r'.*= *', '', linea[0]).replace(" ", "")
    expresion = re.sub(r';$','',expresion)
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