import AFDebugger as db
import AnalizadorLexico as Pl
from CopiarEnsamblador import copiar

if __name__ == '__main__':

    flag = True
    iteracion = 0

    db.debugger('test.af')
    f = open('test.afd', 'r')
    code = f.read().split('\n')
    codeList = []
    # Prepara el código para el algoritmo
    for line in code:
        codeList.append([(line.partition(':')[-1].lstrip()), int(line.partition(':')[0])])
    # Analiza linea por linea
    for line in codeList:
        if not Pl.lexan(line, iteracion):
            flag = False
    iteracion = 1

    print(Pl.tabsim)
    
    # Copia a ensamblador si no hubo errores. 
    if flag:
        copiar("Patito")
        print("Sí funcionó")
        for line in codeList:
            Pl.lexan(line, iteracion)
    else:
        print("No funcionó")
