import asyncio
import sys
import os
import json
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.orchestrator.swarm_manager import SwarmManager

# Disable overly verbose httpx logging for the interactive demo
logging.getLogger("httpx").setLevel(logging.WARNING)

async def interactive_demo():
    print("="*60)
    print("    yAI OMNI-INTELLIGENCE - INTERACTIVE DEMO (Pillars 1-7)   ")
    print("="*60)
    print("\nThe 7 Pillars are fully active:")
    print("1. WebContainer Workspaces")
    print("2. VLM Browser Perception")
    print("3. Graphify & Langflow Visual DAGs")
    print("4. G-Stack & Supabase")
    print("5. Dynamic Skill Injection (Stitch)")
    print("6. Mythos UX Simulation (Fable5)")
    print("7. Red Team Offensive Security Auditor (H4cker)")
    print("-" * 60)
    
    # Check if NVIDIA_API_KEY is set
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))
    
    if not os.environ.get("NVIDIA_API_KEY"):
        print("\n[WARNING] NVIDIA_API_KEY is not set in .env")
        print("The Swarm will fall back to local mock modes or fail. Please add it to your .env file.\n")
    
    user_idea = input("\nWhat would you like yAI to build? (e.g., 'A realtime chat app'): ")
    if not user_idea.strip():
        user_idea = "A simple login portal"
        print(f"Defaulting to: {user_idea}")
        
    print("\n>>> INITIALIZING OMNI-SWARM >>>\n")
    manager = SwarmManager()
    
    # We execute the Swarm. The SwarmManager now internally calls Mythos, Architect, Coder, and Auditor(Red Team).
    try:
        result = await manager.spawn_swarm(user_idea)
        
        print("\n" + "="*60)
        print("                       FINAL OUTPUT                      ")
        print("="*60)
        print("\n>>> GENERATED CODE & ARCHITECTURE:\n")
        print(result.get("code", "No code generated."))
        
        print("\n" + "="*60)
        print("                GRAPHIFY EXECUTION DAG                   ")
        print("="*60)
        graph = result.get("graph", {})
        print(f"Nodes executed: {len(graph.get('nodes', []))}")
        print(f"Edges mapped: {len(graph.get('edges', []))}")
        for node in graph.get('nodes', []):
            print(f" - [{node['data']['status'].upper()}] {node['id']}: {node['data']['label']}")
            
        print("\n(The JSON DAG is ready to be exported to Langflow/Dify frontend).")
        
    except Exception as e:
        print(f"\n[FATAL ERROR] The Swarm encountered an error: {str(e)}")
        
if __name__ == "__main__":
    try:
        asyncio.run(interactive_demo())
    except KeyboardInterrupt:
        print("\nSwarm execution aborted by user.")
