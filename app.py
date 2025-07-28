"""
Automata Compiler API

A Flask web API for compiling Automata Language (.af) code online.
Perfect for demonstrating compiler functionality and educational purposes.
"""

from flask import Flask, request, jsonify, render_template_string, send_from_directory
from flask_cors import CORS
import os
import tempfile
import traceback
from pathlib import Path
import sys

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.compiler import SimpleCompiler
from src.utils.preprocessor import SourcePreprocessor
from src.lexer.token_analyzer import TokenAnalyzer

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024  # 16KB max file size
TEMP_DIR = tempfile.mkdtemp()

@app.route('/')
def home():
    """Main page with API documentation and online compiler interface."""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/health')
def health_check():
    """Health check endpoint for monitoring."""
    return jsonify({
        "status": "healthy",
        "service": "Automata Compiler API",
        "version": "1.0.0"
    })

@app.route('/api/compile', methods=['POST'])
def compile_code():
    """
    Compile Automata Language code.
    
    Expected JSON payload:
    {
        "code": "int x = 42;\nprint(x);",
        "filename": "optional_filename"
    }
    
    Returns:
    {
        "success": true/false,
        "message": "compilation result",
        "tokens": [...],
        "symbol_table": [...],
        "assembly": "...",
        "preprocessed": "..."
    }
    """
    try:
        data = request.get_json()
        if not data or 'code' not in data:
            return jsonify({
                "success": False,
                "error": "Missing 'code' in request body"
            }), 400
        
        source_code = data['code']
        filename = data.get('filename', 'user_code')
        
        # Validate code length
        if len(source_code) > 10000:  # 10KB limit
            return jsonify({
                "success": False,
                "error": "Code too long (max 10KB)"
            }), 400
        
        # Create temporary file
        temp_file = os.path.join(TEMP_DIR, f"{filename}.af")
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(source_code)
        
        # Compile the code
        compiler = SimpleCompiler(temp_file)
        success = compiler.compile()
        
        result = {
            "success": success,
            "message": "Compilation successful" if success else "Compilation failed",
            "filename": filename
        }
        
        # Add compilation results if successful
        if success:
            # Read generated files
            try:
                # Preprocessed code
                preprocessed_file = f"{temp_file}d"
                if os.path.exists(preprocessed_file):
                    with open(preprocessed_file, 'r', encoding='utf-8') as f:
                        result["preprocessed"] = f.read()
                
                # Assembly code
                assembly_file = f"{filename}.asm"
                if os.path.exists(assembly_file):
                    with open(assembly_file, 'r', encoding='utf-8') as f:
                        result["assembly"] = f.read()
                
                # Symbol table
                result["symbol_table"] = [
                    {
                        "name": symbol.name if hasattr(symbol, 'name') else symbol[0],
                        "type": symbol.data_type.value if hasattr(symbol, 'data_type') and hasattr(symbol.data_type, 'value') else (symbol[1] if len(symbol) > 1 else "unknown"),
                        "value": symbol.value if hasattr(symbol, 'value') else (symbol[2] if len(symbol) > 2 else None)
                    }
                    for symbol in compiler.symbol_table
                ]
                
                # Tokens (limited to first 100 for performance)
                if compiler.tokens:
                    result["tokens"] = [
                        {
                            "type": token.type.value if hasattr(token.type, 'value') else str(token.type),
                            "lexeme": token.lexeme,
                            "line": token.line,
                            "column": token.column
                        }
                        for token in compiler.tokens[:100]  # Limit to first 100 tokens
                    ]
                
            except Exception as e:
                result["warning"] = f"Could not read all output files: {str(e)}"
        
        # Cleanup
        cleanup_temp_files(temp_file, filename)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Internal server error: {str(e)}",
            "traceback": traceback.format_exc() if app.debug else None
        }), 500

@app.route('/api/examples')
def get_examples():
    """Get available code examples."""
    examples = []
    examples_dir = Path('examples')
    
    if examples_dir.exists():
        for file_path in examples_dir.glob('*.af'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                examples.append({
                    "name": file_path.stem,
                    "filename": file_path.name,
                    "code": content,
                    "description": extract_description(content)
                })
            except Exception as e:
                print(f"Error reading example {file_path}: {e}")
    
    return jsonify({
        "examples": examples,
        "count": len(examples)
    })

@app.route('/api/examples/<example_name>')
def get_example(example_name):
    """Get a specific example by name."""
    example_file = Path('examples') / f"{example_name}.af"
    
    if not example_file.exists():
        return jsonify({
            "success": False,
            "error": "Example not found"
        }), 404
    
    try:
        with open(example_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return jsonify({
            "success": True,
            "name": example_name,
            "filename": example_file.name,
            "code": content,
            "description": extract_description(content)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error reading example: {str(e)}"
        }), 500

@app.route('/docs')
def documentation():
    """API documentation endpoint."""
    return jsonify({
        "title": "Automata Compiler API Documentation",
        "version": "1.0.0",
        "description": "REST API for compiling Automata Language (.af) code",
        "endpoints": {
            "GET /": "Main page with web interface",
            "GET /api/health": "Health check",
            "POST /api/compile": "Compile Automata code",
            "GET /api/examples": "Get all available examples",
            "GET /api/examples/<name>": "Get specific example",
            "GET /docs": "This documentation"
        },
        "compile_endpoint": {
            "method": "POST",
            "url": "/api/compile",
            "content_type": "application/json",
            "payload": {
                "code": "string (required) - The Automata code to compile",
                "filename": "string (optional) - Custom filename"
            },
            "response": {
                "success": "boolean - Compilation success",
                "message": "string - Result message",
                "preprocessed": "string - Preprocessed code",
                "assembly": "string - Generated assembly code",
                "symbol_table": "array - Variable declarations",
                "tokens": "array - Lexical tokens"
            }
        }
    })

def extract_description(code):
    """Extract description from code comments."""
    lines = code.split('\n')
    description_lines = []
    
    for line in lines[:5]:  # Check first 5 lines
        line = line.strip()
        if line.startswith('//'):
            desc = line[2:].strip()
            if desc and not desc.lower().startswith(('basic', 'this demonstrates')):
                description_lines.append(desc)
    
    return ' '.join(description_lines) if description_lines else "Automata Language example"

def cleanup_temp_files(base_file, filename):
    """Clean up temporary files created during compilation."""
    cleanup_patterns = [
        base_file,
        f"{base_file}d",
        f"{filename}.asm",
        f"{filename}_tokens.csv"
    ]
    
    for pattern in cleanup_patterns:
        try:
            if os.path.exists(pattern):
                os.remove(pattern)
        except:
            pass

# HTML Template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Automata Compiler API</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f5f7fa; }
        .container { max-width: 1200px; margin: 0 auto; background: white; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px 10px 0 0; }
        .content { padding: 30px; }
        .compiler-section { margin: 20px 0; }
        textarea { width: 100%; height: 200px; font-family: 'Monaco', 'Courier New', monospace; border: 2px solid #e0e6ed; border-radius: 5px; padding: 15px; font-size: 14px; }
        button { background: #667eea; color: white; border: none; padding: 12px 24px; border-radius: 5px; cursor: pointer; font-size: 16px; margin: 10px 5px; }
        button:hover { background: #5a6fd8; }
        .output { background: #f8f9fa; border: 2px solid #e9ecef; border-radius: 5px; padding: 15px; margin: 10px 0; max-height: 300px; overflow-y: auto; }
        .success { border-color: #28a745; background: #d4edda; }
        .error { border-color: #dc3545; background: #f8d7da; }
        .endpoint { background: #e9ecef; padding: 15px; border-radius: 5px; margin: 10px 0; }
        .method { background: #007bff; color: white; padding: 4px 8px; border-radius: 3px; font-size: 12px; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        @media (max-width: 768px) { .grid { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Automata Compiler API</h1>
            <p>Compile Automata Language (.af) code online • Educational Compiler Implementation</p>
        </div>
        
        <div class="content">
            <div class="grid">
                <div>
                    <div class="compiler-section">
                        <h2>💻 Online Compiler</h2>
                        <textarea id="codeInput" placeholder="Enter your Automata code here...
Example:
int x = 42;
int y = 10;
int result = x + y;
print('Result: ' + result);"></textarea>
                        <br>
                        <button onclick="compileCode()">🚀 Compile</button>
                        <button onclick="loadExample()">📖 Load Example</button>
                        <button onclick="clearAll()">🗑️ Clear</button>
                    </div>
                    
                    <div id="output" class="output" style="display:none;">
                        <h3>Compilation Results</h3>
                        <div id="outputContent"></div>
                    </div>
                </div>
                
                <div>
                    <h2>📚 API Endpoints</h2>
                    
                    <div class="endpoint">
                        <span class="method">POST</span> <strong>/api/compile</strong>
                        <p>Compile Automata code and get results</p>
                    </div>
                    
                    <div class="endpoint">
                        <span class="method">GET</span> <strong>/api/examples</strong>
                        <p>Get all available code examples</p>
                    </div>
                    
                    <div class="endpoint">
                        <span class="method">GET</span> <strong>/api/health</strong>
                        <p>API health check</p>
                    </div>
                    
                    <div class="endpoint">
                        <span class="method">GET</span> <strong>/docs</strong>
                        <p>Complete API documentation</p>
                    </div>
                    
                    <h3>🚀 Features</h3>
                    <ul>
                        <li>✅ Lexical Analysis & Tokenization</li>
                        <li>✅ LR Syntax Parsing</li>
                        <li>✅ Semantic Analysis & Type Checking</li>
                        <li>✅ x86 Assembly Code Generation</li>
                        <li>✅ RESTful API with JSON responses</li>
                        <li>✅ CORS enabled for frontend integration</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <script>
        async function compileCode() {
            const code = document.getElementById('codeInput').value;
            if (!code.trim()) {
                alert('Please enter some code to compile!');
                return;
            }
            
            try {
                const response = await fetch('/api/compile', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ code: code, filename: 'web_input' })
                });
                
                const result = await response.json();
                showOutput(result, response.ok);
            } catch (error) {
                showOutput({ success: false, error: 'Network error: ' + error.message }, false);
            }
        }
        
        async function loadExample() {
            try {
                const response = await fetch('/api/examples');
                const data = await response.json();
                
                if (data.examples && data.examples.length > 0) {
                    const example = data.examples[0];
                    document.getElementById('codeInput').value = example.code;
                } else {
                    alert('No examples available');
                }
            } catch (error) {
                alert('Error loading example: ' + error.message);
            }
        }
        
        function clearAll() {
            document.getElementById('codeInput').value = '';
            document.getElementById('output').style.display = 'none';
        }
        
        function showOutput(result, success) {
            const output = document.getElementById('output');
            const content = document.getElementById('outputContent');
            
            output.className = 'output ' + (success && result.success ? 'success' : 'error');
            output.style.display = 'block';
            
            let html = `<p><strong>Status:</strong> ${result.success ? '✅ Success' : '❌ Failed'}</p>`;
            html += `<p><strong>Message:</strong> ${result.message || result.error || 'Unknown error'}</p>`;
            
            if (result.symbol_table && result.symbol_table.length > 0) {
                html += `<p><strong>Variables:</strong> ${result.symbol_table.length} declared</p>`;
                html += '<details><summary>Symbol Table</summary><pre>' + 
                       JSON.stringify(result.symbol_table, null, 2) + '</pre></details>';
            }
            
            if (result.tokens && result.tokens.length > 0) {
                html += `<p><strong>Tokens:</strong> ${result.tokens.length} generated</p>`;
            }
            
            if (result.assembly) {
                html += '<details><summary>Generated Assembly</summary><pre>' + 
                       result.assembly + '</pre></details>';
            }
            
            content.innerHTML = html;
        }
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    app.run(host='0.0.0.0', port=port, debug=debug) 