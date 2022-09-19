import AFDebugger as db
import AnalizadorLexico as Pl

if __name__ == '__main__':

    db.debugger('ejemplo.af')
    f = open('ejemplo.afd', 'r')
    code = f.read().split('\n')
    codeList = []
    # Prepara el código para el algoritmo
    for line in code:
        codeList.append([(line.partition(':')[-1].lstrip()), int(line.partition(':')[0])])
    # Analiza linea por linea
    for line in codeList:
        Pl.lexan(line)

    print(Pl.tabsim)
