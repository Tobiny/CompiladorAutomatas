pila segment para stack 'stack'
        DB 500 dup (?)
pila ends
extra segment para public 'data'

extra ends
datos segment para public 'data'
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

        ;Codigo.


        ret
p0      endp

codigo  ends
        end p0
