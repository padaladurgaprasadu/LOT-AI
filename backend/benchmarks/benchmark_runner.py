import os
import sys
import json
import time
import asyncio
from typing import Dict, Any

# Ensure backend module can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend.orchestrator.swarm_manager import SwarmManager
from backend.agents.response_orchestrator import ResponseOrchestrator

class BenchmarkRunner:
    def __init__(self):
        self.dataset_path = os.path.join(os.path.dirname(__file__), 'test_datasets.json')
        with open(self.dataset_path, 'r') as f:
            self.datasets = json.load(f).get('datasets', [])
            
    async def run_ttft_benchmark(self, query: str):
        """Measure Time To First Token for Research Queries"""
        print(f"\n[Benchmarking TTFT] Query: '{query}'")
        start_time = time.time()
        orchestrator = ResponseOrchestrator()
        
        generator = orchestrator.execute_pipeline(query, "")
        
        first_token_time = None
        total_tokens = 0
        try:
            async for token in generator:
                if first_token_time is None and token.strip():
                    first_token_time = time.time() - start_time
                total_tokens += 1
        except Exception as e:
            print(f"Error during TTFT benchmark: {e}")
            
        end_time = time.time()
        total_time = end_time - start_time
        tps = total_tokens / total_time if total_time > 0 else 0
        
        print(f"  -> TTFT (Latency): {first_token_time:.2f}s" if first_token_time else "  -> TTFT (Latency): Failed")
        print(f"  -> Total Generation Time: {total_time:.2f}s")
        print(f"  -> Tokens Per Second: {tps:.2f} t/s")

    async def run_build_benchmark(self, query: str):
        """Measure End-to-End Build Velocity for the Swarm Orchestrator"""
        print(f"\n[Benchmarking BUILD] Query: '{query}'")
        start_time = time.time()
        
        manager = SwarmManager()
        
        try:
            # Run the newly optimized parallel swarm
            result = await manager.spawn_swarm(query, "")
            
            end_time = time.time()
            total_time = end_time - start_time
            
            print(f"  -> Parallel Build Completion Time: {total_time:.2f}s")
            
            mode = result.get('mode', 'enterprise')
            if mode == 'vibe':
                print(f"  -> Mode: Vibe (Instant)")
            else:
                files_generated = len(result.get('code', {}).get('files', [])) if isinstance(result.get('code'), dict) else 0
                print(f"  -> Files Generated: {files_generated}")
                
        except Exception as e:
            print(f"Error during Build benchmark: {e}")

    async def run_all(self):
        print("=========================================")
        print("      yAI Automated Benchmark Suite      ")
        print("=========================================")
        for test in self.datasets:
            if test['type'] == 'research':
                await self.run_ttft_benchmark(test['query'])
            elif test['type'] == 'build':
                # We will only run one build test to save tokens during demo
                if test['id'] == 'build_test_1':
                    await self.run_build_benchmark(test['query'])
        print("\n[✔] Benchmark Suite Completed Successfully.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="yAI Benchmark Suite")
    parser.add_argument('--dataset', type=str, default=None, help='Academic dataset to run (e.g., mmlu, gsm8k, swe-bench)')
    parser.add_argument('--limit', type=int, default=3, help='Limit number of questions to evaluate')
    args = parser.parse_args()

    if args.dataset:
        from backend.benchmarks.eval_engine import AcademicEvalEngine
        evaluator = AcademicEvalEngine()
        print(f"=========================================")
        print(f"   yAI Academic Evaluation: {args.dataset.upper()}")
        print(f"=========================================")
        results = asyncio.run(evaluator.run_evaluation(args.dataset, args.limit))
        print(f"\n[OK] Evaluation Complete. Results: {json.dumps(results, indent=2)}")
    else:
        runner = BenchmarkRunner()
        asyncio.run(runner.run_all())
