import os
import subprocess
import threading
import time

class SandboxExecuter:
    """The yAI Sandbox Executer: Writes files and runs terminal commands autonomously."""
    
    def __init__(self, sandbox_dir="yai_workspace"):
        self.sandbox_dir = os.path.abspath(sandbox_dir)
        if not os.path.exists(self.sandbox_dir):
            os.makedirs(self.sandbox_dir)
            print(f"[Sandbox] Initialized workspace at {self.sandbox_dir}")
            
    def write_files(self, files_dict: dict):
        """
        Takes a dictionary of {filepath: content} and writes them to the sandbox.
        """
        print(f"\n[Sandbox] Writing {len(files_dict)} files to workspace...")
        for rel_path, content in files_dict.items():
            full_path = os.path.join(self.sandbox_dir, rel_path)
            # Ensure parent directories exist
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  -> Created: {rel_path}")
            
    def run_command(self, command: str) -> dict:
        """
        Executes a shell command in the sandbox and returns stdout/stderr.
        This is the foundation for the Self-Healing Loop.
        """
        print(f"\n[Sandbox] Running command: `{command}`")
        try:
            result = subprocess.run(
                command,
                cwd=self.sandbox_dir,
                shell=True,
                capture_output=True,
                text=True,
                timeout=60 # Increased timeout for npm installs
            )
            
            output = {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "code": result.returncode
            }
            
            if output["success"]:
                print("[Sandbox] Command succeeded.")
            else:
                print(f"[Sandbox] Command failed with code {result.returncode}. (Triggering Debugger Agent...)")
                
            return output
            
        except subprocess.TimeoutExpired:
            print("[Sandbox] Command timed out.")
            return {"success": False, "stdout": "", "stderr": "Command timed out after 60 seconds.", "code": 124}
            
    def start_preview_server(self, command: str, port: int):
        """
        Spins up a background thread running the server so the user can preview it instantly.
        """
        print(f"\n[Live Preview] Starting server on port {port}...")
        
        def run_server():
            subprocess.run(command, cwd=self.sandbox_dir, shell=True)
            
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        
        # Give it a second to spin up
        time.sleep(2)
        print(f"\n[Live Preview] Server is live! Preview at: http://localhost:{port}")
        return True

if __name__ == "__main__":
    # Test the sandbox functionality
    print("Testing Sandbox Executer...")
    executer = SandboxExecuter("test_yai_workspace")
    
    # Test file writing
    executer.write_files({
        "index.html": "<h1>yAI Live Preview Test</h1>",
        "css/style.css": "h1 { color: blue; }"
    })
    
    # Test command execution
    result = executer.run_command("dir")
    print("\nCommand stdout:", result["stdout"])
    print("Sandbox Test Complete.")
