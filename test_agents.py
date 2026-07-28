import sys
sys.path.insert(0, ".")

from backend.agents.expert_agents import find_best_agent, AGENT_REGISTRY

print(f"Total agents in registry: {len(AGENT_REGISTRY)}")
print()
print("=== ROUTING PRECISION TESTS ===")

tests = [
    ("write a machine learning pipeline",               "ml_engineer"),
    ("debug this python error traceback",               "debugger"),
    ("explain quantum computing to me",                 "tutor"),
    ("build me a full-stack web app",                   "fullstack"),
    ("design a microservices architecture for SaaS",    "architecture"),
    ("I need a security audit of my API",               "cybersecurity"),
    ("I want to learn React hooks",                     "tutor"),
    ("create a RAG pipeline with LangChain",            "langchain_expert"),
    ("write unit tests for my FastAPI endpoints",       "qa"),
    ("how do I set up kubernetes with helm",            "devops"),
    ("what is a transformer model in deep learning",    "ml_engineer"),
    ("build a React frontend component",                "frontend"),
    ("write a PostgreSQL backend API endpoint",         "backend"),
    ("analyze my company's tech debt",                  "cto"),
    ("I want to build a fintech payment system",        "fintech"),
    ("help me with genomics bioinformatics",            "biotech"),
    ("explain orbital mechanics and delta-v",           "space"),
    ("what's a good color palette for my UI",           "artist"),
    ("design a distributed system for Twitter scale",   "system_designer"),
    ("sql query to find top customers last month",      "data_analyst"),
]

passed = 0
for query, expected in tests:
    result = find_best_agent(query)
    status = "PASS" if result == expected else "FAIL"
    if result == expected:
        passed += 1
    print(f"  {status} expected={expected:<20} got={result:<20} | {query[:50]}")

print()
print(f"Score: {passed}/{len(tests)} ({100*passed//len(tests)}%)")
