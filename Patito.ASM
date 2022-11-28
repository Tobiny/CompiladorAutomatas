pila segment para stack 'stack'
        DB 500 dup (?)
pila ends
extra segment para public 'data'

extra ends
datos segment para public 'data'
        x DW 2
        y DW 10
        nueva DW 0
        z DW 0
        numerolectura db 6,?,6 dup(?)
        t1 DW ?
        str1 DB "Serbia ", "$"
        str2 DB " veces campeao do mundo", "$"
        t2 DW ?
        t3 DW ?
        t4 DW ?
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
        xor dx, dx
        mov ax, y
        mov bx, x
        div bx
        mov t1, ax
        
        xor ax, ax
        mov ax, t1
        mov z, ax

        mov AX, z
        push AX
        call todec
        pop ax

        lea dx, numeroLectura
        mov ah, 0ah
        int 21h
        lea bx, numeroLectura+1
        mov ch, 0
        mov cl, [bx]
        push cx
        cr:
            inc bx
            mov al, [bx]
            cmp al, 30h
            jb fuera
            cmp al, 39h
            ja fuera
            sub [bx], 30h
            loop cr
        pop cx
        dec cx
        mov si, 0ah
        lea bx, numeroLectura+2
        mov al, [bx]
        mov ah, 0
        jcxz tp
        cc:
            mul si
            jo fuera
            inc bx
            mov dl, [bx]
            mov dh, 0
            add ax, dx
        loop cc
        tp:
            jc fuera
            mov z, ax
        fuera:
        mov dl, 10
        mov AH,2
        int 21h

        mov dx, offset str1
        mov ah, 9
        int 21h

        mov AX, z
        push AX
        call todec
        pop ax

        mov dx, offset str2
        mov ah, 9
        int 21h

        xor ax, ax
        xor bx, bx
        mov ax, z
        mov bx, 2
        mul bx
        mov t1, ax
        
        xor ax, ax
        xor bx, bx
        mov ax, 5
        mov bx, 8
        add ax, bx
        mov t2, ax
        
        xor ax, ax
        xor bx, bx
        mov ax, t2
        mov bx, 2
        sub ax, bx
        mov t3, ax
        
        xor ax, ax
        xor bx, bx
        mov ax, t1
        mov bx, t3
        add ax, bx
        mov t4, ax
        
        xor ax, ax
        mov ax, t4
        mov nueva, ax

        mov AX, nueva
        push AX
        call todec
        pop ax

        ;Codigo.


        ret
p0      endp

todec proc near
    ;Metemos a la pila el valor de bp para usarlo como apuntador
		push BP
		mov BP,SP

		;Metemos a la pila los valores de los registros para no modificarlos despues
		push AX
		push BX
		push DX
		push CX

		;Inicializamos los contadores
		mov cx,0
		mov dx,0
		label1:
        ; si ax resulta 0
			cmp ax,0
			je print1

        ;inicializamos bx a 10
        mov bx,10

        ; divimos para cambiarlo a decimal
        div bx

        ;lo ponemos en la pila
        push dx

        ;incrementamos el contador
        inc cx

        ;ponemos dx a 0
        xor dx,dx
        jmp label1
		print1:
			;vemos el contador para ver si es mayor a cero
			cmp cx,0
			je exit

			;lo sacmos de la pila
			pop dx

			;lo convertimos a ASCII sumando 48
			add dx,48

			;imprimimos el caracter
			mov ah,02h
			int 21h

			;decrementamos el contador
			dec cx
			jmp print1
	exit:

		;Sacamos de la pila los valores que introdujimos al principio
		pop CX
		pop DX
		pop BX
		pop AX


		POP BP

    ret
todec endp

codigo  ends
        end p0












