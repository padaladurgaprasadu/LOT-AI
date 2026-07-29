"""
yAI Omni-Intelligence Model Registry v3.0
==========================================
11-Model NVIDIA Liquid Routing Engine.
Maps every agent role to its optimal frontier model based on task type.

Model Roster (NVIDIA NIM API):
  INSTANT   → meta/llama-3.1-8b-instruct           (chat, intent routing, < 100ms TTFT)
  FAST      → mistralai/mistral-medium-3.5-128b    (docs, deployment, summaries)
  CODING    → deepseek-ai/deepseek-r1               (coding, debugging, DB, DevOps)
  PLANNING  → nvidia/nemotron-3-ultra-253b-v1       (CEO, Architect, planning, tool calling)
  REASONING → nvidia/nemotron-3-ultra-550b-a55b     (1M ctx, agentic reasoning, QA, Security)
  RESEARCH  → deepseek-ai/deepseek-v4               (1M ctx MoE, research, web knowledge)
  VISION    → qwen/qwen3-235b-a22b                  (UI design, VQA, screenshots)
  MULTIMOD  → nvidia/llama-3.2-90b-vision-instruct  (image-to-code, vision tasks)
  LONGCTX   → google/gemma-4-31b-it                 (long context, agentic fine-tuning)
  MOE_CHAT  → minimax/minimax-m2.7-230b             (coding, reasoning, office tasks)
  FRONTIER  → minimax/minimax-m3-preview             (multimodal, tool-calling flagship)
"""

import os
from typing import Any, List
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from backend.utils.logger import get_logger

logger = get_logger(__name__)

NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"

# ═══════════════════════════════════════════════════════════════
# THE 11-MODEL NVIDIA LIQUID ROUTING TABLE
# Every agent role maps to a purpose-built frontier model.
# ═══════════════════════════════════════════════════════════════
NVIDIA_MODEL_TIERS = {
    # ⚡ INSTANT — Sub-100ms, lightweight, chat + intent classification
    "instant": "meta/llama-3.1-8b-instruct",

    # 🏎️ FAST — Docs, summaries, deployment configs, fast code snippets
    "fast": "meta/llama-3.1-8b-instruct",

    # 💻 CODING — Llama 3.3 70B Instruct
    "coding": "meta/llama-3.3-70b-instruct",

    # 🏗️ PLANNING — Llama 3.3 70B Instruct
    "planning": "meta/llama-3.3-70b-instruct",

    # 🧠 REASONING — Llama 3.3 70B Instruct
    "reasoning": "meta/llama-3.3-70b-instruct",

    # 🔬 RESEARCH — Llama 3.3 70B Instruct
    "research": "meta/llama-3.3-70b-instruct",

    # 👁️ VISION — Llama 3.2 90B Vision
    "vision": "meta/llama-3.2-90b-vision-instruct",

    # 🖼️ MULTIMODAL — Llama 3.2 90B Vision
    "multimodal": "meta/llama-3.2-90b-vision-instruct",

    # 📜 LONGCTX — Llama 3.3 70B Instruct
    "longctx": "meta/llama-3.3-70b-instruct",

    # 💬 MOE_CHAT — Llama 3.3 70B Instruct
    "moe_chat": "meta/llama-3.3-70b-instruct",

    # 👑 FRONTIER — Llama 3.3 70B Instruct
    "frontier": "meta/llama-3.3-70b-instruct",

    # ⚡ REASONING TIER — Nemotron 70B
    "gpt7_reasoning": "nvidia/llama-3.1-nemotron-70b-instruct",

    # 📚 LONG CONTEXT TIER — Llama 3.3 70B
    "kimi_k5_longctx": "meta/llama-3.3-70b-instruct",

    # ⚡ FLASH TIER — Llama 3.1 8B
    "gemini_flash5": "meta/llama-3.1-8b-instruct",

    # 🌐 GLM TIER — Llama 3.3 70B
    "glm_5_2": "meta/llama-3.3-70b-instruct",

    # ⚡ MISTRAL TIER — Llama 3.3 70B
    "mistral_medium": "meta/llama-3.3-70b-instruct"
}

# ═══════════════════════════════════════════════════════════════
# AGENT ROLE → CAPABILITY TIER MAPPING
# Every swarm agent is wired to its optimal model.
# ═══════════════════════════════════════════════════════════════
ROLE_TO_TIER = {
    # Core Orchestration
    "ceo":                  "planning",
    "cto":                  "planning",
    "architect":            "planning",
    "planner":              "planning",
    "planning":             "planning",
    "orchestrator":         "planning",
    "system_designer":      "planning",
    "system designer":      "planning",
    "mythos":               "planning",
    "router":               "instant",
    "intent_router":        "instant",
    "general_chat":         "instant",

    # Coding & Engineering Agents
    "developer":            "coding",
    "frontend":             "coding",
    "frontend coder":       "coding",
    "frontend developer":   "coding",
    "backend":              "coding",
    "backend coder":        "coding",
    "backend developer":    "coding",
    "fullstack":            "coding",
    "full stack developer": "coding",
    "web developer":        "coding",
    "web_developer":        "coding",
    "devops":               "coding",
    "devops engineer":      "coding",
    "database coder":       "coding",
    "deployment agent":     "coding",
    "executor":             "coding",
    "debugger":             "coding",

    # Deep Reasoning Agents (Nemotron 550B)
    "qa":                   "reasoning",
    "qa engineer":          "reasoning",
    "security engineer":    "reasoning",
    "cybersecurity":        "reasoning",
    "auditor":              "reasoning",
    "reviewer":             "reasoning",
    "data_scientist":       "reasoning",
    "data scientist":       "reasoning",
    "ml_engineer":          "reasoning",
    "ml engineer":          "reasoning",
    "ai expert":            "reasoning",
    "ai_expert":            "reasoning",
    "ece_engineer":         "reasoning",
    "ece engineer":         "reasoning",
    "eee_engineer":         "reasoning",
    "eee engineer":         "reasoning",
    "medical_coding":       "reasoning",
    "medical coding":       "reasoning",
    "biotech":              "reasoning",
    "fintech":              "reasoning",
    "space":                "reasoning",
    "designcritique":       "vision",

    # Research (DeepSeek V4 — 1M context)
    "research":             "research",
    "research agent":       "research",
    "langchain_expert":     "research",
    "langchain expert":     "research",

    # Vision (Qwen VLM 400B)
    "vision":               "vision",
    "ux designer":          "vision",
    "ui designer":          "vision",
    "artist":               "vision",
    "vqa":                  "multimodal",

    # Fast/Chat Models
    "tutor":                "fast",
    "documentation agent":  "fast",
    "chat":                 "fast",
    "memory":               "instant",

    # MoE Chat (MiniMax M2.7)
    "business_analyst":         "moe_chat",
    "business analyst":         "moe_chat",
    "data_analyst":             "moe_chat",
    "data analyst":             "moe_chat",
    "domainorchestrator":       "moe_chat",

    # Frontier (MiniMax M3 Preview)
    "novelty":                  "frontier",
    "innovation":               "frontier",
    "architecture_studio":      "frontier",
    "architecture studio":      "frontier",

    # GLM-5.2 — Agentic Long-Horizon Coding & Reasoning
    "langchain_expert":         "glm_5_2",
    "langchain expert":         "glm_5_2",
    "langgraph":                "glm_5_2",
    "general_chat":             "glm_5_2",
    "general chat":             "glm_5_2",

    # Mistral Medium 3.5 — 128K Fast Reasoning
    "system_designer":          "mistral_medium",
    "system designer":          "mistral_medium",
    "fintech":                  "mistral_medium",
    "fintech_agent":            "mistral_medium",
    "space":                    "mistral_medium",
    "space_agent":              "mistral_medium",
    "space engineer":           "mistral_medium",

    # Default
    "default":                  "fast",
}


def _build_nvidia_llm(model: str, temperature: float = 0.1, max_tokens: int = 16384):
    """Constructs a single NVIDIA NIM LLM instance with robust fallback chains."""
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        raise ValueError("NVIDIA_API_KEY not set in environment.")
    
    primary = ChatOpenAI(
        base_url=NVIDIA_BASE_URL,
        api_key=api_key,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        timeout=30,
        max_retries=2,
        streaming=True,
    )
    fallback = ChatOpenAI(
        base_url=NVIDIA_BASE_URL,
        api_key=api_key,
        model="meta/llama-3.3-70b-instruct",
        temperature=temperature,
        max_tokens=max_tokens,
        timeout=30,
        max_retries=2,
        streaming=True,
    )
    return primary.with_fallbacks([fallback])


class AIModelRegistry:
    """
    yAI Omni-Intelligence Model Registry v3.0
    11-Model Liquid Routing — the right model for every job.
    """

    @staticmethod
    def get_provider() -> str:
        """NVIDIA is the primary provider. Falls back to OpenAI → Google → Groq."""
        if os.getenv("NVIDIA_API_KEY"):
            return "nvidia"
        if os.getenv("OPENAI_API_KEY"):
            return "openai"
        if os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY"):
            return "google"
        if os.getenv("GROQ_API_KEY"):
            return "groq"
        return "fallback"

    @staticmethod
    def resolve_capability(role: str, complexity: str = "fast") -> str:
        """
        Maps an agent role + complexity to a model tier name.
        complexity kwarg used as final fallback if role is unknown.
        """
        role_key = role.lower().replace(" ", " ").strip()

        # Direct role match first
        for key, tier in ROLE_TO_TIER.items():
            if key in role_key:
                return tier

        # Complexity fallback mapping
        COMPLEXITY_MAP = {
            "omega":      "reasoning",
            "smart":      "planning",
            "reasoning":  "reasoning",
            "coding":     "coding",
            "vision":     "vision",
            "safety":     "reasoning",
            "fast":       "fast",
            "instant":    "instant",
        }
        return COMPLEXITY_MAP.get(complexity, "fast")

    @staticmethod
    def get_llm_for_tier(tier: str, temperature: float = 0.1) -> Any:
        """
        Returns an instantiated LLM for a given tier string.
        Always attempts NVIDIA first. Falls back to OpenAI/Groq if key missing.
        """
        provider = AIModelRegistry.get_provider()

        if provider == "nvidia":
            model = NVIDIA_MODEL_TIERS.get(tier, NVIDIA_MODEL_TIERS["fast"])
            logger.info(f"[ModelRegistry] Routing to NVIDIA/{model} (tier={tier})")
            try:
                return _build_nvidia_llm(model, temperature=temperature)
            except Exception as e:
                logger.warning(f"[ModelRegistry] Failed to build {model}: {e}. Falling back to instant.")
                return _build_nvidia_llm(NVIDIA_MODEL_TIERS["instant"], temperature=temperature)

        elif provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            model = "gpt-4o" if tier in ("reasoning", "planning", "coding") else "gpt-4o-mini"
            return ChatOpenAI(api_key=api_key, model=model, temperature=temperature, streaming=True)

        elif provider == "google":
            api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
            model = "gemini-1.5-pro" if tier in ("reasoning", "planning") else "gemini-1.5-flash"
            return ChatGoogleGenerativeAI(model=model, google_api_key=api_key, temperature=temperature, streaming=True)

        elif provider == "groq":
            api_key = os.getenv("GROQ_API_KEY")
            model = "llama3-70b-8192" if tier in ("reasoning", "planning", "coding") else "llama-3.1-8b-instant"
            return ChatGroq(model_name=model, groq_api_key=api_key, temperature=temperature, streaming=True)

        else:
            logger.error("[ModelRegistry] No provider API key found. Using dummy fallback.")
            return ChatOpenAI(api_key="dummy", model="gpt-4o-mini", temperature=temperature, streaming=True)

    @staticmethod
    def get_llm_chain(capability: str, temperature: float = 0.1) -> Any:
        """
        Public API: Get the best LLM for a capability/tier string.
        Used by all agents throughout the Swarm pipeline.
        """
        tier = AIModelRegistry.resolve_capability(capability, complexity=capability)
        return AIModelRegistry.get_llm_for_tier(tier, temperature=temperature)

    @staticmethod
    def get_optimal_llm(task_role: str, complexity: str = "fast") -> Any:
        """
        Compatibility shim — resolves role+complexity to a tier and returns the LLM.
        """
        tier = AIModelRegistry.resolve_capability(task_role, complexity=complexity)
        return AIModelRegistry.get_llm_for_tier(tier)

    @staticmethod
    def get_all_llms(capability: str, temperature: float = 0.1) -> List[Any]:
        """Returns a list of LLMs for ensemble/MoA usage."""
        primary = AIModelRegistry.get_llm_chain(capability, temperature)
        return [primary]
