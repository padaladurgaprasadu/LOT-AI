import os
import sys
import json
import asyncio

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.memory.repo_graph import DAIMG
from backend.orchestrator.swarm_manager import SwarmManager

async def test_pillar_3():
    print("=== Testing Graphify Memory ===")
    daimg = DAIMG(".")
    print("Building DAIMG...")
    daimg.build_graph()
    
    print("Extracting Langflow format...")
    langflow_graph = daimg.export_to_langflow_format()
    print(f"Graph JSON output snippet (Nodes: {len(langflow_graph['nodes'])}, Edges: {len(langflow_graph['edges'])}):")
    print(json.dumps(langflow_graph, indent=2)[:500] + "\n...")

    print("\n=== Testing Visual Orchestration ===")
    print("Spawning Swarm with mocked fast response...")
    manager = SwarmManager()
    
    # Mocking _agent_execute for fast test
    async def mock_execute(role, prompt):
        return f"{role} says: APPROVED" if "Auditor" in role else f"Mock {role} code."
        
    manager._agent_execute = mock_execute
    
    result = await manager.spawn_swarm("Build a login component", "Context: None")
    
    print("\nExecution Graph (DAG) JSON output snippet:")
    print(json.dumps(result.get("graph", {}), indent=2))
    
if __name__ == "__main__":
    asyncio.run(test_pillar_3())
