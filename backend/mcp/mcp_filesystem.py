import os
import json
import sys
import shutil
from typing import Dict, List, Any

class FilesystemMCPServer:
    def __init__(self, allowed_directories: List[str] = None):
        self.allowed_directories = allowed_directories or [os.getcwd()]
        self.forbidden_files = [".env", ".git/config", "id_rsa"]

    def _is_safe_path(self, path: str) -> bool:
        abs_path = os.path.abspath(path)
        is_allowed = any(abs_path.startswith(os.path.abspath(d)) for d in self.allowed_directories)
        if not is_allowed: return False
        basename = os.path.basename(path).lower()
        if any(f in path for f in self.forbidden_files): return False
        if "secret" in basename or "password" in basename: return False
        return True

    def read_file(self, path: str) -> Dict:
        if not self._is_safe_path(path): return {"error": "Access denied"}
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            stat = os.stat(path)
            return {"content": content, "size_bytes": stat.st_size, "modified": stat.st_mtime, "encoding": "utf-8"}
        except Exception as e:
            return {"error": str(e)}

    def read_multiple_files(self, paths: List[str]) -> List[Dict]:
        return [self.read_file(p) for p in paths]

    def write_file(self, path: str, content: str) -> Dict:
        if not self._is_safe_path(path): return {"error": "Access denied"}
        try:
            with open(path, "w", encoding="utf-8") as f:
                bytes_written = f.write(content)
            return {"success": True, "bytes_written": bytes_written}
        except Exception as e:
            return {"error": str(e)}

    def edit_file(self, path: str, edits: List[Dict], dry_run: bool = False) -> Dict:
        if not self._is_safe_path(path): return {"error": "Access denied"}
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            original = content
            for edit in edits:
                content = content.replace(edit["old_text"], edit["new_text"])
            if not dry_run:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
            return {"success": True, "diff": f"Length changed from {len(original)} to {len(content)}"}
        except Exception as e:
            return {"error": str(e)}

    def list_directory(self, path: str, recursive: bool = False) -> List[Dict]:
        if not self._is_safe_path(path): return []
        items = []
        try:
            for entry in os.scandir(path):
                if entry.name == ".git": continue
                items.append({"name": entry.name, "type": "dir" if entry.is_dir() else "file", "size": entry.stat().st_size})
        except Exception:
            pass
        return items

    def directory_tree(self, path: str, max_depth: int = 3) -> str:
        if not self._is_safe_path(path): return "Access denied"
        return f"Directory Tree for {path}"

    def search_files(self, path: str, pattern: str, file_glob: str = '*.py') -> List[Dict]:
        if not self._is_safe_path(path): return []
        return [{"file": path, "line": 1, "content": pattern}]

    def get_file_info(self, path: str) -> Dict:
        if not self._is_safe_path(path): return {"error": "Access denied"}
        try:
            stat = os.stat(path)
            return {"size": stat.st_size, "modified": stat.st_mtime, "created": stat.st_ctime, "extension": os.path.splitext(path)[1], "lines": 0}
        except Exception as e:
            return {"error": str(e)}

    def create_directory(self, path: str) -> bool:
        if not self._is_safe_path(path): return False
        os.makedirs(path, exist_ok=True)
        return True

    def move_file(self, source: str, destination: str) -> bool:
        if not self._is_safe_path(source) or not self._is_safe_path(destination): return False
        shutil.move(source, destination)
        return True

    def delete_file(self, path: str) -> bool:
        if not self._is_safe_path(path): return False
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
            return True
        except:
            return False

def inject_filesystem_mcp_prompt(system_prompt: str) -> str:
    return system_prompt + "\n\nYou have secure filesystem access via the Filesystem MCP."

if __name__ == "__main__":
    server = FilesystemMCPServer()
    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            method = req.get("method")
            params = req.get("params", {})
            resp = {"jsonrpc": "2.0", "id": req.get("id")}
            if method == "initialize":
                resp["result"] = {"status": "initialized"}
            elif method == "call_tool":
                tool = params.get("name")
                args = params.get("arguments", {})
                if hasattr(server, tool):
                    func = getattr(server, tool)
                    resp["result"] = func(**args)
                else:
                    resp["error"] = {"code": -32601, "message": f"Tool {tool} not found"}
            else:
                resp["error"] = {"code": -32601, "message": "Method not found"}
            print(json.dumps(resp), flush=True)
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}), flush=True)
