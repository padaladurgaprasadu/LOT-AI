"""
Real test execution runner using pytest.
Runs tests and parses JSON test results.
"""

import subprocess
import json
import os
import shutil

def run_pytest(working_dir: str, timeout: int = 120) -> dict:
    """Runs pytest in the specified directory and parses results."""
    report_file = "/tmp/lotai_test_report.json" if os.name != 'nt' else "C:\\Windows\\Temp\\lotai_test_report.json"
    
    if shutil.which("pytest") is None:
        return {
            "total": 0, "passed": 0, "failed": 0, "errors": 1, "coverage_pct": 0.0,
            "status": "error", "message": "pytest not installed"
        }

    cmd = ["pytest", "--tb=short", "--json-report", f"--json-report-file={report_file}"]

    try:
        process = subprocess.run(
            cmd,
            cwd=working_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            text=True
        )
    except subprocess.TimeoutExpired:
        return {
            "total": 0, "passed": 0, "failed": 0, "errors": 1, "coverage_pct": 0.0,
            "status": "timeout", "message": f"Tests timed out after {timeout}s"
        }
    except Exception as e:
        return {
            "total": 0, "passed": 0, "failed": 0, "errors": 1, "coverage_pct": 0.0,
            "status": "error", "message": str(e)
        }

    if not os.path.exists(report_file):
        return {
            "total": 0, "passed": 0, "failed": 0, "errors": 0, "coverage_pct": 0.0,
            "status": "no_tests", "message": "No test report generated"
        }

    try:
        with open(report_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        summary = data.get("summary", {})
        total = summary.get("total", 0)
        passed = summary.get("passed", 0)
        failed = summary.get("failed", 0)
        errors = summary.get("error", 0)
        
        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "errors": errors,
            "coverage_pct": 0.0,
            "status": "success" if process.returncode == 0 else "failed",
            "message": "Tests executed"
        }
    except Exception as e:
        return {
            "total": 0, "passed": 0, "failed": 0, "errors": 1, "coverage_pct": 0.0,
            "status": "parse_error", "message": f"Failed to parse report: {str(e)}"
        }

def inject_test_runner_prompt(system_prompt: str) -> str:
    """Injects test runner directive into the system prompt."""
    directive = "\n[TEST DIRECTIVE]: Ensure all tests pass. Write robust pytest assertions.\n"
    return system_prompt + directive
