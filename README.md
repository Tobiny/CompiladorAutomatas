# 🤖 Automata Language Compiler API

A modern web-based compiler for the Automata Language (.af) featuring a complete compilation pipeline from lexical analysis to x86 assembly generation. Built with Python Flask and designed for educational purposes and portfolio demonstration.

## 🌐 Live Demo

**Try it online:** [https://simple-language-compiler.onrender.com/](https://simple-language-compiler.onrender.com/) 

## 🚀 Features

### 🔧 Compiler Features
- **Lexical Analysis**: Complete tokenization with comprehensive error handling
- **Syntax Analysis**: LR(1) parser for arithmetic expressions and language constructs
- **Semantic Analysis**: Type checking and variable declaration validation
- **Code Generation**: x86 assembly code output
- **Preprocessing**: Comment removal, whitespace normalization, and syntax validation

### 🌐 Web API Features
- **RESTful API**: JSON-based endpoints for online compilation
- **Interactive Web Interface**: Built-in HTML interface for testing
- **CORS Support**: Enable frontend integration
- **Example Programs**: Built-in code examples and templates
- **Health Monitoring**: API health check endpoints
- **Error Handling**: Comprehensive error reporting and validation

### 📋 Language Support
- **Data Types**: `int`, `boolean`, `str`
- **Operations**: Arithmetic (`+`, `-`, `*`, `/`), Logical (`&&`, `||`, `!`)
- **Control Flow**: `if` statements, `while` loops
- **I/O Operations**: `print()`, `read()` functions
- **Variables**: Declaration, assignment, and complex expressions

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)

### Local Development
```bash
# Clone the repository
git clone https://github.com/tobiny/automata-compiler-api.git
cd automata-compiler-api

# Install dependencies
pip install -r requirements.txt

# Run the web API
python app.py

# Or compile files directly
python compile.py examples/basic_program.af
```

### Docker (Optional)
```bash
# Build and run with Docker
docker build -t automata-compiler .
docker run -p 5000:5000 automata-compiler
```

## 🌐 API Documentation

### Base URL
- **Local**: `http://localhost:5000`
- **Production**: `https://simple-language-compiler.onrender.com/`

### Endpoints

#### `POST /api/compile`
Compile Automata Language code and get comprehensive results.

**Request Body:**
```json
{
  "code": "int x = 42;\nprint(x);",
  "filename": "my_program"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Compilation successful",
  "preprocessed": "1: int x = 42;\n2: print(x);",
  "assembly": "...",
  "symbol_table": [
    {"name": "x", "type": "int", "value": 42}
  ],
  "tokens": [
    {"type": "INT", "lexeme": "int", "line": 1, "column": 0}
  ]
}
```

#### `GET /api/examples`
Get all available code examples.

**Response:**
```json
{
  "examples": [
    {
      "name": "basic_program",
      "filename": "basic_program.af",
      "code": "int x = 42;...",
      "description": "Basic Automata Program - Variables and I/O Operations"
    }
  ],
  "count": 3
}
```

#### `GET /api/examples/{name}`
Get a specific example by name.

#### `GET /api/health`
API health check endpoint.

#### `GET /docs`
Complete API documentation.

## 💡 Example Programs

### Basic Operations
```javascript
// Variables and arithmetic
int x = 42;
int y = 10;
int result = x + y * 2;
print("Result: " + result);
```

### Control Flow
```javascript
// Conditional logic
boolean flag = True;
if(flag && x > 30) {
    print("Condition satisfied!");
}
```

### Complex Expressions
```javascript
// Nested operations
int calculation = ((x + y) * 2) / (y - 5);
print(calculation);
```

## 🏗️ Project Architecture

```
automata-compiler-api/
├── 🌐 app.py                 # Flask API application
├── 🔧 compile.py             # CLI compilation script
├── 📁 src/
│   ├── 🔍 lexer/             # Lexical analysis
│   │   ├── token_analyzer.py
│   │   └── lexical_analyzer.py
│   ├── 📝 parser/            # Syntax analysis
│   │   └── lr_parser.py
│   ├── ⚙️ codegen/           # Code generation
│   │   ├── assembly_generator.py
│   │   └── templates/
│   ├── 🛠️ utils/            # Utilities
│   │   ├── preprocessor.py
│   │   └── file_buffer.py
│   └── 🎯 compiler.py        # Main compiler orchestrator
├── 📚 examples/              # Sample programs
│   ├── basic_program.af
│   ├── arithmetic.af
│   └── control_flow.af
├── 📖 docs/                  # Documentation
└── 🧪 tests/                # Test suites
```

## 🚀 Deployment

### Deploy to Render.com
1. **Fork/Clone** this repository
2. **Connect** your GitHub repo to Render.com
3. **Create** a new Web Service
4. **Configure**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Environment: `Python 3.9+`
5. **Deploy** automatically from GitHub

### Environment Variables
```bash
FLASK_ENV=production
PORT=5000
PYTHONPATH=.
```

## 📊 Technical Details

### Compilation Pipeline
1. **Preprocessing** → Comment removal, normalization
2. **Lexical Analysis** → Tokenization
3. **Syntax Analysis** → LR(1) parsing
4. **Semantic Analysis** → Type checking, symbol table
5. **Code Generation** → x86 assembly output

### Supported Grammar
```
program → declaration*
declaration → type identifier ('=' expression)? ';'
expression → logical_or_expression
logical_or_expression → logical_and_expression ('||' logical_and_expression)*
...
```

### Performance
- **Compilation Speed**: ~50-100 lines/second
- **Memory Usage**: <10MB per compilation
- **File Size Limit**: 10KB source code
- **Concurrent Users**: Supports multiple simultaneous compilations

## 🧪 Testing

```bash
# Run unit tests
python -m pytest tests/

# Test API endpoints
curl -X POST http://localhost:5000/api/compile \
  -H "Content-Type: application/json" \
  -d '{"code": "int x = 42; print(x);"}'

# Load test with example
curl http://localhost:5000/api/examples/basic_program
```

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** changes (`git commit -m 'Add amazing feature'`)
4. **Push** to branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Fernando** - Portfolio Project  
*Demonstrating expertise in:*
- Compiler Design & Implementation
- Modern Python Development
- RESTful API Design
- Web Application Deployment
- Software Engineering Best Practices

## 🔗 Links

- **Live Demo**: [simple-language-compiler.onrender.com](https://simple-language-compiler.onrender.com/)
- **GitHub**: [Repository](https://github.com/your-username/automata-compiler-api)

---

⭐ **Star this repository if you found it helpful!** ⭐ 