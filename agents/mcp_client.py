import json
import subprocess
import asyncio
from typing import List, Dict, Any

class yAIMCPClient:
    """
    Model Context Protocol (MCP) Client for yAI.
    Allows yAI Agents (specifically the Executer) to connect to native OS resources
    like File Systems, Emails, Databases, and custom enterprise tools via MCP servers.
    This gives yAI the OS-level integration required to crush single-sandbox tools.
    """
    
    def __init__(self):
        # Dictionary of registered MCP server commands
        self.mcp_servers = {
            "filesystem": ["npx", "-y", "@modelcontextprotocol/server-filesystem", "./sandbox"],
            "fetch": ["npx", "-y", "@modelcontextprotocol/server-fetch"]
        }
        self.active_processes = {}

    async def connect_server(self, server_name: str):
        """Starts an MCP server process communicating via stdio."""
        if server_name not in self.mcp_servers:
            raise ValueError(f"MCP server {server_name} not registered.")
            
        cmd = self.mcp_servers[server_name]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        self.active_processes[server_name] = process
        print(f"[yAIMCPClient] Connected to MCP server: {server_name}")
        return process

    async def call_tool(self, server_name: str, tool_name: str, arguments: dict) -> dict:
        """Calls a specific tool on an active MCP server via JSON-RPC."""
        if server_name not in self.active_processes:
            await self.connect_server(server_name)
            
        process = self.active_processes[server_name]
        
        # Format the JSON-RPC request compliant with MCP spec
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }
        
        # Send to server via stdin
        req_bytes = (json.dumps(request) + "\n").encode()
        process.stdin.write(req_bytes)
        await process.stdin.drain()
        
        # Read response from stdout
        response_line = await process.stdout.readline()
        if not response_line:
            err = await process.stderr.read()
            raise RuntimeError(f"MCP Server error: {err.decode()}")
            
        return json.loads(response_line.decode())

# Singleton client for the OS
mcp_client = yAIMCPClient()

# Example Usage by the Executer Agent:
# async def fetch_email():
#     result = await mcp_client.call_tool("fetch", "fetch_url", {"url": "https://api.internal/emails/latest"})
#     print(result)
