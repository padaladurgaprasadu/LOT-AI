import os
import sys
import asyncio

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.base_agent import yAIAgentFactory
from memory.cag_core import memory_core

async def run_research_session():
    print("\n" + "="*60)
    print("[*] yAI RESEARCH AGENT: KNOWLEDGE DISCOVERY [*]")
    print("="*60)

    try:
        print("\n[1] Initializing the yAI Agent Factory...")
        factory = yAIAgentFactory()
        
        print("\n[2] Spinning up 'Research Agent' (Checking Persona Registry)...")
        research_agent = factory.create_agent("Research Agent")
        
        print("\n[3] Simulating a deep research request...")
        question = "I need a short research report on the current consensus regarding the effectiveness of Mixture of Experts (MoE) architectures in LLMs vs dense architectures. Keep it under 500 words."
        print(f"\nUser: {question}\n")
        
        print("Research Agent is processing (Applying Methodology Workflow)...\n")
        
        response = research_agent.invoke({"input": question})
        
        print("-" * 60)
        print(response.content)
        print("-" * 60)
        
        print("\n[SUCCESS] Research Complete. Findings logged to CAG Memory.")

    except Exception as e:
        print(f"\n[FAILED] TEST FAILED: {str(e)}")

if __name__ == "__main__":
    asyncio.run(run_research_session())
