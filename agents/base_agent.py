import os
import sys
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

# Ensure the root directory is in sys.path to import memory core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from memory.cag_core import memory_core

load_dotenv()

class yAIAgentWrapper:
    """Wraps a LangChain runnable to intercept and proactively log thoughts to global memory."""
    def __init__(self, role: str, runnable):
        self.role = role
        self.runnable = runnable

    def invoke(self, input_data: dict):
        # 1. Recall past memories before acting
        query = input_data.get("input", "")
        past_memories = memory_core.recall_context(query=query, n_results=2)
        
        # 2. Inject memories into the input dynamically
        if past_memories:
            memory_context = "\n[SYSTEM MEMORY RECALL]:\n" + "\n".join(past_memories)
            input_data["input"] = memory_context + "\n\n[NEW REQUEST]:\n" + input_data["input"]
        
        # 3. Invoke the model
        response = self.runnable.invoke(input_data)
        
        # 4. Proactively log the output back to global CAG memory
        content = response.content if hasattr(response, 'content') else str(response)
        memory_core.log_thought(agent_role=self.role, content=content)
        
        return response


class yAIAgentFactory:
    """Factory to instantiate the highly specialized experts for the yAI OS."""
    
    MODEL_REGISTRY = {
        "Router Agent": {"primary": "nvidia/nemotron-3-ultra-550b-a55b"},
        "General Chat": {"primary": "mistral-medium-3.5-128b", "fallback": "gemma-4-31b-it"},
        "Tutor Agent": {"primary": "nvidia/nemotron-3-ultra-550b-a55b", "fallback": "glm-5.2"},
        "Research Agent": {"primary": "nvidia/nemotron-3-ultra-550b-a55b", "fallback": "glm-5.2"},
        "Developer Agent": {"primary": "deepseek-v4", "fallback": "glm-5.2"},
        "Full Stack Developer": {"primary": "deepseek-v4", "fallback": "nvidia/nemotron-3-ultra-550b-a55b"},
        "Backend Developer": {"primary": "deepseek-v4"},
        "Frontend Developer": {"primary": "deepseek-v4", "fallback": "mistral-medium-3.5-128b"},
        "QA Analyst": {"primary": "glm-5.2", "fallback": "deepseek-v4"},
        "Architecture Agent & Studio": {"primary": "nvidia/nemotron-3-ultra-550b-a55b"},
        "Planning Agent": {"primary": "nvidia/nemotron-3-ultra-550b-a55b"},
        "CTO Agent": {"primary": "nvidia/nemotron-3-ultra-550b-a55b", "fallback": "mistral-medium-3.5-128b"},
        "AI Expert Agent": {"primary": "nvidia/nemotron-3-ultra-550b-a55b"},
        "Machine Learning Agent & Engineer": {"primary": "deepseek-v4", "fallback": "nvidia/nemotron-3-ultra-550b-a55b"},
        "Web Developer": {"primary": "deepseek-v4"},
        "Debugger Agent": {"primary": "deepseek-v4", "fallback": "glm-5.2"},
        "System Designer": {"primary": "nvidia/nemotron-3-ultra-550b-a55b"},
        "Artist": {"primary": "qwen-3.5-vlm", "fallback": "minimax-m3"},
        "Novelty Agent": {"primary": "nvidia/nemotron-3-ultra-550b-a55b", "fallback": "mistral-medium-3.5-128b"}
    }
    
    def __init__(self):
        self.api_key = os.getenv("NVIDIA_API_KEY")

    def _create_llm(self, model_name: str) -> ChatOpenAI:
        return ChatOpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=self.api_key,
            model=model_name,
            temperature=0.4,
            max_tokens=8192
        )
        
    def get_system_prompt(self, role: str) -> str:
        # Check if a highly specialized persona exists
        safe_role_name = role.lower().replace(" ", "_").replace("&", "and")
        persona_path = os.path.join(os.path.dirname(__file__), "personas", f"{safe_role_name}.md")
        
        if os.path.exists(persona_path):
            with open(persona_path, "r", encoding="utf-8") as f:
                print(f"[yAIAgentFactory] Loaded specialized persona for {role}")
                return f.read()

        # Fallback generic expert prompt
        return f"""You are a {role} within the yAI Operating System.
You possess exactly 15 years of deep industry expertise in this specific domain.
You are not a general-purpose AI; you are a hyper-specialized expert.
Your goal is to produce 100x better results than any existing tool by thinking deeply, predicting edge cases, and outputting flawless, production-ready solutions.
Never apologize, never break character, and always act with absolute professional CTO-level authority."""

    def create_agent(self, role: str):
        """Returns a memory-augmented LangChain chain configured for this specific role."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.get_system_prompt(role)),
            ("human", "{input}")
        ])
        
        # 1. Look up model config
        config = self.MODEL_REGISTRY.get(role, {"primary": "nvidia/nemotron-3-ultra-550b-a55b"})
        primary_model_name = config["primary"]
        
        print(f"[yAIAgentFactory] Routing '{role}' to primary model: {primary_model_name}")
        primary_llm = self._create_llm(primary_model_name)
        
        chain = prompt | primary_llm
        
        # 2. Add fallback if specified
        if "fallback" in config:
            fallback_model_name = config["fallback"]
            print(f"[yAIAgentFactory] Adding fallback model: {fallback_model_name} for '{role}'")
            fallback_llm = self._create_llm(fallback_model_name)
            chain = chain.with_fallbacks([prompt | fallback_llm])
            
        return yAIAgentWrapper(role=role, runnable=chain)

# The Official yAI 34 Agent Roster
YAI_AGENTS = [
    # Core Orchestration
    "Router Agent", "Planning Agent", "CTO Agent", "Architecture Agent & Studio",
    "Reviewer Agent", "Executer Agent", "Debugger Agent",
    # Software Engineering & IT
    "Developer Agent", "Full Stack Developer", "Frontend Developer", "Backend Developer",
    "Web Developer", "DevOps Agent", "QA Analyst", "System Designer",
    "Cybersecurity Agent & Engineer", "Database Analyst",
    # Deep Tech & Hardware
    "Machine Learning Agent & Engineer", "AI Expert Agent", "Data Scientist",
    "ECE Engineer", "EEE Engineer",
    # Domain Specific
    "Medical Coding Agent", "Bio-tech Engineer", "Fintech Agent", "Business Analyst",
    # Creative & Educational
    "Tutor Agent", "General Chat", "Research Agent", "Artist", "Novelty Agent"
]

if __name__ == "__main__":
    # Test instantiation of a highly specialized agent
    factory = yAIAgentFactory()
    cto_agent = factory.create_agent("CTO Agent")
    print(f"Successfully initialized memory-augmented factory with {len(YAI_AGENTS)} expert roles.")
    print("Testing CTO Agent instantiation... OK")
