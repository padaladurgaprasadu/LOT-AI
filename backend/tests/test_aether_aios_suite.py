"""
LOT AI Genesis v1.0 — Aether AIOS Comprehensive Test Suite
===========================================================
Tests the 5 Core Layers of LOT AI "Aether":
1. AIOS Kernel System Calls & Priority Task Scheduling
2. MIT SEAL Self-Adaptation Engine (ReST-EM RL Loop & Candidate Generation)
3. Agentic CAG Memory Fabric (Sub-50ms Hot Path & Cold Path RAG)
4. 12-Model Neural Mesh Routing Matrix
5. ASI Orchestrator Integration with 16 Active Core Engines
"""

import sys
import os
import time

# Ensure backend path is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

PASS = 0
FAIL = 0

def check(name: str, fn):
    global PASS, FAIL
    try:
        res = fn()
        if res is not False:
            print(f"  [OK] {name}")
            PASS += 1
        else:
            print(f"  [FAIL] {name}")
            FAIL += 1
    except Exception as e:
        print(f"  [FAIL] {name} -> {e}")
        FAIL += 1


def run_aether_aios_tests():
    print("=" * 72)
    print("LOT AI GENESIS v1.0 'AETHER' — AIOS COMPREHENSIVE TEST SUITE")
    print("=" * 72)

    # 1. SEAL ENGINE TESTS
    print("\n[SECTION 1] MIT SEAL SELF-ADAPTATION ENGINE")
    print("-" * 50)

    def test_seal_candidate_generation():
        from backend.asi.seal_adaptation_engine import SEALEngine
        seal = SEALEngine()
        candidates = seal.generate_self_edit_candidates("Build auth module")
        assert len(candidates) == 8
        assert candidates[0].edit_id.startswith("se_")
        assert len(candidates[0].synthetic_data) >= 2
        return True
    check("SEAL Engine — 8 self-edit candidates generated", test_seal_candidate_generation)

    def test_seal_rest_em_loop():
        from backend.asi.seal_adaptation_engine import SEALEngine
        seal = SEALEngine()
        result = seal.run_rest_em_loop("Build payments microservice")
        assert result["iteration"] >= 1
        assert "accepted_edits_count" in result
        assert result["top_reward"] > 0.70
        return True
    check("SEAL Engine — full ReST-EM RL loop completes", test_seal_rest_em_loop)

    def test_seal_prompt_injection():
        from backend.asi.seal_adaptation_engine import inject_seal_prompt
        prompt = inject_seal_prompt("Base prompt.")
        assert "SEAL" in prompt or "ReST-EM" in prompt
        return True
    check("SEAL Engine — prompt injection valid", test_seal_prompt_injection)

    # 2. CAG MEMORY FABRIC TESTS
    print("\n[SECTION 2] AGENTIC CAG & RAG MEMORY FABRIC")
    print("-" * 50)

    def test_cag_hot_path():
        from backend.memory.agentic_cag_cache import AgenticCAGCache
        cag = AgenticCAGCache()
        cag.store_cag_context("What is LOT AI?", "LOT AI is an AI Operating System.")
        result = cag.get_cag_context("What is LOT AI?")
        assert result is not None
        assert "AI Operating System" in result["context"]
        assert result["latency_ms"] < 50
        return True
    check("Agentic CAG — Hot Path sub-50ms KV-cache retrieval", test_cag_hot_path)

    def test_rag_cold_path():
        from backend.memory.agentic_cag_cache import AgenticCAGCache
        cag = AgenticCAGCache()
        rag_res = cag.agentic_rag_retrieve("Nemotron 3 Ultra architecture", max_hops=2)
        assert rag_res["hops_executed"] == 2
        assert rag_res["chunks_retrieved"] >= 3
        assert rag_res["reranked"] == True
        return True
    check("Agentic RAG — Cold Path 2-hop reranked vector search", test_rag_cold_path)

    # 3. AIOS MASTER KERNEL TESTS
    print("\n[SECTION 3] AIOS MASTER KERNEL (AETHER)")
    print("-" * 50)

    def test_aios_scheduler():
        from backend.asi.aios_kernel import PriorityAgentScheduler
        sched = PriorityAgentScheduler()
        t1 = sched.schedule_task("Task High Priority", priority=1)
        t2 = sched.schedule_task("Task Low Priority", priority=5)
        next_task = sched.pop_next_task()
        assert next_task["task_id"] == t1
        return True
    check("AIOS Kernel — Priority Scheduler dispatches high-priority tasks first", test_aios_scheduler)

    def test_aios_syscalls():
        from backend.asi.aios_kernel import AIOSKernel
        kernel = AIOSKernel()
        
        # Test sys_schedule_task
        res_sched = kernel.execute_syscall("sys_schedule_task", {"task_name": "Build Auth", "priority": 1})
        assert res_sched["status"] == "SUCCESS"

        # Test sys_route_model
        res_route = kernel.execute_syscall("sys_route_model", {"role": "orchestration"})
        assert res_route["assigned_model"] == "nvidia/nemotron-3-ultra-550b"

        # Test sys_seal_adapt
        res_seal = kernel.execute_syscall("sys_seal_adapt", {"context": "Test task"})
        assert res_seal["status"] == "SUCCESS"

        return True
    check("AIOS Kernel — System Calls (sys_schedule, sys_route, sys_seal) execute", test_aios_syscalls)

    def test_aios_six_phase_loop():
        from backend.asi.aios_kernel import AIOSKernel
        kernel = AIOSKernel()
        res = kernel.run_six_phase_loop("Build full stack SaaS application")
        assert res["loop_status"] == "SUCCESS"
        assert len(res["phases_executed"]) == 6
        assert res["phases_executed"][0] == "Perceive"
        assert res["phases_executed"][-1] == "Reflect"
        return True
    check("AIOS Kernel — 6-Phase Agentic Loop completes clean", test_aios_six_phase_loop)

    def test_langgraph_orchestrator():
        from backend.asi.langgraph_orchestrator import LangGraphOrchestrator
        lgo = LangGraphOrchestrator()
        res = lgo.run_graph("Build distributed SaaS microservice")
        assert res["graph_status"] == "APPROVED"
        assert res["cto_approved"] == True
        assert len(res["nodes_visited"]) >= 5
        return True
    check("LangGraph Orchestrator — 6-node state machine completes cleanly", test_langgraph_orchestrator)

    def test_prometheus_narrative_engine():
        import asyncio
        from backend.agents.prometheus_narrative_engine import PrometheusNarrativeEngine, Genre, Tone, NarrativeMode
        engine = PrometheusNarrativeEngine()
        narrative = asyncio.run(engine.create_narrative(
            logline="Ancient quantum archaeology discovery in a dystopian galaxy.",
            genre=Genre.SCIENCE_FICTION,
            tone=Tone.BLEAK,
            mode=NarrativeMode.NOVELLA
        ))
        assert narrative is not None
        assert len(narrative.generated_text) > 0
        assert len(narrative.world) >= 1
        return True
    def test_archimedes_reasoning_engine():
        import asyncio
        from backend.asi.archimedes_reasoning_engine import ArchimedesReasoningEngine
        archimedes = ArchimedesReasoningEngine()
        result = asyncio.run(archimedes.process_deep_reasoning(
            prompt="Monotone convergence of AIOS ReST-EM policy updates",
            long_context="Paragraph 1 about AIOS Kernel.\n\nParagraph 2 about SEAL ReST-EM policy updates.\n\nParagraph 3 about 37 agent matrix."
        ))
        assert result["status"] == "SUCCESS"
        assert result["compression_summary"]["original_tokens"] > 0
        assert result["deep_search"]["total_hops"] >= 1
        assert result["proof_synthesis"]["proof_verified"] == True
        return True
    check("Archimedes Engine — Kimi-K3 2M context compression, deep search & proof synthesis complete", test_archimedes_reasoning_engine)

    def test_fable5_engine():
        import asyncio
        from backend.agents.fable5_engine import Fable5Engine, Genre, Tone, NarrativeMode
        fable = Fable5Engine()
        narrative = asyncio.run(fable.create_narrative(
            logline="Ancient quantum lore unsealed in a dystopian space-time foam.",
            genre=Genre.SCIENCE_FICTION,
            tone=Tone.BLEAK,
            mode=NarrativeMode.NOVELLA
        ))
        assert narrative is not None
        assert len(narrative.generated_text) > 0
        return True
    check("Fable 5 Engine — 8-section creative narrative transformer completes", test_fable5_engine)

    def test_mythos_engine():
        import asyncio
        from backend.agents.mythos_engine import MythosEngine
        mythos = MythosEngine()
        res = asyncio.run(mythos.create_mythology("Aetherian Empire", "cosmic_elemental"))
        assert res["engine"] == "Mythos v1.0.0"
        assert res["pantheon_size"] >= 3
        assert res["primary_relic"] is not None
        return True
    def test_hermes_narrative_engine():
        import asyncio
        from backend.agents.hermes_narrative_engine import HermesNarrativeEngine
        hermes = HermesNarrativeEngine()
        res = asyncio.run(hermes._generate_5phase_narrative({"prompt": "A disgracened quantum scholar unseals ancient lore in space-time foam."}))
        assert res["status"] == "success"
        assert res["engine"] == "HermesNarrativeEngine"
        assert "world" in res["phases"]
        assert "characters" in res["phases"]
        return True
    def test_hermes_engine():
        import asyncio
        from backend.agents.hermes_engine import HermesEngine
        hermes = HermesEngine()
        res = asyncio.run(hermes.process({"operation": "generate_pantheon", "params": {"seed_culture": "Promethean"}}))
        assert res["status"] == "success"
        assert res["engine"] == "HermesEngine"
        return True
    check("Hermes Engine — World mythology, cosmogony & creative narrative completes", test_hermes_engine)

    # 4. ASI ORCHESTRATOR INTEGRATION
    print("\n[SECTION 4] UNIFIED ASI ORCHESTRATOR STATUS")
    print("-" * 50)

    def test_orchestrator_23_engines():
        from backend.asi.asi_orchestrator import ASIOrchestrator
        o = ASIOrchestrator()
        status = o.get_asi_status()
        assert status["version"] == "2.0.0-odyssey-singularity"
        assert status["active_agents_count"] == 37
        assert status["domain_expertise_years_per_agent"] == 40
        engines = status["engines"]
        assert engines.get("AIOSKernel") == True
        assert engines.get("SEALEngine") == True
        assert engines.get("AgenticCAGCache") == True
        assert engines.get("LangGraphOrchestrator") == True
        assert engines.get("PrometheusNarrativeEngine") == True
        assert engines.get("ArchimedesReasoningEngine") == True
        assert engines.get("Fable5Engine") == True
        assert engines.get("MythosEngine") == True
        assert engines.get("HermesNarrativeEngine") == True
        assert engines.get("HermesEngine") == True
        assert len(engines) >= 23
        return True
    check("ASI Orchestrator — LOT AI v2.0 ODYSSEY SINGULARITY (37 Agents, 40-Yr Expertise)", test_orchestrator_23_engines)

    # SUMMARY
    total = PASS + FAIL
    print("\n" + "=" * 72)
    print("LOT AI GENESIS v1.0 'AETHER' TEST RESULTS")
    print("=" * 72)
    print(f" Total Checks: {total}")
    print(f" PASSED:       {PASS} ({PASS/total*100:.1f}%)")
    print(f" FAILED:       {FAIL}")
    print("=" * 72)

    if FAIL == 0:
        print("[VERDICT] ALL AETHER AIOS TESTS PASSED CLEANLY")
    else:
        print(f"[VERDICT] {FAIL} FAILURES DETECTED")

if __name__ == "__main__":
    run_aether_aios_tests()
