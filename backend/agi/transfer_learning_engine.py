"""
Cross-domain knowledge transfer engine.
Maps concepts between different software engineering domains.
"""
from typing import List, Dict

CROSS_DOMAIN_PATTERNS = {
    ('distributed_systems', 'frontend'): 'Circuit Breaker → React Error Boundary',
    ('erlang_actor_model', 'python'): 'Actor Model → asyncio + queues',
    ('dynamic_programming', 'react'): 'Memoization → useMemo + useCallback',
    ('database_indexing', 'search'): 'B-tree index → MeiliSearch facets',
    ('tcp_flow_control', 'api'): 'Backpressure → Rate limiting + queuing',
    ('pid_control', 'animation'): 'PID controller → spring animation physics',
    ('caching_algorithms', 'ui'): 'LRU cache → React Query stale-while-revalidate',
    ('consensus_algorithms', 'state'): 'Raft protocol → Redux saga',
    ('graph_algorithms', 'dependencies'): 'Topological sort → build order resolution',
    ('compression', 'api'): 'Run-length encoding → API response streaming'
}

def find_analogous_pattern(problem_description: str) -> List[Dict[str, str]]:
    results = []
    problem_lower = problem_description.lower()
    
    for (source, target), mapping in CROSS_DOMAIN_PATTERNS.items():
        if source.replace('_', ' ') in problem_lower or target in problem_lower:
            results.append({
                "source_domain": source,
                "target_domain": target,
                "insight": mapping
            })
            
    if not results:
        results.append({
            "source_domain": "general",
            "target_domain": "general",
            "insight": "Pattern matching → Regular expressions"
        })
        
    return results

def generate_transfer_insight(source_domain: str, target_problem: str) -> str:
    analogies = find_analogous_pattern(f"{source_domain} {target_problem}")
    if analogies:
        return f"Applying {analogies[0]['source_domain']} to this problem: {analogies[0]['insight']}"
    return "No direct transfer insight found."

def inject_transfer_learning_prompt(system_prompt: str, task: str = '') -> str:
    directive = (
        f"\n\n[TRANSFER LEARNING DIRECTIVE]\n"
        f"Leverage cross-domain analogies for task: {task}. "
        "Think about patterns from other fields that apply here."
    )
    return system_prompt + directive
