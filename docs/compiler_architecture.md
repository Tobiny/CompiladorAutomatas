# Compiler Architecture

## Overview

The Simple Language Compiler is implemented as a multi-phase compiler that transforms Duck Language source code into x86 assembly code. The compiler follows traditional compiler design principles with clearly separated phases.

## Compilation Pipeline

```
Source Code (.dl)
       ↓
   Preprocessor
       ↓
 Preprocessed Code (.dld)
       ↓
  Lexical Analyzer
       ↓
    Token Stream
       ↓
   Syntax Analyzer
       ↓
    Parse Tree
       ↓
  Semantic Analyzer
       ↓
 Intermediate Code (Quadruples)
       ↓
  Code Generator
       ↓
 Assembly Code (.asm)
```

## Phase 1: Preprocessing

**Location**: `src/utils/preprocessor.py`

The preprocessor prepares the source code for compilation by:

- **Comment Removal**: Strips single-line (`#`) and multi-line (`/* */`) comments while preserving string literals
- **Whitespace Normalization**: Removes extra whitespace and normalizes line spacing
- **Line Numbering**: Adds line numbers for error reporting
- **Bracket Validation**: Ensures braces `{}` are properly balanced
- **Empty Line Removal**: Eliminates blank lines to reduce processing overhead

**Key Features**:
- Uses regex patterns to distinguish between comments and string content
- Maintains a bracket stack for balance validation
- Preserves source line numbers for debugging

## Phase 2: Lexical Analysis

**Location**: `src/lexer/`

Two implementations are provided:

### Primary Lexical Analyzer (`lexical_analyzer.py`)
- Comprehensive lexical analysis with integrated syntax and semantic analysis
- Handles variable declarations, assignments, and control structures
- Manages symbol table and performs type checking
- Generates intermediate code (quadruples)

### Token Analyzer (`token_analyzer.py`) 
- Pure lexical analyzer that generates token streams
- Uses enum-based token types for type safety
- Implements regex-based pattern matching
- Suitable for traditional compiler pipelines

**Token Types Supported**:
- Keywords: `int`, `boolean`, `str`, `if`, `while`, `print`, `read`
- Operators: `+`, `-`, `*`, `/`, `==`, `!=`, `<`, `>`, `&&`, `||`, `!`
- Delimiters: `(`, `)`, `{`, `}`, `;`, `,`
- Literals: integers, booleans, strings
- Identifiers: variable names

## Phase 3: Syntax Analysis

**Location**: `src/parser/`

### LR Parser (`lr_parser.py`)
Implements LR(1) parsing for arithmetic expressions with:
- **Action Table**: Defines shift/reduce actions for each state-symbol combination
- **Goto Table**: Handles non-terminal transitions
- **Production Rules**: Defines the grammar for expression parsing
- **Error Recovery**: Provides meaningful error messages for syntax errors

**Grammar Supported**:
```
E → E + T | E - T | T
T → T * F | T / F | F  
F → (E) | id | num
```

### Integrated Syntax Analyzer
Part of the main lexical analyzer, handles:
- Variable declarations with type checking
- Assignment statements with expression validation
- Control structures (`if`, `while`) with condition parsing
- I/O statements (`print`, `read`) with parameter validation

## Phase 4: Semantic Analysis

**Capabilities**:
- **Symbol Table Management**: Tracks variable declarations and types
- **Type Checking**: Ensures type compatibility in assignments and expressions
- **Variable Declaration Validation**: Prevents duplicate declarations
- **Usage Validation**: Ensures variables are declared before use
- **Scope Management**: Currently supports global scope only

**Symbol Table Structure**:
```
[variable_name, type, value, identifier, read_status]
```

**Type System**:
- `int`: 16-bit signed integers
- `boolean`: True/False values  
- `str`: String literals

## Phase 5: Intermediate Code Generation

**Format**: Quadruples (3-address code)

**Quadruple Structure**:
```
[operator, operand1, operand2, result]
```

**Supported Operations**:
- Arithmetic: `+`, `-`, `*`, `/`
- Logical: `&&`, `||`, `!`, `==`, `!=`, `<`, `>`
- Assignment: Direct value assignment
- I/O: `print`, `read` operations

**Example**:
```duck
int x = (a + b) * c;
```
Generates:
```
[+, a, b, t1]
[*, t1, c, t2] 
[=, t2, _, x]
```

## Phase 6: Code Generation

**Location**: `src/codegen/assembly_generator.py`

Transforms quadruples into x86 assembly code targeting 16-bit architecture.

**Features**:
- **Register Management**: Uses AX, BX, DX registers efficiently
- **Memory Management**: Allocates data segment variables
- **Template System**: Uses assembly code templates for consistency
- **I/O Handling**: Implements print and read operations using DOS interrupts

**Assembly Code Structure**:
```assembly
; Stack segment
pila segment para stack 'stack'
    DB 500 dup (?)
pila ends

; Data segment  
datos segment para public 'data'
    ; Variable declarations
    ; Temporary variables
    ; String literals
datos ends

; Code segment
codigo segment para public 'code'
    ; Main program logic
    ; Utility procedures (print numbers, etc.)
codigo ends
```

## File Buffer System

**Location**: `src/utils/file_buffer.py`

Provides efficient file I/O for large source files:
- **Chunked Reading**: Reads files in configurable chunks to manage memory
- **Generator-based**: Uses Python generators for memory efficiency
- **Error Handling**: Comprehensive error handling for file operations

## Compiler Driver

**Location**: `src/compiler.py`

The main compiler driver coordinates all phases:
1. **Two-Pass Compilation**: First pass for analysis, second pass for code generation
2. **Error Propagation**: Stops compilation on errors and reports them
3. **Output Management**: Generates multiple output files (.dld, .asm, debug info)
4. **Symbol Table Display**: Shows final symbol table for debugging

## Error Handling Strategy

### Compile-Time Errors
- **Lexical Errors**: Invalid characters, malformed tokens
- **Syntax Errors**: Grammar violations, unbalanced parentheses
- **Semantic Errors**: Type mismatches, undeclared variables
- **Declaration Errors**: Duplicate variable names

### Error Reporting
- Line number precision for all error messages
- Descriptive error messages with context
- Graceful error recovery where possible

## Data Structures

### Symbol Table
```python
[
    ['variable_name', 'type', value, 'id_string', 'read_status'],
    # Example:
    ['x', 'int', 42, 'id0', 'NoLectura']
]
```

### Number Table  
```python
[
    [numeric_value, 'identifier'],
    # Example:
    [42, 'n0']
]
```

### Quadruple Table
```python
[
    ['operator', 'operand1', 'operand2', 'result'],
    # Example:
    ['+', 'id0', 'n0', 't1']
]
```

## Optimization Opportunities

### Current Limitations
- No dead code elimination
- No constant folding
- No register allocation optimization
- No common subexpression elimination

### Potential Improvements
- **Constant Folding**: Evaluate constant expressions at compile time
- **Dead Code Elimination**: Remove unreachable code
- **Register Allocation**: Better register usage strategies
- **Peephole Optimization**: Local optimizations on generated assembly

## Testing Strategy

### Unit Tests
- Individual component testing for each compiler phase
- Token stream validation
- Parse tree verification
- Symbol table consistency checks

### Integration Tests
- End-to-end compilation testing
- Assembly code execution validation
- Error handling verification

### Example Programs
- Basic arithmetic operations
- Control flow structures
- I/O operations
- Error cases for negative testing

## Future Extensions

### Language Features
- Function definitions and calls
- Local variable scoping
- Arrays and data structures
- Enhanced type system

### Compiler Features
- Optimization passes
- Better error recovery
- Debug information generation
- Multiple target architectures

### Development Tools
- Interactive debugger
- Syntax highlighting
- IDE integration
- Profiling tools 