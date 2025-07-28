# Simple Language Compiler

A complete compiler implementation for a simple programming language that supports variables, arithmetic operations, control structures, and I/O operations. The compiler generates x86 assembly code from high-level source code.

## 🚀 Features

- **Lexical Analysis**: Tokenizes source code with comprehensive error handling
- **Syntax Analysis**: LR parser for arithmetic expressions and language constructs
- **Semantic Analysis**: Type checking and variable declaration validation
- **Code Generation**: Produces x86 assembly code
- **Control Structures**: Support for `if` statements and `while` loops
- **Data Types**: Integer, boolean, and string variables
- **I/O Operations**: Print and read operations
- **Expression Evaluation**: Complex arithmetic and logical expressions

## 📋 Language Syntax

### Variable Declarations
```javascript
int number = 42;
boolean flag = True;
str message = "Hello World";
```

### Arithmetic Operations
```javascript
int result = (x + y) * z - 10;
```

### Control Structures
```javascript
if(x > 5 && y < 10) {
    print("Condition met");
}

while(counter < 100) {
    counter = counter + 1;
}
```

### I/O Operations
```javascript
print("Enter a number: ");
read(userInput);
print("You entered: " + userInput);
```

## 🏗️ Project Structure

```
simple-language-compiler/
├── src/
│   ├── lexer/
│   │   ├── lexical_analyzer.py     # Main lexical analyzer
│   │   └── token_analyzer.py       # Alternative token analyzer
│   ├── parser/
│   │   ├── lr_parser.py            # LR syntax analyzer
│   │   └── syntax_analyzer.py      # Integrated syntax analyzer
│   ├── semantic/
│   │   └── semantic_analyzer.py    # Semantic analysis
│   ├── codegen/
│   │   ├── assembly_generator.py   # x86 assembly code generator
│   │   └── templates/              # Assembly templates
│   ├── utils/
│   │   ├── preprocessor.py         # Source code preprocessor
│   │   └── file_buffer.py          # File reading utilities
│   └── compiler.py                 # Main compiler driver
├── examples/
│   ├── basic_program.dl            # Basic example
│   ├── arithmetic.dl               # Arithmetic operations
│   └── control_flow.dl             # Control structures
├── tests/
│   └── test_programs/
├── docs/
│   ├── language_specification.md
│   └── compiler_architecture.md
└── README.md
```

## 🛠️ Installation & Usage

### Prerequisites
- Python 3.7+
- Assembly compiler (for running generated code)

### Running the Compiler

1. **Compile a program:**
   ```bash
   python src/compiler.py examples/basic_program.dl
   ```

2. **The compiler will generate:**
   - Preprocessed source file (`.dld`)
   - Assembly output (`.asm`)
   - Symbol table and quadruples (console output)

### Example Program

Create a file `hello.dl`:
```javascript
int main() {
    str greeting = "Hello, World!";
    int number = 42;
    
    print(greeting);
    print("The answer is: " + number);
    
    if(number > 40) {
        print("Number is greater than 40");
    }
    
    return 0;
}
```

Compile it:
```bash
python src/compiler.py hello.dl
```

## 🧠 Compiler Architecture

1. **Preprocessor**: Removes comments and normalizes whitespace
2. **Lexical Analyzer**: Converts source into tokens
3. **Syntax Analyzer**: Builds parse trees using LR parsing
4. **Semantic Analyzer**: Validates types and variable usage
5. **Code Generator**: Produces x86 assembly code

## 📊 Technical Details

- **Parsing Algorithm**: LR(1) parser for expressions
- **Target Architecture**: x86 assembly (16-bit)
- **Symbol Table**: Dynamic variable tracking
- **Intermediate Code**: Quadruple representation
- **Error Handling**: Comprehensive error reporting

## 🤝 Contributing

This project was created as a learning exercise in compiler design. Feel free to:
- Report bugs
- Suggest improvements
- Add new language features
- Improve documentation

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Created as part of compiler design studies, demonstrating:
- Formal language theory implementation
- Multi-phase compilation process
- Assembly code generation
- Software engineering best practices 