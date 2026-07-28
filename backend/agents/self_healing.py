import os
import json
import re
from backend.utils.logger import get_logger
from backend.utils.nvidia_client import NvidiaMoEClient
from backend.utils.model_registry import AIModelRegistry

logger = get_logger("SelfHealingEngine")

class SelfHealingEngine:
    """
    yAI Autonomous Self-Healing Engine v1.0
    Automatically intercepts runtime errors, build failures, and stack traces,
    invokes the DeepSeek-R1 Debugger Agent, and generates precise zero-shot patches.
    """

    def __init__(self, project_dir: str = None):
        self.project_dir = project_dir
        self.nv_client = NvidiaMoEClient()
        self.debugger_llm = AIModelRegistry.get_llm_for_tier("coding")

    async def diagnose_and_heal(self, error_trace: str, context_code: str = "") -> dict:
        """
        Parses an error log/stack trace, determines root cause, and outputs the exact file path and fixed content.
        """
        logger.info("[SelfHealing] Intercepted runtime error trace. Initiating autonomous healing...")

        system_prompt = """You are the Lead Debugger Agent & Principal Systems Engineer in yAI.
Your job is to analyze stack traces, runtime errors, and broken imports, identify the exact root cause, and output a production-ready fix.

OUTPUT FORMAT MANDATORY:
<thinking>
1. Identify the failing line number and root cause.
2. Formulate the precise architectural patch.
</thinking>

<diagnosis>
Provide a 2-sentence explanation of why the failure occurred and how it was resolved.
</diagnosis>

<file path="relative/path/to/file">
[COMPLETE FIXED FILE CONTENT]
</file>"""

        user_prompt = f"""RUNTIME ERROR TRACE:
```
{error_trace}
```

CURRENT BROKEN FILE CONTEXT:
```
{context_code}
```

Analyze the failure and provide the complete fixed file content inside <file path="..."> tags."""

        try:
            from langchain_core.messages import SystemMessage, HumanMessage
            messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]
            
            response = await self.debugger_llm.ainvoke(messages)
            content = response.content if hasattr(response, 'content') else str(response)

            # Extract diagnosis
            diag_match = re.search(r'<diagnosis>(.*?)</diagnosis>', content, re.DOTALL)
            diagnosis = diag_match.group(1).strip() if diag_match else "Resolved runtime error and updated file AST."

            # Extract file fix
            file_match = re.search(r'<file\s+path="([^"]+)">(.*?)</file>', content, re.DOTALL)
            if file_match:
                rel_path = file_match.group(1).strip()
                fixed_code = file_match.group(2).strip()

                if self.project_dir:
                    full_path = os.path.abspath(os.path.join(self.project_dir, rel_path.replace("/", os.sep)))
                    if full_path.startswith(os.path.abspath(self.project_dir)):
                        os.makedirs(os.path.dirname(full_path), exist_ok=True)
                        with open(full_path, "w", encoding="utf-8") as f:
                            f.write(fixed_code)

                return {
                    "status": "healed",
                    "diagnosis": diagnosis,
                    "file_path": rel_path,
                    "fixed_code": fixed_code
                }
            else:
                return {
                    "status": "diagnosis_only",
                    "diagnosis": diagnosis,
                    "fixed_code": None
                }

        except Exception as e:
            logger.error(f"[SelfHealing] Diagnosis failed: {e}")
            return {
                "status": "error",
                "diagnosis": f"Healing attempt encountered an error: {str(e)}",
                "fixed_code": None
            }
