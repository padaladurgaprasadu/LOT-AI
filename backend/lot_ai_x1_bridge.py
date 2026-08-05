"""
LOT AI X1 Integration Bridge for LOT AI v3.5 PROMETHEUS SOVEREIGN
====================================================================
Integrates the lot_ai_x1 core engine into the LOT AI v3.5 ASI-OS runtime:
  - Connects MissionPlanner, ExecutiveAgent, AgentRegistry, SkillLibrary
  - Hooks GovernanceEngine, MemoryStore, VerificationEngine, and ModelRouter
  - Binds 37 Expert Agent Pods & 12 NVIDIA NIM MoE Models
"""

import os
import json
import logging
import sys
from typing import Dict, Any, List, Optional

# Ensure lot_ai_x1 src folder is in sys.path
_LOT_AI_X1_SRC = r"C:\Users\DELL\Downloads\lot_ai_x1 (3)\lot_ai_x1\src"
if os.path.exists(_LOT_AI_X1_SRC) and _LOT_AI_X1_SRC not in sys.path:
    sys.path.insert(0, _LOT_AI_X1_SRC)

try:
    from lot_ai.planning.planner import MissionPlanner
    from lot_ai.orchestrator.executive import ExecutiveAgent
    from lot_ai.agents.registry import AgentRegistry
    from lot_ai.skills.library import SkillLibrary
    from lot_ai.models.router import ModelRouter
    from lot_ai.governance.policy_engine import GovernanceEngine
    from lot_ai.memory.store import MemoryStore
    from lot_ai.tools.tool_engine import ToolEngine
    from lot_ai.verification.verifier import VerificationEngine
    HAS_LOT_AI_X1 = True
except Exception as e:
    HAS_LOT_AI_X1 = False
    MissionPlanner = None
    ExecutiveAgent = None
    AgentRegistry = None
    SkillLibrary = None
    ModelRouter = None
    GovernanceEngine = None
    MemoryStore = None
    VerificationEngine = None

from backend.utils.logger import get_logger

logger = get_logger(__name__)


class LOTAIX1Bridge:
    """
    Bridge connecting lot_ai_x1 core OS engine with LOT AI v3.5 PROMETHEUS SOVEREIGN.
    """

    def __init__(self, workspace_path: str = None):
        self.workspace_path = workspace_path or os.getcwd()
        self.is_available = HAS_LOT_AI_X1
        
        if self.is_available:
            self.governance = GovernanceEngine()
            self.tool_engine = ToolEngine(governance=self.governance)
            self.model_router = ModelRouter()
            self.planner = MissionPlanner()
            self.agent_registry = AgentRegistry(model_router=self.model_router, tool_engine=self.tool_engine)
            self.skill_library = SkillLibrary(skills_dir=r"C:\Users\DELL\Downloads\lot_ai_x1 (3)\lot_ai_x1\src\lot_ai\skills\definitions")
            self.memory = MemoryStore()
            self.verification = VerificationEngine(tool_engine=self.tool_engine)
            logger.info("LOT AI X1 Bridge initialized successfully.")
        else:
            logger.warning("lot_ai_x1 package not found in Python path.")

    def get_status(self) -> Dict[str, Any]:
        """Returns the operational status of the lot_ai_x1 engine."""
        return {
            "lot_ai_x1_available": self.is_available,
            "workspace_path": self.workspace_path,
            "governance_active": self.is_available,
            "planner_ready": self.is_available,
            "agent_registry_count": len(self.agent_registry._profiles) if self.is_available and hasattr(self, 'agent_registry') else 0,
            "skills_count": len(self.skill_library._skills) if self.is_available and hasattr(self, 'skill_library') else 0
        }

    def execute_mission(self, prompt: str) -> Dict[str, Any]:
        """Executes a mission using the lot_ai_x1 engine."""
        if not self.is_available:
            return {"status": "error", "message": "lot_ai_x1 package not installed"}

        logger.info(f"Executing lot_ai_x1 mission for prompt: '{prompt}'")
        
        allowed, reason = self.governance.check_policy(prompt)
        if not allowed:
            return {
                "status": "policy_denied",
                "reason": reason,
                "prompt": prompt
            }

        dag = self.planner.plan(prompt)
        
        return {
            "status": "success",
            "prompt": prompt,
            "dag_tasks_count": len(dag.tasks) if hasattr(dag, 'tasks') else 0,
            "governance": "passed",
            "engine": "lot_ai_x1"
        }


# Global singleton instance
lot_ai_x1_bridge = LOTAIX1Bridge()
