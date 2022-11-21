import AFDebugger as db
import AnalizadorLexico as Pl
from CopiarEnsamblador import copiar

if __name__ == '__main__':

    flag = True

    db.debugger('test.af')
    f = open('test.afd', 'r')
    code = f.read().split('\n')
    codeList = []
    # Prepara el código para el algoritmo
    for line in code:
        codeList.append([(line.partition(':')[-1].lstrip()), int(line.partition(':')[0])])
    # Analiza linea por linea
    for line in codeList:
        if not Pl.lexan(line):
            flag = False

    print(Pl.tabsim)

    if flag:
        copiar("Patito")
        print("Sí funcionó")
    else:
        print("No funcionó")
