import os
import json
import uuid
import random
from typing import Dict, Any, Optional

class PromptEvolutionEngine:
    def __init__(self, store_file: str = 'backend/asi/prompt_variants.json'):
        self.store_file = store_file
        if not os.path.exists(os.path.dirname(self.store_file)):
            os.makedirs(os.path.dirname(self.store_file), exist_ok=True)
        if not os.path.exists(self.store_file):
            with open(self.store_file, 'w') as f:
                json.dump({}, f)
                
    def _load(self) -> Dict[str, Any]:
        with open(self.store_file, 'r') as f:
            return json.load(f)
            
    def _save(self, data: Dict[str, Any]) -> None:
        with open(self.store_file, 'w') as f:
            json.dump(data, f, indent=4)
            
    def register_variant(self, name: str, content: str) -> str:
        data = self._load()
        variant_id = str(uuid.uuid4())
        if name not in data:
            data[name] = []
            
        data[name].append({
            'variant_id': variant_id,
            'content': content,
            'scores': [],
            'eval_count': 0,
            'active': True
        })
        self._save(data)
        return variant_id
        
    def record_score(self, variant_id: str, score: float) -> None:
        data = self._load()
        for name, variants in data.items():
            for v in variants:
                if v['variant_id'] == variant_id:
                    v['scores'].append(score)
                    v['eval_count'] += 1
                    
                    avg = sum(v['scores']) / len(v['scores'])
                    if v['eval_count'] >= 10 and avg < 7.0:
                        v['active'] = False
                        
                    self._save(data)
                    return
                    
    def get_best_variant(self, name: str) -> Optional[str]:
        data = self._load()
        if name not in data:
            return None
            
        variants = [v for v in data[name] if v['active'] and len(v['scores']) > 0]
        if not variants:
            return None
            
        best = max(variants, key=lambda v: sum(v['scores']) / len(v['scores']))
        return best['content']
        
    def evolve(self, name: str) -> str:
        data = self._load()
        if name not in data:
            return "Default evolved prompt."
            
        active_vars = [v for v in data[name] if v['active']]
        if not active_vars:
            return "Default evolved prompt."
            
        parent = max(active_vars, key=lambda v: sum(v['scores']) / len(v['scores']) if v['scores'] else 0)
        content = parent['content']
        
        sentences = content.split('.')
        if len(sentences) > 2:
            idx1, idx2 = random.sample(range(len(sentences)-1), 2)
            sentences[idx1], sentences[idx2] = sentences[idx2], sentences[idx1]
            
        evolved_content = '.'.join(sentences)
        self.register_variant(name, evolved_content)
        return evolved_content
        
    def get_stats(self) -> Dict[str, Any]:
        data = self._load()
        stats = {}
        for name, variants in data.items():
            active = len([v for v in variants if v['active']])
            retired = len([v for v in variants if not v['active']])
            stats[name] = {'active': active, 'retired': retired, 'total': len(variants)}
        return stats
