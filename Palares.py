import re
variables = re.compile(r'^[a-zA-Z]+$')
tabsim = [[],[],[],[]]

palabras = ['main','int','boolean','str','readin','print','for', 'if', 'while']
declar = ['int','str','boolean']

def ispalres(pal, declarar):
    if declarar:
        return pal in declar
    return pal in palabras

def palres(linea):
    if len(linea[0]) != 3:
        print('Error de sintaxis en la línea', linea[1])
    else:
        if linea[0][1] in palabras:
            print('No puede declarar variables con palabras reservadas, error en linea',linea[1])
        elif bool(variables.match(linea[0][1])) and linea[0][2] == ';':
            if linea[0][1] in tabsim[0]:
                print('Error, variable ya declarada, en la línea',linea[1])
            else:
                tabsim[0].append(linea[0][1])
                tabsim[1].append(linea[0][0])
                if linea[0][0] == 'int':
                    tabsim[2].append(0)
                elif linea[0][0] == 'str':
                    tabsim[2].append('')
                elif linea[0][0] == 'boolean':
                    tabsim[2].append(False)
                tabsim[3].append('id'+str(len(tabsim[3])))
        else:
            print('Error de sintaxis con el nombrado de variable en la línea', linea[1])

