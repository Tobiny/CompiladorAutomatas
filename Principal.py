import AFDebugger as db
import csv
import pandas as pd
from Buffer import Buffer
from LexicalAnalyzer import LexicalAnalyzer

if __name__ == '__main__':
    Buffer = Buffer()
    Analyzer = LexicalAnalyzer()

    db.debugger('ejemplo.af')

    f = open('ejemplo.afn', 'w')
    f.write('TIPO,LEXEMA,FILA,COLUMNA\n')
    f.close()

    # Lista para cada lista retornada por la función tokenize
    token = []
    lexeme = []
    row = []
    column = []

    # Tokenizar y recargar el buffer
    for i in Buffer.load_buffer():
        t, lex, lin, col = Analyzer.tokenize(i)
        token += t
        lexeme += lex
        row += lin
        column += col
    df = pd.read_csv("ejemplo.afn")
    salida = {"TIPO":[], "LEXEMA":[], "FILA":[], "COLUMNA":[]}
    with open('ejemplo.afn') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            # if row["TIPO"] == "ID":
            #     if row["LEXEMA"] in salida["LEXEMA"]:
            #         pass
            #         #raise("Error, identificador declarado")
            #     if row["LEXEMA"] not in salida["LEXEMA"]:
            #         salida['TIPO'].append(row["TIPO"])
            #         salida['LEXEMA'].append(row["LEXEMA"])
            #         salida['FILA'].append(row["FILA"])
            #         salida['COLUMNA'].append(row["COLUMNA"])
            # elif row["TIPO"] != "ID":
                salida['TIPO'].append(row["TIPO"])
                salida['LEXEMA'].append(row["LEXEMA"])
                salida['FILA'].append(row["FILA"])
                salida['COLUMNA'].append(row["COLUMNA"])
    list_salida = []
    f = open('ejemplo.afn', 'w')
    f.write('TIPO,LEXEMA,FILA,COLUMNA\n')
    for i in range(len(salida['TIPO'])):
        f.write(salida['TIPO'][i]+',')
        f.write(salida['LEXEMA'][i]+',')
        f.write(salida['FILA'][i]+',')
        f.write(salida['COLUMNA'][i])
        list_salida.append(
            salida['TIPO'][i] + ',' + salida['LEXEMA'][i] + ',' + salida['FILA'][i] + ',' + salida['COLUMNA'][i])
        f.write('\n')

    f.close()


    f = open('ejemplo.afnn', 'w')
    f.write(str(list_salida))
    f.close()
