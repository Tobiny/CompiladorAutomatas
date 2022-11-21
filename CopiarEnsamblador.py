import AnalizadorLexico as Pl

def copiar(archivo):
    f = open('P00.ASM', 'r')
    txt = open(archivo + '.ASM', 'w')
    code = f.read().split('\n')
    cont = 0
    for linea in code:
        txt.write(linea + '\n')
        if linea == "datos segment para public 'data'":
            for simb in Pl.tabsim:
                if simb[1] == "int":
                    txt.write("        " + simb[0] + " DB " + str(simb[2]) + "\n")
                elif simb[1] == "str":
                    txt.write("        " + simb[0] + " DB " + str(len(simb[2])) + ",?," + str(len(simb[2])) + " dup(?)" + "\n")
            for cad in Pl.strings:
                cont += 1
                txt.write('        ' + 'str' + str(cont) + ' DB ' + '"' + cad + '$"' + '\n')