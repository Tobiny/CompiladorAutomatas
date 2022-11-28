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
                            if len(simb[2]) == 0:
                                txt.write(
                                    "        " + simb[0] + " db 20,?,20 dup(?)\n")
                            else:
                                txt.write(
                                    "        " + simb[0] + " DB " + str(simb[2]) + ', \"$\"' + '\n')


def copiarImpresion(cadenas, todo, tabsim):
    global cont
    pila = []
    contPila = 0
    with open('Patito.ASM', 'r') as txt:
        txt = txt.read().split('\n')
        with open('Patito.ASM', 'w') as output:
            for linea in txt:
                if linea == "        ;Cadenas a imprimir.":
                    for cad in cadenas:
                        cont += 1
                        pila.append(cont)
                        output.write('        str' + str(cont) + ' DB "' + cad + '", \"$\"' + '\n')
                if linea == "        ;Codigo.":
                    for elemento in todo:
                        flag = False
                        for cad in cadenas:
                            if elemento == cad:
                                output.write('        mov dx, offset str' + str(pila[contPila]) + '\n')
                                output.write('        mov ah, 9\n')
                                output.write('        int 21h\n')
                                output.write('\n')
                                flag = True
                                contPila += 1
                                break
                        if not flag:
                            for simbolo in tabsim:
                                if elemento == simbolo[0]:
                                    if simbolo[4] == "SiLectura":
                                        output.write('        xor bx, bx\n')
                                        output.write('        mov bl, '+simbolo[0]+'[1]\n')
                                        output.write('        mov '+simbolo[0]+'[bx+2], \'$\'\n')
                                        output.write('        mov dx, offset '+simbolo[0]+' + 2\n')
                                    else:
                                        if simbolo[1] == "int":
                                            output.write("        ;Impresión decimal\n")
                                        elif simbolo[1] == "str":
                                            output.write('        mov dx, offset ' + elemento + '\n')

                                    output.write('        mov ah, 9\n')
                                    output.write('        int 21h\n')
                                    output.write('\n')
                output.write(linea + '\n') 


def copiarLectura(variable):
    with open('Patito.ASM', 'r') as txt:
        txt = txt.read().split('\n')
        with open('Patito.ASM', 'w') as output:
            for linea in txt:
                if linea == "        ;Codigo.":
                    output.write('        xor ax, ax\n')
                    output.write('        xor bx, bx\n')
                    output.write('        mov dx, offset ' + variable + '\n')
                    output.write('        mov ah, 0ah\n')
                    output.write('        int 21h\n')
                    output.write('        mov dl, 10\n')
                    output.write('        mov AH,2\n')
                    output.write('        int 21h\n')
                    output.write('\n')
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
                            output.write('        lea AX, ' + str(cuadroplo[1]) + '\n')
                            output.write('        lea BX, ' + str(cuadroplo[2]) + '\n')
                            output.write('        add AX, BX\n')
                            output.write('        mov ' + cuadroplo[3] + ', AX\n')
                        case '-':
                            output.write('        lea AX, ' + str(cuadroplo[1]) + '\n')
                            output.write('        lea BX, ' + str(cuadroplo[2]) + '\n')
                            output.write('        sub AX, BX\n')
                            output.write('        mov ' + cuadroplo[3] + ', AX\n')
                        case '*':
                            output.write('        mov AH, 0\n')
                            output.write('        lea AL, ' + str(cuadroplo[1]) + '\n')
                            output.write('        lea BL, ' + str(cuadroplo[2]) + '\n')
                            output.write('        mul BL\n')
                            output.write('        mov ' + cuadroplo[3] + ', AL\n')
                        case '/':
                            output.write('        mov AH, 0\n')
                            output.write('        lea AL, ' + str(cuadroplo[1]) + '\n')
                            output.write('        lea BL, ' + str(cuadroplo[2]) + '\n')
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
