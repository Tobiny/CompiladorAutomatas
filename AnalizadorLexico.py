from enum import Flag
from operator import le
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
tabnum = []
palabras = ['main', 'int', 'boolean', 'str', 'readin', 'print', 'for', 'if', 'while', 'else']
declar = ['int', 'str', 'boolean']
syntax_result = 0


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
            tabsim.append([m.group(2), 'int', syntax_result, 'id' + str(len(tabsim), 'NoLectura' )])
            return

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
                    variable[2] = syntax_result
                    variable[4] = 'NoLectura'
                    break
            return
        else:
            return
    
    #Revisa si es un if.
    m = re.match(r'^if\(.*\);$', linea[0])
    if m is not None:
        logic_analyzer(linea, tabsim)
        return

    #Revisa si es una impresión.
    m = re.match(r'^imp\([a-zA-Z\+\s"]*\);$', linea[0])
    if m is not None:
        imprimir(linea, tabsim)
        return

    #Revisa si es una lectura.
    m = re.match(r'^leer\([a-zA-Z\+\s"]*\);$', linea[0])
    if m is not None:
        lectura(linea, tabsim)
        return
    
    # Si no es ninguna opción marca error.
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
        add.append('NoLectura')
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
        add.append('NoLectura')
        tabsim.append(add)
        return True


# Añade los números en una expresión matemática a una tabla de números. Recibe una lista con los números encontrados en la línea.
def addTablaNum(numeros_en_linea):
    declarada = False
    # Por cada número en la lista lo añade a la tabla si no estaba antes.
    for n in numeros_en_linea:
        # Si ya hay números es la tabla verífica que no se añadan repetidos.
        if len(tabnum) > 0:
            for num in tabnum:
                if int(n) == num[0]:
                    declarada = True
                    break
        # Si hay repetidos pasa al siguiente número.
        if declarada:
            break
        # Añade el número commo valor entero y su identificador de tipo n0, n1, etc.
        else:
            add = []
            add.append(int(n))
            add.append('n' + str(len(tabnum)))
            tabnum.append(add)
    
    return


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
        add.append('NoLectura')
        tabsim.append(add)
        return True


# Analiíza que la línea sea sintacticamente correcta.
def syntactic_analyzer(linea, tabsim):
    # Recibe una lista con la línea y su numero de línea ['linea (string)', numero de linea (int)].
    numero_linea = linea[1]
    # Elimina lo que viene antes del igual, el punto y coma, y los espacios.
    expresion = re.sub(r'.*= *', '', linea[0]).replace(" ", "")
    expresion = re.sub(r';$','',expresion)
    # Almacena todas las variables presentes en la linea.
    variables_en_linea = re.findall(r'[a-zA-Z]+\d*', expresion)
    # Almacena todos los números presentes en la línea.
    numeros_en_linea = re.findall(r'\b\d+\b', expresion)
    # Añade estos números a la tabla de números.
    addTablaNum(numeros_en_linea)
    # Busca que todas las variables estén declaradas y que los paréntesis estén balanceados.
    if buscar_tokens(variables_en_linea, tabsim, numero_linea, expresion):
        # Crea la pila del analizador sintático.
        pila = [0]
        # Crea la pila donde se guardarán los valores de las variables y los números de la expresión. Eventualmente guardará el resultado final.
        pilaValores = []
        # Contador para avanzar el apuntador dentro de la expresión para saber qué elemento está analizando.
        contExpresion = 0
        # Tope de la pila de valores.
        tope = 0
        # Contador de las variables y números que ya fueron analizadas.
        contador = 0
        # Cambia la expresión de manera que trabaje con los id's de las variables y los números.
        expresion_procesada = reemplazar_variables(expresion)
        # Determina la longitud de la expresión.
        longitudExpresion = len(expresion_procesada) - 1
        # Almacena en una lista todas los id's de las variables y números dentro de la expresión.
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
        # Indica cuantos simbolos se sacan de la pila si es reducción.
        sacarsimbolos = {1: 3, 2: 3, 3: 1, 4: 3, 5: 3, 6: 1, 7: 3, 8: 1}
        # Indica con qué letra va a comparar la pila. (0 = E, 1 = T, 2 = F)
        producciones_primer_simbolo = {1: 0, 2: 0, 3: 0, 4: 1, 5: 1, 6: 1, 7: 2, 8: 2}
        # Asigna un número a cada operador para que sea más fácil trabajar con ellos.
        simbolos = {"+": 1, "-": 2, "*": 3, "/": 4, "(": 5, ")": 6, "$": 7}
        # Algoritmo.
        while True:
            # Crea una bandera que indica si el elemento analizado es un id de variable, un id numérico o un operador. 
            flag = "o"
            # Si el contador es más grande que la expresión le marcamos el final de cadena.
            if contExpresion > longitudExpresion:
                a = "$"
            # De lo contrario a es igual al símbolo que estamos analizando.
            else:
                a = expresion_procesada[contExpresion]
                # Si el elemento inicia con "i" o "n" cambia la bandera a su respetivo caso.
                if a == "i" or a == "n":
                    flag = a
                    # Almacena el id de la variable o número en "a".
                    a = varinex[contador]
                    # Mueve el apuntador hasta el final del id.
                    contExpresion += len(a)
            # Estado de la pila.
            x = pila[len(pila) - 1]
            # Acción a realizar.
            y = 0
            # Si "a" esta dentro de los simbolos, "y" toma su valor en la tabla.
            if a in simbolos:
                y = simbolos[a]
            # Si es estado de aceptación.
            if ACCION[x][y] == "A":
                print("Analisis sintáctico linea " + str(numero_linea) + ": Correcto")
                # Almacena el resultado final de la operación en la variable global.
                global syntax_result
                syntax_result = pilaValores[tope-1]
                # Limpia la tabla de números para la siguiente operación.
                tabnum.clear()
                return True
            # Si es estado de error.
            elif ACCION[x][y] == "E":
                print("Analisis sintáctico linea " + str(numero_linea) + ": Incorrecto")
                return False
            # Si hay que ejecutar el algoritmo.
            else:
                # Indica si va a desplazar o reducir.
                siguenteAccion = ACCION[x][y][0]
                # Indica que aación va a seguir.
                numeroAccion = ACCION[x][y][1]
                # Si hay que desplazar.
                if siguenteAccion == "D":
                    # Añade a la pila la accion que iba a seguir.
                    pila.append(numeroAccion)
                    # Si el elemento analizado no es un operador añade su valor a la tabla de valores.
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
                        # Aumenta el tope de la tabla de valores.
                        tope += 1
                        # Actualiza el contador de las variables y número analizados.
                        contador += 1
                    # Si es un operador solamente recorre el apuntador una posición.
                    else:
                        contExpresion += 1
                # Si hay que reducir.
                elif siguenteAccion == "R":
                    # Saca acciones de la pila de acuerdo a la longitud de la producción.
                    for x in range(sacarsimbolos[numeroAccion]):
                        pila.pop()
                    # Guarda la ultima acción en la pila.
                    t = pila[len(pila) - 1]
                    # La compara con la producción realizada para indicar la siguiente acción.
                    pila.append(IR_A[t][producciones_primer_simbolo[numeroAccion]])
                    # Si la producción es de suma, resta, multiplicación o división realiza la operación.
                    if sacarsimbolos[numeroAccion] == 3 and not numeroAccion == 7:
                        # Almacena el resultado de la respectiva operación en la penúltima posición de la pila. 
                        match numeroAccion:
                            case 1:
                                pilaValores[tope-2] += pilaValores[tope-1]
                            case 2:
                                pilaValores[tope-2] -= pilaValores[tope-1]
                            case 4:
                                pilaValores[tope-2] *= pilaValores[tope-1]
                            case 5:
                                pilaValores[tope-2] /= pilaValores[tope-1]
                        # Saca el último valor de la pila dejando en el tope el resultado de la operación.
                        pilaValores.pop()
                        # Reduce el tope.
                        tope -= 1


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
    variables_lectura = []
    for variable in variables_en_linea:
        for simb in tabsim:
            if variable == simb[0]:
                if simb[4] == 'SiLectura':
                    variables_lectura.append(variable)
                variable_no_declarada = False
                break
            else:
                variable_no_declarada = True
        if variable_no_declarada:
            contador_no_declaradas += 1
    if len(variables_lectura) > 0:
        print("Error en linea", str(numero_linea) + ", esperando lectura de las siguientes variables:", variables_lectura)
        return False
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


# Remplaza las variables y los números en la expresión para trabajar con sus id's. 
def reemplazar_variables(expresion):
    # Busca todas las variables y/o números en la expresión.
    varinex = re.findall(r'[a-zA-Z]+[0-9]*|\b\d+\b', expresion)
    # Elimina los repetidos.
    varinex = list(dict.fromkeys(varinex))
    # Los ordena por longitud.
    varinex.sort(key=len)
    # Invierte el orden.
    varinex.reverse()
    # Por cada número en la expresión lo busca en la tabla de números y lo reemplaza dentro de la expresión con su id.
    for variable in re.findall(r'\b\d+\b', expresion):
        for num in tabnum:
            if int(variable) == num[0]:
                expresion = expresion.replace(variable, num[1])
                break
    # Por cada variable en la expresión la busca en la tabla de símbolos y la reemplaza dentro de la expresión con su id.
    for variable in varinex:
        for simb in tabsim:
            if variable == simb[0]:
                expresion = expresion.replace(variable, simb[3])
                break
    # Regresa la expresión ahora con los id's en lugar de las variables y números.
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


def imprimir(linea, tabsim):
    flag = False
    expresion = re.sub(r'^imp\(', '', linea[0])
    expresion = re.sub(r'\);$', '', expresion)
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
            print("Error en la linea", linea[1], ", la variable", variable, "no está declarada")
            return
        
    print("Analisis de impresión en la linea", linea[1], "correcto, esperando impresión")


def lectura(linea, tabsim):
    flag = False
    expresion = re.sub(r'^leer\(', '', linea[0])
    expresion = re.sub(r'\);$', '', expresion)

    for simb in tabsim:
        if expresion != simb[0]:
            flag = False
        else:
            flag = True
            simb[4] = 'SiLectura'
            break
    if not flag:
        print("Error en la linea", linea[1] + ", la variable", expresion, "no está declarada")
        return
    

    print("Analisis de lectura en la linea", linea[1], "correcto, esperando lectura")