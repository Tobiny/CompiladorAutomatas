#!/usr/bin/env python3
"""
Simple Language Compiler - Convenience Script

This script provides a convenient way to run the compiler from the project root.
It automatically handles path resolution and provides better error messages.
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

from src.compiler import main

if __name__ == "__main__":
    # Update help message for project root usage
    if len(sys.argv) != 2:
        print("Simple Language Compiler")
        print("========================")
        print()
        print("Usage: python compile.py <source_file.dl>")
        print()
        print("Examples:")
        print("   python compile.py examples/basic_program.dl")
        print("   python compile.py examples/arithmetic.dl") 
        print("   python compile.py examples/control_flow.dl")
        print()
        print("The compiler will generate:")
        print("   - <filename>.dld  (preprocessed source)")
        print("   - <filename>_tokens.csv  (lexical analysis)")
        print("   - <filename>.asm  (assembly output)")
        sys.exit(1)
    
    # Verify file exists
    source_file = sys.argv[1]
    if not os.path.exists(source_file):
        print(f"❌ Error: Source file '{source_file}' not found")
        sys.exit(1)
    
    # Run the compiler
    main() 