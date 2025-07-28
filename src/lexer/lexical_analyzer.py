"""
Comprehensive Lexical Analyzer

This module provides comprehensive lexical analysis for the Simple Language Compiler,
including variable declarations, assignments, expressions, and control structures.
It integrates lexical analysis with syntax and semantic validation.
"""

import re
from typing import List, Tuple, Dict, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum


class DataType(Enum):
    """Supported data types in the language."""
    INT = "int"
    BOOLEAN = "boolean"
    STRING = "str"


@dataclass
class SymbolEntry:
    """Represents an entry in the symbol table."""
    name: str
    data_type: DataType
    value: Union[int, bool, str]
    identifier: str
    read_status: str = "NoRead"


@dataclass
class NumberEntry:
    """Represents an entry in the number table."""
    value: int
    identifier: str


@dataclass
class Quadruple:
    """Represents a quadruple in intermediate code."""
    operator: str
    operand1: str
    operand2: str
    result: str


class LexicalAnalyzer:
    """
    Comprehensive lexical analyzer that handles:
    - Variable declarations
    - Assignments 
    - Arithmetic expressions
    - Logical expressions
    - Control structures (if, while)
    - I/O operations (print, read)
    """
    
    def __init__(self):
        """Initialize the lexical analyzer."""
        self.symbol_table: List[SymbolEntry] = []
        self.number_table: List[NumberEntry] = []
        self.quadruples: List[Quadruple] = []
        self.reserved_words = ['main', 'int', 'boolean', 'str', 'read', 'print', 'for', 'if', 'while', 'else']
        self.data_types = ['int', 'str', 'boolean']
        self.syntax_result = 0
        self.logic_result = True
        self.operation_in_comparison = False
        self.error_occurred = False
        self.should_reset = True
        self.last_temp = 't4'
        
        # Compile regex patterns for different statement types
        self._compile_patterns()
    
    def _compile_patterns(self):
        """Compile regex patterns for statement recognition."""
        # Variable declarations
        self.declaration_patterns = [
            re.compile(r'(^str)\s*([a-zA-Z]+[0-9]*)\s*(;$)'),     # String declarations
            re.compile(r'(^int)\s*([a-zA-Z]+[0-9]*)\s*(;$)'),     # Integer declarations  
            re.compile(r'(^boolean)\s*([a-zA-Z]+[0-9]*)\s*(;$)')  # Boolean declarations
        ]
        
        # Declaration with assignment
        self.declare_assign_patterns = [
            re.compile(r'(^str)\s*([a-zA-Z]+[0-9]*)\s*=\s*(\"[^\"]*\")\s*(;$)'),     # String with assignment
            re.compile(r'(^int)\s*([a-zA-Z]+[0-9]*)\s*=\s*([0-9]+)\s*(;$)'),        # Integer with assignment
            re.compile(r'(^boolean)\s*([a-zA-Z]+[0-9]*)\s*=\s*(True|False)\s*(;$)') # Boolean with assignment
        ]
        
        # Declaration with variable assignment
        self.declare_assign_var_patterns = [
            re.compile(r'(^str)\s*([a-zA-Z]+[0-9]*)\s*=\s*([a-zA-Z]+[0-9]*)\s*(;$)'),
            re.compile(r'(^int)\s*([a-zA-Z]+[0-9]*)\s*=\s*([a-zA-Z]+[0-9]*)\s*(;$)'),
            re.compile(r'(^boolean)\s*([a-zA-Z]+[0-9]*)\s*=\s*([a-zA-Z]+[0-9]*)\s*(;$)')
        ]
        
        # Assignment patterns
        self.assignment_patterns = [
            re.compile(r'^([a-zA-Z]+[0-9]*)\s*=\s*(True|False)\s*(;$)'),      # Boolean assignment
            re.compile(r'^([a-zA-Z]+[0-9]*)\s*=\s*([a-zA-Z]+[0-9]*)\s*(;$)'), # Variable assignment
            re.compile(r'^([a-zA-Z]+[0-9]*)\s*=\s*([0-9]+)\s*(;$)'),         # Integer assignment
            re.compile(r'^([a-zA-Z]+[0-9]*)\s*=\s*(\"[^\"]*\")\s*(;$)')      # String assignment
        ]
    
    def is_reserved_word(self, word: str, check_data_types: bool = False) -> bool:
        """
        Check if a word is reserved.
        
        Args:
            word: Word to check
            check_data_types: If True, check only data types
            
        Returns:
            True if word is reserved
        """
        if check_data_types:
            return word in self.data_types
        return word in self.reserved_words
    
    def add_to_symbol_table(self, name: str, data_type: DataType, value: Union[int, bool, str]) -> bool:
        """
        Add a variable to the symbol table.
        
        Args:
            name: Variable name
            data_type: Variable type
            value: Initial value
            
        Returns:
            True if successfully added
        """
        # Check if already declared
        for symbol in self.symbol_table:
            if symbol.name == name:
                return False  # Already declared
        
        # Create new symbol entry
        identifier = f"id{len(self.symbol_table)}"
        symbol = SymbolEntry(name, data_type, value, identifier)
        self.symbol_table.append(symbol)
        return True
    
    def find_symbol(self, name: str) -> Optional[SymbolEntry]:
        """Find a symbol in the symbol table."""
        for symbol in self.symbol_table:
            if symbol.name == name:
                return symbol
        return None
    
    def add_to_number_table(self, numbers: List[str]):
        """Add numbers to the number table."""
        for num_str in numbers:
            num_value = int(num_str)
            
            # Check if already exists
            exists = False
            for entry in self.number_table:
                if entry.value == num_value:
                    exists = True
                    break
            
            if not exists:
                identifier = f"n{len(self.number_table)}"
                self.number_table.append(NumberEntry(num_value, identifier))
    
    def process_variable_declaration(self, line: List[str]) -> bool:
        """Process a variable declaration statement."""
        line_content, line_number = line
        
        # Try each declaration pattern
        for i, pattern in enumerate(self.declaration_patterns):
            match = pattern.match(line_content)
            if match:
                data_type_str = match.group(1)
                var_name = match.group(2)
                
                if self.is_reserved_word(var_name):
                    print(f'Cannot declare variables with reserved words, error on line {line_number}')
                    return False
                
                # Determine data type and default value
                if data_type_str == 'int':
                    data_type = DataType.INT
                    default_value = 0
                elif data_type_str == 'str':
                    data_type = DataType.STRING
                    default_value = ""
                elif data_type_str == 'boolean':
                    data_type = DataType.BOOLEAN
                    default_value = False
                
                # Add to symbol table
                if not self.add_to_symbol_table(var_name, data_type, default_value):
                    print(f'Error, variable already declared, on line {line_number}')
                    return False
                
                return True
        
        return False
    
    def process_declaration_with_assignment(self, line: List[str]) -> bool:
        """Process a variable declaration with immediate assignment."""
        line_content, line_number = line
        
        # Try each declaration with assignment pattern
        for i, pattern in enumerate(self.declare_assign_patterns):
            match = pattern.match(line_content)
            if match:
                data_type_str = match.group(1)
                var_name = match.group(2)
                value_str = match.group(3)
                
                if self.is_reserved_word(var_name) or self.is_reserved_word(value_str):
                    print(f'Cannot declare variables with reserved words, error on line {line_number}')
                    return False
                
                # Parse value based on type
                if data_type_str == 'int':
                    data_type = DataType.INT
                    value = int(value_str)
                elif data_type_str == 'str':
                    data_type = DataType.STRING
                    value = value_str
                elif data_type_str == 'boolean':
                    data_type = DataType.BOOLEAN
                    value = value_str == "True"
                
                # Add to symbol table
                if not self.add_to_symbol_table(var_name, data_type, value):
                    print(f'Error, variable already declared, on line {line_number}')
                    return False
                
                return True
        
        return False
    
    def process_assignment(self, line: List[str], assignment_type: int, iteration: int) -> bool:
        """Process a variable assignment statement."""
        line_content, line_number = line
        
        # This is a simplified version - full implementation would handle all assignment types
        # and integrate with the code generation system
        
        pattern = self.assignment_patterns[assignment_type]
        match = pattern.match(line_content)
        if not match:
            return False
        
        var_name = match.group(1)
        value_str = match.group(2)
        
        # Find variable in symbol table
        symbol = self.find_symbol(var_name)
        if not symbol:
            print(f'Error, variable not declared, on line {line_number}')
            return False
        
        # Type checking and assignment based on assignment_type
        if assignment_type == 0:  # Boolean assignment
            if symbol.data_type != DataType.BOOLEAN:
                print(f'Error, trying to assign boolean to non-boolean variable on line {line_number}')
                return False
            symbol.value = value_str == "True"
        
        elif assignment_type == 1:  # Variable assignment
            source_symbol = self.find_symbol(value_str)
            if not source_symbol:
                print(f'Error, source variable not declared on line {line_number}')
                return False
            if symbol.data_type != source_symbol.data_type:
                print(f'Error, type mismatch in assignment on line {line_number}')
                return False
            symbol.value = source_symbol.value
        
        elif assignment_type == 2:  # Integer assignment
            if symbol.data_type != DataType.INT:
                print(f'Error, trying to assign integer to non-integer variable on line {line_number}')
                return False
            symbol.value = int(value_str)
        
        elif assignment_type == 3:  # String assignment
            if symbol.data_type != DataType.STRING:
                print(f'Error, trying to assign string to non-string variable on line {line_number}')
                return False
            symbol.value = value_str
        
        return True
    
    def process_arithmetic_expression(self, line: List[str], iteration: int) -> bool:
        """Process arithmetic expressions with LR parsing."""
        # This would integrate with the LR parser from lr_parser.py
        # For now, returning True as placeholder
        line_content, line_number = line
        
        # Extract expression part
        expression = re.sub(r'.*=\s*', '', line_content).replace(" ", "")
        variables = re.findall(r'[a-zA-Z]+\d*', expression)
        numbers = re.findall(r'\b\d+\b', expression)
        
        # Add numbers to number table
        self.add_to_number_table(numbers)
        
        # Validate variables are declared
        for var in variables:
            if not self.find_symbol(var):
                print(f'Error, variable {var} not declared, on line {line_number}')
                return False
        
        # Check parentheses balance
        if expression.count('(') != expression.count(')'):
            print(f'Error, unbalanced parentheses on line {line_number}')
            return False
        
        print(f'Syntax analysis line {line_number}: Correct')
        return True
    
    def process_control_structure(self, line: List[str], iteration: int) -> bool:
        """Process if and while statements."""
        line_content, line_number = line
        
        # Extract condition
        if line_content.startswith('if('):
            condition = re.sub(r'^if\(', '', line_content)
        elif line_content.startswith('while('):
            condition = re.sub(r'^while\(', '', line_content)
        else:
            return False
        
        condition = re.sub(r'\){.*', '', condition)
        
        if condition in ['True', 'False']:
            print(f'Logic analysis line {line_number}: Correct')
            print(f'Comparison {condition}')
            return True
        
        # Process condition (simplified)
        variables = re.findall(r'[a-zA-Z]+\d*', condition)
        for var in variables:
            if not self.find_symbol(var):
                print(f'Error, variable {var} not declared in condition, on line {line_number}')
                return False
        
        print(f'Logic analysis line {line_number}: Correct')
        return True
    
    def process_print_statement(self, line: List[str], iteration: int) -> bool:
        """Process print statements."""
        line_content, line_number = line
        
        # Extract print content
        content = re.sub(r'^print\(', '', line_content)
        content = re.sub(r'\);\s*$', '', content)
        
        # Find variables in print statement
        variables = re.findall(r'[a-zA-Z]+[0-9]*', content)
        
        # Validate all variables are declared
        for var in variables:
            if not self.find_symbol(var):
                print(f'Error on line {line_number}, variable {var} not declared')
                return False
        
        return True
    
    def process_read_statement(self, line: List[str], iteration: int) -> bool:
        """Process read statements."""
        line_content, line_number = line
        
        # Extract variable name
        var_name = re.sub(r'^read\(', '', line_content)
        var_name = re.sub(r'\);\s*$', '', var_name)
        
        # Validate variable exists
        symbol = self.find_symbol(var_name)
        if not symbol:
            print(f'Error on line {line_number}, variable {var_name} not declared')
            return False
        
        # Mark as requiring input
        symbol.read_status = 'SiRead'
        return True
    
    def analyze_line(self, line: List[str], iteration: int) -> bool:
        """
        Analyze a single line of code.
        
        Args:
            line: [line_content, line_number]
            iteration: Compilation pass number
            
        Returns:
            True if line analyzed successfully
        """
        if iteration == 1 and self.should_reset:
            self.symbol_table.clear()
            self.number_table.clear()
            self.quadruples.clear()
            self.should_reset = False
        
        if not self.logic_result:
            if re.match(r'.*}', line[0]):
                self.logic_result = True
            return True
        
        line_content = line[0]
        
        # Try variable declaration
        if self.process_variable_declaration(line):
            return True
        
        # Try declaration with assignment  
        if self.process_declaration_with_assignment(line):
            return True
        
        # Try assignments
        for i, pattern in enumerate(self.assignment_patterns):
            if pattern.match(line_content):
                return self.process_assignment(line, i, iteration)
        
        # Try arithmetic expressions
        if re.match(r'^(int)\s+([a-zA-Z]+[0-9]*)\s*=.*([+|\-|*|\/|\(|\)])+.*(;)', line_content):
            return self.process_arithmetic_expression(line, iteration)
        
        if re.match(r'^([a-zA-Z]+[0-9]*)\s*=.*([+|\-|*|\/|\(|\)])+.*(;)', line_content):
            return self.process_arithmetic_expression(line, iteration)
        
        # Try control structures
        if re.match(r'^if\(.*\){$|^if\(.*\){', line_content) or re.match(r'^while\(.*\){$|^while\(.*\){', line_content):
            return self.process_control_structure(line, iteration)
        
        # Try print statements
        if re.match(r'^print\([a-zA-Z0-9\+\s"]*\);', line_content):
            return self.process_print_statement(line, iteration)
        
        # Try read statements
        if re.match(r'^read\([a-zA-Z]+[0-9]*\);', line_content):
            return self.process_read_statement(line, iteration)
        
        # Try closing brace
        if re.match(r'}', line_content):
            return True
        
        # If nothing matches, it's a syntax error
        print(f"Error, check line {line[1]} as there is a syntax error in declaration or assignment")
        return False
    
    def get_symbol_table(self) -> List[SymbolEntry]:
        """Get the current symbol table."""
        return self.symbol_table
    
    def get_number_table(self) -> List[NumberEntry]:
        """Get the current number table."""
        return self.number_table
    
    def get_quadruples(self) -> List[Quadruple]:
        """Get the generated quadruples."""
        return self.quadruples
    
    def reset(self):
        """Reset the analyzer state."""
        self.symbol_table.clear()
        self.number_table.clear()
        self.quadruples.clear()
        self.syntax_result = 0
        self.logic_result = True
        self.operation_in_comparison = False
        self.error_occurred = False
        self.should_reset = True


def analyze_source_lines(lines: List[List[str]], iteration: int = 0) -> Tuple[bool, LexicalAnalyzer]:
    """
    Convenience function to analyze multiple lines.
    
    Args:
        lines: List of [line_content, line_number] pairs
        iteration: Compilation pass number
        
    Returns:
        Tuple of (success, analyzer_instance)
    """
    analyzer = LexicalAnalyzer()
    success = True
    
    for line in lines:
        if not analyzer.analyze_line(line, iteration):
            success = False
    
    return success, analyzer


if __name__ == "__main__":
    # Example usage
    test_lines = [
        ['int x = 42;', 1],
        ['boolean flag = True;', 2], 
        ['str message = "Hello World";', 3],
        ['print(message + " " + x);', 4]
    ]
    
    success, analyzer = analyze_source_lines(test_lines, 0)
    
    if success:
        print("Analysis completed successfully!")
        print(f"Symbol table: {len(analyzer.get_symbol_table())} entries")
        for symbol in analyzer.get_symbol_table():
            print(f"  {symbol.name}: {symbol.data_type.value} = {symbol.value}")
    else:
        print("Analysis failed!") 