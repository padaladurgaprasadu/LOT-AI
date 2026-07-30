import os
import time
import subprocess
import tempfile
import json
from typing import Dict, Any

def run_code(code: str, language: str = 'python', timeout_s: int = 10) -> Dict[str, Any]:
    """
    Run code in a secure sandbox.
    """
    safe = True
    
    # Simple block list
    if language == 'python':
        blocked = ['os.system', 'subprocess', 'socket', 'eval', 'exec']
        for b in blocked:
            if b in code:
                return {'stdout': '', 'stderr': f'Blocked dangerous import/call: {b}', 'exit_code': -1, 'runtime_ms': 0, 'language': language, 'safe': False}
    elif language == 'javascript':
        blocked = ['fs.rmSync', 'child_process', 'net']
        for b in blocked:
            if b in code:
                return {'stdout': '', 'stderr': f'Blocked dangerous API: {b}', 'exit_code': -1, 'runtime_ms': 0, 'language': language, 'safe': False}
    else:
        return {'stdout': '', 'stderr': 'Unsupported language', 'exit_code': -1, 'runtime_ms': 0, 'language': language, 'safe': False}

    ext = 'py' if language == 'python' else 'js'
    cmd_prefix = ['python'] if language == 'python' else ['node']
    
    with tempfile.NamedTemporaryFile(suffix=f'.{ext}', delete=False, mode='w') as f:
        f.write(code)
        temp_path = f.name
        
    start_time = time.time()
    try:
        process = subprocess.run(
            cmd_prefix + [temp_path],
            capture_output=True,
            text=True,
            timeout=timeout_s
        )
        stdout = process.stdout
        stderr = process.stderr
        exit_code = process.returncode
    except subprocess.TimeoutExpired:
        stdout = ''
        stderr = 'Timeout expired'
        exit_code = -1
        safe = False
    except Exception as e:
        stdout = ''
        stderr = str(e)
        exit_code = -1
        safe = False
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
    runtime_ms = int((time.time() - start_time) * 1000)
    
    return {
        'stdout': stdout,
        'stderr': stderr,
        'exit_code': exit_code,
        'runtime_ms': runtime_ms,
        'language': language,
        'safe': safe
    }
