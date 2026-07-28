import os
import sys
import json
import time
import asyncio
from typing import Dict, Any, List

# Ensure backend module can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend.agents.response_orchestrator import ResponseOrchestrator

try:
    from datasets import load_dataset
except ImportError:
    print("[EvalEngine] HuggingFace 'datasets' library is not installed. Run 'pip install datasets evaluate'")
    load_dataset = None

class AcademicEvalEngine:
    """
    Evaluates yAI against industry-standard benchmarks (MMLU, GSM8K, SWE-bench, etc.)
    using HuggingFace datasets.
    """
    def __init__(self):
        self.orchestrator = ResponseOrchestrator()

    async def _evaluate_question(self, question: str) -> str:
        """Runs a single question through the yAI Response Orchestrator."""
        generator = self.orchestrator.execute_pipeline(question, "")
        full_response = ""
        try:
            async for token in generator:
                if token:
                    full_response += token
        except Exception as e:
            return f"Error: {e}"
        return full_response

    async def eval_gsm8k(self, limit: int = 5) -> Dict[str, Any]:
        """Evaluates math reasoning."""
        if not load_dataset: return {"error": "datasets library missing"}
        
        print(f"\n[EVAL] Loading GSM8K Benchmark (Limit: {limit})...")
        dataset = load_dataset("gsm8k", "main", split="test")
        
        results = []
        for i in range(min(limit, len(dataset))):
            item = dataset[i]
            question = item['question']
            answer_key = item['answer']
            
            print(f"  -> Q{i+1}: {question[:60]}...")
            start_time = time.time()
            ai_answer = await self._evaluate_question(question)
            latency = time.time() - start_time
            
            results.append({
                "question": question,
                "ai_answer": ai_answer,
                "ground_truth": answer_key,
                "latency_sec": round(latency, 2)
            })
            
        return {"benchmark": "GSM8K", "runs": len(results), "data": results}

    async def eval_mmlu(self, limit: int = 5) -> Dict[str, Any]:
        """Evaluates massive multitask language understanding."""
        if not load_dataset: return {"error": "datasets library missing"}
        
        print(f"\n[EVAL] Loading MMLU Benchmark (Limit: {limit})...")
        # For demo purposes we load a specific subset of MMLU
        dataset = load_dataset("cais/mmlu", "all", split="test")
        
        results = []
        for i in range(min(limit, len(dataset))):
            item = dataset[i]
            question = item['question']
            choices = item['choices']
            answer_idx = item['answer']
            
            prompt = f"{question}\nChoices:\n0: {choices[0]}\n1: {choices[1]}\n2: {choices[2]}\n3: {choices[3]}\nAnswer concisely."
            
            print(f"  -> Q{i+1}: {question[:60]}...")
            start_time = time.time()
            ai_answer = await self._evaluate_question(prompt)
            latency = time.time() - start_time
            
            results.append({
                "question": question,
                "choices": choices,
                "ai_answer": ai_answer,
                "ground_truth_idx": answer_idx,
                "latency_sec": round(latency, 2)
            })
            
        return {"benchmark": "MMLU", "runs": len(results), "data": results}

    async def run_evaluation(self, dataset_name: str, limit: int) -> Dict[str, Any]:
        if dataset_name.lower() == "gsm8k":
            return await self.eval_gsm8k(limit)
        elif dataset_name.lower() == "mmlu":
            return await self.eval_mmlu(limit)
        else:
            return {"error": f"Dataset '{dataset_name}' not yet fully implemented in EvalEngine for dry run."}
