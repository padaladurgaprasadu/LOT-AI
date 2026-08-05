"""
LOT AI Spline 3D & WebGL Engine Unit Test Suite
================================================
"""

import sys
import os
import io

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from backend.agents.spline_3d_engine import Spline3DEngine, inject_spline_3d_prompt


def test_spline_catalog():
    print("[Test 1] Testing Spline 3D Scene Catalog...")
    engine = Spline3DEngine()
    assert len(engine.catalog) >= 5
    assert "glass_cyber_ring" in engine.catalog
    print("  [OK] Passed: Catalog contains 5+ production 3D scenes.")


def test_spline_intent_matching():
    print("\n[Test 2] Testing Intent-Based 3D Scene Selection...")
    engine = Spline3DEngine()

    test_queries = {
        "Build a SaaS product landing page": "3D Spatial Device Hero",
        "Design a neural AI brain visualization": "Quantum Particle Sphere",
        "Create a developer CLI website": "3D Neo-Brutalist Mechanical Keyboard",
        "Build a luxury minimal fashion site": "Minimalist Organic Glass Fluid",
    }

    for query, expected_title in test_queries.items():
        scene = engine.get_recommended_scene(query)
        assert scene["title"] == expected_title, f"Expected '{expected_title}', got '{scene['title']}' for '{query}'"
        print(f"  [OK] Query: '{query}' -> Scene: {scene['title']}")


def test_spline_prompt_injection():
    print("\n[Test 3] Testing Spline 3D Prompt Directive Injection...")
    base_prompt = "You are a web designer."
    user_query = "Build an insane 3D website with spline"

    injected = inject_spline_3d_prompt(base_prompt, user_query)
    assert "[✨ INSANE 3D SPLINE & WEBGL ENGINE ACTIVE]" in injected
    assert "@splinetool/react-spline" in injected
    print("  [OK] Passed: Prompt injection active for 3D/Spline intent.")


if __name__ == "__main__":
    print("==================================================")
    print("Running Spline 3D WebGL Engine Unit Tests")
    print("==================================================")
    test_spline_catalog()
    test_spline_intent_matching()
    test_spline_prompt_injection()
    print("\n==================================================")
    print("ALL SPLINE 3D TESTS PASSED SUCCESSFULLY!")
    print("==================================================")
