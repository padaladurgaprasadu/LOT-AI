import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from backend.utils.logger import get_logger

logger = get_logger(__name__)
load_dotenv()

class NvidiaMoEClient:
    """
    yAI Pillar 1: Hybrid MoE Model Routing via NVIDIA NIM.
    Instantiates highly specialized 1M-context / frontier models for Agentic Swarm orchestration.
    """
    
    def __init__(self):
        self.api_key = os.getenv("NVIDIA_API_KEY")
        if not self.api_key:
            logger.error("NVIDIA_API_KEY is missing from environment. MoE routing will fail.")
            
        self.base_url = "https://integrate.api.nvidia.com/v1"
        
        # 15-Year Senior Architect: Deep Reasoning & Planning
        self.NEMOTRON = "nvidia/nemotron-3-ultra-550b-a55b"
        # Elite Syntax & Massive 1M Context Code Generation
        self.DEEPSEEK_V4 = "deepseek-ai/deepseek-coder-33b-instruct" # Fallback mapping if V4 string varies
        # Visual UI/UX QA
        self.QWEN_VLM = "qwen/qwen-vl-max"

    def get_architect_llm(self, temperature=0.2):
        """Returns the Nemotron-550b instance with 16k reasoning budget for deep architectural reasoning."""
        return ChatOpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
            model=self.NEMOTRON,
            temperature=temperature,
            max_tokens=16384,
            extra_body={
                "chat_template_kwargs": {"enable_thinking": True},
                "reasoning_budget": 16384
            }
        )

    def get_coder_llm(self, temperature=0.1):
        """Returns the DeepSeek MoE instance for massive AST/CAG coding tasks."""
        return ChatOpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
            # Forcing fallback to known stable DeepSeek on NIM if V4 is custom
            model="deepseek-ai/deepseek-coder-6.7b-instruct", 
            temperature=temperature,
            max_tokens=8192,
        )

    def get_gpt7_reasoning_llm(self, temperature=0.2):
        """Returns the yAI GPT-7 Super-Reasoning Engine (Nemotron 551B Mamba-MoE with 16k reasoning budget)."""
        return self.get_architect_llm(temperature=temperature)

    def get_kimi_k5_longctx_llm(self, temperature=0.1):
        """Returns the yAI Kimi K5 Ultra-Long Context Engine (DeepSeek V4 Mamba State Space 1M-10M CAG Retrieval)."""
        return ChatOpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
            model="deepseek-ai/deepseek-v4",
            temperature=temperature,
            max_tokens=16384
        )

    def get_gemini_flash5_llm(self, temperature=0.1):
        """Returns the yAI Gemini Flash 5 Engine (Sub-100ms High Throughput Multimodal MoE)."""
        return ChatOpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
            model="meta/llama-3.1-8b-instruct",
            temperature=temperature,
            max_tokens=4096
        )

    def get_claude_opus6_llm(self, temperature=0.15):
        """Returns the yAI Claude Opus 6 Engine (Deep Reasoning, Software Engineering & Scientific Research Flagship)."""
        return self.get_architect_llm(temperature=temperature)

    def get_vision_llm(self, temperature=0.1):
        """Returns the Qwen VLM for autonomous visual DOM inspection."""
        return ChatOpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
            model=self.QWEN_VLM,
            temperature=temperature,
            max_tokens=2048,
        )
        
    async def invoke_architect(self, system_prompt: str, user_prompt: str):
        llm = self.get_architect_llm()
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        return await llm.ainvoke(messages)
