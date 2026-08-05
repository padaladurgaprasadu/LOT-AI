"""
LOT AI Fable 6 vs Claude Verification & Benchmark Test Suite
============================================================
Tests Fable 6 engine modes, prompt injection, and meta-critique capabilities.
"""

import sys
import os

# Ensure backend is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.agents.fable6_engine import Fable6Engine, inject_fable6_prompt


def test_fable6_initialization():
    print("[Test 1] Fable 6 Engine Initialization...")
    engine = Fable6Engine()
    assert engine.engine_name == "LOT AI Fable 6"
    assert engine.version == "6.0.0"
    assert len(engine.capabilities) == 10
    print("  [OK] Passed: Engine initialized with 10 novelty categories.")


def test_fable6_mode_detection():
    print("\n[Test 2] Fable 6 Creative Mode Detection...")
    engine = Fable6Engine()

    test_queries = {
        "Tell me a story about an autonomous AI startup": "narrative_architecture",
        "Invent a new zero-to-one product for fintech": "zero_to_one_product",
        "Design an award-winning UX interface for mobile": "award_winning_ux",
        "Synthesize a breakthrough idea fusing biology and physics": "cross_domain_fusion",
        "Create a category-defining brand identity and logo concept": "brand_identity",
        "What is the capital of France": "sovereign_synthesis",
    }

    for query, expected_mode in test_queries.items():
        mode = engine._detect_creative_mode(query)
        assert mode == expected_mode, f"Expected {expected_mode}, got {mode} for '{query}'"
        print(f"  [OK] '{query[:45]}...' -> Mode: {mode}")


def test_fable6_prompt_injection():
    print("\n[Test 3] System Prompt Injection...")
    base_prompt = "You are a helpful AI assistant."
    creative_query = "Design an innovative space station OS UI"

    injected_prompt = inject_fable6_prompt(base_prompt, creative_query)
    assert "[💎 LOT AI FABLE 6 CREATIVE INTELLIGENCE ACTIVE]" in injected_prompt
    assert "[✨ UI COMPONENT TOKENS]" in injected_prompt
    print("  [OK] Passed: Fable 6 prompt directives injected successfully.")


def test_fable6_state_run():
    print("\n[Test 4] Synchronous State Pipeline Run...")
    engine = Fable6Engine()
    state = {
        "goal": "Build a zero-to-one product for healthcare",
        "execution_logs": [],
    }

    result_state = engine.run(state)
    assert result_state.get("fable6_active") is True
    assert result_state.get("fable6_mode") == "zero_to_one_product"
    assert result_state.get("fable6_novelty_tokens")["blue_ocean_score"] == 9.4
    print("  [OK] Passed: State pipeline executed with Blue-Ocean score 9.4.")


if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    print("==================================================")
    print("Running LOT AI Fable 6 Benchmark Verification")
    print("==================================================")
    test_fable6_initialization()
    test_fable6_mode_detection()
    test_fable6_prompt_injection()
    test_fable6_state_run()
    print("\n==================================================")
    print("ALL FABLE 6 TESTS PASSED SUCCESSFULLY! (100% READY)")
    print("==================================================")
