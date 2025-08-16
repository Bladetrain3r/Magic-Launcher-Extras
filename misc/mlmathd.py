#!/usr/bin/env python3
"""
MLMathD - Math Coprocessor Protocol
A daemon that provides deterministic math over HTTP/pipe/socket
Natural language agents can't be trusted with arithmetic
Under 250 lines of numerical honesty
"""

import json
import sys
import math
import socket
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

# Safe math environment - no imports, no file access, just math
SAFE_MATH = {
    # Basic arithmetic is built-in
    'abs': abs, 'round': round, 'min': min, 'max': max,
    'sum': sum, 'pow': pow, 'divmod': divmod,
    
    # Math module functions
    'sqrt': math.sqrt, 'log': math.log, 'log10': math.log10,
    'exp': math.exp, 'sin': math.sin, 'cos': math.cos,
    'tan': math.tan, 'pi': math.pi, 'e': math.e,
    'floor': math.floor, 'ceil': math.ceil,
    'factorial': math.factorial, 'gcd': math.gcd,
    
    # Constants for common calculations
    'KB': 1024, 'MB': 1048576, 'GB': 1073741824,
    'HOUR': 3600, 'DAY': 86400, 'YEAR': 31536000,
}

class MathProcessor:
    """Deterministic math evaluation"""
    
    @staticmethod
    def evaluate(expression, variables=None):
        """Safely evaluate math expressions"""
        try:
            # Merge variables into safe environment
            env = SAFE_MATH.copy()
            if variables:
                env.update(variables)
            
            # Evaluate with restricted environment
            result = eval(expression, {"__builtins__": {}}, env)
            
            # Return full precision and formatted versions
            return {
                'success': True,
                'expression': expression,
                'result': result,
                'type': type(result).__name__,
                'formatted': MathProcessor.format_result(result)
            }
        except ZeroDivisionError:
            return {
                'success': False,
                'error': 'Division by zero',
                'expression': expression
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'expression': expression
            }
    
    @staticmethod
    def format_result(value):
        """Format results for human reading"""
        if isinstance(value, bool):
            return str(value)
        elif isinstance(value, int):
            return f"{value:,}"
        elif isinstance(value, float):
            if value.is_integer():
                return f"{int(value):,}"
            elif abs(value) > 1000000 or abs(value) < 0.0001:
                return f"{value:.6e}"
            else:
                return f"{value:.6f}".rstrip('0').rstrip('.')
        else:
            return str(value)
    
    @staticmethod
    def batch_evaluate(expressions):
        """Evaluate multiple expressions"""
        results = []
        variables = {}
        
        for expr in expressions:
            # Handle variable assignment
            if '=' in expr and not any(op in expr for op in ['==', '!=', '<=', '>=']):
                parts = expr.split('=', 1)
                var_name = parts[0].strip()
                var_expr = parts[1].strip()
                
                # Evaluate the right side
                result = MathProcessor.evaluate(var_expr, variables)
                if result['success']:
                    variables[var_name] = result['result']
                    result['variable'] = var_name
                results.append(result)
            else:
                # Regular expression
                results.append(MathProcessor.evaluate(expr, variables))
        
        return results

class HTTPHandler(BaseHTTPRequestHandler):
    """HTTP interface for math coprocessor"""
    
    def do_POST(self):
        """Handle math requests"""
        if self.path != '/calculate':
            self.send_error(404)
            return
        
        try:
            length = int(self.headers['Content-Length'])
            data = json.loads(self.rfile.read(length))
            
            if 'expression' in data:
                # Single expression
                result = MathProcessor.evaluate(
                    data['expression'],
                    data.get('variables', {})
                )
            elif 'expressions' in data:
                # Batch processing
                result = {
                    'batch': True,
                    'results': MathProcessor.batch_evaluate(data['expressions'])
                }
            else:
                result = {'success': False, 'error': 'No expression provided'}
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result, indent=2).encode())
            
        except Exception as e:
            self.send_error(500, str(e))
    
    def do_GET(self):
        """Simple calculation via GET"""
        if self.path.startswith('/calc/'):
            expression = self.path[6:]  # Remove /calc/
            result = MathProcessor.evaluate(expression)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result, indent=2).encode())
        else:
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"MLMathD - Math Coprocessor Protocol\n")
            self.wfile.write(b"POST /calculate with {expression: '2+2'}\n")
            self.wfile.write(b"GET /calc/2+2\n")
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass

def socket_server(port=9999):
    """Raw socket interface for maximum speed"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', port))
    server.listen(5)
    print(f"Socket server on port {port}")
    
    while True:
        client, addr = server.accept()
        expression = client.recv(1024).decode().strip()
        
        if expression:
            result = MathProcessor.evaluate(expression)
            if result['success']:
                response = str(result['result'])
            else:
                response = f"ERROR: {result['error']}"
            client.send(response.encode())
        
        client.close()

def pipe_mode():
    """Pipe mode for command line usage"""
    print("MLMathD Pipe Mode (one expression per line, Ctrl+D to exit)")
    
    variables = {}
    for line in sys.stdin:
        expression = line.strip()
        if not expression or expression.startswith('#'):
            continue
        
        result = MathProcessor.evaluate(expression, variables)
        
        if result['success']:
            # Check for variable assignment
            if 'variable' in result:
                variables[result['variable']] = result['result']
                print(f"{result['variable']} = {result['formatted']}")
            else:
                print(result['formatted'])
        else:
            print(f"ERROR: {result['error']}", file=sys.stderr)

def test_mode():
    """Run verification tests"""
    tests = [
        ("2 + 2", 4),
        ("771866 / 4", 192966.5),
        ("sqrt(2)", 1.4142135623730951),
        ("1.56e22 / 1e24", 0.0156),
        ("10 * KB", 10240),
        ("factorial(10)", 3628800),
        ("log10(1000000)", 6.0),
        ("3.14159 * (10 ** 2)", 314.159),
    ]
    
    print("Running math verification tests...")
    passed = 0
    for expr, expected in tests:
        result = MathProcessor.evaluate(expr)
        if result['success']:
            if abs(result['result'] - expected) < 1e-10:
                print(f"✓ {expr} = {result['result']}")
                passed += 1
            else:
                print(f"✗ {expr} = {result['result']} (expected {expected})")
        else:
            print(f"✗ {expr} failed: {result['error']}")
    
    print(f"\n{passed}/{len(tests)} tests passed")
    return passed == len(tests)

def main():
    """Multi-mode math coprocessor"""
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'test':
            # Run tests
            sys.exit(0 if test_mode() else 1)
        
        elif sys.argv[1] == 'daemon':
            # HTTP daemon mode
            port = int(sys.argv[2]) if len(sys.argv) > 2 else 8888
            print(f"MLMathD HTTP on port {port}")
            print(f"Usage: curl -X POST http://localhost:{port}/calculate -d '{{\"expression\":\"2+2\"}}'")
            server = HTTPServer(('', port), HTTPHandler)
            server.serve_forever()
        
        elif sys.argv[1] == 'socket':
            # Raw socket mode
            port = int(sys.argv[2]) if len(sys.argv) > 2 else 9999
            socket_server(port)
        
        elif sys.argv[1] == 'pipe':
            # Explicit pipe mode
            pipe_mode()
        
        else:
            # Direct calculation
            expression = ' '.join(sys.argv[1:])
            result = MathProcessor.evaluate(expression)
            if result['success']:
                print(result['formatted'])
            else:
                print(f"ERROR: {result['error']}", file=sys.stderr)
                sys.exit(1)
    else:
        # Default to pipe mode if stdin is not a terminal
        if not sys.stdin.isatty():
            pipe_mode()
        else:
            print("MLMathD - Math Coprocessor Protocol")
            print("\nUsage:")
            print("  mlmathd.py <expression>      # Direct calculation")
            print("  mlmathd.py daemon [port]     # HTTP server mode")
            print("  mlmathd.py socket [port]     # Raw socket mode")
            print("  mlmathd.py pipe              # Pipe mode")
            print("  mlmathd.py test              # Run verification")
            print("\nExamples:")
            print("  mlmathd.py '771866 / 4'")
            print("  echo '2 + 2' | mlmathd.py")
            print("  mlmathd.py daemon 8888")
            print("\nHTTP API:")
            print("  curl -X POST http://localhost:8888/calculate \\")
            print("    -d '{\"expression\":\"sqrt(2)\"}'")

if __name__ == '__main__':
    main()