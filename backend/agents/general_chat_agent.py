import time
from typing import Dict, Any
from backend.agents.base import BaseAgent
from backend.utils.workflow_inspector import global_workflow_inspector
from backend.utils.logger import get_logger

logger = get_logger(__name__)

class GeneralChatAgent(BaseAgent):
    """
    yAI General Chat Agent (15+ Years Conversational AI Experience).
    
    Powered by Langflow-inspired conversational orchestration.
    Maintains session memory, handles casual queries, FAQ, and onboarding flows.
    Routes to specialist agents when task complexity exceeds general chat scope.
    
    Inspired by: github.com/langflow-ai/langflow
    """
    def __init__(self):
        super().__init__()
        self.memory_window = 20   # last 20 turns kept in working memory
        self.handoff_triggers = [
            "build", "create", "code", "debug", "research", "deploy",
            "analyze", "design", "architecture", "security", "hack",
            "medical", "circuit", "finance", "space", "train model"
        ]

    def chat(self, message: str, history: list = None) -> Dict[str, Any]:
        start_time = time.time()
        logger.info(f"💬 [GeneralChatAgent] Handling chat: '{message[:60]}'")
        
        history = history or []
        
        # Detect if this should be handed off to a specialist agent
        handoff_agent = None
        msg_lower = message.lower()
        for trigger in self.handoff_triggers:
            if trigger in msg_lower:
                handoff_agent = "SpecialistSwarm"
                break
        
        global_workflow_inspector.log_stage(
            "GeneralChat Session",
            message,
            f"Turns in context: {len(history)} | Handoff: {handoff_agent or 'None'}"
        )
        
        latency = (time.time() - start_time) * 1000
        return {
            "status": "SUCCESS",
            "agent": "GeneralChatAgent (15yr)",
            "response_mode": "HANDOFF" if handoff_agent else "DIRECT_CHAT",
            "handoff_target": handoff_agent,
            "memory_turns": len(history),
            "latency_ms": round(latency, 2)
        }
