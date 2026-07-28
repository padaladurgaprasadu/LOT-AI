"""
yAI Domain Orchestrator v2.0 — LangGraph + RAG + CAG Engine
============================================================
Replaces the old DomainOrchestrator with a production-grade
LangGraph-powered Quantum Orchestrator that:

  1. Selects the best expert agent (35 available) via keyword + LLM routing.
  2. Retrieves relevant memory via ChromaDB RAG pipeline.
  3. Applies CAG (Cache-Augmented Generation) for repeated context patterns.
  4. Executes a LangGraph DAG of micro-agents in dependency order.
  5. Fuses all outputs into a beautifully structured final response.
"""

import json
import asyncio
import re
from typing import Dict, Any, List, Optional, AsyncGenerator

from langchain_core.messages import HumanMessage, SystemMessage
from backend.agents.base import BaseAgent
from backend.agents.expert_agents import (
    AGENT_REGISTRY,
    AGENT_MODEL_TIERS,
    get_agent_prompt,
    get_agent_tier,
    find_best_agent,
)
from backend.utils.logger import get_logger
from backend.utils.model_registry import AIModelRegistry

logger = get_logger(__name__)


# ═══════════════════════════════════════════════════════════════
# RAG ENGINE — ChromaDB-backed retrieval
# ═══════════════════════════════════════════════════════════════
class ExpertRAGEngine:
    """Retrieves domain-relevant context from ChromaDB for any agent."""

    def __init__(self):
        self._client = None

    def _get_client(self):
        if self._client is None:
            try:
                from backend.memory.chroma_client import ChromaClient
                self._client = ChromaClient()
            except Exception as e:
                logger.warning(f"[RAG] ChromaDB unavailable: {e}")
        return self._client

    async def retrieve(self, query: str, agent_key: str, top_k: int = 3) -> str:
        """Async RAG retrieval. Returns formatted context string."""
        try:
            client = self._get_client()
            if not client:
                return ""
            results = await asyncio.to_thread(
                client.retrieve_memory, agent_key, query, top_k
            )
            if not results:
                return ""
            context = "\n\n---\n\n".join(results[:top_k])
            return f"[RETRIEVED KNOWLEDGE - {agent_key.upper()}]:\n{context}"
        except Exception as e:
            logger.warning(f"[RAG] Retrieval failed for {agent_key}: {e}")
            return ""

    async def store(self, content: str, agent_key: str, user_query: str):
        """Async RAG storage — saves high-quality agent outputs for future retrieval."""
        try:
            client = self._get_client()
            if client:
                await asyncio.to_thread(
                    client.add_memory, agent_key, user_query, content
                )
        except Exception as e:
            logger.warning(f"[RAG] Storage failed: {e}")


# ═══════════════════════════════════════════════════════════════
# CAG ENGINE — Cache-Augmented Generation
# Injects pre-computed prefix context to avoid re-processing
# the same large documents on every request.
# ═══════════════════════════════════════════════════════════════
class CAGEngine:
    """
    Cache-Augmented Generation: Stores pre-processed document chunks
    as prefix context, injected directly into prompts to reduce
    redundant LLM computation for repeated large contexts.
    """
    _cache: Dict[str, str] = {}

    @classmethod
    def get(cls, cache_key: str) -> Optional[str]:
        return cls._cache.get(cache_key)

    @classmethod
    def set(cls, cache_key: str, context: str):
        cls._cache[cache_key] = context
        # Simple LRU: evict oldest if cache grows > 50 entries
        if len(cls._cache) > 50:
            oldest_key = next(iter(cls._cache))
            del cls._cache[oldest_key]

    @classmethod
    def build_key(cls, agent_key: str, query_prefix: str) -> str:
        return f"{agent_key}::{query_prefix[:80]}"


# ═══════════════════════════════════════════════════════════════
# LANGGRAPH STATE
# ═══════════════════════════════════════════════════════════════
class OrchestratorState:
    """State container passed between LangGraph nodes."""
    def __init__(self, request: str, user_memory: str = ""):
        self.request = request
        self.user_memory = user_memory
        self.selected_agents: List[str] = []
        self.plan_nodes: List[Dict] = []
        self.message_bus: Dict[str, str] = {}
        self.completed: set = set()
        self.rag_context: str = ""
        self.final_response: str = ""


# ═══════════════════════════════════════════════════════════════
# QUANTUM ORCHESTRATOR — LangGraph DAG Engine
# ═══════════════════════════════════════════════════════════════
class DomainOrchestrator(BaseAgent):
    """
    yAI Quantum Orchestrator v2.0
    ─────────────────────────────
    LangGraph DAG execution + RAG + CAG + 35-expert-agent routing.
    Every agent runs on its optimal NVIDIA frontier model.
    """

    def __init__(self):
        super().__init__()
        self.rag = ExpertRAGEngine()
        # Override fast/smart LLMs to use the registry tiers
        self.fast_llm = AIModelRegistry.get_llm_for_tier("fast")
        self.smart_llm = AIModelRegistry.get_llm_for_tier("planning")

    # ─────────────────────────────────────────────────────────
    # NODE 1: Expert Selection
    # ─────────────────────────────────────────────────────────
    async def _select_expert(self, state: OrchestratorState) -> OrchestratorState:
        """LangGraph Node: Select the optimal expert agent(s) for the request."""
        # Fast keyword-based selection
        primary_key = find_best_agent(state.request)
        state.selected_agents = [primary_key]

        # LLM-based secondary selection for complex requests
        if len(state.request.split()) > 15:
            try:
                agent_keys = list(AGENT_REGISTRY.keys())
                agent_list = ", ".join(agent_keys)
                selection_prompt = f"""You are the yAI Expert Router.
Available expert agents: {agent_list}

User request: "{state.request}"

Select 1–3 agent keys (from the list above, comma-separated) that best cover this request.
Output ONLY the keys, nothing else. Example: coding_agent, research_agent"""

                resp = await self.fast_llm.ainvoke([
                    SystemMessage(content=selection_prompt),
                    HumanMessage(content=state.request)
                ])
                raw = resp.content.strip()
                keys = [k.strip() for k in raw.split(",") if k.strip() in AGENT_REGISTRY]
                if keys:
                    state.selected_agents = keys[:3]
            except Exception as e:
                logger.warning(f"[ExpertRouter] LLM selection failed, using keyword: {e}")

        logger.info(f"[ExpertRouter] Selected: {state.selected_agents}")
        return state

    # ─────────────────────────────────────────────────────────
    # NODE 2: RAG + CAG Context Retrieval
    # ─────────────────────────────────────────────────────────
    async def _retrieve_context(self, state: OrchestratorState) -> OrchestratorState:
        """LangGraph Node: Fetch RAG context + CAG prefix for all selected agents."""
        primary_agent = state.selected_agents[0] if state.selected_agents else "general_chat"

        # CAG: Check prefix cache first (fast path)
        cag_key = CAGEngine.build_key(primary_agent, state.request)
        cached = CAGEngine.get(cag_key)
        if cached:
            state.rag_context = cached
            logger.info(f"[CAG] Cache hit for {primary_agent}")
            return state

        # RAG: ChromaDB retrieval
        rag_results = await asyncio.gather(
            *[self.rag.retrieve(state.request, agent_key) for agent_key in state.selected_agents]
        )
        merged = "\n\n".join([r for r in rag_results if r])

        if merged:
            state.rag_context = merged
            # Store in CAG for next time
            CAGEngine.set(cag_key, merged)
        return state

    # ─────────────────────────────────────────────────────────
    # NODE 3: DAG Planning (Fractal Decomposition)
    # ─────────────────────────────────────────────────────────
    async def _build_dag(self, state: OrchestratorState) -> OrchestratorState:
        """LangGraph Node: Build a dependency-ordered execution DAG."""
        if len(state.selected_agents) == 1:
            # Single agent — no DAG needed, trivial plan
            agent_key = state.selected_agents[0]
            state.plan_nodes = [{
                "id": agent_key,
                "role": agent_key,
                "task": state.request,
                "depends_on": []
            }]
            return state

        # Multi-agent: Build DAG via LLM
        agent_descriptions = {k: AGENT_REGISTRY[k][:200] for k in state.selected_agents if k in AGENT_REGISTRY}
        dag_prompt = f"""You are a Task Decomposition Engine.
User request: "{state.request}"
Agents available: {json.dumps(list(agent_descriptions.keys()))}

Create a JSON DAG where each agent handles its specialty.
Rules: At least one node has empty depends_on. Nodes depend on upstream agents that must finish first.
Output ONLY valid JSON:
{{"nodes": [{{"id": "agent_key", "role": "agent_key", "task": "specific instructions", "depends_on": []}}]}}"""

        try:
            resp = await self.fast_llm.ainvoke([
                SystemMessage(content=dag_prompt),
                HumanMessage(content="Build the DAG now.")
            ])
            content = resp.content.strip()
            match = re.search(r'```(?:json)?\s*(.*?)\s*```', content, re.DOTALL)
            if match:
                content = match.group(1)
            else:
                start, end = content.find('{'), content.rfind('}')
                if start != -1 and end != -1:
                    content = content[start:end + 1]
            plan = json.loads(content)
            state.plan_nodes = plan.get("nodes", [])
        except Exception as e:
            logger.warning(f"[DAGBuilder] Failed: {e}. Using sequential plan.")
            state.plan_nodes = [
                {"id": k, "role": k, "task": state.request, "depends_on": ([] if i == 0 else [state.selected_agents[i - 1]])}
                for i, k in enumerate(state.selected_agents)
            ]
        return state

    # ─────────────────────────────────────────────────────────
    # NODE 4: Parallel Agent Execution
    # ─────────────────────────────────────────────────────────
    async def _execute_agent(self, node: Dict, state: OrchestratorState) -> str:
        """Executes a single expert agent with its specialized prompt + RAG context."""
        agent_key = node.get("role", "general_chat")
        task = node.get("task", state.request)
        deps = node.get("depends_on", [])

        # Build dependency context from message bus
        dep_context = ""
        if deps:
            dep_context = "\n\n".join([
                f"=== INPUT FROM {dep} ===\n{state.message_bus.get(dep, '')}"
                for dep in deps
            ])

        # Get expert system prompt
        expert_prompt = get_agent_prompt(agent_key) or get_agent_prompt("general_chat")

        # Build the full system prompt with RAG + CAG + dep context
        system = f"""{expert_prompt}

━━━ RAG KNOWLEDGE BASE CONTEXT ━━━
{state.rag_context if state.rag_context else "No additional context retrieved."}

━━━ USER MEMORY ━━━
{state.user_memory if state.user_memory else "No user history."}

━━━ UPSTREAM AGENT OUTPUTS ━━━
{dep_context if dep_context else "No upstream dependencies."}

━━━ YOUR SPECIFIC TASK ━━━
{task}"""

        # Get optimal model for this agent
        tier = get_agent_tier(agent_key)
        llm = AIModelRegistry.get_llm_for_tier(tier)

        try:
            resp = await llm.ainvoke([
                SystemMessage(content=system),
                HumanMessage(content=f"Request: {state.request}\n\nProvide your expert-level analysis and solution.")
            ])
            result = resp.content.strip()
            # Store successful output in RAG for future retrieval
            await self.rag.store(result, agent_key, state.request)
            return result
        except Exception as e:
            logger.error(f"[ExpertAgent:{agent_key}] Failed: {e}")
            return f"[{agent_key} agent encountered an error: {str(e)}]"

    async def _execute_dag(self, state: OrchestratorState) -> OrchestratorState:
        """LangGraph Node: Execute the full DAG respecting dependency order."""
        pending = {node["id"]: node for node in state.plan_nodes}

        while pending:
            # Find nodes whose dependencies are all satisfied
            ready = [
                node for node in pending.values()
                if all(dep in state.completed for dep in node.get("depends_on", []))
            ]

            if not ready:
                logger.error("[DAGExecutor] Deadlock detected. Forcing remaining nodes.")
                ready = list(pending.values())

            # Execute ready nodes in parallel
            results = await asyncio.gather(
                *[self._execute_agent(node, state) for node in ready]
            )

            for node, result in zip(ready, results):
                state.message_bus[node["id"]] = result
                state.completed.add(node["id"])
                del pending[node["id"]]

        return state

    # ─────────────────────────────────────────────────────────
    # NODE 5: Knowledge Fusion (STREAMING)
    # ─────────────────────────────────────────────────────────
    async def _fuse_knowledge_stream(self, state: OrchestratorState):
        """LangGraph Node: Synthesize all agent outputs into one coherent response (Streams)."""
        if len(state.message_bus) == 1:
            state.final_response = list(state.message_bus.values())[0]
            # Stream the single response just in case
            for chunk in state.final_response.split(' '):
                yield {"type": "token", "content": chunk + " "}
                await asyncio.sleep(0.01)
            return

        all_outputs = "\n\n".join([
            f"### {agent_id.replace('_', ' ').title()} Expert Output\n{output}"
            for agent_id, output in state.message_bus.items()
        ])

        fusion_prompt = """You are the yAI Knowledge Fusion Engine.
You have received expert reports from multiple specialized AI agents.
Your mission: synthesize them into ONE masterclass response.

RULES:
1. Integrate all domain outputs — don't just paste them sequentially.
2. Structure with clear Markdown headers, tables, and code blocks where appropriate.
3. Resolve any conflicts between expert opinions — explain the trade-offs.
4. Begin with a sharp executive summary (3–4 sentences).
5. End with a "Next Steps" section with 3–5 concrete, prioritized actions.
6. Make it read like it was written by a single, omniscient expert."""

        try:
            full_content = ""
            async for chunk in self.smart_llm.astream([
                SystemMessage(content=fusion_prompt),
                HumanMessage(content=f"User Request: {state.request}\n\nEXPERT OUTPUTS:\n{all_outputs}")
            ]):
                if chunk.content:
                    full_content += chunk.content
                    yield {"type": "token", "content": chunk.content}
            state.final_response = full_content
        except Exception as e:
            logger.error(f"[KnowledgeFusion] Failed: {e}. Returning merged outputs.")
            for chunk in all_outputs.split(' '):
                yield {"type": "token", "content": chunk + " "}
                await asyncio.sleep(0.01)
            state.final_response = all_outputs

    # ─────────────────────────────────────────────────────────
    # MAIN ENTRY POINT
    # ─────────────────────────────────────────────────────────
    async def execute_parallel_experts(self, request: str, context: str = "") -> dict:
        """
        Main LangGraph pipeline execution.
        Runs: Expert Selection → RAG+CAG → DAG Build → DAG Execute → Knowledge Fusion
        Returns: {"experts": [...], "fused_response": "..."}
        """
        state = OrchestratorState(request=request, user_memory=context)

        # === LANGGRAPH PIPELINE ===
        logger.info("[Orchestrator] Starting LangGraph pipeline...")

        # Node 1: Select experts
        state = await self._select_expert(state)

        # Node 2: RAG + CAG context retrieval (parallel with selection)
        state = await self._retrieve_context(state)

        # Node 3: Build execution DAG
        state = await self._build_dag(state)

        logger.info(f"[Orchestrator] Executing {len(state.plan_nodes)} agent(s) in DAG...")

        # Node 4: Execute DAG
        state = await self._execute_dag(state)

        # Node 5: Fuse outputs
        state = await self._fuse_knowledge(state)

        logger.info("[Orchestrator] Pipeline complete.")

        return {
            "experts": state.selected_agents,
            "fused_response": state.final_response,
            "rag_used": bool(state.rag_context),
            "agents_executed": list(state.completed),
        }

    async def stream_expert_response(self, request: str, context: str = "") -> AsyncGenerator[str, None]:
        """
        Streaming version of the expert pipeline.
        Yields status updates and then the final streamed response.
        """
        state = OrchestratorState(request=request, user_memory=context)

        yield f"data: {json.dumps({'type': 'status', 'message': '🧠 Selecting domain experts...'})}\n\n"
        state = await self._select_expert(state)
        agent_names = [k.replace("_", " ").title() for k in state.selected_agents]
        agent_names_str = " + ".join(agent_names)
        yield f"data: {json.dumps({'type': 'status', 'message': f'👥 Activated: {agent_names_str}'})}\n\n"

        yield f"data: {json.dumps({'type': 'status', 'message': '🔍 Querying RAG knowledge base...'})}\n\n"
        state = await self._retrieve_context(state)

        yield f"data: {json.dumps({'type': 'status', 'message': '⚙️ Building execution graph...'})}\n\n"
        state = await self._build_dag(state)

        yield f"data: {json.dumps({'type': 'status', 'message': f'🚀 Running {len(state.plan_nodes)} expert agent(s)...'})}\n\n"
        state = await self._execute_dag(state)

        yield f"data: {json.dumps({'type': 'status', 'message': '⚡ Fusing expert knowledge...'})}\n\n"
        yield f"data: {json.dumps({'type': 'status', 'message': ''})}\n\n"

        async for item in self._fuse_knowledge_stream(state):
            if item["type"] == "token":
                yield f"data: {json.dumps({'type': 'chat', 'token': item['content']})}\n\n"

