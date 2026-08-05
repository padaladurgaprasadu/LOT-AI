import json
import subprocess
import threading
import uuid
from typing import Dict, List, Any, Optional

try:
    from backend.utils.logger import get_logger
    logger = get_logger(__name__)
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

class yAIMCPManager:
    def __init__(self):
        self.servers: Dict[str, Dict] = {}
        self.processes: Dict[str, subprocess.Popen] = {}
        self.tools: Dict[str, Dict[str, Dict]] = {}
        self._register_builtin_servers()

    def _register_builtin_servers(self):
        # Auto-register all 5 built-in MCP servers on init
        self.register_server("context7", "stdio", ["python", "-m", "backend.mcp.mcp_context7"])
        self.register_server("github", "stdio", ["python", "-m", "backend.mcp.mcp_github"])
        self.register_server("playwright", "stdio", ["python", "-m", "backend.mcp.mcp_playwright"])
        self.register_server("sequential_thinking", "stdio", ["python", "-m", "backend.mcp.mcp_sequential_thinking"])
        self.register_server("filesystem", "stdio", ["python", "-m", "backend.mcp.mcp_filesystem"])

    def register_server(self, name: str, transport: str, command: List[str]) -> Dict:
        self.servers[name] = {
            "name": name,
            "transport": transport,
            "command": command,
            "status": "registered"
        }
        self.tools[name] = {}
        logger.info(f"Registered MCP server: {name}")
        return self.servers[name]

    def connect_server(self, name: str) -> bool:
        if name not in self.servers:
            logger.error(f"Server {name} not registered")
            return False
            
        server_config = self.servers[name]
        try:
            process = subprocess.Popen(
                server_config["command"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            self.processes[name] = process
            self.servers[name]["status"] = "connected"
            logger.info(f"Connected to MCP server: {name}")
            
            # Fetch tools via initialization
            init_response = self._send_jsonrpc(name, "initialize", {"protocolVersion": "2.0"})
            if init_response and "result" in init_response:
                logger.info(f"Initialized server {name} successfully")
                
            return True
        except Exception as e:
            logger.error(f"Failed to connect to server {name}: {e}")
            return False

    def disconnect_server(self, name: str) -> bool:
        if name in self.processes:
            process = self.processes[name]
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            del self.processes[name]
            self.servers[name]["status"] = "disconnected"
            logger.info(f"Disconnected server: {name}")
            return True
        return False

    def list_tools(self, server_name: str = None) -> List[Dict]:
        tools_list = []
        if server_name:
            if server_name in self.tools:
                for tool_name, tool_data in self.tools[server_name].items():
                    tools_list.append({"server": server_name, **tool_data})
        else:
            for srv_name, srv_tools in self.tools.items():
                for tool_name, tool_data in srv_tools.items():
                    tools_list.append({"server": srv_name, **tool_data})
        return tools_list

    def register_mcp_tool(self, server_name: str, tool_name: str, description: str, parameters: dict):
        if server_name not in self.tools:
            self.tools[server_name] = {}
        self.tools[server_name][tool_name] = {
            "name": tool_name,
            "description": description,
            "parameters": parameters
        }
        logger.info(f"Registered tool {tool_name} for server {server_name}")

    def call_tool(self, server_name: str, tool_name: str, arguments: Dict) -> Dict:
        if server_name not in self.processes:
            logger.warning(f"Server {server_name} not connected, attempting to connect")
            if not self.connect_server(server_name):
                return {"error": f"Failed to connect to server {server_name}"}
                
        response = self._send_jsonrpc(server_name, "call_tool", {
            "name": tool_name,
            "arguments": arguments
        })
        return response

    def _send_jsonrpc(self, server_name: str, method: str, params: Dict) -> Dict:
        if server_name not in self.processes:
            return {"error": {"code": -32000, "message": "Server not connected"}}
            
        process = self.processes[server_name]
        request_id = str(uuid.uuid4())
        request = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": method,
            "params": params
        }
        
        try:
            request_str = json.dumps(request) + "\n"
            process.stdin.write(request_str)
            process.stdin.flush()
            
            response_str = process.stdout.readline()
            if not response_str:
                return {"error": {"code": -32000, "message": "Server closed connection"}}
                
            response = json.loads(response_str)
            return response
        except Exception as e:
            logger.error(f"JSON-RPC error for server {server_name}: {e}")
            return {"error": {"code": -32603, "message": str(e)}}

    def get_langchain_tools(self) -> List:
        try:
            from langchain.tools import StructuredTool
        except ImportError:
            logger.error("LangChain not installed")
            return []
            
        langchain_tools = []
        for server_name, server_tools in self.tools.items():
            for tool_name, tool_data in server_tools.items():
                def _create_tool_func(s_name=server_name, t_name=tool_name):
                    def _tool_func(**kwargs):
                        return self.call_tool(s_name, t_name, kwargs)
                    return _tool_func
                
                langchain_tools.append(StructuredTool.from_function(
                    func=_create_tool_func(),
                    name=f"{server_name}_{tool_name}",
                    description=tool_data.get("description", "")
                ))
        return langchain_tools

    def get_all_tools_for_prompt(self) -> str:
        prompt = "Available MCP Tools:\n"
        for server_name, server_tools in self.tools.items():
            prompt += f"\nServer: {server_name}\n"
            for tool_name, tool_data in server_tools.items():
                prompt += f"  - {tool_name}: {tool_data.get('description', '')}\n"
                prompt += f"    Parameters: {json.dumps(tool_data.get('parameters', {}))}\n"
        return prompt
