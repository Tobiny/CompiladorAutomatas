import Debugger
import re
import Palares as pl
import json  # Libreria para convertir str a lista

if __name__ == '__main__':

    Debugger.debugger('ejemplo.af')
    f = open('ejemplo.afd', 'r')
    code = f.read().split('\n')
    codeList = []
    # Prepara el código para el algoritmo
    for line in code:
        codeList.append([(line.partition(':')[-1].lstrip()).split(), int(line.partition(':')[0])])

        # Analiza linea por linea
    for line in codeList:
        if pl.ispalres(line[0][0], True):
            pl.palres(line)
        else: print('Error de declaración en la linea', line[1])
print(pl.tabsim)