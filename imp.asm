;---------------------
;Mover la direccion de la cadena en un registro
;Guardar el registro en la pila
;Invocar al procedimiento
;Sumar 2 a SP para regresar al tope de la pila
;---------------------
public imprimir
codigo segment para public 'code'
imprimir proc far
    ;guardamos el valor + 6 del parametro de entrada
    push bp
    mov bp, sp
    ;Guardamos los registros en la pila para mantener el valor
    push bx
    push ax
    ;movemos a dx la direccion de la cadena
    mov dx, [bp+6]
    mov ah, 9            
	int 21h    
    ;Sacamos los valores guardados
    pop ax
    pop bx
    pop bp
    ret
imprimir endp
codigo ends
end