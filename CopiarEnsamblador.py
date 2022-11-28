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
                            txt.write("        " + simb[0] + " DW " + str(int(simb[2])) + "\n")
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
                                    if simbolo[1] == "int":
                                        output.write("        mov AX, "+simbolo[0]+"\n")
                                        output.write("        push AX\n")
                                        output.write("        call todec\n")
                                        output.write("        pop ax\n")
                                    elif simbolo[1] == "str":
                                        output.write('        mov dx, offset ' + elemento + '\n')
                                        output.write('        mov ah, 9\n')
                                        output.write('        int 21h\n')
                                    output.write('\n')
                output.write(linea + '\n') 


def copiarLectura(variable, tabsim):
    with open('Patito.ASM', 'r') as txt:
        txt = txt.read().split('\n')
        with open('Patito.ASM', 'w') as output:
            for linea in txt:
                if linea == "        ;Codigo.":
                    for simb in tabsim:
                        if variable == simb[0]:
                            if simb[1] == 'str':
                                output.write('        xor ax, ax\n')
                                output.write('        xor bx, bx\n')
                                output.write('        mov dx, offset ' + variable + '\n')
                                output.write('        mov ah, 0ah\n')
                                output.write('        int 21h\n')
                                output.write('        mov dl, 10\n')
                                output.write('        mov AH,2\n')
                                output.write('        int 21h\n')
                                output.write('\n')
                            elif simb[1] == 'int':
                                output.write('        lea dx, numeroLectura\n')
                                output.write('        mov ah, 0ah\n')
                                output.write('        int 21h\n')
                                output.write('        lea bx, numeroLectura+1\n')
                                output.write('        mov ch, 0\n')
                                output.write('        mov cl, [bx]\n')
                                output.write('        push cx\n')
                                output.write('        cr:\n')
                                output.write('            inc bx\n')
                                output.write('            mov al, [bx]\n')
                                output.write('            cmp al, 30h\n')
                                output.write('            jb fuera\n')
                                output.write('            cmp al, 39h\n')
                                output.write('            ja fuera\n')
                                output.write('            sub [bx], 30h\n')
                                output.write('            loop cr\n')
                                output.write('        pop cx\n')
                                output.write('        dec cx\n')
                                output.write('        mov si, 0ah\n')
                                output.write('        lea bx, numeroLectura+2\n')
                                output.write('        mov al, [bx]\n')
                                output.write('        mov ah, 0\n')
                                output.write('        jcxz tp\n')
                                output.write('        cc:\n')
                                output.write('            mul si\n')
                                output.write('            jo fuera\n')
                                output.write('            inc bx\n')
                                output.write('            mov dl, [bx]\n')
                                output.write('            mov dh, 0\n')
                                output.write('            add ax, dx\n')
                                output.write('        loop cc\n')
                                output.write('        tp:\n')
                                output.write('            jc fuera\n')
                                output.write('            mov ' + variable + ', ax\n')
                                output.write('        fuera:\n')
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
                        output.write("        " + cuadroplo[3] + " DW ?\n")
                        variables_temporales.append(cuadroplo[3])
                if linea == "        ;Codigo.":
                    match cuadroplo[0]:
                        case '+':
                            output.write('        xor ax, ax\n')
                            output.write('        xor bx, bx\n')
                            output.write('        mov ax, ' + str(cuadroplo[1]) + '\n')
                            output.write('        mov bx, ' + str(cuadroplo[2]) + '\n')
                            output.write('        add ax, bx\n')
                            output.write('        mov ' + cuadroplo[3] + ', ax\n')
                            output.write('        \n')
                        case '-':
                            output.write('        xor ax, ax\n')
                            output.write('        xor bx, bx\n')
                            output.write('        mov ax, ' + str(cuadroplo[1]) + '\n')
                            output.write('        mov bx, ' + str(cuadroplo[2]) + '\n')
                            output.write('        sub ax, bx\n')
                            output.write('        mov ' + cuadroplo[3] + ', ax\n')
                            output.write('        \n')
                        case '*':
                            output.write('        xor ax, ax\n')
                            output.write('        xor bx, bx\n')
                            output.write('        mov ax, ' + str(cuadroplo[1]) + '\n')
                            output.write('        mov bx, ' + str(cuadroplo[2]) + '\n')
                            output.write('        mul bx\n')
                            output.write('        mov ' + cuadroplo[3] + ', ax\n')
                            output.write('        \n')
                        case '/':
                            output.write('        xor ax, ax\n')
                            output.write('        xor bx, bx\n')
                            output.write('        xor dx, dx\n')
                            output.write('        mov ax, ' + str(cuadroplo[1]) + '\n')
                            output.write('        mov bx, ' + str(cuadroplo[2]) + '\n')
                            output.write('        div bx\n')
                            output.write('        mov ' + cuadroplo[3] + ', ax\n')
                            output.write('        \n')
                output.write(linea + '\n') 
                    

def copiarResultadoSintactico(variable, resultado):
    with open('Patito.ASM', 'r') as txt:
        txt = txt.read().split('\n')
        with open('Patito.ASM', 'w') as output:
            for linea in txt:
                if linea == "        ;Codigo.":
                    output.write('        xor ax, ax\n')
                    output.write('        mov ax, '+resultado+'\n')
                    output.write('        mov ' + variable + ', ax\n')
                    output.write('\n')
                output.write(linea + '\n')


def copiarAsignacion(variable, valor):
    with open('Patito.ASM', 'r') as txt:
        txt = txt.read().split('\n')
        with open('Patito.ASM', 'w') as output:
            for linea in txt:
                if linea == "        ;Codigo.":
                    output.write('        mov ' + variable + ', ' + str(valor) + '\n')
                output.write(linea + '\n')