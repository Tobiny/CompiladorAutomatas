"""
Simple Language Compiler

A complete compiler implementation for the Duck Language, featuring:
- Lexical analysis with comprehensive tokenization
- LR parsing for arithmetic expressions
- Semantic analysis with type checking
- x86 assembly code generation

Author: Fernando (Portfolio Project)
"""

__version__ = "1.0.0"
__author__ = "Fernando"

from .compiler import SimpleCompiler

__all__ = ['SimpleCompiler'] 