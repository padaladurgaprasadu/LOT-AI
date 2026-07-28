import asyncio
import sys
import os
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.orchestrator.swarm_manager import SwarmManager

async def test_final():
    print("=== Testing Omni-Intelligence Final Pillars (5, 6, 7) ===")
    
    manager = SwarmManager()
    
    # Mocking fast_llm to avoid external API calls during testing, but simulate the flow
    async def mock_execute(role, prompt):
        print(f"\n[{role}] received prompt snippet: {prompt[:150]}...")
        if role == "Architect":
            return "Design: Uses React and Supabase. Incorporates Mythos UX constraints and Bandit skill."
        elif role == "Coder":
            return "def vulnerable_login():\n  query = f'SELECT * FROM users WHERE name = {user_input}'"
        elif role == "Auditor":
            # Simulate the Red Team Auditor finding a SQLi
            if "SELECT * FROM users WHERE name =" in prompt:
                return "VULNERABILITY DETECTED: SQL Injection possible. Rewrite with parameterized queries."
            return "APPROVED"
            
    manager._agent_execute = mock_execute
    
    # Mock MythosSimEngine
    from backend.agents.mythos_reflection import MythosSimEngine
    async def mock_mythos(task):
        return "UX Matrix: Ensure login button provides immediate loading state, and handle invalid auth gracefully."
    MythosSimEngine.simulate_user_journey = mock_mythos
    
    task = "Build a login form."
    print(f"\nSubmitting task to Omni-Swarm: {task}")
    
    result = await manager.spawn_swarm(task)
    
    print("\n=== FINAL DAG EXECUTION GRAPH ===")
    print(json.dumps(result.get("graph"), indent=2))

if __name__ == "__main__":
    asyncio.run(test_final())
