def analisislr(expresion):
    ACCION = [
             [("D", 5), "E",      "E",     ("D", 4), "E",      "E"],
             ["E",      ("D",6),  "E",     "E",      "E",      "A"],
             ["E",      ("R",2),  ("D",7), "E",      ("R",2),  ("R",2)],
             ["E",      ("R",4),  ("R",4), "E",      ("R",4),  ("R",4)],
             [("D",5),  "E",      "E",     ("S",4),  "E",      "E"],
             ["E",      ("R",6),  ("R",6), "E",      ("R",6),  ("R",6)],
             [("D",5),  "E",      "E",     ("D",4),  "E",      "E"],
             [("D",5),  "E",      "E",     ("D",4),  "E",      "E"],
             ["E",      ("D",6),  "E",     "E",      ("D",11), "E"],
             ["E",      ("R",1),  ("D",7), "E",      ("R",1),  ("R",1)],
             ["E",      ("R",3),  ("R",3), "E",      ("R",3),  ("R",3)],
             ["E",      ("R",5),  ("R",5), "E",      ("R",5),  ("R",5)]
             ]
    sacarsimbolos = {1:3, 2:1, 3:3, 4:1, 5:3, 6:1}
    producciones  = {1:0, 2:0, 3:1, 4:1, 5:1, 6:2}
    IR_A = [[1,2,3], ["E"], ["E"], ["E"], [8,2,3], ["E"], ["E",9,3], ["E", "E", 10]]
    pila = [0]
    contador = 0
    simbolos = {"+":1, "*":2, "(":3, ")":4, "$":5}

    while True:
        longitudExpresion = len(expresion)-1
        if contador > longitudExpresion: a = "$"
        else: a = expresion[contador]
        x = pila[len(pila) - 1]
        y = 0
        if a in simbolos:
            y = simbolos[a]
        if ACCION[x][y] != "E" and ACCION[x][y] != "A":
            siguenteAccion = ACCION[x][y][0]
            numeroAccion = ACCION[x][y][1]
            if siguenteAccion == "D":
                pila.append(numeroAccion)
                contador += 1
            if siguenteAccion == "R":
                for x in range(sacarsimbolos[numeroAccion]):
                    pila.pop()
                t = pila[len(pila) - 1]
                pila.append(IR_A[t][producciones[numeroAccion]])
        elif ACCION[x][y] == "A":
            print("Aceptar")
            break
        else:
            print("ERROR EN LA ASIGNACIÓN")
            break




if __name__ == '__main__':
    analisislr("a+(b*c)")