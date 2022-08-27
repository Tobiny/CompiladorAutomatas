"""Clase Buffer

CLase que nos permitirá leer cadena por cadena (pueden ser varias)
del archivo eliminando espacios y renglones en blanco
"""
class Buffer:
    def load_buffer(self):
        arq = open('ejemplo.afd', 'r')
        text = arq.readline()

        buffer = []
        cont = 1

        # El tamaño del buffer puede ser cambiado con cont
        while text != "":
            buffer.append(text)
            text = arq.readline()
            cont += 1

            if cont == 10 or text == '':
                # Retorna todo el buffer
                buf = ''.join(buffer)
                cont = 1
                yield buf

                # Resetea el buffer
                buffer = []

        arq.close()