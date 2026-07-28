import os
import time
import json
from typing import Dict, Any, List
from backend.utils.logger import get_logger

logger = get_logger(__name__)

class WorkflowInspector:
    """
    yAI 10,000X Workflow Audit & Debugging Inspector.
    Tracks and logs all 9 stages of the Autonomous Engineering Pipeline:
    User Prompt ➔ Router ➔ Planner ➔ Architect ➔ Developer ➔ Code Generator ➔ File Writer ➔ Reviewer ➔ Preview
    """
    def __init__(self):
        self.stage_logs: List[Dict[str, Any]] = []

    def log_stage(self, stage_name: str, input_data: Any, output_data: Any, model_used: str = "N/A", execution_time_ms: float = 0.0, error: str = None, tools_called: List[str] = None, files_created: List[str] = None):
        entry = {
            "stage": stage_name,
            "timestamp": time.time(),
            "model_used": model_used,
            "execution_time_ms": round(execution_time_ms, 2),
            "input": str(input_data)[:200],
            "output": str(output_data)[:300],
            "error": error,
            "tools_called": tools_called or [],
            "files_created": files_created or []
        }
        self.stage_logs.append(entry)
        
        status_icon = "❌" if error else "✅"
        logger.info(f"{status_icon} [WorkflowStage: {stage_name}] | Model: {model_used} | Latency: {execution_time_ms:.1f}ms | Files: {len(files_created or [])}")
        if error:
            logger.error(f"   ⚠️ Stage Error in {stage_name}: {error}")
            
        return entry

    def get_audit_summary(self) -> Dict[str, Any]:
        return {
            "total_stages": len(self.stage_logs),
            "failed_stages": [s for s in self.stage_logs if s.get("error")],
            "all_files_created": [f for s in self.stage_logs for f in s.get("files_created", [])],
            "timeline": self.stage_logs
        }

# Global Singleton Workflow Inspector
global_workflow_inspector = WorkflowInspector()
