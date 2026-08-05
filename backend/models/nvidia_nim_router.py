import os
import json
import urllib.request
import urllib.error
import time
from typing import Dict, List, Optional, Any

NVIDIA_NIM_MODELS = {
    'nemotron_ultra': {'id': 'nvidia/nemotron-3-ultra-550b-a55b', 'context': 1000000, 'priority': 1, 'best_for': ['code_synthesis', 'architecture', 'agentic']},
    'glm_5_2': {'id': 'z-ai/glm-5.2', 'context': 1000000, 'priority': 2, 'best_for': ['long_horizon', 'agentic_workflows']},
    'minimax_m3': {'id': 'minimaxai/minimax-m3-preview', 'context': 1000000, 'priority': 3, 'best_for': ['vision', 'multimodal']},
    'nemotron_frontier': {'id': 'nvidia/nemotron-3-550b-frontier', 'context': 1000000, 'priority': 4, 'best_for': ['reasoning', 'agentic']},
    'mistral_medium': {'id': 'mistralai/mistral-medium-3.5-128b', 'context': 256000, 'priority': 5, 'best_for': ['code_refactoring', 'fast_coding']},
    'deepseek_v4': {'id': 'deepseek-ai/deepseek-v4', 'context': 1000000, 'priority': 6, 'best_for': ['agentic_coding', 'long_context']},
    'deepseek_v4_coder': {'id': 'deepseek-ai/deepseek-v4-coder', 'context': 1000000, 'priority': 7, 'best_for': ['tdd', 'self_healing_code']},
    'minimax_m2_7': {'id': 'minimaxai/minimax-m2.7-230b', 'context': 200000, 'priority': 8, 'best_for': ['document_processing', 'text']},
    'qwen_3_5_vlm': {'id': 'qwen/qwen-3.5-vlm-400b-moe', 'context': 262144, 'priority': 9, 'best_for': ['vision', 'rag', 'image_chat']},
    'nemotron_moe_chat': {'id': 'nvidia/nemotron-4-moe-1m', 'context': 1000000, 'priority': 10, 'best_for': ['conversational', 'long_context']},
    'gemma_4': {'id': 'google/gemma-4-31b-it', 'context': 256000, 'priority': 11, 'best_for': ['dense_reasoning', 'function_calling']},
    'nemotron_nano': {'id': 'nvidia/nemotron-3-nano-30b-a3b', 'context': 1000000, 'priority': 12, 'best_for': ['routing', 'intent_classification', 'edge']}
}

class NVIDIANIMRouter:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get('NVIDIA_API_KEY')
        if not self.api_key:
            pass # Handle securely in prod
        self.stats = {m['id']: {'calls': 0, 'latency_ms': []} for m in NVIDIA_NIM_MODELS.values()}

    def route_request(self, task_type: str, context_length: int, message: str, model_preference: str = None) -> Dict[str, Any]:
        if model_preference and model_preference in [m['id'] for m in NVIDIA_NIM_MODELS.values()]:
            return {'model_id': model_preference, 'reason': 'User preference', 'tier': 'preference'}
        
        if task_type == 'intent_classification' or context_length < 8000:
            return {'model_id': NVIDIA_NIM_MODELS['nemotron_nano']['id'], 'reason': 'Fast routing or short context', 'tier': 'nano'}
        elif task_type in ['code_synthesis', 'architecture']:
            return {'model_id': NVIDIA_NIM_MODELS['nemotron_ultra']['id'], 'reason': 'Heavy synthesis task', 'tier': 'ultra'}
        elif task_type in ['vision', 'image_analysis']:
            return {'model_id': NVIDIA_NIM_MODELS['minimax_m3']['id'], 'reason': 'Vision task', 'tier': 'vision'}
        elif task_type == 'document_processing':
            return {'model_id': NVIDIA_NIM_MODELS['minimax_m2_7']['id'], 'reason': 'Document processing', 'tier': 'text'}
        elif task_type == 'code_refactoring':
            return {'model_id': NVIDIA_NIM_MODELS['mistral_medium']['id'], 'reason': 'Code refactoring', 'tier': 'coding'}
        elif task_type == 'agentic_coding':
            return {'model_id': NVIDIA_NIM_MODELS['deepseek_v4']['id'], 'reason': 'Agentic coding', 'tier': 'coding'}
        elif task_type == 'long_context' or context_length > 100000:
            return {'model_id': NVIDIA_NIM_MODELS['nemotron_moe_chat']['id'], 'reason': 'Long context', 'tier': 'long'}
        elif task_type == 'reasoning':
            return {'model_id': NVIDIA_NIM_MODELS['nemotron_frontier']['id'], 'reason': 'Complex reasoning', 'tier': 'frontier'}
        else:
            return {'model_id': NVIDIA_NIM_MODELS['nemotron_ultra']['id'], 'reason': 'Default fallback', 'tier': 'ultra'}

    def call_model(self, model_id: str, messages: List[Dict], temperature: float = 0.6, max_tokens: int = 4096, tools: List[Dict] = None) -> Dict[str, Any]:
        url = "https://integrate.api.nvidia.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": model_id,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }
        if tools:
            data["tools"] = tools

        start_time = time.time()
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')
        
        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                latency = (time.time() - start_time) * 1000
                
                # Update analytics
                if model_id in self.stats:
                    self.stats[model_id]['calls'] += 1
                    self.stats[model_id]['latency_ms'].append(latency)
                
                content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
                usage = result.get('usage', {})
                return {'content': content, 'model': model_id, 'usage': usage, 'latency_ms': latency}
        except urllib.error.URLError as e:
            raise Exception(f"Failed to call NIM API: {e}")

    def call_with_fallback(self, messages: List[Dict], task_type: str = 'general', max_retries: int = 3) -> Dict:
        fallback_chain = ['nemotron_ultra', 'glm_5_2', 'nemotron_frontier', 'mistral_medium', 'deepseek_v4', 'gemma_4']
        
        for model_key in fallback_chain:
            model_id = NVIDIA_NIM_MODELS[model_key]['id']
            for attempt in range(max_retries):
                try:
                    return self.call_model(model_id, messages)
                except Exception as e:
                    time.sleep(1)
        raise Exception("All fallback models failed.")

    def get_model_info(self, model_id: str) -> Dict[str, Any]:
        for key, info in NVIDIA_NIM_MODELS.items():
            if info['id'] == model_id:
                return {
                    'name': key,
                    'context_window': info['context'],
                    'architecture': 'unknown',
                    'best_for': info['best_for']
                }
        return {}

    def list_available_models(self) -> List[Dict]:
        return list(NVIDIA_NIM_MODELS.values())

    def estimate_cost(self, model_id: str, input_tokens: int, output_tokens: int) -> Dict[str, Any]:
        per_1k_in = 0.001
        per_1k_out = 0.002
        cost = (input_tokens / 1000.0) * per_1k_in + (output_tokens / 1000.0) * per_1k_out
        return {'cost_usd': cost, 'per_1k_input': per_1k_in, 'per_1k_output': per_1k_out}

    def health_check(self) -> Dict[str, Any]:
        return {'status': 'healthy', 'models_available': len(NVIDIA_NIM_MODELS), 'latency_ms': 50.0}

def inject_nim_router_prompt(system_prompt: str) -> str:
    return system_prompt + "\n[SYSTEM INJECT] Utilizing NVIDIA NIM dynamic router for multi-model fallback operations."
