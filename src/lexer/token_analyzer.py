"""
Token Analyzer

This module provides lexical analysis capabilities, converting source code
into a stream of tokens for further processing by the parser.
"""

import re
from typing import List, Tuple, NamedTuple
from enum import Enum


class TokenType(Enum):
    """Enumeration of all token types in the language."""
    # Keywords
    MAIN = "MAIN"
    INT = "INT"
    BOOLEAN = "BOOLEAN"
    STRING = "STRING"
    IF = "IF"
    ELSE = "ELSE"
    WHILE = "WHILE"
    READ = "READ"
    PRINT = "PRINT"
    TRUE = "TRUE"
    FALSE = "FALSE"
    
    # Identifiers and literals
    IDENTIFIER = "IDENTIFIER"
    INTEGER_LITERAL = "INTEGER_LITERAL"
    STRING_LITERAL = "STRING_LITERAL"
    
    # Operators
    ASSIGN = "ASSIGN"              # =
    EQUAL = "EQUAL"                # ==
    NOT_EQUAL = "NOT_EQUAL"        # !=
    LESS_THAN = "LESS_THAN"        # <
    LESS_EQUAL = "LESS_EQUAL"      # <=
    GREATER_THAN = "GREATER_THAN"  # >
    GREATER_EQUAL = "GREATER_EQUAL"# >=
    LOGICAL_AND = "LOGICAL_AND"    # &&
    LOGICAL_OR = "LOGICAL_OR"      # ||
    LOGICAL_NOT = "LOGICAL_NOT"    # !
    PLUS = "PLUS"                  # +
    MINUS = "MINUS"                # -
    MULTIPLY = "MULTIPLY"          # *
    DIVIDE = "DIVIDE"              # /
    
    # Delimiters
    LEFT_PAREN = "LEFT_PAREN"      # (
    RIGHT_PAREN = "RIGHT_PAREN"    # )
    LEFT_BRACE = "LEFT_BRACE"      # {
    RIGHT_BRACE = "RIGHT_BRACE"    # }
    SEMICOLON = "SEMICOLON"        # ;
    COMMA = "COMMA"                # ,
    
    # Special tokens
    NEWLINE = "NEWLINE"
    WHITESPACE = "WHITESPACE"
    UNKNOWN = "UNKNOWN"
    EOF = "EOF"


class Token(NamedTuple):
    """Represents a single token."""
    type: TokenType
    lexeme: str
    line: int
    column: int


class TokenAnalyzer:
    """
    Lexical analyzer that converts source code into tokens.
    """
    
    def __init__(self):
        """Initialize the token analyzer."""
        self.line_number = 1
        self.column_offset = 0
        
        # Token patterns (order matters for precedence)
        self.token_patterns = [
            # Keywords (must come before IDENTIFIER)
            (TokenType.MAIN, r'\bmain\b'),
            (TokenType.INT, r'\bint\b'),
            (TokenType.BOOLEAN, r'\bboolean\b'),
            (TokenType.STRING, r'\bstr\b'),
            (TokenType.IF, r'\bif\b'),
            (TokenType.ELSE, r'\belse\b'),
            (TokenType.WHILE, r'\bwhile\b'),
            (TokenType.READ, r'\bread\b'),
            (TokenType.PRINT, r'\bprint\b'),
            (TokenType.TRUE, r'\bTrue\b'),
            (TokenType.FALSE, r'\bFalse\b'),
            
            # Multi-character operators (must come before single-character)
            (TokenType.EQUAL, r'=='),
            (TokenType.NOT_EQUAL, r'!='),
            (TokenType.LESS_EQUAL, r'<='),
            (TokenType.GREATER_EQUAL, r'>='),
            (TokenType.LOGICAL_AND, r'&&'),
            (TokenType.LOGICAL_OR, r'\|\|'),
            
            # Single-character operators
            (TokenType.ASSIGN, r'='),
            (TokenType.LESS_THAN, r'<'),
            (TokenType.GREATER_THAN, r'>'),
            (TokenType.LOGICAL_NOT, r'!'),
            (TokenType.PLUS, r'\+'),
            (TokenType.MINUS, r'-'),
            (TokenType.MULTIPLY, r'\*'),
            (TokenType.DIVIDE, r'/'),
            
            # Delimiters
            (TokenType.LEFT_PAREN, r'\('),
            (TokenType.RIGHT_PAREN, r'\)'),
            (TokenType.LEFT_BRACE, r'\{'),
            (TokenType.RIGHT_BRACE, r'\}'),
            (TokenType.SEMICOLON, r';'),
            (TokenType.COMMA, r','),
            
            # Literals
            (TokenType.STRING_LITERAL, r'"[^"]*"'),
            (TokenType.INTEGER_LITERAL, r'\b\d+\b'),
            (TokenType.IDENTIFIER, r'\b[a-zA-Z][a-zA-Z0-9]*\b'),
            
            # Whitespace and newlines
            (TokenType.NEWLINE, r'\n'),
            (TokenType.WHITESPACE, r'[ \t]+'),
        ]
        
        # Compile all patterns into a single regex
        self.compiled_pattern = self._compile_patterns()
    
    def _compile_patterns(self) -> re.Pattern:
        """Compile all token patterns into a single regex."""
        pattern_groups = []
        for token_type, pattern in self.token_patterns:
            pattern_groups.append(f'(?P<{token_type.value}>{pattern})')
        
        combined_pattern = '|'.join(pattern_groups)
        return re.compile(combined_pattern)
    
    def tokenize(self, source_code: str) -> List[Token]:
        """
        Convert source code into a list of tokens.
        
        Args:
            source_code: The source code to tokenize
            
        Returns:
            List of Token objects
            
        Raises:
            SyntaxError: If an invalid character is encountered
        """
        tokens = []
        line_start = 0
        
        for match in self.compiled_pattern.finditer(source_code):
            token_type_name = match.lastgroup
            token_lexeme = match.group()
            
            # Convert string back to TokenType enum
            token_type = TokenType(token_type_name)
            
            # Calculate position
            column = match.start() - line_start
            
            # Handle newlines
            if token_type == TokenType.NEWLINE:
                line_start = match.end()
                self.line_number += 1
                continue  # Skip newlines in token stream
            
            # Skip whitespace tokens
            if token_type == TokenType.WHITESPACE:
                continue
            
            # Create token
            token = Token(token_type, token_lexeme, self.line_number, column)
            tokens.append(token)
        
        # Add EOF token
        tokens.append(Token(TokenType.EOF, "", self.line_number, 0))
        
        return tokens
    
    def tokenize_with_output(self, source_code: str, output_file: str = None) -> List[Token]:
        """
        Tokenize source code and optionally write results to file.
        
        Args:
            source_code: Source code to tokenize
            output_file: Optional output file for token results
            
        Returns:
            List of tokens
        """
        tokens = self.tokenize(source_code)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('TYPE,LEXEME,LINE,COLUMN\n')
                for token in tokens:
                    if token.type != TokenType.EOF:
                        f.write(f'{token.type.value},{token.lexeme},{token.line},{token.column}\n')
        
        return tokens
    
    def reset(self):
        """Reset the analyzer state for processing a new file."""
        self.line_number = 1
        self.column_offset = 0


def analyze_tokens(source_code: str, output_file: str = None) -> List[Token]:
    """
    Convenience function to tokenize source code.
    
    Args:
        source_code: Source code to analyze
        output_file: Optional output file
        
    Returns:
        List of tokens
    """
    analyzer = TokenAnalyzer()
    return analyzer.tokenize_with_output(source_code, output_file)


if __name__ == "__main__":
    # Example usage
    test_code = '''
    int x = 42;
    boolean flag = True;
    str message = "Hello World";
    
    if (x > 10) {
        print("x is greater than 10");
    }
    '''
    
    analyzer = TokenAnalyzer()
    tokens = analyzer.tokenize(test_code)
    
    for token in tokens:
        print(f"Token: {token.type.value:15} | Lexeme: '{token.lexeme:10}' | Line: {token.line} | Column: {token.column}") 