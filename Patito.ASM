pila segment para stack 'stack'
        DB 500 dup (?)
pila ends
extra segment para public 'data'

extra ends
datos segment para public 'data'
        x DB 10
        y DB 20
        z DB 0
        a DB 0
        pais db 20,?,20 dup(?)
        cad DB "Brasil ", "$"
        str1 DB " veces campeao do Mundo", "$"
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

        xor ax, ax
        xor bx, bx
        mov dx, offset pais
        mov ah, 0ah
        int 21h
        mov dl, 10
        mov AH,2
        int 21h

        xor bx, bx
        mov bl, pais[1]
        mov pais[bx+2], '$'
        mov dx, offset pais + 2
        mov ah, 9
        int 21h

        mov dx, offset str1
        mov ah, 9
        int 21h

        ;Codigo.


        ret
p0      endp

codigo  ends
        end p0



