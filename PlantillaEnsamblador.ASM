pila segment para stack 'stack'
        DB 500 dup (?)
pila ends
extra segment para public 'data'

extra ends
datos segment para public 'data'
        numerolectura db 6,?,6 dup(?)
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
