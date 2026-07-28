import sys, os
sys.path.insert(0, "C:/Users/DELL/OneDrive/Desktop/Tatvamasi/yAI")

from dotenv import load_dotenv
load_dotenv()

from backend.utils.model_registry import AIModelRegistry, NVIDIA_MODEL_TIERS, ROLE_TO_TIER

print("=== 11-MODEL NVIDIA TIER REGISTRY ===")
for tier, model in NVIDIA_MODEL_TIERS.items():
    print(f"  {tier:<12} -> {model}")

print()
print("=== AGENT ROLE ROUTING ===")
test_roles = ["ceo", "architect", "frontend coder", "backend coder", 
              "qa engineer", "security engineer", "research agent", "ux designer", "intent_router"]
for role in test_roles:
    tier = "fast"
    for key, t in ROLE_TO_TIER.items():
        if key in role.lower():
            tier = t
            break
    model = NVIDIA_MODEL_TIERS.get(tier, "?")
    print(f"  {role:<22} -> {tier:<12} -> {model[:55]}")

print()
print("Registry loaded successfully!")
