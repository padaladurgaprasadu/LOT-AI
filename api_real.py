import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize OpenAI client pointing to NVIDIA endpoint
client = OpenAI(
  base_url="https://integrate.api.nvidia.com/v1",
  api_key=os.getenv("NVIDIA_API_KEY")
)

def test_nvidia_connection():
    print("Connecting to NVIDIA Nemotron 3 Ultra 550B MoE...")
    try:
        completion = client.chat.completions.create(
          model="nvidia/nemotron-3-ultra-550b-a55b",
          messages=[{"role": "user", "content": "You are the core of yAI, an AI Operating System. Say hello and briefly state your capabilities as an expert AI."}],
          temperature=0.7,
          top_p=0.95,
          max_tokens=1024,
          extra_body={
              "chat_template_kwargs": {"enable_thinking": True},
              "reasoning_budget": 1024
          }
        )
        print("\n--- Response Received ---")
        print(completion.choices[0].message.content)
        print("-------------------------\n")
        print("Connection successful! Nemotron is online.")
    except Exception as e:
        print(f"Error connecting to NVIDIA API: {e}")

if __name__ == "__main__":
    test_nvidia_connection()
