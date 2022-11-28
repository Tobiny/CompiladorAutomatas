import AnalizadorLexico as Pl

cont = 0
variables_temporales = []

def copiar(archivo):
    with open('PlantillaEnsamblador.ASM', 'r') as code:
        code = code.read().split('\n')
        with open(archivo + '.ASM', 'w') as txt:
            for linea in code:
                txt.write(linea + '\n')
                if linea == "datos segment para public 'data'":
                    for simb in Pl.tabsim:
                        if simb[1] == "int":
                            txt.write("        " + simb[0] + " DB " + str(int(simb[2])) + "\n")
                        elif simb[1] == "str":
                            txt.write("        " + simb[0] + " DB " + str(len(simb[2])) + ",?," + str(len(simb[2])) + " dup(?)" + "\n")


def copiarImpresion(cadenas, todo):
    global cont
    with open('Patito.ASM', 'r') as txt:
        txt = txt.read().split('\n')
        with open('Patito.ASM', 'w') as output:
            for linea in txt:
                if linea == "        ;Cadenas a imprimir.":
                    for cad in cadenas:
                        cont += 1
                        output.write('        str' + str(cont) + ' DB ' + cad + ', 0' + '\n')
                if linea == "        ;Codigo.":
                    for elemento in todo:
                        flag = False
                        for cad in cadenas:
                            if elemento == cad:
                                output.write('        lea si, str' + str(cont) + '\n')
                                output.write('        call imprimir\n')
                                flag = True
                                break
                        if not flag:
                            output.write('        lea si, ' + elemento + '\n')
                            output.write('        call imprimir\n')
                output.write(linea + '\n') 


def copiarLectura(variable):
    with open('Patito.ASM', 'r') as txt:
        txt = txt.read().split('\n')
        with open('Patito.ASM', 'w') as output:
            for linea in txt:
                if linea == "        ;Codigo.":
                    output.write('        lea dx, ' + variable + '\n')
                    output.write('        call leer\n')
                output.write(linea + '\n') 


def copiarCuadroplo(cuadroplo):
    with open('Patito.ASM', 'r') as txt:
        txt = txt.read().split('\n')
        with open('Patito.ASM', 'w') as output:
            for linea in txt:
                if linea == "        ;Cadenas a imprimir.":
                    flag = False
                    for var in variables_temporales:
                        if var == cuadroplo[3]:
                            flag = True
                            break
                    if not flag:
                        output.write("        " + cuadroplo[3] + " DB ?\n")
                        variables_temporales.append(cuadroplo[3])
                if linea == "        ;Codigo.":
                    match cuadroplo[0]:
                        case '+':
                            output.write('        mov AX, ' + str(cuadroplo[1]) + '\n')
                            output.write('        mov BX, ' + str(cuadroplo[2]) + '\n')
                            output.write('        add AX, BX\n')
                            output.write('        mov ' + cuadroplo[3] + ', AX\n')
                        case '-':
                            output.write('        mov AX, ' + str(cuadroplo[1]) + '\n')
                            output.write('        mov BX, ' + str(cuadroplo[2]) + '\n')
                            output.write('        sub AX, BX\n')
                            output.write('        mov ' + cuadroplo[3] + ', AX\n')
                        case '*':
                            output.write('        mov AH, 0\n')
                            output.write('        mov AL, ' + str(cuadroplo[1]) + '\n')
                            output.write('        mov BL, ' + str(cuadroplo[2]) + '\n')
                            output.write('        mul BL\n')
                            output.write('        mov ' + cuadroplo[3] + ', AL\n')
                        case '/':
                            output.write('        mov AH, 0\n')
                            output.write('        mov AL, ' + str(cuadroplo[1]) + '\n')
                            output.write('        mov BL, ' + str(cuadroplo[2]) + '\n')
                            output.write('        div BL\n')
                            output.write('        mov ' + cuadroplo[3] + ', AL\n')
                output.write(linea + '\n') 
                    

def copiarResultadoSintactico(variable, resultado):
    with open('Patito.ASM', 'r') as txt:
        txt = txt.read().split('\n')
        with open('Patito.ASM', 'w') as output:
            for linea in txt:
                if linea == "        ;Codigo.":
                    output.write('        mov ' + variable + ', ' + str(resultado) + '\n')
                output.write(linea + '\n') 
