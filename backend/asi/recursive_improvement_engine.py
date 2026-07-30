import os
import json
import uuid
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class ImprovementSuggestion:
    file_path: str
    function_name: str
    issue_type: str
    description: str
    priority: int
    suggested_fix: str
    
    def to_dict(self):
        return {
            'file_path': self.file_path,
            'function_name': self.function_name,
            'issue_type': self.issue_type,
            'description': self.description,
            'priority': self.priority,
            'suggested_fix': self.suggested_fix
        }

class RecursiveImprovementEngine:
    def __init__(self, queue_file: str = 'backend/asi/improvement_queue.json'):
        self.queue_file = queue_file
        if not os.path.exists(os.path.dirname(self.queue_file)):
            os.makedirs(os.path.dirname(self.queue_file), exist_ok=True)
        if not os.path.exists(self.queue_file):
            with open(self.queue_file, 'w') as f:
                json.dump([], f)
                
    def scan_codebase(self, base_path: str) -> List[ImprovementSuggestion]:
        suggestions = []
        for root, dirs, files in os.walk(base_path):
            for file in files:
                if file.endswith('.py'):
                    full_path = os.path.join(root, file)
                    with open(full_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        if len(lines) > 300:
                            suggestions.append(ImprovementSuggestion(
                                file_path=full_path,
                                function_name="global",
                                issue_type="file_length",
                                description="File exceeds 300 lines",
                                priority=3,
                                suggested_fix="Refactor into smaller modules"
                            ))
        return suggestions
        
    def add_to_queue(self, suggestion: ImprovementSuggestion) -> str:
        queue = self.get_queue()
        queue_id = str(uuid.uuid4())
        item = suggestion.to_dict()
        item['queue_id'] = queue_id
        item['approved'] = False
        queue.append(item)
        
        with open(self.queue_file, 'w') as f:
            json.dump(queue, f, indent=4)
            
        return queue_id
        
    def get_queue(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self.queue_file):
            return []
        with open(self.queue_file, 'r') as f:
            return json.load(f)
            
    def approve_suggestion(self, queue_id: str) -> bool:
        queue = self.get_queue()
        found = False
        for item in queue:
            if item.get('queue_id') == queue_id:
                item['approved'] = True
                found = True
                break
        if found:
            with open(self.queue_file, 'w') as f:
                json.dump(queue, f, indent=4)
        return found
