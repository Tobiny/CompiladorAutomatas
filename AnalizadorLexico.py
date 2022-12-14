import re
import CopiarEnsamblador as copy

variables = re.compile(r'^[a-zA-Z]+')
declaraciones = [re.compile(r'(^str)\s*([a-zA-Z]+[0-9]*)\s*(;$)'),  # Strings
                 re.compile(r'(^int)\s*([a-zA-Z]+[0-9]*)\s*(;$)'),  # Integers
                 re.compile(r'(^boolean)\s*([a-zA-Z]+[0-9]*)\s*(;$)')]  # Booleanos

declaraAsigna = [re.compile(r'(^str)\s*([a-zA-Z]+[0-9]*)\s*=\s*(\"[^\"]*\")\s*(;$)'),  # Strings
                 re.compile(r'(^int)\s*([a-zA-Z]+[0-9]*)\s*=\s*([0-9]+)\s*(;$)'),  # Integers
                 re.compile(r'(^boolean)\s*([a-zA-Z]+[0-9]*)\s*=\s*(True|False)\s*(;$)')]  # Booleanos

declaraAsignaVar = [re.compile(r'(^str)\s*([a-zA-Z]+[0-9]*)\s*=\s*([a-zA-Z]+[0-9]*)\s*(;$)'),
                    re.compile(r'(^int)\s*([a-zA-Z]+[0-9]*)\s*=\s*([a-zA-Z]+[0-9]*)\s*(;$)'),
                    re.compile(r'(^boolean)\s*([a-zA-Z]+[0-9]*)\s*=\s*([a-zA-Z]+[0-9]*)\s*(;$)')]

asignaciones = [re.compile(r'^([a-zA-Z]+[0-9]*)\s*=\s*(True|False)\s*(;$)'),  # Para boolean
                re.compile(r'^([a-zA-Z]+[0-9]*)\s*=\s*([a-zA-Z]+[0-9]*)\s*(;$)'),  # Para variables
                re.compile(r'^([a-zA-Z]+[0-9]*)\s*=\s*([0-9]+)\s*(;$)'),  # Para int
                re.compile(r'^([a-zA-Z]+[0-9]*)\s*=\s*(\"[^\"]*\")\s*(;$)'),  # Para str
                ]

tabsim = []
tabnum = []
cuadroplo = []
palabras = ['main', 'int', 'boolean', 'str', 'leer', 'imp', 'for', 'if', 'while', 'else']
declar = ['int', 'str', 'boolean']
syntax_result = 0
logic_result = True
operacion_en_comparacion = False
error = False
resetear = True
ultimaT = '4T'


def ispalres(pal, declarar):
    if declarar:
        return pal in declar
    return pal in palabras


def lexan(linea, iteracion):
    global logic_result
    global resetear
    global ultimaT

    if iteracion == 1 and resetear:
        tabsim.clear()
        tabnum.clear()
        cuadroplo.clear()
        resetear = False

    if not logic_result:
        if re.match(r'.*}', linea[0]):
            logic_result = True
        return True

    for a in range(0, len(declaraciones)):
        m = declaraciones[a].match(linea[0])
        if m:
            if m.group(2) in palabras:
                print('No puede declarar variables con palabras reservadas, error en la l??nea ', linea[1])
                return False
            else:
                return addTabSim(linea, m)

    for a in range(0, len(asignaciones)):
        m = asignaciones[a].match(linea[0])
        if m:
            if (m.group(1) in palabras) or (m.group(2) in palabras):
                print('No puede asignar el valor a las palabras reservadas, error en la linea', linea[1])
                return False
            else:
                return asigTabSim(linea, m, a, iteracion)

    for a in range(0, len(declaraAsigna)):
        m = declaraAsigna[a].match(linea[0])
        if m:
            if (m.group(2) in palabras) or (m.group(3) in palabras):
                print('No puede declarar variables con palabras reservadas, error en la l??nea', linea[1])
                return False
            else:
                return asDeTabSim(linea, m)

    for a in range(0, len(declaraAsignaVar)):
        m = declaraAsignaVar[a].match(linea[0])
        if m:
            if (m.group(2) in palabras) or (m.group(3) in palabras):
                print('No puede declarar variables con palabras reservadas, error en la l??nea', linea[1])
                return False
            else:
                return asDeVarTabSim(linea, m)

    m = re.match(r'^(int)\s+([a-zA-Z]+[0-9]*)\s*=.*([+|\-|*|\/|\(|\)])+.*(;)', linea[0])
    if m is not None:
        if (m.group(2) in palabras) or (
                re.match(r'=.*(int|main|boolean|str|readin|print|for|if|while|else).*', linea[0])):
            print('No puede declarar variables con palabras reservadas, error en la l??nea ', linea[1])
            return False
        declarada = False
        for simb in tabsim:
            if m.group(2) == simb[0]:
                declarada = True
                break
        if declarada:
            print('Error, variable ya declarada, en la l??nea', linea[1])
            return False
        if (syntactic_analyzer(linea, tabsim, iteracion)):
            if iteracion == 1:
                copy.copiarResultadoSintactico(m.group(2), ultimaT)
            # tabsim.append([m.group(2), 'int', syntax_result, 'id' + str(len(tabsim)), 'NoLectura'])
            return True

    m = re.match(r'^([a-zA-Z]+[0-9]*)\s*=.*([+|\-|*|\/|\(|\)])+.*(;)', linea[0])
    if m is not None:
        if (m.group(1) in palabras) or (
                re.match(r'=.*(int|main|boolean|str|readin|print|for|if|while|else).*', linea[0])):
            print('No puede declarar variables con palabras reservadas, error en la l??nea ', linea[1])
            return False
        declarada = False
        for simb in tabsim:
            if m.group(1) == simb[0]:
                declarada = True
                break
        if not declarada:
            print('Error, variable no declarada, en la l??nea', linea[1])
            return False
        if (syntactic_analyzer(linea, tabsim, iteracion)):
            for variable in tabsim:
                if m.group(1) == variable[0]:
                    if iteracion == 1:
                        for _ in range(len(cuadroplo)):
                            if _ == len(cuadroplo) - 1:
                                copy.copiarResultadoSintactico(m.group(1), cuadroplo[_][3])
                    # variable[2] = syntax_result
                    # variable[4] = 'NoLectura'
                    break
            return True
        else:
            return False

    # Revisa si es un if.
    m = re.match(r'^if\(.*\){$|^if\(.*\){', linea[0])
    if m is not None:
        return logic_analyzer(linea, tabsim, iteracion)

    # Revisa si es un while.
    m = re.match(r'^while\(.*\){$|^while\(.*\){', linea[0])
    if m is not None:
        return logic_analyzer(linea, tabsim, iteracion)

    # Revisa si es una impresi??n.
    m = re.match(r'^imp\([a-zA-Z0-9\+\s"]*\);', linea[0])
    if m is not None:
        return imprimir(linea, tabsim, iteracion)

    # Revisa si es una lectura.
    m = re.match(r'^leer\([a-zA-Z]+[0-9]*\);', linea[0])
    if m is not None:
        return lectura(linea, tabsim, iteracion)

    # Revisa si es un corchete de cierre.
    m = re.match(r'}', linea[0])
    if m is not None:
        return

    # Si no es ninguna opci??n marca error.
    print("Error, revise la l??nea", linea[1], "ya que existe un error de sintaxis en la declaraci??n o asignaci??n")


def addTabSim(linea, m):
    declarada = False
    for simb in tabsim:
        if m.group(2) == simb[0]:
            declarada = True
            break
    if declarada:
        print('Error, variable ya declarada, en la l??nea', linea[1])
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
        add.append('NoLectura')
        tabsim.append(add)
        return True


def asigTabSim(linea, m, it, iteracion):
    declarada = False
    valor = m.group(2)
    valor = int(valor)
    for simb in tabsim:
        if m.group(1) == simb[0]:
            declarada = True
            if it == 0:
                if simb[1] == 'boolean':
                    if m.group(2) == 'False':
                        if iteracion == 1:
                            copy.copiarAsignacion(simb[0], valor)
                    else:
                        if iteracion == 1:
                            copy.copiarAsignacion(simb[0], valor)
                else:
                    print("Error, est?? intentando introducir una bandera a una variable de otro tipo en la l??nea",
                          linea[1])
                    return False
            elif it == 1:
                for simb1 in tabsim:
                    if m.group(2) == simb1[0]:
                        if iteracion == 1:
                            copy.copiarAsignacion(simb[0], valor)
                    else:
                        print("Error, variable no declarada en la linea",
                              linea[1])
                        return False
            elif it == 2:
                if simb[1] == 'int':
                    if iteracion == 1:
                        copy.copiarAsignacion(simb[0], valor)
                else:
                    print("Error, est?? intentando introducir un entero a una variable de otro tipo en la l??nea",
                          linea[1])
                    return False
            elif it == 3:
                if simb[1] == 'str':
                    if iteracion == 1:
                        copy.copiarAsignacion(simb[0], valor)
                else:
                    print("Error, est?? intentando introducir una cadena a una variable de otro tipo en la l??nea",
                          linea[1])
                    return False
    return True


def asDeTabSim(linea, m):
    declarada = False
    for simb in tabsim:
        if m.group(2) == simb[0]:
            declarada = True
            break
    if declarada:
        print('Error, variable ya declarada, en la l??nea', linea[1])
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
        add.append('NoLectura')
        tabsim.append(add)
        return True


# A??ade los n??meros en una expresi??n matem??tica a una tabla de n??meros. Recibe una lista con los n??meros encontrados en la l??nea.
def addTablaNum(numeros_en_linea):
    declarada = False
    # Por cada n??mero en la lista lo a??ade a la tabla si no estaba antes.
    for n in numeros_en_linea:
        # Si ya hay n??meros es la tabla ver??fica que no se a??adan repetidos.
        if len(tabnum) > 0:
            for num in tabnum:
                if int(n) == num[0]:
                    declarada = True
                    break
        # Si hay repetidos pasa al siguiente n??mero.
        if declarada:
            declarada = False
        # A??ade el n??mero commo valor entero y su identificador de tipo n0, n1, etc.
        else:
            add = []
            add.append(int(n))
            add.append('n' + str(len(tabnum)))
            tabnum.append(add)


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
        print('Error, variable ya declarada, en la l??nea', linea[1])
        return False
    if not encontrada:
        print('Error, variable a asignar no ha sido declarada, en la l??nea', linea[1])
        return False
    else:
        if m.group(1) != tipo:
            print("Error, tipo de dato de la variable a asignar es distinto a la que se va a declarar en la l??nea",
                  linea[1])
            return False
        add = [m.group(2), m.group(1)]
        for simb in tabsim:
            if m.group(3) == simb[0]:
                add.append(simb[2])
                break
        add.append('id' + str(len(tabsim)))
        add.append('NoLectura')
        tabsim.append(add)
        return True


# Anali??za que la l??nea sea sintacticamente correcta.
def syntactic_analyzer(linea, tabsim, iteracion):

    global ultimaT

    if not operacion_en_comparacion:
        cuadroplo.clear()
    # Recibe una lista con la l??nea y su numero de l??nea ['linea (string)', numero de linea (int)].
    numero_linea = linea[1]
    # Elimina lo que viene antes del igual, el punto y coma, y los espacios.
    expresion = re.sub(r'.*= *', '', linea[0]).replace(" ", "")
    expresion = re.sub(r';$', '', expresion)
    # Almacena todas las variables presentes en la linea.
    variables_en_linea = re.findall(r'[a-zA-Z]+\d*', expresion)
    # Analiza que no sean booleanos o strings.
    for simb in tabsim:
        for var in variables_en_linea:
            if var == simb[0] and (simb[1] == "str" or simb[1] == "boolean"):
                print("Analisis sint??ctico linea " + str(
                    numero_linea) + ": No se puede hacer operaciones con valores boleanos o cadenas.")
                return False
    # Almacena todos los n??meros presentes en la l??nea.
    numeros_en_linea = re.findall(r'\b\d+\b', expresion)
    # A??ade estos n??meros a la tabla de n??meros.
    addTablaNum(numeros_en_linea)
    # Busca que todas las variables est??n declaradas y que los par??ntesis est??n balanceados.
    if buscar_tokens(variables_en_linea, tabsim, numero_linea, expresion):
        # Crea la lista de la fila a a??adir en la tabla de cuadruplos.
        add = []
        # Crea la pila del analizador sint??tico.
        pila = [0]
        # Crea la pila de los id's para usarlos en los cuadruplos.
        pilaIdentificadores = []
        # Crea la pila donde se guardar??n los valores de las variables y los n??meros de la expresi??n. Eventualmente guardar?? el resultado final.
        pilaValores = []
        # Contador para avanzar el apuntador dentro de la expresi??n para saber qu?? elemento est?? analizando.
        contExpresion = 0
        # Tope de la pila de valores.
        tope = 0
        # Contador de las variables y n??meros que ya fueron analizadas.
        contador = 0
        # Cambia la expresi??n de manera que trabaje con los id's de las variables y los n??meros.
        expresion_procesada = reemplazar_variables(expresion)
        # Determina la longitud de la expresi??n.
        longitudExpresion = len(expresion_procesada) - 1
        # Almacena en una lista todas los id's de las variables y n??meros dentro de la expresi??n.
        varinex = re.findall(r'[a-zA-Z]+[0-9]*', expresion_procesada)
        # Se llena tabla de acciones, ir a y todas las relacionadas.
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
        # Indica cuantos simbolos se sacan de la pila si es reducci??n.
        sacarsimbolos = {1: 3, 2: 3, 3: 1, 4: 3, 5: 3, 6: 1, 7: 3, 8: 1}
        # Indica con qu?? letra va a comparar la pila. (0 = E, 1 = T, 2 = F)
        producciones_primer_simbolo = {1: 0, 2: 0, 3: 0, 4: 1, 5: 1, 6: 1, 7: 2, 8: 2}
        # Asigna un n??mero a cada operador para que sea m??s f??cil trabajar con ellos.
        simbolos = {"+": 1, "-": 2, "*": 3, "/": 4, "(": 5, ")": 6, "$": 7}
        # Algoritmo.
        while True:
            # Crea una bandera que indica si el elemento analizado es un id de variable, un id num??rico o un operador. 
            flag = "o"
            # Si el contador es m??s grande que la expresi??n le marcamos el final de cadena.
            if contExpresion > longitudExpresion:
                a = "$"
            # De lo contrario a es igual al s??mbolo que estamos analizando.
            else:
                a = expresion_procesada[contExpresion]
                if a == "t":
                    a = "n"
                # Si el elemento inicia con "i" o "n" cambia la bandera a su respetivo caso.
                if a == "i" or a == "n":
                    flag = a
                    # Almacena el id de la variable o n??mero en "a".
                    a = varinex[contador]
                    # Mueve el apuntador hasta el final del id.
                    contExpresion += len(a)
            # Estado de la pila.
            x = pila[len(pila) - 1]
            # Acci??n a realizar.
            y = 0
            # Si "a" esta dentro de los simbolos, "y" toma su valor en la tabla.
            if a in simbolos:
                y = simbolos[a]
            # Si es estado de aceptaci??n.
            if ACCION[x][y] == "A":
                print("Analisis sint??ctico linea " + str(numero_linea) + ": Correcto")
                # Almacena el resultado final de la operaci??n en la variable global.
                global syntax_result
                syntax_result = pilaValores[tope - 1]
                if not operacion_en_comparacion:
                    # Limpia la tabla de n??meros para la siguiente operaci??n.
                    tabnum.clear()
                    ultimaT = 't' + str(len(cuadroplo))
                    # Imprime la tabla de cuadruplos.
                    print(cuadroplo)
                return True
            # Si es estado de error.
            elif ACCION[x][y] == "E":
                print("Analisis sint??ctico linea " + str(numero_linea) + ": Incorrecto")
                return False
            # Si hay que ejecutar el algoritmo.
            else:
                # Indica si va a desplazar o reducir.
                siguenteAccion = ACCION[x][y][0]
                # Indica que aaci??n va a seguir.
                numeroAccion = ACCION[x][y][1]
                # Si hay que desplazar.
                if siguenteAccion == "D":
                    # A??ade a la pila la accion que iba a seguir.
                    pila.append(numeroAccion)
                    # Si el elemento analizado no es un operador a??ade su valor a la tabla de valores.
                    if not flag == "o":
                        if flag == "i":
                            for simb in tabsim:
                                if a == simb[3]:
                                    pilaValores.append(int(simb[2]))
                                    break
                        else:
                            for num in tabnum:
                                if a == num[1]:
                                    pilaValores.append(num[0])
                                    break
                        # A??ade el id a la pila de id's.
                        pilaIdentificadores.append(a)
                        # Aumenta el tope de la tabla de valores.
                        tope += 1
                        # Actualiza el contador de las variables y n??mero analizados.
                        contador += 1
                    # Si es un operador solamente recorre el apuntador una posici??n.
                    else:
                        contExpresion += 1
                # Si hay que reducir.
                elif siguenteAccion == "R":
                    # Saca acciones de la pila de acuerdo a la longitud de la producci??n.
                    for x in range(sacarsimbolos[numeroAccion]):
                        pila.pop()
                    # Guarda la ultima acci??n en la pila.
                    t = pila[len(pila) - 1]
                    # La compara con la producci??n realizada para indicar la siguiente acci??n.
                    pila.append(IR_A[t][producciones_primer_simbolo[numeroAccion]])
                    # Si la producci??n es de suma, resta, multiplicaci??n o divisi??n realiza la operaci??n.
                    if sacarsimbolos[numeroAccion] == 3 and not numeroAccion == 7:
                        # Marca si es operaci??n.
                        es_operacion = True
                        # Limpia el cuadruplo.
                        add = []
                        # Almacena el resultado de la respectiva operaci??n en la pen??ltima posici??n de la pila. 
                        match numeroAccion:
                            case 1:
                                pilaValores[tope - 2] += pilaValores[tope - 1]
                                add.append("+")
                            case 2:
                                pilaValores[tope - 2] -= pilaValores[tope - 1]
                                add.append("-")
                            case 4:
                                pilaValores[tope - 2] *= pilaValores[tope - 1]
                                add.append("*")
                            case 5:
                                pilaValores[tope - 2] /= pilaValores[tope - 1]
                                add.append("/")
                        # A??ade al cuadruplo las variables o los numeros de la operaci??n.
                        if pilaIdentificadores[tope - 2][0] == "i":
                            for simb in tabsim:
                                if pilaIdentificadores[tope - 2] == simb[3]:
                                    add.append(simb[0])
                                    es_operacion = False
                                    break
                        else:
                            for num in tabnum:
                                if pilaIdentificadores[tope - 2] == num[1]:
                                    add.append(num[0])
                                    es_operacion = False
                                    break
                        if es_operacion:
                            add.append(pilaIdentificadores[tope - 2])
                        es_operacion = True
                        if pilaIdentificadores[tope - 1][0] == "i":
                            for simb in tabsim:
                                if pilaIdentificadores[tope - 1] == simb[3]:
                                    add.append(simb[0])
                                    es_operacion = False
                                    break
                        else:
                            for num in tabnum:
                                if pilaIdentificadores[tope - 1] == num[1]:
                                    add.append(num[0])
                                    es_operacion = False
                                    break
                        if es_operacion:
                            add.append(pilaIdentificadores[tope - 1])
                        es_operacion = True
                        add.append('t' + str(len(cuadroplo) + 1))
                        if iteracion == 1:
                            copy.copiarCuadroplo(add)
                        cuadroplo.append(add)
                        pilaIdentificadores[tope - 2] = add[3]
                        pilaIdentificadores.pop()
                        # Saca el ??ltimo valor de la pila dejando en el tope el resultado de la operaci??n.
                        pilaValores.pop()
                        # Reduce el tope.
                        tope -= 1


def logic_analyzer(linea, tabsim, iteracion):
    cuadroplo.clear()
    numero_linea = linea[1]
    instruccion = linea[0].split('{')
    instruccion.pop(0)
    instruccion.append(numero_linea)
    expresion = re.sub(r'^if\(|^while\(', '', linea[0])
    expresion = re.sub(r'\){.*', '', expresion)
    if expresion == "True":
        print("Analisis l??gico linea " + str(numero_linea) + ": Correcto")
        print("Comparaci??n True")
        return True
    elif expresion == "False":
        print("Analisis l??gico linea " + str(numero_linea) + ": Correcto")
        print("Comparaci??n False")
        return True
    expresion = reemplazar_operadores_logicos(expresion)
    expresion = expresion.replace(" ", "")
    operaciones = re.findall(r'[\w\(\)\+\-\*\/]+[\+\-\*\/][\w\(\)\+\-\*\/]+', expresion)
    operaciones = [el for el in operaciones if el]
    if operaciones:
        global operacion_en_comparacion
        operacion_en_comparacion = True
    for operacion in operaciones:
        op = [operacion, numero_linea]
        if not syntactic_analyzer(op, tabsim, iteracion):
            return False
        else:
            add = []
            expresion = expresion.replace(operacion, str(syntax_result))
            add.append(syntax_result)
            add.append('t' + str(len(cuadroplo)))
            tabnum.append(add)
    variables_en_linea = re.findall(r'[a-zA-Z]+\d*', expresion)
    variables_en_linea = [el for el in variables_en_linea if el]
    numeros_en_linea = re.findall(r'-*\b\d+\b', expresion)
    if not variables_en_linea and len(numeros_en_linea) == 1:
        print("Analisis l??gico linea " + str(numero_linea) + ": Incorrecto")
        return False
    addTablaNum(numeros_en_linea)
    expresion_procesada = reemplazar_variables(expresion)
    if buscar_tokens(variables_en_linea, tabsim, numero_linea, expresion):
        add = []
        pila = [0]
        pilaIdentificadores = []
        pilaValores = []
        contExpresion = 0
        tope = 0
        contador = 0
        expresion_procesada = reemplazar_variables(expresion)
        longitudExpresion = len(expresion_procesada) - 1
        varinex = re.findall(r'[a-zA-Z]+[0-9]*', expresion_procesada)
        ACCION = [
            [("D", 7), "E", "E", "E", "E", "E", "E", ("D", 5), ("D", 6), "E", "E"],  # 0
            ["E", ("D", 8), ("D", 9), "E", "E", "E", "E", "E", "E", "E", "A"],  # 1
            ["E", ("R", 3), ("R", 3), ("D", 10), ("D", 11), "E", "E", "E", "E", ("R", 3), ("R", 3)],  # 2
            ["E", ("R", 6), ("R", 6), ("R", 6), ("R", 6), ("D", 12), ("D", 13), "E", "E", ("R", 6), ("R", 6)],  # 3
            ["E", ("R", 9), ("R", 9), ("R", 9), ("R", 9), ("R", 9), ("R", 9), "E", "E", ("R", 9), ("R", 9)],  # 4
            [("D", 7), "E", "E", "E", "E", "E", "E", ("D", 5), ("D", 6), "E", "E"],  # 5
            [("D", 7), "E", "E", "E", "E", "E", "E", ("D", 5), ("D", 6), "E", "E"],  # 6
            ["E", ("R", 12), ("R", 12), ("R", 12), ("R", 12), ("R", 12), ("R", 12), "E", "E", ("R", 12), ("R", 12)],
            # 7
            [("D", 7), "E", "E", "E", "E", "E", "E", ("D", 5), ("D", 6), "E", "E"],  # 8
            [("D", 7), "E", "E", "E", "E", "E", "E", ("D", 5), ("D", 6), "E", "E"],  # 9
            [("D", 7), "E", "E", "E", "E", "E", "E", ("D", 5), ("D", 6), "E", "E"],  # 10
            [("D", 7), "E", "E", "E", "E", "E", "E", ("D", 5), ("D", 7), "E", "E"],  # 11
            [("D", 7), "E", "E", "E", "E", "E", "E", ("D", 5), ("D", 7), "E", "E"],  # 12
            [("D", 7), "E", "E", "E", "E", "E", "E", ("D", 5), ("D", 7), "E", "E"],  # 13
            ["E", ("R", 10), ("R", 10), ("R", 10), ("R", 10), ("R", 10), ("R", 10), "E", "E", ("R", 10), ("R", 10)],
            # 14
            ["E", ("D", 8), ("D", 9), "E", "E", "E", "E", "E", "E", ("D", 22), "E"],  # 15
            ["E", ("R", 1), ("R", 1), ("D", 10), ("D", 11), "E", "E", "E", "E", ("R", 1), ("R", 1)],  # 16
            ["E", ("R", 2), ("R", 2), ("D", 10), ("D", 11), "E", "E", "E", "E", ("R", 2), ("R", 2)],  # 17
            ["E", ("R", 4), ("R", 4), ("R", 4), ("R", 4), ("D", 12), ("D", 13), "E", "E", ("R", 4), ("R", 4)],  # 18
            ["E", ("R", 5), ("R", 5), ("R", 5), ("R", 5), ("D", 12), ("D", 13), "E", "E", ("R", 5), ("R", 5)],  # 19
            ["E", ("R", 7), ("R", 7), ("R", 7), ("R", 7), ("R", 7), ("R", 7), "E", "E", ("R", 7), ("R", 7)],  # 20
            ["E", ("R", 8), ("R", 8), ("R", 8), ("R", 8), ("R", 8), ("R", 8), "E", "E", ("R", 8), ("R", 8)],  # 21
            ["E", ("R", 11), ("R", 11), ("R", 11), ("R", 11), ("R", 11), ("R", 11), "E", "E", ("R", 11),
             ("R", 11)]]  # 22
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
            ["E", "E", "E", "E"]]  # 22

        sacarsimbolos = {1: 3, 2: 3, 3: 1, 4: 3, 5: 3, 6: 1, 7: 3, 8: 3, 9: 1, 10: 2, 11: 3, 12: 1}
        producciones_primer_simbolo = {1: 0, 2: 0, 3: 0, 4: 1, 5: 1, 6: 1, 7: 2, 8: 2, 9: 2, 10: 3, 11: 3, 12: 3}
        simbolos = {"?": 1, "??": 2, "??": 3, ".": 4, ">": 5, "<": 6, "!": 7, "(": 8, ")": 9, "$": 10}
        while True:
            flag = "o"
            if contExpresion > longitudExpresion:
                a = "$"
            else:
                a = expresion_procesada[contExpresion]
                if a == "t":
                    a = "n"
                # Si el elemento inicia con "i" o "n" cambia la bandera a su respetivo caso.
                if a == "i" or a == "n":
                    flag = a
                    # Almacena el id de la variable o n??mero en "a".
                    a = varinex[contador]
                    # Mueve el apuntador hasta el final del id.
                    contExpresion += len(a)
            # Estado
            x = pila[len(pila) - 1]
            # Accion
            y = 0
            if a in simbolos:
                y = simbolos[a]
            if ACCION[x][y] == "A":
                print("Analisis l??gico linea " + str(numero_linea) + ": Correcto")
                global logic_result
                logic_result = pilaValores[tope - 1]
                print("Comparaci??n", logic_result)
                tabnum.clear()
                print(cuadroplo)
                if instruccion[0] != '':
                    lexan(instruccion)
                operacion_en_comparacion = False
                return True
            elif ACCION[x][y] == "E":
                print("Analisis l??gico linea " + str(numero_linea) + ": Incorrecto")
                return False
            else:
                siguenteAccion = ACCION[x][y][0]
                numeroAccion = ACCION[x][y][1]
                if siguenteAccion == "D":
                    pila.append(numeroAccion)
                    if not flag == "o":
                        if flag == "i":
                            for simb in tabsim:
                                if a == simb[3]:
                                    pilaValores.append(simb[2])
                                    break
                        else:
                            for num in tabnum:
                                if a == num[1]:
                                    pilaValores.append(num[0])
                                    break
                        pilaIdentificadores.append(a)
                        tope += 1
                        # Actualiza el contador de las variables y n??mero analizados.
                        contador += 1
                    # Si es un operador solamente recorre el apuntador una posici??n.
                    else:
                        contExpresion += 1
                elif siguenteAccion == "R":
                    for x in range(sacarsimbolos[numeroAccion]):
                        pila.pop()
                    t = pila[len(pila) - 1]
                    pila.append(IR_A[t][producciones_primer_simbolo[numeroAccion]])
                    if sacarsimbolos[numeroAccion] >= 2 and not numeroAccion == 11:
                        # Marca si es negaci??n.
                        es_negacion = False
                        # Limpia el cuadruplo.
                        add = []
                        # Almacena el resultado de la respectiva operaci??n en la pen??ltima posici??n de la pila. 
                        match numeroAccion:
                            case 1:
                                pilaValores[tope - 2] = pilaValores[tope - 2] or pilaValores[tope - 1]
                                add.append("/&")
                            case 2:
                                pilaValores[tope - 2] = pilaValores[tope - 2] and pilaValores[tope - 1]
                                add.append("&&")
                            case 4:
                                pilaValores[tope - 2] = pilaValores[tope - 2] == pilaValores[tope - 1]
                                add.append("==")
                            case 5:
                                pilaValores[tope - 2] = pilaValores[tope - 2] != pilaValores[tope - 1]
                                add.append("!=")
                            case 7:
                                pilaValores[tope - 2] = pilaValores[tope - 2] > pilaValores[tope - 1]
                                add.append(">")
                            case 8:
                                pilaValores[tope - 2] = pilaValores[tope - 2] < pilaValores[tope - 1]
                                add.append("<")
                            case 10:
                                if isinstance(pilaValores[tope - 1], int) or isinstance(pilaValores[tope - 1], str):
                                    print("Analisis l??gico linea " + str(
                                        numero_linea) + ": Solo se pueden negar variables boleanas.")
                                    logic_result = False
                                    return False
                                pilaValores[tope - 1] = not pilaValores[tope - 1]
                                add.append("!")
                                es_negacion = True
                        # A??ade al cuadruplo las variables o los numeros de la operaci??n.
                        if pilaIdentificadores[tope - 2][0] == "i":
                            for simb in tabsim:
                                if es_negacion:
                                    if pilaIdentificadores[tope - 1] == simb[3]:
                                        add.append(simb[0])
                                        break
                                else:
                                    if pilaIdentificadores[tope - 2] == simb[3]:
                                        add.append(simb[0])
                                        break
                        elif pilaIdentificadores[tope - 2][0] == "n":
                            for num in tabnum:
                                if pilaIdentificadores[tope - 2] == num[1]:
                                    add.append(num[0])
                                    break
                        else:
                            add.append(pilaIdentificadores[tope - 2])
                        if es_negacion:
                            add.append('')
                        else:
                            if pilaIdentificadores[tope - 1][0] == "i":
                                for simb in tabsim:
                                    if pilaIdentificadores[tope - 1] == simb[3]:
                                        add.append(simb[0])
                                        break
                            elif pilaIdentificadores[tope - 1][0] == "n":
                                for num in tabnum:
                                    if pilaIdentificadores[tope - 1] == num[1]:
                                        add.append(num[0])
                                        break
                            else:
                                add.append(pilaIdentificadores[tope - 1])
                        add.append('t' + str(len(cuadroplo) + 1))
                        cuadroplo.append(add)
                        if es_negacion:
                            pilaIdentificadores[tope - 2] = add[3]
                        else:
                            pilaIdentificadores[tope - 1] = add[3]
                        es_negacion = False
                        # Saca el ??ltimo valor de la pila dejando en el tope el resultado de la operaci??n.
                        if numeroAccion != 10:
                            pilaValores.pop()
                            pilaIdentificadores.pop()
                            # Reduce el tope.
                            tope -= 1


def buscar_tokens(variables_en_linea, tabsim, numero_linea, expresion):
    variable_no_declarada = False
    contador_no_declaradas = 0
    variables_lectura = []
    # for variable in variables_en_linea:
    #     for simb in tabsim:
    #         if variable == simb[0]:
    #             if simb[4] == 'SiLectura':
    #                 variables_lectura.append(variable)
    #             variable_no_declarada = False
    #             break
    #         else:
    #             variable_no_declarada = True
    #     if variable_no_declarada:
    #         contador_no_declaradas += 1
    if len(variables_lectura) > 0:
        print("Error en linea", str(numero_linea) + ", esperando lectura de las siguientes variables:",
              variables_lectura)
        return False
    if contador_no_declaradas <= 0:
        if len(re.sub('[^(]', '', expresion)) != len(re.sub('[^)]', '', expresion)):
            print("Error en linea " + str(numero_linea) + ": par??ntesis no balanceados")
            return False
        else:
            return True
    else:
        print("Error en linea " + str(numero_linea) + ": existen " + str(contador_no_declaradas)
              + " variables sin declarar")
        return False


# Remplaza las variables y los n??meros en la expresi??n para trabajar con sus id's. 
def reemplazar_variables(expresion):
    # Busca todas las variables y/o n??meros en la expresi??n.
    varinex = re.findall(r'[a-zA-Z]+[0-9]*|\B-\b\d+\b|\b\d+\b', expresion)
    # Elimina los repetidos.
    varinex = list(dict.fromkeys(varinex))
    # Los ordena por longitud.
    varinex.sort(key=len)
    # Invierte el orden.
    varinex.reverse()
    # Por cada n??mero en la expresi??n lo busca en la tabla de n??meros y lo reemplaza dentro de la expresi??n con su id.
    for variable in dict.fromkeys(re.findall(r'\B-\d+\b|\b\d+\b', expresion)):
        for num in tabnum:
            if int(variable) == num[0]:
                reemplazo_regex = r'\b' + re.escape(variable) + r'\b'
                expresion = re.sub(reemplazo_regex, num[1], expresion)
                break
    # Por cada variable en la expresi??n la busca en la tabla de s??mbolos y la reemplaza dentro de la expresi??n con su id.
    for variable in varinex:
        for simb in tabsim:
            if variable == simb[0]:
                expresion = expresion.replace(variable, simb[3])
                break
    # Regresa la expresi??n ahora con los id's en lugar de las variables y n??meros.
    return expresion


def reemplazar_operadores_logicos(expresion):
    for variable in re.findall(r'\/&', expresion):
        expresion = expresion.replace(variable, '?')
    for variable in re.findall(r'&&', expresion):
        expresion = expresion.replace(variable, '??')
    for variable in re.findall(r'==', expresion):
        expresion = expresion.replace(variable, '??')
    for variable in re.findall(r'!=', expresion):
        expresion = expresion.replace(variable, '.')
    return expresion


def imprimir(linea, tabsim, iteracion):
    flag = False
    expresion = re.sub(r'^imp\(', '', linea[0])
    expresion = re.sub(r'\);}*', '', expresion)
    variables_en_linea = re.findall(r'".*"|([^+\s]*)', expresion)
    variables_en_linea = [el for el in variables_en_linea if el]

    for variable in variables_en_linea:
        flag = True
        for simb in tabsim:
            if variable != simb[0]:
                flag = False
            else:
                flag = True
                break
        if not flag:
            print("Error en la linea", linea[1], ", la variable", variable, "no est?? declarada")
            return False

    if iteracion == 1:
        todo = re.findall(r'".*?"|[^+\s]*', expresion)
        todo = [el for el in todo if el]
        for _ in range(len(todo)):
            todo[_] = re.sub('"', '', todo[_])

        cadenas = re.findall(r'"(.*?)"', expresion)
        cadenas = [el for el in cadenas if el]
        copy.copiarImpresion(cadenas, todo, tabsim)
    return True


def lectura(linea, tabsim, iteracion):
    flag = True
    expresion = re.sub(r'^leer\(', '', linea[0])
    expresion = re.sub(r'\);}*', '', expresion)

    for simb in tabsim:
        if expresion != simb[0]:
            flag = False
        else:
            flag = True
            simb[4] = 'SiLectura'
            break
    if not flag:
        print("Error en la linea", linea[1], ", la variable", expresion, "no est?? declarada")
        return False

    if iteracion == 1:
        copy.copiarLectura(expresion, tabsim)
    return True
