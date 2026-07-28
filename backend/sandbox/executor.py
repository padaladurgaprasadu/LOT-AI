import os
import asyncio
from typing import Dict, Any, Optional
from backend.utils.logger import get_logger
from backend.utils.model_registry import AIModelRegistry

logger = get_logger(__name__)

class AutonomousExecutor:
    """
    yAI Pillar 7: Autonomous Code Execution & Self-Healing
    Executes code in isolated workspaces, captures errors, and uses an LLM
    to automatically generate fixes (Self-Healing Loop).
    """
    def __init__(self, workspace_manager=None):
        if workspace_manager is None:
            from backend.sandbox.workspace_manager import WorkspaceManager
            self.workspace_manager = WorkspaceManager()
        else:
            self.workspace_manager = workspace_manager
            
        # Executor uses a strong coding model for self-healing
        self.healer_llm = AIModelRegistry.get_llm_for_tier("coding")

    async def execute_and_heal(self, workspace_id: str, command: str, max_attempts: int = 3) -> Dict[str, Any]:
        """
        Executes a command. If it fails, reads the error, generates a fix command or code patch,
        and retries up to max_attempts.
        """
        if workspace_id not in self.workspace_manager.active_workspaces:
            return {"status": "error", "message": "Workspace not found."}

        logger.info(f"[Executor] Starting execution for: {command}")
        
        last_error = ""
        for attempt in range(max_attempts):
            logger.info(f"[Executor] Attempt {attempt + 1}/{max_attempts} for command: {command}")
            result = await self.workspace_manager.execute_in_workspace(workspace_id, command)
            
            if not result.startswith("Error:"):
                # Success
                logger.info(f"[Executor] Execution succeeded on attempt {attempt + 1}")
                return {"status": "success", "output": result, "attempts": attempt + 1}
            
            # Failure - Start self-healing
            last_error = result
            logger.warning(f"[Executor] Execution failed. Triggering Self-Healing. Error: {last_error}")
            
            # If we've reached max attempts, don't try to heal again
            if attempt == max_attempts - 1:
                break
                
            heal_prompt = f"""You are the yAI Auto-Healing Execution Agent.
The system attempted to run the following command in a sandboxed workspace:
`{command}`

It failed with this error output:
```
{last_error}
```

Analyze the error. Provide exactly ONE terminal command that will fix the issue. 
For example:
- If a dependency is missing, output the pip/npm install command.
- If a file has a syntax error, you can output a sed command or python one-liner to fix it.
- If it's a permission issue, output a chmod command.

OUTPUT FORMAT:
Output ONLY the raw command string to execute to fix this. Do not use markdown backticks. Do not provide explanations.
"""
            
            try:
                from langchain_core.messages import SystemMessage, HumanMessage
                heal_response = await self.healer_llm.ainvoke([
                    SystemMessage(content="You are the yAI Auto-Healing Agent. You write fixes for failing commands."),
                    HumanMessage(content=heal_prompt)
                ])
                fix_command = heal_response.content.strip()
                
                # Clean up formatting
                if fix_command.startswith("```"):
                    lines = fix_command.split("\\n")
                    if len(lines) > 2:
                        fix_command = "\\n".join(lines[1:-1]).strip()
                    else:
                        fix_command = fix_command.replace("```", "").strip()
                elif fix_command.startswith("`") and fix_command.endswith("`"):
                    fix_command = fix_command.replace("`", "").strip()
                    
                logger.info(f"[Executor] Proposed fix command: {fix_command}")
                
                # Execute the fix
                fix_result = await self.workspace_manager.execute_in_workspace(workspace_id, fix_command)
                logger.info(f"[Executor] Fix execution result: {fix_result}")
                
            except Exception as e:
                logger.error(f"[Executor] Self-healing LLM failed: {e}")
                
        # If we exit the loop, all attempts failed
        return {"status": "failed", "last_error": last_error, "attempts": max_attempts}
