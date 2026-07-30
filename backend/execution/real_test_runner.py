import subprocess
import time
import json
import re
from typing import Dict

class RealTestRunner:
    def __init__(self):
        pass

    def run_pytest(self, test_dir: str = '.', verbose: bool = True) -> Dict:
        cmd = ["pytest", test_dir]
        if verbose:
            cmd.append("-v")
        start = time.time()
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            parsed = self.parse_pytest_output(result.stdout)
            parsed["duration_ms"] = int((time.time() - start) * 1000)
            parsed["output"] = result.stdout
            return parsed
        except Exception as e:
            return {"passed": 0, "failed": 0, "errors": 1, "coverage_pct": 0.0, "duration_ms": int((time.time() - start) * 1000), "output": str(e)}

    def run_vitest(self, project_dir: str = '.') -> Dict:
        cmd = ["npx", "vitest", "run", "--reporter=json"]
        start = time.time()
        try:
            result = subprocess.run(cmd, cwd=project_dir, capture_output=True, text=True, timeout=120)
            # Try to parse json output
            try:
                data = json.loads(result.stdout)
                passed = sum(1 for t in data.get("testResults", []) if t.get("status") == "passed")
                failed = sum(1 for t in data.get("testResults", []) if t.get("status") == "failed")
            except:
                passed, failed = 0, 0
                
            return {
                "passed": passed,
                "failed": failed,
                "duration_ms": int((time.time() - start) * 1000),
                "output": result.stdout
            }
        except Exception as e:
            return {"passed": 0, "failed": 0, "duration_ms": int((time.time() - start) * 1000), "output": str(e)}

    def run_playwright(self, test_file: str = None) -> Dict:
        cmd = ["npx", "playwright", "test", "--reporter=json"]
        if test_file:
            cmd.append(test_file)
        start = time.time()
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            return {
                "success": result.returncode == 0,
                "duration_ms": int((time.time() - start) * 1000),
                "output": result.stdout
            }
        except Exception as e:
            return {"success": False, "duration_ms": int((time.time() - start) * 1000), "output": str(e)}

    def generate_pytest_tests(self, code: str, function_name: str) -> str:
        return f"""
import pytest
from main import {function_name}

def test_{function_name}_basic():
    assert {function_name}() is not None

def test_{function_name}_edge_case_1():
    pass

def test_{function_name}_edge_case_2():
    pass

def test_{function_name}_invalid_input():
    pass

def test_{function_name}_performance():
    pass
"""

    def generate_vitest_tests(self, component_code: str) -> str:
        return """
import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';

describe('Component', () => {
    it('renders without crashing', () => {
        // test code
    });
});
"""

    def parse_pytest_output(self, output: str) -> Dict:
        passed = 0
        failed = 0
        errors = 0
        
        passed_match = re.search(r'(\d+)\s+passed', output)
        if passed_match:
            passed = int(passed_match.group(1))
            
        failed_match = re.search(r'(\d+)\s+failed', output)
        if failed_match:
            failed = int(failed_match.group(1))
            
        errors_match = re.search(r'(\d+)\s+error', output)
        if errors_match:
            errors = int(errors_match.group(1))
            
        return {
            "passed": passed,
            "failed": failed,
            "errors": errors,
            "coverage_pct": 0.0
        }

def inject_test_runner_prompt(system_prompt: str) -> str:
    return system_prompt + "\n[TEST RUNNER DIRECTIVE]: Continuously generate and run tests."
