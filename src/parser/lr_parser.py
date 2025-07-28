"""
LR Parser for Arithmetic Expressions

This module implements an LR(1) parser for arithmetic expressions.
It validates the syntax of mathematical expressions and performs syntax analysis.
"""

import re
from typing import List, Tuple, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class ParseResult:
    """Result of parsing operation."""
    success: bool
    message: str
    line_number: int


class ArithmeticLRParser:
    """
    LR(1) parser for arithmetic expressions.
    
    Supports:
    - Basic arithmetic operators: +, -, *, /
    - Parentheses for grouping
    - Variables and numeric literals
    """
    
    def __init__(self):
        """Initialize the LR parser with parsing tables."""
        self._setup_parsing_tables()
    
    def _setup_parsing_tables(self):
        """Setup the LR parsing action and goto tables."""
        
        # Action table: [state][symbol] = (action_type, state/production)
        # D = Shift, R = Reduce, A = Accept, E = Error
        self.action_table = [
            [("D", 5), "E", "E", ("D", 4), "E", "E"],      # State 0
            ["E", ("D", 6), "E", "E", "E", "A"],           # State 1
            ["E", ("R", 2), ("D", 7), "E", ("R", 2), ("R", 2)],  # State 2
            ["E", ("R", 4), ("R", 4), "E", ("R", 4), ("R", 4)],  # State 3
            [("D", 5), "E", "E", ("D", 4), "E", "E"],      # State 4
            ["E", ("R", 6), ("R", 6), "E", ("R", 6), ("R", 6)],  # State 5
            [("D", 5), "E", "E", ("D", 4), "E", "E"],      # State 6
            [("D", 5), "E", "E", ("D", 4), "E", "E"],      # State 7
            ["E", ("D", 6), "E", "E", ("D", 11), "E"],     # State 8
            ["E", ("R", 1), ("D", 7), "E", ("R", 1), ("R", 1)],  # State 9
            ["E", ("R", 3), ("R", 3), "E", ("R", 3), ("R", 3)],  # State 10
            ["E", ("R", 5), ("R", 5), "E", ("R", 5), ("R", 5)]   # State 11
        ]
        
        # Goto table: [state][non_terminal]
        self.goto_table = [
            [1, 2, 3],   # State 0
            "E",         # State 1
            "E",         # State 2
            "E",         # State 3
            [8, 2, 3],   # State 4
            "E",         # State 5
            ["E", 9, 3], # State 6
            ["E", "E", 10], # State 7
            "E",         # State 8
            "E",         # State 9
            "E",         # State 10
            "E"          # State 11
        ]
        
        # Production rules: production_number -> number_of_symbols_to_pop
        self.production_symbols = {1: 3, 2: 1, 3: 3, 4: 1, 5: 3, 6: 1}
        
        # Non-terminal mappings for goto table
        self.nonterminal_index = {1: 0, 2: 0, 3: 1, 4: 1, 5: 2, 6: 2}
        
        # Symbol to index mapping
        self.symbol_index = {"+": 1, "*": 2, "(": 3, ")": 4, "$": 5, "0": 0}
    
    def _validate_parentheses(self, expression: str) -> bool:
        """
        Check if parentheses are balanced in the expression.
        
        Args:
            expression: The expression to validate
            
        Returns:
            True if parentheses are balanced
        """
        open_count = len(re.findall(r'\(', expression))
        close_count = len(re.findall(r'\)', expression))
        return open_count == close_count
    
    def _find_undeclared_variables(self, variables: List[str], symbol_table: List[List[str]]) -> List[str]:
        """
        Find variables that are not declared in the symbol table.
        
        Args:
            variables: List of variable names in expression
            symbol_table: Symbol table with declared variables
            
        Returns:
            List of undeclared variables
        """
        undeclared = []
        
        for variable in variables:
            declared = False
            for symbol_entry in symbol_table:
                if variable == symbol_entry[0]:  # symbol_entry[0] is variable name
                    declared = True
                    break
            
            if not declared:
                undeclared.append(variable)
        
        return undeclared
    
    def _preprocess_expression(self, expression: str) -> str:
        """
        Preprocess expression by replacing variables and numbers with '0'.
        
        Args:
            expression: Raw expression
            
        Returns:
            Preprocessed expression with variables replaced by '0'
        """
        # Replace variables (letters + optional digits) with '0'
        processed = re.sub(r'[a-zA-Z]+\d*', '0', expression)
        # Replace numbers with '0'
        processed = re.sub(r'\d+', '0', processed)
        return processed
    
    def parse_expression(self, line_data: Tuple[str, int], symbol_table: List[List[str]]) -> ParseResult:
        """
        Parse an arithmetic expression using LR parsing.
        
        Args:
            line_data: Tuple of (expression_line, line_number)
            symbol_table: Symbol table with variable declarations
            
        Returns:
            ParseResult indicating success/failure and message
        """
        line_content, line_number = line_data
        
        # Extract expression (everything after '=')
        expression = re.sub(r'.*=\s*', '', line_content).replace(" ", "")
        
        # Find all variables in the expression
        variables = re.findall(r'[a-zA-Z]+\d*', expression)
        
        # Check for undeclared variables
        undeclared_vars = self._find_undeclared_variables(variables, symbol_table)
        if undeclared_vars:
            return ParseResult(
                False, 
                f"Error on line {line_number}: {len(undeclared_vars)} undeclared variables: {undeclared_vars}",
                line_number
            )
        
        # Check parentheses balance
        if not self._validate_parentheses(expression):
            return ParseResult(
                False,
                f"Error on line {line_number}: unbalanced parentheses",
                line_number
            )
        
        # Preprocess expression for parsing
        processed_expression = self._preprocess_expression(expression)
        expression_length = len(processed_expression) - 1
        
        # Initialize parsing state
        stack = [0]
        input_pointer = 0
        
        # LR parsing algorithm
        while True:
            # Get current input symbol
            if input_pointer > expression_length:
                current_symbol = "$"
            else:
                current_symbol = processed_expression[input_pointer]
            
            # Get current state
            current_state = stack[-1]
            
            # Get symbol index for action table
            symbol_idx = self.symbol_index.get(current_symbol, 0)  # Default to 0 for variables/numbers
            
            # Get action from action table
            action = self.action_table[current_state][symbol_idx]
            
            if action == "A":
                # Accept - parsing successful
                return ParseResult(
                    True,
                    f"Syntax analysis line {line_number}: Correct",
                    line_number
                )
            
            elif action == "E":
                # Error - parsing failed
                return ParseResult(
                    False,
                    f"Syntax analysis line {line_number}: Incorrect",
                    line_number
                )
            
            else:
                action_type, action_value = action
                
                if action_type == "D":  # Shift
                    stack.append(action_value)
                    input_pointer += 1
                
                elif action_type == "R":  # Reduce
                    production_num = action_value
                    
                    # Pop symbols from stack
                    symbols_to_pop = self.production_symbols[production_num]
                    for _ in range(symbols_to_pop):
                        stack.pop()
                    
                    # Get new state from goto table
                    current_state = stack[-1]
                    nonterminal_idx = self.nonterminal_index[production_num]
                    new_state = self.goto_table[current_state][nonterminal_idx]
                    stack.append(new_state)


class ExpressionValidator:
    """Helper class for validating expressions before parsing."""
    
    @staticmethod
    def has_valid_operators(expression: str) -> bool:
        """Check if expression contains only valid operators."""
        valid_chars = set('0123456789+-*/()abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ')
        return all(char in valid_chars for char in expression)
    
    @staticmethod
    def has_balanced_operators(expression: str) -> bool:
        """Check if operators are properly balanced (not starting/ending with binary operators)."""
        expression = expression.strip()
        if not expression:
            return False
        
        # Should not start or end with binary operators
        binary_ops = {'+', '-', '*', '/'}
        if expression[0] in binary_ops or expression[-1] in binary_ops:
            return False
        
        return True


def parse_arithmetic_expression(line: Tuple[str, int], symbol_table: List[List[str]]) -> ParseResult:
    """
    Convenience function to parse an arithmetic expression.
    
    Args:
        line: Tuple of (expression_line, line_number)
        symbol_table: Symbol table with variable declarations
        
    Returns:
        ParseResult with parsing outcome
    """
    parser = ArithmeticLRParser()
    return parser.parse_expression(line, symbol_table)


if __name__ == "__main__":
    # Example usage
    symbol_table = [
        ['a', 'int', 0, 'id0'], 
        ['z', 'int', 0, 'id1'],
        ['x', 'int', 0, 'id2'], 
        ['q', 'int', 0, 'id3']
    ]
    
    test_expressions = [
        ('int x = 7 + 1', 1),
        ('int y = a * (z + 2)', 2),
        ('int result = (a + b) * c', 3)  # This should fail - 'b' and 'c' undeclared
    ]
    
    parser = ArithmeticLRParser()
    
    for expr_line in test_expressions:
        result = parser.parse_expression(expr_line, symbol_table)
        print(f"Line {result.line_number}: {result.message}") 