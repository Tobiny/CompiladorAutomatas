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
    <title>Automata Compiler API - Educational Compiler Implementation</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        /* ===================================
           Automata Compiler - Portfolio Style
           ===================================*/

        /* Root Variables */
        :root {
            --primary-color: #667eea;
            --secondary-color: #764ba2;
            --accent-color: #48bb78;
            --dark-color: #1a202c;
            --gray-color: #4a5568;
            --light-gray: #718096;
            --lighter-gray: #a0aec0;
            --bg-color: #fafafa;
            --white: #ffffff;
            --border-color: #e2e8f0;
            --shadow-color: rgba(0, 0, 0, 0.1);
            --gradient-1: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            --gradient-2: linear-gradient(45deg, #667eea, #764ba2, #f093fb);
            --transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            --success-color: #48bb78;
            --error-color: #f56565;
            --warning-color: #ed8936;
        }

        /* Reset and Base Styles */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            line-height: 1.6;
            color: var(--dark-color);
            background: var(--bg-color);
            overflow-x: hidden;
            scroll-behavior: smooth;
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }

        ::-webkit-scrollbar-track {
            background: var(--bg-color);
        }

        ::-webkit-scrollbar-thumb {
            background: var(--gradient-1);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: var(--secondary-color);
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 24px;
        }

        /* Animated Background */
        .animated-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            overflow: hidden;
        }

        .floating-shapes {
            position: absolute;
            width: 100%;
            height: 100%;
        }

        .shape {
            position: absolute;
            border-radius: 50%;
            opacity: 0.05;
            animation: float 20s infinite linear;
        }

        .shape:nth-child(1) {
            width: 80px;
            height: 80px;
            background: var(--primary-color);
            top: 20%;
            left: 10%;
            animation-delay: 0s;
        }

        .shape:nth-child(2) {
            width: 120px;
            height: 120px;
            background: var(--secondary-color);
            top: 60%;
            right: 10%;
            animation-delay: -7s;
        }

        .shape:nth-child(3) {
            width: 60px;
            height: 60px;
            background: var(--accent-color);
            bottom: 20%;
            left: 20%;
            animation-delay: -14s;
        }

        @keyframes float {
            0%, 100% {
                transform: translateY(0px) rotate(0deg);
            }
            33% {
                transform: translateY(-30px) rotate(120deg);
            }
            66% {
                transform: translateY(30px) rotate(240deg);
            }
        }

        /* Navigation */
        nav {
            position: fixed;
            top: 0;
            width: 100%;
            background: rgba(250, 250, 250, 0.95);
            backdrop-filter: blur(25px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
            z-index: 1000;
            transition: var(--transition);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }

        .nav-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 0;
        }

        .logo {
            font-size: 28px;
            font-weight: 800;
            background: var(--gradient-1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: -1px;
            cursor: pointer;
            transition: var(--transition);
        }

        .logo:hover {
            transform: scale(1.05);
        }

        .nav-info {
            display: flex;
            align-items: center;
            gap: 24px;
        }

        .status-badge {
            display: flex;
            align-items: center;
            gap: 8px;
            background: var(--white);
            border: 1px solid var(--border-color);
            border-radius: 50px;
            padding: 8px 16px;
            font-size: 12px;
            font-weight: 600;
            color: var(--gray-color);
            box-shadow: 0 4px 16px var(--shadow-color);
        }

        .status-dot {
            width: 8px;
            height: 8px;
            background: var(--success-color);
            border-radius: 50%;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% {
                transform: scale(0.95);
                box-shadow: 0 0 0 0 rgba(72, 187, 120, 0.7);
            }
            70% {
                transform: scale(1);
                box-shadow: 0 0 0 10px rgba(72, 187, 120, 0);
            }
            100% {
                transform: scale(0.95);
                box-shadow: 0 0 0 0 rgba(72, 187, 120, 0);
            }
        }

        .github-link {
            background: var(--gradient-1);
            color: white;
            padding: 10px 20px;
            border-radius: 12px;
            text-decoration: none;
            font-weight: 600;
            font-size: 14px;
            transition: var(--transition);
            display: flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }

        .github-link:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        }

        /* Hero Section */
        .hero {
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            background: var(--bg-color);
            overflow: hidden;
            padding-top: 100px;
        }

        .hero-content {
            text-align: center;
            max-width: 1000px;
            position: relative;
            z-index: 2;
        }

        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            background: var(--white);
            border: 1px solid var(--border-color);
            border-radius: 50px;
            padding: 12px 24px;
            margin-bottom: 32px;
            font-size: 14px;
            font-weight: 600;
            color: var(--gray-color);
            letter-spacing: 0.5px;
            box-shadow: 0 8px 32px var(--shadow-color);
            animation: fadeInDown 1s ease 0.2s both;
        }

        .hero h1 {
            font-size: clamp(2.5rem, 6vw, 4rem);
            font-weight: 800;
            color: var(--dark-color);
            margin-bottom: 24px;
            letter-spacing: -2px;
            line-height: 1.1;
            animation: fadeInUp 1s ease 0.4s both;
        }

        .gradient-text {
            background: var(--gradient-1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .hero-description {
            font-size: clamp(1.1rem, 3vw, 1.4rem);
            color: var(--light-gray);
            margin-bottom: 48px;
            max-width: 700px;
            margin-left: auto;
            margin-right: auto;
            line-height: 1.7;
            animation: fadeInUp 1s ease 0.6s both;
        }

        /* Main Content */
        .main-content {
            padding: 60px 0 120px;
        }

        .content-grid {
            display: grid;
            grid-template-columns: 1fr 400px;
            gap: 60px;
            align-items: start;
        }

        /* Compiler Section */
        .compiler-card {
            background: var(--white);
            border-radius: 24px;
            padding: 40px;
            border: 1px solid var(--border-color);
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
            position: relative;
            overflow: hidden;
        }

        .compiler-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: var(--gradient-1);
        }

        .section-title {
            font-size: 24px;
            font-weight: 700;
            color: var(--dark-color);
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .section-subtitle {
            color: var(--light-gray);
            margin-bottom: 32px;
            font-size: 15px;
        }

        .code-editor {
            position: relative;
            margin-bottom: 24px;
        }

        .editor-header {
            background: var(--bg-color);
            border: 1px solid var(--border-color);
            border-bottom: none;
            border-radius: 12px 12px 0 0;
            padding: 12px 20px;
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 14px;
            color: var(--gray-color);
            font-weight: 500;
        }

        .editor-dots {
            display: flex;
            gap: 6px;
        }

        .dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
        }

        .dot.red { background: #ff5f56; }
        .dot.yellow { background: #ffbd2e; }
        .dot.green { background: #27ca3f; }

        textarea {
            width: 100%;
            height: 300px;
            font-family: 'Monaco', 'SF Mono', 'Consolas', monospace;
            border: 1px solid var(--border-color);
            border-top: none;
            border-radius: 0 0 12px 12px;
            padding: 20px;
            font-size: 14px;
            line-height: 1.5;
            resize: vertical;
            background: var(--white);
            color: var(--dark-color);
            transition: var(--transition);
        }

        textarea:focus {
            outline: none;
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        .button-group {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
        }

        .btn {
            padding: 12px 24px;
            border: none;
            border-radius: 12px;
            font-size: 14px;
            font-weight: 600;
            text-decoration: none;
            transition: var(--transition);
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            letter-spacing: -0.2px;
            position: relative;
            overflow: hidden;
        }

        .btn-primary {
            background: var(--gradient-1);
            color: white;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 40px rgba(102, 126, 234, 0.4);
        }

        .btn-secondary {
            background: var(--white);
            color: var(--gray-color);
            border: 2px solid var(--border-color);
        }

        .btn-secondary:hover {
            border-color: var(--primary-color);
            color: var(--primary-color);
            transform: translateY(-2px);
        }

        .btn-danger {
            background: var(--white);
            color: var(--error-color);
            border: 2px solid var(--error-color);
        }

        .btn-danger:hover {
            background: var(--error-color);
            color: white;
            transform: translateY(-2px);
        }

        /* Output Section */
        .output-section {
            margin-top: 32px;
            opacity: 0;
            transform: translateY(20px);
            transition: all 0.5s ease;
        }

        .output-section.visible {
            opacity: 1;
            transform: translateY(0);
        }

        .output-card {
            background: var(--white);
            border-radius: 16px;
            border: 2px solid var(--border-color);
            overflow: hidden;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.06);
        }

        .output-header {
            background: var(--bg-color);
            padding: 16px 24px;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            gap: 12px;
            font-weight: 600;
            font-size: 14px;
        }

        .output-content {
            padding: 24px;
            max-height: 400px;
            overflow-y: auto;
        }

        .success .output-card {
            border-color: var(--success-color);
        }

        .success .output-header {
            background: rgba(72, 187, 120, 0.1);
            color: var(--success-color);
        }

        .error .output-card {
            border-color: var(--error-color);
        }

        .error .output-header {
            background: rgba(245, 101, 101, 0.1);
            color: var(--error-color);
        }

        .result-item {
            margin-bottom: 16px;
            padding: 12px 16px;
            background: var(--bg-color);
            border-radius: 8px;
            border-left: 4px solid var(--primary-color);
        }

        .result-label {
            font-weight: 600;
            color: var(--dark-color);
            margin-bottom: 4px;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .result-value {
            color: var(--gray-color);
            font-size: 14px;
        }

        details {
            margin-top: 12px;
        }

        summary {
            cursor: pointer;
            font-weight: 600;
            color: var(--primary-color);
            padding: 8px 0;
            transition: var(--transition);
        }

        summary:hover {
            color: var(--secondary-color);
        }

        pre {
            background: var(--dark-color);
            color: #a0aec0;
            padding: 16px;
            border-radius: 8px;
            overflow-x: auto;
            font-size: 12px;
            line-height: 1.4;
            margin-top: 8px;
        }

        /* Sidebar */
        .sidebar {
            position: sticky;
            top: 120px;
        }

        .info-card {
            background: var(--white);
            border-radius: 24px;
            padding: 32px;
            border: 1px solid var(--border-color);
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
            margin-bottom: 32px;
            transition: var(--transition);
        }

        .info-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
        }

        .info-title {
            font-size: 20px;
            font-weight: 700;
            color: var(--dark-color);
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .api-endpoint {
            background: var(--bg-color);
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 16px;
            border: 1px solid var(--border-color);
            transition: var(--transition);
        }

        .api-endpoint:hover {
            border-color: var(--primary-color);
            box-shadow: 0 4px 16px rgba(102, 126, 234, 0.1);
        }

        .method {
            background: var(--primary-color);
            color: white;
            padding: 4px 8px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.5px;
            margin-right: 12px;
        }

        .method.get { background: var(--success-color); }
        .method.post { background: var(--primary-color); }

        .endpoint-url {
            font-family: 'Monaco', monospace;
            font-weight: 600;
            color: var(--dark-color);
            font-size: 14px;
        }

        .endpoint-desc {
            color: var(--light-gray);
            font-size: 13px;
            margin-top: 8px;
            line-height: 1.5;
        }

        .features-list {
            list-style: none;
            padding: 0;
        }

        .features-list li {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
            font-size: 14px;
            color: var(--gray-color);
        }

        .features-list .icon {
            color: var(--success-color);
            font-size: 16px;
        }

        /* Language Guide */
        .language-guide {
            background: var(--white);
            border-radius: 24px;
            padding: 32px;
            border: 1px solid var(--border-color);
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
            margin-top: 40px;
        }

        .guide-section {
            margin-bottom: 32px;
        }

        .guide-section h3 {
            font-size: 18px;
            font-weight: 700;
            color: var(--dark-color);
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .code-example {
            background: var(--dark-color);
            color: #a0aec0;
            padding: 20px;
            border-radius: 12px;
            font-family: 'Monaco', monospace;
            font-size: 13px;
            line-height: 1.6;
            margin: 16px 0;
            border-left: 4px solid var(--primary-color);
        }

        .syntax-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 12px;
            background: var(--bg-color);
            border-radius: 8px;
            margin-bottom: 8px;
        }

        .syntax-term {
            font-family: 'Monaco', monospace;
            font-size: 13px;
            color: var(--primary-color);
            font-weight: 600;
        }

        .syntax-desc {
            font-size: 13px;
            color: var(--gray-color);
        }

        /* Animation Keyframes */
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(40px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        /* Loading Animation */
        .loading {
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }

        .spinner {
            width: 16px;
            height: 16px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-top: 2px solid white;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        /* Mobile Responsiveness */
        @media (max-width: 1024px) {
            .content-grid {
                grid-template-columns: 1fr;
                gap: 40px;
            }
            
            .sidebar {
                position: relative;
                top: 0;
            }
        }

        @media (max-width: 768px) {
            .container {
                padding: 0 16px;
            }
            
            .nav-container {
                padding: 16px 0;
            }
            
            .logo {
                font-size: 24px;
            }
            
            .nav-info {
                gap: 16px;
            }
            
            .github-link {
                display: none;
            }
            
            .hero {
                padding-top: 80px;
                min-height: auto;
                padding-bottom: 40px;
            }
            
            .compiler-card, .info-card, .language-guide {
                padding: 24px;
            }
            
            .button-group {
                flex-direction: column;
            }
            
            .btn {
                justify-content: center;
                width: 100%;
            }
            
            textarea {
                height: 250px;
            }
        }

        /* Dark theme support */
        @media (prefers-color-scheme: dark) {
            :root {
                --bg-color: #1a202c;
                --white: #2d3748;
                --dark-color: #f7fafc;
                --gray-color: #a0aec0;
                --light-gray: #718096;
                --border-color: #4a5568;
            }
        }
    </style>
</head>
<body>
    <!-- Animated Background -->
    <div class="animated-bg">
        <div class="floating-shapes">
            <div class="shape"></div>
            <div class="shape"></div>
            <div class="shape"></div>
        </div>
    </div>

    <!-- Navigation -->
    <nav>
        <div class="container">
            <div class="nav-container">
                <div class="logo">🤖 Automata Compiler</div>
                <div class="nav-info">
                    <div class="status-badge">
                        <div class="status-dot"></div>
                        <span>API Online</span>
                    </div>
                    <a href="https://github.com" class="github-link" target="_blank">
                        <i class="fab fa-github"></i>
                        View on GitHub
                    </a>
                </div>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero">
        <div class="container">
            <div class="hero-content">
                <div class="hero-badge">
                    <i class="fas fa-graduation-cap"></i>
                    Educational Compiler Implementation
                </div>
                <h1>
                    <span class="gradient-text">Automata Language</span><br>
                    Online Compiler
                </h1>
                <p class="hero-description">
                    Experience modern compiler design with our educational Automata Language (.af) compiler. 
                    Features complete lexical analysis, LR parsing, semantic analysis, and x86 assembly generation. 
                    Perfect for learning compiler theory and demonstrating language processing concepts.
                </p>
            </div>
        </div>
    </section>

    <!-- Main Content -->
    <section class="main-content">
        <div class="container">
            <div class="content-grid">
                <!-- Compiler Interface -->
                <div>
                    <div class="compiler-card">
                        <h2 class="section-title">
                            <i class="fas fa-code"></i>
                            Online Compiler
                        </h2>
                        <p class="section-subtitle">
                            Write and compile Automata Language code directly in your browser. 
                            Get instant feedback on syntax, semantics, and generated assembly.
                        </p>
                        
                        <div class="code-editor">
                            <div class="editor-header">
                                <div class="editor-dots">
                                    <div class="dot red"></div>
                                    <div class="dot yellow"></div>
                                    <div class="dot green"></div>
                                </div>
                                <span><i class="fas fa-file-code"></i> main.af</span>
                            </div>
                            <textarea id="codeInput" placeholder="// Welcome to Automata Language Compiler
// Try this basic example:

int x = 42;
int y = 10;
int sum = x + y;

print('The sum is: ' + sum);

// Features supported:
// - Variable declarations (int, string)
// - Arithmetic operations (+, -, *, /)
// - Control flow (if/else statements)
// - Input/output operations
// - String concatenation"></textarea>
                        </div>
                        
                        <div class="button-group">
                            <button class="btn btn-primary" onclick="compileCode()">
                                <i class="fas fa-play"></i>
                                <span class="btn-text">Compile Code</span>
                            </button>
                            <button class="btn btn-secondary" onclick="loadExample()">
                                <i class="fas fa-lightbulb"></i>
                                Load Example
                            </button>
                            <button class="btn btn-danger" onclick="clearAll()">
                                <i class="fas fa-trash"></i>
                                Clear Editor
                            </button>
                        </div>
                    </div>

                    <!-- Output Section -->
                    <div id="outputSection" class="output-section">
                        <div id="outputContainer" class="output-card">
                            <div class="output-header">
                                <i class="fas fa-terminal"></i>
                                <span>Compilation Results</span>
                            </div>
                            <div id="outputContent" class="output-content">
                                <!-- Results will be inserted here -->
                            </div>
                        </div>
                    </div>

                    <!-- Language Guide -->
                    <div class="language-guide">
                        <h2 class="section-title">
                            <i class="fas fa-book"></i>
                            Language Guide
                        </h2>
                        
                        <div class="guide-section">
                            <h3><i class="fas fa-cogs"></i> Syntax Overview</h3>
                            <div class="syntax-item">
                                <span class="syntax-term">int variable = value;</span>
                                <span class="syntax-desc">Integer declaration</span>
                            </div>
                            <div class="syntax-item">
                                <span class="syntax-term">string text = "hello";</span>
                                <span class="syntax-desc">String declaration</span>
                            </div>
                            <div class="syntax-item">
                                <span class="syntax-term">print(expression);</span>
                                <span class="syntax-desc">Output statement</span>
                            </div>
                            <div class="syntax-item">
                                <span class="syntax-term">read(variable);</span>
                                <span class="syntax-desc">Input statement</span>
                            </div>
                        </div>

                        <div class="guide-section">
                            <h3><i class="fas fa-calculator"></i> Arithmetic Operations</h3>
                            <div class="code-example">int result = (x + y) * z / 2 - 1;</div>
                            <p>Supports +, -, *, / with proper precedence and parentheses.</p>
                        </div>

                        <div class="guide-section">
                            <h3><i class="fas fa-code-branch"></i> Control Flow</h3>
                            <div class="code-example">if (condition) {
    // statements
} else {
    // alternative statements
}</div>
                            <p>Conditional execution with if/else statements and comparison operators.</p>
                        </div>

                        <div class="guide-section">
                            <h3><i class="fas fa-link"></i> String Operations</h3>
                            <div class="code-example">string message = "Hello " + name + "!";
print(message);</div>
                            <p>String concatenation using the + operator for combining text.</p>
                        </div>
                    </div>
                </div>

                <!-- Sidebar -->
                <div class="sidebar">
                    <!-- API Endpoints -->
                    <div class="info-card">
                        <h3 class="info-title">
                            <i class="fas fa-server"></i>
                            API Endpoints
                        </h3>
                        
                        <div class="api-endpoint">
                            <div>
                                <span class="method post">POST</span>
                                <span class="endpoint-url">/api/compile</span>
                            </div>
                            <p class="endpoint-desc">
                                Compile Automata code and receive detailed compilation results including tokens, 
                                symbol table, and generated assembly code.
                            </p>
                        </div>
                        
                        <div class="api-endpoint">
                            <div>
                                <span class="method get">GET</span>
                                <span class="endpoint-url">/api/examples</span>
                            </div>
                            <p class="endpoint-desc">
                                Retrieve all available code examples with descriptions and source code.
                            </p>
                        </div>
                        
                        <div class="api-endpoint">
                            <div>
                                <span class="method get">GET</span>
                                <span class="endpoint-url">/api/health</span>
                            </div>
                            <p class="endpoint-desc">
                                Check API service health and availability status.
                            </p>
                        </div>
                        
                        <div class="api-endpoint">
                            <div>
                                <span class="method get">GET</span>
                                <span class="endpoint-url">/docs</span>
                            </div>
                            <p class="endpoint-desc">
                                Access complete API documentation with request/response schemas.
                            </p>
                        </div>
                    </div>

                    <!-- Features -->
                    <div class="info-card">
                        <h3 class="info-title">
                            <i class="fas fa-star"></i>
                            Compiler Features
                        </h3>
                        
                        <ul class="features-list">
                            <li>
                                <i class="fas fa-check icon"></i>
                                <span>Complete Lexical Analysis with tokenization</span>
                            </li>
                            <li>
                                <i class="fas fa-check icon"></i>
                                <span>LR(1) Syntax Parser with error detection</span>
                            </li>
                            <li>
                                <i class="fas fa-check icon"></i>
                                <span>Semantic Analysis & Type Checking</span>
                            </li>
                            <li>
                                <i class="fas fa-check icon"></i>
                                <span>x86 Assembly Code Generation</span>
                            </li>
                            <li>
                                <i class="fas fa-check icon"></i>
                                <span>Symbol Table Management</span>
                            </li>
                            <li>
                                <i class="fas fa-check icon"></i>
                                <span>Intermediate Code Generation</span>
                            </li>
                            <li>
                                <i class="fas fa-check icon"></i>
                                <span>RESTful API with JSON responses</span>
                            </li>
                            <li>
                                <i class="fas fa-check icon"></i>
                                <span>CORS enabled for integration</span>
                            </li>
                            <li>
                                <i class="fas fa-check icon"></i>
                                <span>Real-time compilation feedback</span>
                            </li>
                            <li>
                                <i class="fas fa-check icon"></i>
                                <span>Educational documentation</span>
                            </li>
                        </ul>
                    </div>

                    <!-- Technical Stack -->
                    <div class="info-card">
                        <h3 class="info-title">
                            <i class="fas fa-tools"></i>
                            Technical Stack
                        </h3>
                        
                        <ul class="features-list">
                            <li>
                                <i class="fab fa-python icon"></i>
                                <span>Python 3.11+ Backend</span>
                            </li>
                            <li>
                                <i class="fas fa-server icon"></i>
                                <span>Flask Web Framework</span>
                            </li>
                            <li>
                                <i class="fas fa-code icon"></i>
                                <span>Custom Parser Implementation</span>
                            </li>
                            <li>
                                <i class="fas fa-microchip icon"></i>
                                <span>x86 Assembly Target</span>
                            </li>
                            <li>
                                <i class="fas fa-cloud icon"></i>
                                <span>Deployed on Render.com</span>
                            </li>
                            <li>
                                <i class="fab fa-git-alt icon"></i>
                                <span>Version Control with Git</span>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <script>
        // State management
        let isCompiling = false;
        let currentExample = 0;

        // Example codes
        const examples = [
            {
                name: "Basic Variables",
                code: `// Basic variable declarations and operations
int x = 42;
int y = 15;
int sum = x + y;
string message = "The result is: ";

print(message + sum);`
            },
            {
                name: "Arithmetic Operations", 
                code: `// Demonstrating arithmetic operations
int a = 10;
int b = 3;

int addition = a + b;
int subtraction = a - b;
int multiplication = a * b;
int division = a / b;

print("Addition: " + addition);
print("Subtraction: " + subtraction);
print("Multiplication: " + multiplication);
print("Division: " + division);`
            },
            {
                name: "String Concatenation",
                code: `// String operations and concatenation
string firstName = "John";
string lastName = "Doe";
string fullName = firstName + " " + lastName;

int age = 25;
string bio = "Name: " + fullName + ", Age: " + age;

print(bio);`
            }
        ];

        async function compileCode() {
            if (isCompiling) return;
            
            const code = document.getElementById('codeInput').value.trim();
            if (!code) {
                showNotification('Please enter some code to compile!', 'warning');
                return;
            }
            
            setCompiling(true);
            
            try {
                const response = await fetch('/api/compile', {
                    method: 'POST',
                    headers: { 
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify({ 
                        code: code, 
                        filename: 'web_input_' + Date.now()
                    })
                });
                
                const result = await response.json();
                showOutput(result, response.ok);
                
            } catch (error) {
                console.error('Compilation error:', error);
                showOutput({ 
                    success: false, 
                    error: 'Network error: Unable to connect to compiler service. Please try again.' 
                }, false);
            } finally {
                setCompiling(false);
            }
        }
        
        async function loadExample() {
            try {
                // First try to load from API
                const response = await fetch('/api/examples');
                if (response.ok) {
                    const data = await response.json();
                    if (data.examples && data.examples.length > 0) {
                        const example = data.examples[currentExample % data.examples.length];
                        document.getElementById('codeInput').value = example.code;
                        currentExample++;
                        showNotification(`Loaded example: ${example.name}`, 'success');
                        return;
                    }
                }
            } catch (error) {
                console.log('API examples not available, using fallback');
            }
            
            // Fallback to local examples
            const example = examples[currentExample % examples.length];
            document.getElementById('codeInput').value = example.code;
            currentExample++;
            showNotification(`Loaded example: ${example.name}`, 'success');
        }
        
        function clearAll() {
            document.getElementById('codeInput').value = '';
            document.getElementById('outputSection').classList.remove('visible');
            showNotification('Editor cleared', 'info');
        }
        
        function setCompiling(compiling) {
            isCompiling = compiling;
            const button = document.querySelector('.btn-primary');
            const text = button.querySelector('.btn-text');
            
            if (compiling) {
                button.disabled = true;
                button.style.opacity = '0.7';
                text.innerHTML = '<div class="loading"><div class="spinner"></div>Compiling...</div>';
            } else {
                button.disabled = false;
                button.style.opacity = '1';
                text.innerHTML = 'Compile Code';
            }
        }
        
        function showOutput(result, success) {
            const outputSection = document.getElementById('outputSection');
            const outputContainer = document.getElementById('outputContainer');
            const outputContent = document.getElementById('outputContent');
            
            // Set status class
            outputSection.className = 'output-section visible ' + (success && result.success ? 'success' : 'error');
            
            let html = '';
            
            // Status
            html += `<div class="result-item">
                <div class="result-label">Compilation Status</div>
                <div class="result-value">
                    ${result.success ? 
                        '<i class="fas fa-check-circle" style="color: var(--success-color);"></i> Compilation Successful' : 
                        '<i class="fas fa-times-circle" style="color: var(--error-color);"></i> Compilation Failed'
                    }
                </div>
            </div>`;
            
            // Message
            if (result.message || result.error) {
                html += `<div class="result-item">
                    <div class="result-label">Message</div>
                    <div class="result-value">${result.message || result.error}</div>
                </div>`;
            }
            
            // Success results
            if (result.success) {
                // Symbol Table
                if (result.symbol_table && result.symbol_table.length > 0) {
                    html += `<div class="result-item">
                        <div class="result-label">Symbol Table</div>
                        <div class="result-value">${result.symbol_table.length} variables declared</div>
                        <details>
                            <summary>View Symbol Table Details</summary>
                            <pre>${JSON.stringify(result.symbol_table, null, 2)}</pre>
                        </details>
                    </div>`;
                }
                
                // Tokens
                if (result.tokens && result.tokens.length > 0) {
                    html += `<div class="result-item">
                        <div class="result-label">Lexical Analysis</div>
                        <div class="result-value">${result.tokens.length} tokens generated</div>
                        <details>
                            <summary>View Token Details</summary>
                            <pre>${JSON.stringify(result.tokens.slice(0, 20), null, 2)}${result.tokens.length > 20 ? '\\n... and ' + (result.tokens.length - 20) + ' more tokens' : ''}</pre>
                        </details>
                    </div>`;
                }
                
                // Assembly Code
                if (result.assembly) {
                    html += `<div class="result-item">
                        <div class="result-label">Generated Assembly</div>
                        <div class="result-value">x86 assembly code generated successfully</div>
                        <details>
                            <summary>View Assembly Code</summary>
                            <pre>${result.assembly}</pre>
                        </details>
                    </div>`;
                }
                
                // Preprocessed Code
                if (result.preprocessed) {
                    html += `<div class="result-item">
                        <div class="result-label">Preprocessed Code</div>
                        <div class="result-value">Code preprocessing completed</div>
                        <details>
                            <summary>View Preprocessed Code</summary>
                            <pre>${result.preprocessed}</pre>
                        </details>
                    </div>`;
                }
            }
            
            // Warning
            if (result.warning) {
                html += `<div class="result-item" style="border-left-color: var(--warning-color);">
                    <div class="result-label">Warning</div>
                    <div class="result-value">${result.warning}</div>
                </div>`;
            }
            
            // Debug info
            if (result.traceback && !success) {
                html += `<div class="result-item">
                    <div class="result-label">Debug Information</div>
                    <details>
                        <summary>View Technical Details</summary>
                        <pre>${result.traceback}</pre>
                    </details>
                </div>`;
            }
            
            outputContent.innerHTML = html;
            
            // Scroll to results
            outputSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
        
        function showNotification(message, type = 'info') {
            // Simple notification system
            const notification = document.createElement('div');
            notification.style.cssText = `
                position: fixed;
                top: 100px;
                right: 20px;
                background: ${type === 'success' ? 'var(--success-color)' : 
                            type === 'warning' ? 'var(--warning-color)' : 
                            type === 'error' ? 'var(--error-color)' : 'var(--primary-color)'};
                color: white;
                padding: 12px 20px;
                border-radius: 8px;
                font-weight: 600;
                font-size: 14px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.2);
                z-index: 10000;
                transform: translateX(100%);
                transition: transform 0.3s ease;
            `;
            notification.textContent = message;
            
            document.body.appendChild(notification);
            
            // Animate in
            setTimeout(() => {
                notification.style.transform = 'translateX(0)';
            }, 100);
            
            // Remove after delay
            setTimeout(() => {
                notification.style.transform = 'translateX(100%)';
                setTimeout(() => document.body.removeChild(notification), 300);
            }, 3000);
        }

        // Keyboard shortcuts
        document.addEventListener('keydown', function(e) {
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                e.preventDefault();
                compileCode();
            }
            
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                clearAll();
            }
        });

        // Auto-resize textarea
        const textarea = document.getElementById('codeInput');
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.max(300, this.scrollHeight) + 'px';
        });

        // Initialize with example
        document.addEventListener('DOMContentLoaded', function() {
            // Small delay to ensure everything is loaded
            setTimeout(() => {
                if (!document.getElementById('codeInput').value.trim()) {
                    loadExample();
                }
            }, 500);
        });
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    app.run(host='0.0.0.0', port=port, debug=debug) 