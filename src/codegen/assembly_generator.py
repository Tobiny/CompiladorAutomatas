"""
Assembly Code Generator

This module generates x86 assembly code from intermediate representations
(quadruples) and symbol tables produced by the lexical/semantic analyzer.
"""

import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class AssemblyVariable:
    """Represents a variable in the assembly data segment."""
    name: str
    data_type: str
    value: Any
    size: str = "DW"  # Default to word size


class AssemblyGenerator:
    """
    Generates x86 assembly code from compiler intermediate representation.
    
    Features:
    - Variable declarations in data segment
    - Arithmetic operations
    - I/O operations (print, read)
    - String literal handling
    - Temporary variable management
    """
    
    def __init__(self, template_file: str = "src/codegen/templates/assembly_template.asm"):
        """
        Initialize the assembly generator.
        
        Args:
            template_file: Path to the assembly template file
        """
        self.template_file = template_file
        self.string_counter = 0
        self.temp_variables = []
        self.string_literals = []
        self.variables = []
        
    def generate_program(self, output_file: str, symbol_table: List[Any], 
                        quadruples: List[Any] = None, number_table: List[Any] = None) -> bool:
        """
        Generate complete assembly program.
        
        Args:
            output_file: Output assembly file name
            symbol_table: Symbol table from lexical analyzer
            quadruples: Quadruples from intermediate code generation
            number_table: Number table for constants
            
        Returns:
            True if generation successful
        """
        try:
            # Read template
            template_content = self._read_template()
            if not template_content:
                return False
            
            # Generate assembly sections
            data_section = self._generate_data_section(symbol_table)
            code_section = self._generate_code_section(quadruples or [])
            
            # Combine template with generated code
            assembly_code = self._combine_template(template_content, data_section, code_section)
            
            # Write output file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(assembly_code)
            
            print(f"Assembly code generated successfully: {output_file}")
            return True
            
        except Exception as e:
            print(f"Error generating assembly: {e}")
            return False
    
    def _read_template(self) -> Optional[str]:
        """Read the assembly template file."""
        try:
            if os.path.exists(self.template_file):
                with open(self.template_file, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                # Use built-in template if file not found
                return self._get_builtin_template()
        except Exception as e:
            print(f"Error reading template: {e}")
            return None
    
    def _get_builtin_template(self) -> str:
        """Get built-in assembly template."""
        return """pila segment para stack 'stack'
        DB 500 dup (?)
pila ends

extra segment para public 'data'
extra ends

datos segment para public 'data'
        numeroLectura db 6,?,6 dup(?)
        ; Variables will be inserted here
        ; String literals will be inserted here
datos ends

codigo segment para public 'code'
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

        ; Generated code will be inserted here

        ret
p0      endp

; Utility procedure to convert and print decimal numbers
todec proc near
        push BP
        mov BP,SP
        push AX
        push BX
        push DX
        push CX

        mov cx,0
        mov dx,0
        
label1:
        cmp ax,0
        je print1
        mov bx,10
        div bx
        push dx
        inc cx
        xor dx,dx
        jmp label1

print1:
        cmp cx,0
        je exit
        pop dx
        add dx,48
        mov ah,02h
        int 21h
        dec cx
        jmp print1

exit:
        pop CX
        pop DX
        pop BX
        pop AX
        pop BP
        ret
todec endp

codigo ends
        end p0
"""
    
    def _generate_data_section(self, symbol_table: List[Any]) -> str:
        """
        Generate the data segment with variable declarations.
        
        Args:
            symbol_table: List of symbol table entries
            
        Returns:
            Data section assembly code
        """
        data_lines = []
        
        # Process symbol table entries
        for symbol in symbol_table:
            if hasattr(symbol, 'name') and hasattr(symbol, 'data_type'):
                # Modern symbol entry (SymbolEntry dataclass)
                name = symbol.name
                data_type = symbol.data_type.value if hasattr(symbol.data_type, 'value') else symbol.data_type
                value = symbol.value
            else:
                # Legacy symbol entry (list format)
                name = symbol[0]
                data_type = symbol[1]
                value = symbol[2]
            
            if data_type == "int":
                data_lines.append(f"        {name} DW {int(value)}")
            elif data_type == "str":
                if value and len(str(value)) > 0:
                    # Remove quotes if present
                    clean_value = str(value).strip('"')
                    data_lines.append(f'        {name} DB "{clean_value}", "$"')
                else:
                    # Empty string
                    data_lines.append(f"        {name} db 20,?,20 dup(?)")
            elif data_type == "boolean":
                int_value = 1 if value else 0
                data_lines.append(f"        {name} DW {int_value}")
        
        # Add temporary variables
        for temp_var in self.temp_variables:
            data_lines.append(f"        {temp_var} DW ?")
        
        # Add string literals
        for i, literal in enumerate(self.string_literals, 1):
            data_lines.append(f'        str{i} DB "{literal}", "$"')
        
        return '\n'.join(data_lines)
    
    def _generate_code_section(self, quadruples: List[Any]) -> str:
        """
        Generate the code segment from quadruples.
        
        Args:
            quadruples: List of quadruple intermediate code
            
        Returns:
            Code section assembly code
        """
        code_lines = []
        
        for quad in quadruples:
            if hasattr(quad, 'operator'):
                # Modern quadruple (Quadruple dataclass)
                operator = quad.operator
                operand1 = quad.operand1
                operand2 = quad.operand2
                result = quad.result
            else:
                # Legacy quadruple (list format)
                operator = quad[0]
                operand1 = quad[1] if len(quad) > 1 else ""
                operand2 = quad[2] if len(quad) > 2 else ""
                result = quad[3] if len(quad) > 3 else ""
            
            # Generate assembly for each operation
            if operator == '+':
                code_lines.extend(self._generate_arithmetic('+', operand1, operand2, result))
            elif operator == '-':
                code_lines.extend(self._generate_arithmetic('-', operand1, operand2, result))
            elif operator == '*':
                code_lines.extend(self._generate_arithmetic('*', operand1, operand2, result))
            elif operator == '/':
                code_lines.extend(self._generate_arithmetic('/', operand1, operand2, result))
            elif operator == '=':
                code_lines.extend(self._generate_assignment(operand1, result))
        
        return '\n'.join(code_lines)
    
    def _generate_arithmetic(self, operator: str, op1: str, op2: str, result: str) -> List[str]:
        """Generate assembly for arithmetic operations."""
        lines = [
            '        xor ax, ax',
            '        xor bx, bx',
            f'        mov ax, {op1}',
            f'        mov bx, {op2}'
        ]
        
        if operator == '+':
            lines.append('        add ax, bx')
        elif operator == '-':
            lines.append('        sub ax, bx')
        elif operator == '*':
            lines.append('        mul bx')
        elif operator == '/':
            lines.extend([
                '        xor dx, dx',
                '        div bx'
            ])
        
        lines.append(f'        mov {result}, ax')
        lines.append('')  # Empty line for readability
        
        # Add temporary variable if needed
        if result.startswith('t') and result not in self.temp_variables:
            self.temp_variables.append(result)
        
        return lines
    
    def _generate_assignment(self, source: str, destination: str) -> List[str]:
        """Generate assembly for assignments."""
        return [
            '        xor ax, ax',
            f'        mov ax, {source}',
            f'        mov {destination}, ax',
            ''
        ]
    
    def generate_print_code(self, strings: List[str], elements: List[str], symbol_table: List[Any]) -> str:
        """
        Generate assembly code for print operations.
        
        Args:
            strings: String literals to print
            elements: All elements in print statement
            symbol_table: Symbol table for variable lookup
            
        Returns:
            Assembly code for print operation
        """
        code_lines = []
        string_stack = []
        string_counter = 0
        
        # Register string literals
        for string_literal in strings:
            string_counter += 1
            string_stack.append(string_counter)
            self.string_literals.append(string_literal)
        
        # Generate print code for each element
        stack_index = 0
        for element in elements:
            is_string_literal = False
            
            # Check if element is a string literal
            for string_literal in strings:
                if element == string_literal:
                    code_lines.extend([
                        f'        mov dx, offset str{string_stack[stack_index]}',
                        '        mov ah, 9',
                        '        int 21h',
                        ''
                    ])
                    is_string_literal = True
                    stack_index += 1
                    break
            
            if not is_string_literal:
                # Element is a variable
                symbol = self._find_symbol_in_table(element, symbol_table)
                if symbol:
                    symbol_type = symbol[1] if len(symbol) > 1 else "int"
                    
                    if symbol_type == "int":
                        code_lines.extend([
                            f"        mov AX, {element}",
                            "        push AX",
                            "        call todec",
                            "        pop ax",
                            ''
                        ])
                    elif symbol_type == "str":
                        code_lines.extend([
                            f'        mov dx, offset {element}',
                            '        mov ah, 9',
                            '        int 21h',
                            ''
                        ])
        
        return '\n'.join(code_lines)
    
    def generate_read_code(self, variable: str, symbol_table: List[Any]) -> str:
        """
        Generate assembly code for read operations.
        
        Args:
            variable: Variable to read into
            symbol_table: Symbol table for type lookup
            
        Returns:
            Assembly code for read operation
        """
        symbol = self._find_symbol_in_table(variable, symbol_table)
        if not symbol:
            return ""
        
        symbol_type = symbol[1] if len(symbol) > 1 else "int"
        
        if symbol_type == 'str':
            return f"""        xor ax, ax
        xor bx, bx
        mov dx, offset {variable}
        mov ah, 0ah
        int 21h
        mov dl, 10
        mov AH,2
        int 21h
        
"""
        elif symbol_type == 'int':
            return f"""        lea dx, numeroLectura
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
            mov {variable}, ax
        fuera:
        mov dl, 10
        mov AH,2
        int 21h
        
"""
        return ""
    
    def _find_symbol_in_table(self, name: str, symbol_table: List[Any]) -> Optional[Any]:
        """Find a symbol in the symbol table."""
        for symbol in symbol_table:
            if hasattr(symbol, 'name'):
                if symbol.name == name:
                    return [symbol.name, symbol.data_type.value if hasattr(symbol.data_type, 'value') else symbol.data_type, symbol.value]
            elif len(symbol) > 0 and symbol[0] == name:
                return symbol
        return None
    
    def _combine_template(self, template: str, data_section: str, code_section: str) -> str:
        """Combine template with generated sections."""
        # Replace placeholder comments with actual code
        result = template
        
        # Insert data section
        if "; Variables will be inserted here" in result:
            result = result.replace("; Variables will be inserted here", data_section)
        elif "        ; String literals will be inserted here" in result:
            result = result.replace("        ; String literals will be inserted here", data_section)
        
        # Insert code section
        if "; Generated code will be inserted here" in result:
            result = result.replace("; Generated code will be inserted here", code_section)
        
        return result


def generate_assembly(output_file: str, symbol_table: List[Any], 
                     quadruples: List[Any] = None, number_table: List[Any] = None) -> bool:
    """
    Convenience function to generate assembly code.
    
    Args:
        output_file: Output assembly file name
        symbol_table: Symbol table from analyzer
        quadruples: Intermediate code quadruples
        number_table: Number constants table
        
    Returns:
        True if successful
    """
    generator = AssemblyGenerator()
    return generator.generate_program(output_file, symbol_table, quadruples, number_table)


if __name__ == "__main__":
    # Example usage
    mock_symbol_table = [
        ['x', 'int', 42, 'id0', 'NoRead'],
        ['message', 'str', 'Hello World', 'id1', 'NoRead']
    ]
    
    mock_quadruples = [
        ['+', 'x', '10', 't1'],
        ['=', 't1', '', 'result']
    ]
    
    success = generate_assembly('test_output.asm', mock_symbol_table, mock_quadruples)
    if success:
        print("Assembly generation completed!")
    else:
        print("Assembly generation failed!") 