# calc_mcp.py - Proper MCP server
import asyncio
import json
import sys
import math
from typing import Any, Dict

import asyncio
import json
import sys
import math
from typing import Any, Dict, Optional
from random import randint

class CalcMCP:
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id", 0)  # Default to 0, not null
        
        # Always include jsonrpc and id
        base_response = {
            "jsonrpc": "2.0",
            "id": request_id
        }
        
        if method == "initialize":
            return {
                **base_response,
                "result": {
                    "protocolVersion": "2025-06-18",
                    "capabilities": {
                        "tools": {
                            "listChanged": False
                        }
                    },
                    "serverInfo": {
                        "name": "calc-mcp",
                        "version": "1.0.0"
                    }
                }
            }
        
        elif method == "tools/list":
            return {
                **base_response,
                "result": {
                    "tools": [{
                        "name": "calculate",
                        "description": "Evaluate mathematical expressions. No imports.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "expr": {"type": "string"}
                            },
                            "required": ["expr"]
                        }
                    },
                    {
                        "name": "random_number",
                        "description": "Generate a random number between min and max.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "min": {"type": "integer"},
                                "max": {"type": "integer"}
                            },
                            "required": ["min", "max"]
                        }
                    }
                    ]
                }
            }
        
        elif method == "tools/call":
            tool_name = params.get("name")
            if tool_name == "calculate":
                try:
                    expr = params.get("arguments", {}).get("expr", "")
                    result = eval(expr, {"__builtins__": {}, **math.__dict__})
                    return {
                        **base_response,
                        "result": {
                            "content": [{
                                "type": "text",
                                "text": str(result)
                            }]
                        }
                    }
                except Exception as e:
                    # Use error in result, not at top level
                    return {
                        **base_response,
                        "result": {
                            "content": [{
                                "type": "text", 
                                "text": f"Error: {str(e)}"
                            }],
                            "isError": True
                        }
                    }
            elif tool_name == "random_number":
                min_value = params.get("arguments", {}).get("min", 1)
                max_value = params.get("arguments", {}).get("max", 100)
                result = randint(min_value, max_value)
                return {
                    **base_response,
                    "result": {
                        "content": [{
                            "type": "text",
                            "text": str(result)
                        }]
                    }
                }

        # Method not found - use proper JSON-RPC error format
        return {
            **base_response,
            "error": {
                "code": -32601,
                "message": "Method not found"
            }
        }

async def main():
    calc = CalcMCP()
    
    while True:
        try:
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not line:
                break
                
            request = json.loads(line.strip())
            response = await calc.handle_request(request)
            print(json.dumps(response), flush=True)
            
        except Exception as e:
            print(json.dumps({
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32603, "message": str(e)}
            }), flush=True)

if __name__ == "__main__":
    asyncio.run(main())