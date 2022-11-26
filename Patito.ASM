extern imprimir:far
extern leer:far
pila segment para stack 'stack'
        DB 500 dup (?)
pila ends
extra segment para public 'data'

extra ends
datos segment para public 'data'
        x DB 10
        y DB 20
        z DB 30
        cad DB 6,?,6 dup(?)
        str1 DB "Mundo", 0
        ;Cadenas a imprimir.
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

        lea si, cad
        call imprimir
        lea si, str1
        call imprimir
        lea dx, y
        call leer
        ;Codigo.


        ret
p0      endp

codigo  ends
        end p0



