import asyncio
import sys
import os
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

from backend.tools.perception_engine import PerceptionEngine
from backend.agents.router import ModelRouter

async def run_test():
    engine = PerceptionEngine()
    print("Booting Visual Perception Engine (Pillar 2)...")
    await engine.start()
    
    url = "https://news.ycombinator.com"
    print(f"Navigating to {url}...")
    success = await engine.navigate(url)
    
    if success:
        print("Capturing Visual Context (Base64 JPEG)...")
        base64_img = await engine.capture_visual_context()
        
        if base64_img:
            print("Visual Context Captured. Routing to Qwen-3.5-VLM via OmniIntelligenceEngine...")
            
            prompt = "Look at this screenshot of a website. What website is this? Describe its main UI layout briefly."
            
            response = await ModelRouter.execute_vision_agent(base64_img, prompt)
            
            print("\n=== VLM RESPONSE ===")
            print(response)
        else:
            print("Failed to capture image.")
            
    await engine.close()

if __name__ == "__main__":
    asyncio.run(run_test())
