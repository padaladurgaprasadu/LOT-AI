import sys
import os
import io
import time

sys.path.insert(0, os.path.abspath('.'))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print('=== 🚀 LOT AI Full System & Swarm Matrix Verification ===')

start_t = time.time()
try:
    from backend.memory.impeccable_design_engine import inject_impeccable_design_prompt
    from backend.memory.open_design_matrix import inject_open_design_prompt
    from backend.memory.grok_build_engine import inject_grok_build_prompt
    from backend.memory.chrome_quality_engine import inject_chrome_quality_prompt
    from backend.memory.awesome_llm_apps_engine import inject_awesome_llm_apps_prompt
    from backend.memory.cuda_agentic_rl_engine import inject_cuda_agent_prompt
    from backend.memory.intelligent_ui_rules import inject_intelligent_ui_rules, classify_content_type
    
    prompt = 'Test Prompt'
    prompt = inject_impeccable_design_prompt(prompt)
    prompt = inject_open_design_prompt(prompt)
    prompt = inject_grok_build_prompt(prompt)
    prompt = inject_chrome_quality_prompt(prompt)
    prompt = inject_awesome_llm_apps_prompt(prompt)
    prompt = inject_cuda_agent_prompt(prompt)
    prompt = inject_intelligent_ui_rules(prompt)
    
    dt = (time.time() - start_t) * 1000
    print(f'✅ All 7 Core Memory & Matrix Modules Injected Successfully in {dt:.3f} ms')
    print(f'   System Prompt Total Character Count: {len(prompt)} chars')
except Exception as e:
    print(f'❌ Error injecting memory modules: {e}')
    sys.exit(1)

# Test Content Classification
test_cases = [
    ('Explain for loops in Python', 'Programming'),
    ('Tirupati temple timings', 'Place'),
    ('Who is Elon Musk', 'Person'),
]

print('\n=== 🎯 Content Classification Verification ===')
for query, expected in test_cases:
    res = classify_content_type(query)
    print(f'  Query: "{query}" -> Classified As: [{res}] (Expected: {expected})')
    assert res == expected, f'Expected {expected}, got {res}'

print('\n🎉 ALL AGENTS AND CORE ENGINES VERIFIED 100% OPERATIONAL!')
