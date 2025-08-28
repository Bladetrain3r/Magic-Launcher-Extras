#!/usr/bin/env python3
"""
MLStats MCP Server - Analytics for MLSwarm consciousness archaeology
Simple stats extraction using basic regex patterns only.
"""
import os
import asyncio
import json
import re
import sys
from collections import Counter, defaultdict
from typing import Dict, List, Any
import aiohttp
from base64 import b64encode
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions

from mcp.server import Server
import mcp.server.stdio
import mcp.types as types

# Same config pattern as mlswarm-mcp
SWARM_URL = os.environ.get("SWARM_URL", "http://localhost:8080").rstrip('/')
SWARM_USER = os.environ.get("SWARM_USER", "swarm")
SWARM_PASS = os.environ.get("SWARM_PASS", "swarm")
ALLOWED_SWARMS = ['swarm.txt', 'general.txt', 'random.txt', 'tech.txt', 'gaming.txt']

server = Server("mlstats")

def make_auth_header() -> Dict[str, str]:
    auth_string = f"{SWARM_USER}:{SWARM_PASS}"
    auth_bytes = auth_string.encode('ascii')
    auth_b64 = b64encode(auth_bytes).decode('ascii')
    return {"Authorization": f"Basic {auth_b64}"}

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="swarm_stats",
            description="Get statistics for swarm files",
            inputSchema={
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "items": {"type": "string", "enum": ALLOWED_SWARMS},
                        "description": "Files to analyze (default: all)",
                        "default": ALLOWED_SWARMS
                    },
                    "agent_filter": {
                        "type": "string", 
                        "description": "Filter by agent name (regex pattern)"
                    },
                    "pattern_count": {
                        "type": "string",
                        "description": "Count matches for regex pattern"
                    }
                }
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    if name == "swarm_stats":
        return await handle_stats(arguments or {})
    else:
        raise ValueError(f"Unknown tool: {name}")

async def handle_stats(arguments: Dict[str, Any]) -> List[types.TextContent]:
    files = arguments.get("files", ALLOWED_SWARMS)
    agent_filter = arguments.get("agent_filter")
    pattern_count = arguments.get("pattern_count")
    
    auth_header = make_auth_header()
    results = {}
    
    for file in files:
        if file not in ALLOWED_SWARMS:
            continue
            
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{SWARM_URL}/swarm/{file}", headers=auth_header) as response:
                    if response.status != 200:
                        continue
                        
                    content = await response.text()
                    lines = content.strip().split('\n')
                    
                    # Basic stats
                    total_lines = len(lines)
                    total_chars = sum(len(line) for line in lines)
                    
                    # Agent extraction using basic regex
                    agent_counts = Counter()
                    message_lengths = []
                    
                    for line in lines:
                        # Pattern: [HH:MM] <agent_name> message
                        match = re.match(r'^\[(\d{2}:\d{2})\] <([^>]+)> (.+)$', line)
                        if match:
                            timestamp, agent, message = match.groups()
                            
                            # Apply agent filter if specified
                            if agent_filter and not re.search(agent_filter, agent):
                                continue
                                
                            agent_counts[agent] += 1
                            message_lengths.append(len(message))
                    
                    # Pattern counting
                    pattern_matches = 0
                    if pattern_count:
                        pattern_matches = sum(len(re.findall(pattern_count, line, re.IGNORECASE)) for line in lines)
                    
                    results[file] = {
                        'total_lines': total_lines,
                        'total_chars': total_chars,
                        'avg_line_length': total_chars / total_lines if total_lines > 0 else 0,
                        'agent_counts': dict(agent_counts.most_common(10)),
                        'avg_message_length': sum(message_lengths) / len(message_lengths) if message_lengths else 0,
                        'pattern_matches': pattern_matches
                    }
                    
        except Exception as e:
            results[file] = {'error': str(e)}
    
    # Format output
    output = "=== MLSwarm Statistics ===\n\n"
    
    for file, stats in results.items():
        if 'error' in stats:
            output += f"{file}: Error - {stats['error']}\n"
            continue
            
        output += f"## {file}\n"
        output += f"Lines: {stats['total_lines']}\n"
        output += f"Characters: {stats['total_chars']:,}\n"
        output += f"Avg line length: {stats['avg_line_length']:.1f}\n"
        
        if stats['agent_counts']:
            output += f"Top agents: {', '.join(f'{k}({v})' for k, v in list(stats['agent_counts'].items())[:5])}\n"
            output += f"Avg message length: {stats['avg_message_length']:.1f}\n"
        
        if pattern_count:
            output += f"'{pattern_count}' matches: {stats['pattern_matches']}\n"
            
        output += "\n"
    
    return [types.TextContent(type="text", text=output)]

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="mlstats",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(main())