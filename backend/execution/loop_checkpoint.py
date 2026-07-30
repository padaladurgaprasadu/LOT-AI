import os
import json
import hashlib
from typing import Optional, Dict, List, Any

class LoopCheckpoint:
    def __init__(self, base_dir: str = 'backend/execution/checkpoints'):
        self.base_dir = base_dir
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir, exist_ok=True)
            
    def _get_path(self, task_id: str) -> str:
        return os.path.join(self.base_dir, f"{task_id}.json")
        
    @staticmethod
    def generate_task_id(task: str) -> str:
        return hashlib.sha256(task.encode('utf-8')).hexdigest()[:16]

    def save(self, task_id: str, stage_id: str, state: Dict[str, Any]) -> None:
        data = {
            'task_id': task_id,
            'stage_id': stage_id,
            'state': state
        }
        with open(self._get_path(task_id), 'w') as f:
            json.dump(data, f, indent=4)
            
    def load(self, task_id: str) -> Optional[Dict[str, Any]]:
        path = self._get_path(task_id)
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        return None
        
    def list_all(self) -> List[str]:
        return [f.replace('.json', '') for f in os.listdir(self.base_dir) if f.endswith('.json')]
        
    def delete(self, task_id: str) -> None:
        path = self._get_path(task_id)
        if os.path.exists(path):
            os.remove(path)
