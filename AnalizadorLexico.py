import re

variables = re.compile(r'^[a-zA-Z]+$')
declaraciones = [re.compile(r'(^str)\s*([a-zA-Z]+[0-9]*)\s*(;$)'), re.compile(r'(^int)\s*([a-zA-Z]+[0-9]*)\s*(;$)'),
                 re.compile(r'(^boolean)\s*([a-zA-Z]+[0-9]*)\s*(;$)')]
declaraAsigna = [re.compile(r'(^str)\s*([a-zA-Z]+[0-9]*)\s*=\s*(\"[^\"]*\")\s*(;$)'),
                 re.compile(r'(^int)\s*([a-zA-Z]+[0-9]*)\s*=\s*([0-9]+)\s*(;$)'),
                 re.compile(r'(^boolean)\s*([a-zA-Z]+[0-9]*)\s*=\s*(True|False)\s*(;$)')]
declaraAsignaVar = [re.compile(r'(^str)\s*([a-zA-Z]+[0-9]*)\s*=\s*([a-zA-Z]+[0-9]*)\s*(;$)'),
                    re.compile(r'(^int)\s*([a-zA-Z]+[0-9]*)\s*=\s*([a-zA-Z]+[0-9]*)\s*(;$)'),
                    re.compile(r'(^boolean)\s*([a-zA-Z]+[0-9]*)\s*=\s*([a-zA-Z]+[0-9]*)\s*(;$)')]

asignaciones = [re.compile(r'^([a-zA-Z]+[0-9]*)\s*=\s*([a-zA-Z]+[0-9]*)\s*(;$)'),  # Para variables
                re.compile(r'^([a-zA-Z]+[0-9]*)\s*=\s*([0-9])+\s*(;$)'),  # Para int
                re.compile(r'^([a-zA-Z]+[0-9]*)\s*=\s*(\"[^\"]*\")\s*(;$)'),  # Para str
                re.compile(r'^([a-zA-Z]+[0-9]*)\s*=\s*(True|False)+\s*(;$)')]  # Para boolean
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
    print("Error, revise la línea",linea[1],"ya que existe un error de sintaxis en la declaración o asignación")

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
        add = []
        add.append(m.group(2))
        add.append(m.group(1))
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
    for simb in tabsim:
        if m.group(1) == simb[0]:
            if it == 1:
                if simb[1] == 'int':
                    simb[2] = int(m.group(2))
                else:
                    print("Error, está intentando introducir un entero a una variable de otro tipo en la línea ", linea[1])
                    return False
            elif it == 2:
                if simb[1] == 'str':
                    simb[2] = m.group(2)
                else:
                    print("Error, está intentando introducir una cadena a una variable de otro tipo en la línea ", linea[1])
                    return False
            elif it == 3:
                if simb[1] == 'boolean':
                    simb[2] = m.group(2)
                else:
                    print("Error, está intentando introducir una bandera a una variable de otro tipo en la línea ", linea[1])
                    return False
            elif it == 0:
                for simb1 in tabsim:
                    if m.group(2) == simb1[0]:
                        simb[2] = simb1[1]
            return True


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
            add.append(m.group(3))
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

            print("Error, tipo de dato de la variable a asignar es distinto a la que se va a declarar en la línea",linea[1])
            return
        add = []
        add.append(m.group(2))
        add.append(m.group(1))

        for simb in tabsim:
            if m.group(3) == simb[0]:
                add.append(simb[2])
                break
        add.append('id' + str(len(tabsim)))
        tabsim.append(add)
        return True