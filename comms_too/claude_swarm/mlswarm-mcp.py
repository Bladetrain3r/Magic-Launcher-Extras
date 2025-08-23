#!/usr/bin/env python3
"""
MLSwarm MCP Server - Bridge between Claude and MLSwarm
Just reads and writes to swarm files. That's it.
"""

import asyncio
import json
import logging
import os
import sys
from typing import Any, Dict, List, Optional
import aiohttp
from base64 import b64encode
from datetime import datetime

from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

# Configure these for your setup - read from environment
SWARM_URL = os.environ.get("SWARM_URL", "http://localhost:8080").rstrip('/')
SWARM_USER = os.environ.get("SWARM_USER", "swarm")
SWARM_PASS = os.environ.get("SWARM_PASS", "swarm")

# The blessed whitelist
ALLOWED_SWARMS = [
    'swarm.txt',
    'general.txt', 
    'random.txt',
    'tech.txt',
    'gaming.txt'
]

# Set up logging to stderr so it appears in Claude logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

# Create the server instance
server = Server("mlswarm")

def make_auth_header() -> Dict[str, str]:
    """Create basic auth header"""
    auth_string = f"{SWARM_USER}:{SWARM_PASS}"
    auth_bytes = auth_string.encode('ascii')
    auth_b64 = b64encode(auth_bytes).decode('ascii')
    return {"Authorization": f"Basic {auth_b64}"}

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools"""
    return [
        types.Tool(
            name="swarm_read",
            description="Read messages from a swarm file",
            inputSchema={
                "type": "object",
                "properties": {
                    "file": {
                        "type": "string",
                        "description": "Swarm file to read",
                        "enum": ALLOWED_SWARMS
                    },
                    "last_n": {
                        "type": "integer",
                        "description": "Number of recent lines to return (default: 50)",
                        "default": 50
                    }
                },
                "required": ["file"]
            }
        ),
        types.Tool(
            name="swarm_send",
            description="Send a message to a swarm file",
            inputSchema={
                "type": "object",
                "properties": {
                    "file": {
                        "type": "string",
                        "description": "Swarm file to write to",
                        "enum": ALLOWED_SWARMS
                    },
                    "nick": {
                        "type": "string",
                        "description": "Nickname to use",
                        "default": "Claude"
                    },
                    "message": {
                        "type": "string",
                        "description": "Message to send"
                    }
                },
                "required": ["file", "message"]
            }
        ),
        types.Tool(
            name="swarm_list",
            description="List available swarm files",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool calls"""
    
    if name == "swarm_read":
        return await handle_read(arguments or {})
    elif name == "swarm_send":
        return await handle_send(arguments or {})
    elif name == "swarm_list":
        return await handle_list(arguments or {})
    else:
        raise ValueError(f"Unknown tool: {name}")

async def handle_read(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Read messages from a swarm file"""
    file = arguments.get("file")
    last_n = arguments.get("last_n", 50)
    
    # Nuclear whitelist check (even though schema enforces it)
    if file not in ALLOWED_SWARMS:
        return [types.TextContent(
            type="text",
            text=f"Error: File '{file}' not in allowed list"
        )]
    
    auth_header = make_auth_header()
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{SWARM_URL}/swarm/{file}",
                headers=auth_header
            ) as response:
                if response.status == 200:
                    content = await response.text()
                    lines = content.strip().split('\n')
                    
                    # Get last N lines
                    recent_lines = lines[-last_n:] if len(lines) > last_n else lines
                    
                    result = f"=== Last {len(recent_lines)} messages from {file} ===\n"
                    result += '\n'.join(recent_lines)
                    
                    return [types.TextContent(type="text", text=result)]
                else:
                    return [types.TextContent(
                        type="text",
                        text=f"Error: HTTP {response.status}"
                    )]
                    
    except Exception as e:
        logger.error(f"Error reading swarm: {e}")
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]

async def handle_send(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Send a message to a swarm file"""
    file = arguments.get("file")
    nick = arguments.get("nick", "Claude")
    message = arguments.get("message")
    
    # Nuclear whitelist check
    if file not in ALLOWED_SWARMS:
        return [types.TextContent(
            type="text",
            text=f"Error: File '{file}' not in allowed list"
        )]
    
    auth_header = make_auth_header()
    
    # Format message with timestamp
    timestamp = datetime.now().strftime("%H:%M")
    chat_line = f"[{timestamp}] <{nick}> {message}\n"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{SWARM_URL}/swarm/{file}",
                headers={**auth_header, "Content-Type": "text/plain"},
                data=chat_line
            ) as response:
                if response.status == 200:
                    return [types.TextContent(
                        type="text",
                        text=f"Message sent to {file}"
                    )]
                else:
                    return [types.TextContent(
                        type="text",
                        text=f"Error: HTTP {response.status}"
                    )]
                    
    except Exception as e:
        logger.error(f"Error sending to swarm: {e}")
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]

async def handle_list(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """List available swarm files"""
    result = "=== Available Swarm Files ===\n"
    for file in ALLOWED_SWARMS:
        result += f"• {file}\n"
    result += f"\nTotal: {len(ALLOWED_SWARMS)} swarms"
    return [types.TextContent(type="text", text=result)]

@server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    """List available resources"""
    # Return empty list - we don't need resources for this simple server
    return []

@server.read_resource()
async def handle_read_resource(uri: str) -> str:
    """Read a resource"""
    # Should never be called since we have no resources
    raise ValueError(f"No resources available")

@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    """List available prompts"""
    # Return empty list - we don't need prompts for this simple server
    return []

@server.get_prompt()
async def handle_get_prompt(
    name: str, arguments: dict | None
) -> types.GetPromptResult:
    """Get a prompt"""
    # Should never be called since we have no prompts
    raise ValueError(f"No prompts available")

async def main():
    """Run the MCP server"""
    # Log actual configuration being used (to stderr for Claude logs)
    print(f"MLSwarm MCP Server starting...", file=sys.stderr)
    print(f"SWARM_URL: {SWARM_URL}", file=sys.stderr)
    print(f"SWARM_USER: {SWARM_USER}", file=sys.stderr)
    print(f"Available swarms: {', '.join(ALLOWED_SWARMS)}", file=sys.stderr)
    
    # Run using stdio transport
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="mlswarm",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                )
            )
        )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("MLSwarm MCP Server stopped")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise