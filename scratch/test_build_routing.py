import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

test_prompts = [
    "Build a library management system",
    "create an e-commerce store",
    "develop a CRM dashboard",
    "Build a website for hotel booking",
    "Make an app for food delivery",
    "Explain for loops in python",
    "Who is Elon Musk",
    "Tirupati temple timings"
]

full_app_signals = [
    "full app", "full stack", "web app", "mobile app", "saas",
    "dashboard app", "build me a", "build a website", "create a website",
    "create an app", "build an app", "develop a platform", "entire application",
    "e-commerce site", "scaffold a project", "management system", "portal",
    "system", "application", "platform", "dashboard", "tool", "website"
]

print("==========================================================================")
print("🚀 TESTING PRISMAI AUTONOMOUS WEB APP BUILDER ROUTING")
print("==========================================================================")

for prompt in test_prompts:
    msg_lower = prompt.lower().strip()
    explicit_full_app = any(sig in msg_lower for sig in full_app_signals)
    is_build_action = bool(re.search(r"^(build|create|develop|make|generate)\b", msg_lower)) and not any(k in msg_lower for k in ["who", "what is", "why", "how to", "explain", "meaning"])
    is_build_req = explicit_full_app or (is_build_action and len(prompt.split()) >= 2)
    
    status = "🚀 APP BUILDER ([BUILD] TAG) ✅" if is_build_req else "💬 CHAT / TEXT RESPONSE"
    print(f"• Prompt: '{prompt:38s}' ──► Routing: {status}")

print("==========================================================================")
