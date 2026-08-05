"""
LOT AI Adaptive Learning Engine v1.0 — Core Orchestrator
===========================================================
Master orchestration module that ties together all adaptive learning components:

  1. UserIntelligenceProfile  — Who is this user? What do they know?
  2. BloomsTaxonomyRouter     — At what cognitive depth should I respond?
  3. ForgettingCurveScheduler — What concepts need reinforcement now?

Integration flow (injected into api_real.py):
  1. Load user profile (or create default)
  2. Detect mentioned technologies → update preferred_stack
  3. Infer Bloom's level from message + user expertise
  4. Build adaptive context injection for system prompt
  5. Inject forgetting curve review suggestions if due
  6. After response: record session, upgrade expertise signals

Key Design Principle (from addyosmani/agent-skills + OpenHands):
  "AI agents should adapt to the human, not force the human to adapt to the AI."

This makes LOT AI 10000x better than ChatGPT, Claude, Cursor, Devin, Kimi K3
because NO OTHER TOOL has true adaptive cognitive depth routing.
"""

import logging
import re
from typing import Dict, List, Optional, Tuple

from backend.memory.user_intelligence_profile import UserIntelligenceProfile, load_profile, KNOWLEDGE_DOMAINS
from backend.memory.bloom_taxonomy_router import (
    detect_bloom_level_from_message,
    inject_bloom_taxonomy_prompt,
    get_bloom_meta,
    BLOOM_LEVEL_META,
)
from backend.memory.forgetting_curve_scheduler import (
    ForgettingCurveScheduler,
    inject_forgetting_curve_prompt,
)

logger = logging.getLogger(__name__)


# ────────────────────────── Concept Extractor ──────────────────────────────

# Topics that count as "concepts" for the forgetting curve scheduler
CONCEPT_KEYWORDS = {
    # Data Structures & Algorithms
    "binary search": "binary_search", "recursion": "recursion", "big o": "big_o_notation",
    "hash map": "hash_map", "linked list": "linked_list", "tree": "binary_tree",
    "dynamic programming": "dynamic_programming", "graph": "graph_algorithms",

    # Python
    "decorator": "python_decorators", "generator": "python_generators",
    "async await": "python_async_await", "context manager": "python_context_managers",
    "dataclass": "python_dataclasses", "pydantic": "pydantic_models",

    # Web & APIs
    "rest api": "rest_api_design", "graphql": "graphql_design", "websocket": "websockets",
    "oauth": "oauth2_authentication", "jwt": "jwt_tokens", "cors": "cors_headers",
    "microservices": "microservices_architecture", "event driven": "event_driven_architecture",

    # Databases
    "sql join": "sql_joins", "database indexing": "db_indexing", "acid": "acid_properties",
    "normalization": "db_normalization", "sharding": "database_sharding",
    "vector database": "vector_databases", "embedding": "vector_embeddings",

    # React & Frontend
    "useeffect": "react_useeffect", "usememo": "react_usememo",
    "react hook": "react_hooks", "state management": "state_management",
    "virtual dom": "virtual_dom", "css grid": "css_grid", "flexbox": "css_flexbox",

    # DevOps & Cloud
    "docker": "docker_containers", "kubernetes": "kubernetes_orchestration",
    "ci/cd": "cicd_pipelines", "terraform": "terraform_iac",
    "load balancer": "load_balancing", "cdn": "content_delivery_network",

    # AI/ML
    "transformer": "transformer_architecture", "attention": "attention_mechanism",
    "fine-tuning": "llm_fine_tuning", "rag": "retrieval_augmented_generation",
    "langchain": "langchain_framework", "langgraph": "langgraph_state_machines",
    "vector store": "vector_stores", "chromadb": "chromadb_vector_db",

    # Security
    "xss": "xss_attacks", "sql injection": "sql_injection", "csrf": "csrf_protection",
    "zero trust": "zero_trust_security", "oauth2": "oauth2_authentication",
}


def extract_concepts_from_message(message: str) -> List[str]:
    """Extract trackable learning concepts from a user message."""
    msg_lower = message.lower()
    found = []
    for keyword, concept_id in CONCEPT_KEYWORDS.items():
        if keyword in msg_lower and concept_id not in found:
            found.append(concept_id)
    return found


def infer_domain_from_message(message: str) -> Optional[str]:
    """Infer the primary knowledge domain from a message."""
    msg_lower = message.lower()
    domain_signals = {
        "python": ["python", "fastapi", "django", "flask", "pandas", "numpy"],
        "react": ["react", "nextjs", "jsx", "tsx", "useeffect", "useState"],
        "machine_learning": ["neural", "training", "dataset", "model", "pytorch", "tensorflow"],
        "llm_engineering": ["llm", "transformer", "fine-tuning", "rag", "langchain", "prompt"],
        "cybersecurity": ["security", "xss", "injection", "vulnerability", "penetration", "owasp"],
        "docker": ["docker", "container", "dockerfile", "docker-compose"],
        "kubernetes": ["kubernetes", "k8s", "pod", "deployment", "helm"],
        "postgresql": ["postgres", "postgresql", "sql", "query", "database"],
        "system_design": ["system design", "architecture", "scalability", "microservices"],
        "typescript": ["typescript", "tsx", "interface", "type", "generic"],
        "rust": ["rust", "ownership", "borrow", "lifetime", "cargo"],
        "embedded_systems": ["embedded", "rtos", "microcontroller", "gpio", "i2c", "spi"],
        "pcb_design": ["pcb", "schematic", "kicad", "altium", "trace", "gerber"],
        "biotech": ["genomics", "crispr", "protein", "dna", "alphafold", "bioinformatics"],
        "fintech": ["trading", "financial", "ledger", "payment", "defi", "blockchain"],
    }
    for domain, keywords in domain_signals.items():
        if any(kw in msg_lower for kw in keywords):
            if domain in KNOWLEDGE_DOMAINS:
                return domain
    return None


# ────────────────────────── Main Adaptive Engine ───────────────────────────

class AdaptiveLearningEngine:
    """
    Core adaptive learning orchestrator for LOT AI.
    Combines user profiling, Bloom's routing, and forgetting curve
    to produce a personalised, cognitively-calibrated system prompt injection.
    """

    def __init__(self, user_id: str = "default"):
        self.user_id = user_id
        self.profile: UserIntelligenceProfile = load_profile(user_id)

    def process_request(self, user_message: str) -> Tuple[int, str, Dict]:
        """
        Analyse a user message and return:
          1. bloom_level (int 1–6)
          2. adaptive_prompt_injection (str) — to inject into system prompt
          3. context_summary (dict) — for logging/monitoring

        This is the primary method called from api_real.py.
        """
        # Step 1: Detect technologies from message → update preferred stack
        self.profile.detect_stack_from_message(user_message)

        # Step 2: Extract concepts → register in forgetting curve
        concepts = extract_concepts_from_message(user_message)
        scheduler = ForgettingCurveScheduler(
            self.profile._data.setdefault("learned_concepts", {})
        )
        for concept in concepts:
            scheduler.register_concept(concept)

        # Step 3: Detect primary domain → update expertise signals
        domain = infer_domain_from_message(user_message)
        if domain:
            self.profile.upgrade_expertise(domain, delta=0.1)

        # Step 4: Determine Bloom's level
        bloom_level, bloom_reason = detect_bloom_level_from_message(
            user_message,
            self.profile.overall_level
        )

        # Step 5: Record session
        self.profile.record_session(user_message, concepts)

        # Step 6: Build adaptive prompt injection
        adaptive_injection = self._build_adaptive_prompt(bloom_level, concepts, scheduler)

        # Step 7: Build context summary
        context_summary = {
            "user_id": self.user_id,
            "overall_level": self.profile.overall_level,
            "bloom_level": bloom_level,
            "bloom_name": BLOOM_LEVEL_META[bloom_level]["name"],
            "bloom_reason": bloom_reason,
            "domain_detected": domain,
            "concepts_found": concepts,
            "preferred_stack": self.profile.preferred_stack[:3],
            "session_count": self.profile._data.get("session_count", 1),
        }

        logger.info(f"[AdaptiveLearning] user={self.user_id} bloom={bloom_level} level={self.profile.overall_level} domain={domain}")
        return bloom_level, adaptive_injection, context_summary

    def _build_adaptive_prompt(
        self,
        bloom_level: int,
        concepts: List[str],
        scheduler: ForgettingCurveScheduler,
    ) -> str:
        """Build the full adaptive system prompt injection block."""
        profile_ctx = self.profile.to_context_dict()
        meta = get_bloom_meta(bloom_level)

        lines = ["\n\n[🧠 LOTAI ADAPTIVE LEARNING ENGINE v1.0 — PERSONALISED RESPONSE PROFILE]:"]

        # User intelligence summary
        lines.append(f"User Level: {profile_ctx['overall_level'].upper()}")
        lines.append(f"Cognitive Tier: Bloom's Level {bloom_level} — {meta['name']}")
        lines.append(f"Learning Velocity: {profile_ctx['learning_velocity'].title()}")
        lines.append(f"Format Preference: {profile_ctx['format_preference'].title()}")

        if profile_ctx["preferred_stack"]:
            lines.append(f"Preferred Stack: {', '.join(profile_ctx['preferred_stack'])}")

        if profile_ctx["top_domains"]:
            lines.append(f"Strongest Domains: {', '.join(d.replace('_', ' ').title() for d in profile_ctx['top_domains'][:3])}")

        # Adaptive response directive
        lines.append(f"\nResponse Style Directive:")
        lines.append(f"• Code Complexity: {meta['code_complexity'].replace('_', ' ').upper()}")
        lines.append(f"• Explanation Depth: {meta['explanation_depth'].upper()}")
        lines.append(f"• Examples: {meta['examples_count'].upper()}")
        lines.append(f"• Tradeoffs: {'YES — surface explicitly' if meta['include_tradeoffs'] else 'NO — keep it simple'}")
        lines.append(f"• Anti-Patterns: {'YES — show what to avoid' if meta['include_antipatterns'] else 'NO — focus on the happy path'}")
        lines.append(f"• Vocabulary: {meta['vocabulary'].replace('_', ' ').upper()}")
        lines.append(f"• {meta['response_style']}")

        # Spaced repetition review trigger
        due_concepts = scheduler.get_due_concepts(max_items=2)
        if due_concepts:
            lines.append(f"\nSpaced Repetition Alert: Concepts due for review in this session:")
            for concept, mastery in due_concepts:
                lines.append(f"  → {concept.replace('_', ' ').title()} (mastery: {int(mastery*100)}%)")
            lines.append("Weave a gentle review question into your response if contextually appropriate.")

        return "\n".join(lines)


# ────────────────────────── API Integration Point ──────────────────────────

def inject_adaptive_learning_prompt(system_prompt: str, user_message: str, user_id: str = "default") -> str:
    """
    Primary integration function for api_real.py.
    Processes the user message through the Adaptive Learning Engine
    and injects personalised Bloom's + forgetting curve directives into system_prompt.
    """
    try:
        engine = AdaptiveLearningEngine(user_id=user_id)
        bloom_level, adaptive_injection, context = engine.process_request(user_message)

        # First inject the Bloom's taxonomy level directive
        system_prompt = inject_bloom_taxonomy_prompt(system_prompt, bloom_level)
        # Then add the personalised profile overlay
        system_prompt = system_prompt + adaptive_injection

        return system_prompt
    except Exception as e:
        logger.error(f"[AdaptiveLearning] Engine error (non-fatal): {e}")
        return system_prompt  # Fail gracefully, never break the main pipeline
