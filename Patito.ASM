pila segment para stack 'stack'
        DB 500 dup (?)
pila ends
extra segment para public 'data'

extra ends
datos segment para public 'data'
        x DB 10
        cad DB 6,?,6 dup(?)
        str1 DB "Hola$"
        str2 DB "Mundo$"

datos ends
codigo  segment para public 'code'
        assume cs:codigo, ds:datos, es:extra, ss:pila
        public p0
p0      proc far
        push ds
        mov ax,0
        push ax
        mov ax, datos
        mov ds, ax
        mov ax, extra
        mov es, ax


        ret
p0      endp

codigo  ends
        end p0
