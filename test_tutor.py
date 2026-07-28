import os
import sys
import asyncio

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.base_agent import yAIAgentFactory
from memory.cag_core import memory_core

async def run_tutor_session():
    print("\n" + "="*60)
    print("[*] yAI TUTOR AGENT: LIVE TEACHING SESSION [*]")
    print("="*60)

    try:
        print("\n[1] Initializing the yAI Agent Factory...")
        factory = yAIAgentFactory()
        
        print("\n[2] Spinning up 'Tutor Agent' (Checking Persona Registry)...")
        tutor_agent = factory.create_agent("Tutor Agent")
        
        print("\n[3] Injecting a weak area into the student's CAG Memory Mesh...")
        # Simulate that in a past session, the student struggled with pointers.
        memory_core.log_thought("System", "Student Profile: 12-year-old middle schooler. Previously struggled with the concept of computer memory addresses.")

        print("\n[4] Starting Live Class...")
        question = "Can you explain what a Python Variable is? Explain like I'm 5, and keep it under 3 paragraphs."
        print(f"\nUser: {question}\n")
        
        print("Tutor Agent is thinking deeply (Applying 15-Point Workflow)...\n")
        
        response = tutor_agent.invoke({"input": question})
        
        print("-" * 60)
        print(response.content)
        print("-" * 60)
        
        print("\n[SUCCESS] Session Complete. Analytics and interactions logged to CAG Memory.")

    except Exception as e:
        print(f"\n[FAILED] TEST FAILED: {str(e)}")

if __name__ == "__main__":
    asyncio.run(run_tutor_session())
