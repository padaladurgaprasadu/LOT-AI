import os
import sys
import asyncio

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.base_agent import yAIAgentFactory
from memory.cag_core import memory_core

async def run_general_chat_session():
    print("\n" + "="*60)
    print("[*] yAI GENERAL CHAT AGENT: LIVE SESSION [*]")
    print("="*60)

    try:
        print("\n[1] Initializing the yAI Agent Factory...")
        factory = yAIAgentFactory()
        
        print("\n[2] Spinning up 'General Chat' (Checking Persona Registry)...")
        chat_agent = factory.create_agent("General Chat")
        
        print("\n[3] Simulating a planning and brainstorming request...")
        question = "I want to start a side hustle selling custom mechanical keyboards. Can you give me a 3-step action plan and brainstorm 2 catchy names for the business?"
        print(f"\nUser: {question}\n")
        
        print("General Chat Agent is processing (Applying Conversation Workflow)...\n")
        
        response = chat_agent.invoke({"input": question})
        
        print("-" * 60)
        print(response.content)
        print("-" * 60)
        
        print("\n[SUCCESS] Session Complete. Ideas and plans logged to CAG Memory.")

    except Exception as e:
        print(f"\n[FAILED] TEST FAILED: {str(e)}")

if __name__ == "__main__":
    asyncio.run(run_general_chat_session())
