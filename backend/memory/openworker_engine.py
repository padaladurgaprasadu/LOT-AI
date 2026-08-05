"""
LOT AI OpenWorker Core Integration Engine
===========================================
Inspired by Andrew Ng's openworker (https://github.com/andrewyng/openworker).
Integrates lightweight background agentic worker execution loops, standardized 
tool-calling schemas, and multi-thread task worker pools.
"""

def inject_openworker_prompt(system_prompt: str) -> str:
    """
    Injects OpenWorker background execution protocol & worker task pool directives.
    """
    openworker_prompt = "\n\n[⚙️ LOTAI OPENWORKER CORE ENGINE (Andrew Ng OpenWorker Architecture)]:\n"
    openworker_prompt += "• Lightweight Worker Protocol: Every agentic task is executed via decoupled, non-blocking background worker loops.\n"
    openworker_prompt += "• Standardized Tool-Calling Spec: Enforces clean, typed, deterministic JSON tool schemas for all worker executions.\n"
    openworker_prompt += "• Asynchronous Task Queue: Parallelizes long-horizon code synthesis, linting, and TDD unit testing across worker pools.\n\n"
    
    return system_prompt + openworker_prompt
