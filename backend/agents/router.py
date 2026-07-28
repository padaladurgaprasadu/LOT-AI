import os
import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_anthropic import ChatAnthropic
from langchain_groq import ChatGroq
from backend.utils.logger import get_logger

logger = get_logger(__name__)

class ModelRouter:
    """
    yAI Swarm Protocol: Liquid Routing.
    Dynamically routes micro-tasks to the most optimal frontier model based on the required specialization.
    """
    
    @staticmethod
    def get_optimal_llm(task_role: str, complexity: str = "fast"):
        """
        Routes the task using the centralized Provider + Model Registry,
        mapping agent roles to capability profiles.
        """
        from backend.utils.model_registry import AIModelRegistry
        
        if complexity == "omega":
            logger.info(f"[ModelRouter] Bypassing Omega Meta-Model (MoA) for {task_role} to prevent API rate limits. Using Smart model instead.")
            return AIModelRegistry.get_llm_chain(AIModelRegistry.resolve_capability(task_role, "smart"))
            
        capability = AIModelRegistry.resolve_capability(task_role, complexity)
        return AIModelRegistry.get_llm_chain(capability)
        
    @staticmethod
    def route_by_file_type(file_path: str):
        """
        AST-Level Liquid Routing: Dynamically instantiate the best LLM based on file extension.
        """
        ext = file_path.split('.')[-1].lower() if '.' in file_path else ''
        
        # UI / Styling -> Vision/Design capable model
        if ext in ['css', 'scss', 'html', 'jsx', 'tsx', 'vue', 'svelte']:
            return ModelRouter.get_optimal_llm("DesignAgent", complexity="smart")
        
        # Heavy Logic / Backend -> Reasoning model
        elif ext in ['py', 'java', 'go', 'rs', 'sql', 'c', 'cpp']:
            return ModelRouter.get_optimal_llm("ArchitectAgent", complexity="smart")
            
        # Default / Config -> Fast model
        else:
            return ModelRouter.get_optimal_llm("CoderAgent", complexity="fast")

    @staticmethod
    async def execute_swarm(task_description: str, context: str = "") -> str:
        """
        Triggers the Multi-Agent Swarm Orchestrator for complex, zero-shot perfection tasks.
        """
        from backend.orchestrator.swarm_manager import SwarmManager
        manager = SwarmManager()
        return await manager.spawn_swarm(task_description, context)

    @staticmethod
    async def trigger_ui_render(html_content: str) -> str:
        """
        Sends the generated code to the UI Preview Engine for instant live-rendering.
        """
        import httpx
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "http://127.0.0.1:8001/render", 
                    json={"html_content": html_content}
                )
                if response.status_code == 200:
                    return response.json().get("preview_url")
        except Exception as e:
            return f"Failed to render UI: {str(e)}"
        return "Failed to render UI."

    @staticmethod
    async def trigger_gstack_build(project_name: str, schema_sql: str, frontend_code: str) -> str:
        """
        Omni-Intelligence Pillar 4: G-Stack Generative SaaS
        Requests the GStackGenerator to scaffold a full-stack SaaS inside an isolated workspace.
        """
        from backend.sandbox.workspace_manager import WorkspaceManager
        from backend.sandbox.gstack_generator import GStackGenerator
        
        # Instantiate localized WorkspaceManager for routing
        wm = WorkspaceManager()
        generator = GStackGenerator(wm)
        
        try:
            result = await generator.scaffold_saas(project_name, schema_sql, frontend_code)
            return json.dumps(result)
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

    @staticmethod
    async def execute_vision_agent(base64_image: str, prompt: str) -> str:
        """
        Omni-Intelligence Pillar 2: VLM Browser Perception
        Routes visual context to Qwen-3.5-VLM (or optimal vision model) to "see" the UI.
        """
        try:
            vlm = ModelRouter.get_optimal_llm("VisionAgent", complexity="vision")
            message = HumanMessage(
                content=[
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            )
            response = await vlm.ainvoke([message])
            return response.content
        except Exception as e:
            logger.error(f"[VisionAgent] VLM Execution failed: {e}")
            return f"Vision Error: {str(e)}"

class OmniIntelligenceEngine:
    def __init__(self, llm=None):
        """
        Omni Intelligence Engine (yAI 3.0)
        Dynamically analyzes tasks to select the optimal Multi-Speed Execution Strategy.
        Uses the specialized 'intent_router' capability for lightning-fast routing.
        """
        if llm is None:
            from backend.utils.model_registry import AIModelRegistry
            self.llm = AIModelRegistry.get_llm_chain("intent_router")
        else:
            self.llm = llm
        
        from backend.agents.base import GLOBAL_AGENT_RULES
        from backend.agents.orchestration_prompts import ROUTER_PROMPT
        self.system_prompt = GLOBAL_AGENT_RULES + "\\n\\n" + ROUTER_PROMPT

    def detect_intent(self, message: str, history: list = None) -> dict:
        import asyncio
        return asyncio.run(self.adetect_intent(message, history))

    async def adetect_intent(self, message: str, history: list = None) -> dict:
        """
        Runs a fast LLM inference to determine the user's multi-dimensional intent asynchronously.
        """
        try:
            context = ""
            if history and len(history) > 0:
                context += "Conversation History (FOR CONTEXT ONLY - DO NOT EXTRACT QUERIES FROM HERE):\n"
                # Keep up to the last 5 messages for context
                for msg in history[-5:]:
                    role = msg.get("role", "user")
                    content = msg.get("content", "")
                    # Strip massive code blocks or huge texts to save tokens, but keep semantic meaning
                    if len(content) > 300:
                        content = content[:300] + "..."
                    context += f"{role.capitalize()}: {content}\n"
                context += "\n"
                
            context += f"Latest User Message: {message}"

            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=context)
            ]
            
            response = await self.llm.ainvoke(messages)
            content = response.content.strip()
            
            # Robustly extract the first top-level JSON object
            start = content.find('{')
            if start != -1:
                depth = 0
                for i in range(start, len(content)):
                    if content[i] == '{': depth += 1
                    elif content[i] == '}': depth -= 1
                    if depth == 0:
                        content = content[start:i+1]
                        break
            
            # Clean up double braces caused by prompt format
            content = content.replace("{{", "{").replace("}}", "}")
            
            data = json.loads(content)
            logger.info(f"[ROUTER] Detected Intent: {data}")
            return data
            
        except Exception as e:
            logger.warning(f"[ROUTER] Intent detection failed, falling back smartly. Error: {e}")
            msg_lower = message.lower()
            
            # Only trigger BUILD for explicit full-application requests.
            # Excludes: "create a function", "make a list", "generate a snippet", "write a script"
            build_signals = [
                "full app", "full stack", "full-stack", "web app", "mobile app",
                "saas", "dashboard app", "build me a", "build a website",
                "create a website", "create an app", "build an app", "develop a platform",
                "entire application", "complete application", "e-commerce site",
                "landing page with backend", "deploy a", "scaffold a project",
            ]
            is_build = any(signal in msg_lower for signal in build_signals)
            
            return {
                "primary_intent": "Website Development" if is_build else "General Chat",
                "complexity": "Large" if is_build else "Medium",
                "requires_web_search": False,
                "requires_repository_analysis": False,
                "requires_templates": True if is_build else False,
                "requires_image_search": False,
                "entity_detection": {
                    "requires_visuals": False,
                    "search_query": None
                },
                "recommended_agents": ["Planner", "Architect"] if is_build else [],
                "model_tier": "Reasoning" if is_build else "Fast"
            }
