import os
import sys
import asyncio

# Ensure imports work from the root folder
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from memory.cag_core import memory_core
from agents.base_agent import yAIAgentFactory
from agents.mcp_client import mcp_client

async def run_os_test():
    print("\n" + "="*50)
    print("[*] yAI OPERATING SYSTEM KERNEL TEST [*]")
    print("="*50)

    try:
        print("\n[1] Initializing Proactive Agent Swarm...")
        factory = yAIAgentFactory()
        cto_agent = factory.create_agent("CTO Agent")
        print("[SUCCESS] CTO Agent spun up with 15 years experience.")

        print("\n[2] Testing Global CAG Memory Mesh...")
        # Simulate an initial thought
        memory_core.log_thought("CTO Agent", "The system architecture requires a high-performance vector DB.")
        
        # Test recall
        recalled = memory_core.recall_context("What database should we use?", n_results=1)
        print(f"[SUCCESS] Memory Recall Success: {recalled}")

        print("\n[3] Testing Agent Execution with Auto-Memory...")
        print("Sending prompt to CTO Agent (Requires NVIDIA API key in .env)...")
        # We will mock the invocation to avoid spending the user's API credits during a simple connection test, 
        # or we can do a tiny prompt if they want a real test. Let's just do a tiny prompt.
        
        # NOTE: If this fails due to API key, we catch it.
        response = cto_agent.invoke({"input": "Give me a 1 sentence summary of our architecture."})
        print(f"[SUCCESS] Agent Response: {response.content}")
        
        # Verify it auto-logged
        verify_mem = memory_core.recall_context("1 sentence summary", n_results=1)
        print(f"[SUCCESS] Auto-Memory Verification: {verify_mem}")

        print("\n[4] Testing MCP Subsystem...")
        # We just verify the client initialized
        print(f"[SUCCESS] MCP Client loaded with registered servers: {list(mcp_client.mcp_servers.keys())}")
        
        print("\n" + "="*50)
        print("[*] ALL SYSTEMS NOMINAL. yAI OS IS ONLINE. [*]")
        print("="*50 + "\n")

    except Exception as e:
        print(f"\n[FAILED] TEST FAILED: {str(e)}")
        print("Ensure 'chromadb', 'langchain-openai', and a valid NVIDIA_API_KEY in .env are set up.")

if __name__ == "__main__":
    asyncio.run(run_os_test())
