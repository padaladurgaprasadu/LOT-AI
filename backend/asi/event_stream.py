import json
import os
import time
import threading
import uuid
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any

@dataclass
class BaseEvent:
    timestamp: float

@dataclass
class AgentActionEvent(BaseEvent):
    agent_id: str
    action_type: str
    content: str
    tool_name: str
    tool_args: Dict

@dataclass
class CodeExecutionEvent(BaseEvent):
    language: str
    code: str
    stdout: str
    stderr: str
    exit_code: int
    runtime_ms: float

@dataclass
class ToolCallEvent(BaseEvent):
    tool_name: str
    server_name: str
    arguments: Dict
    result: Any
    duration_ms: float

@dataclass
class UserInputEvent(BaseEvent):
    message: str
    intent: str
    routed_to: str

@dataclass
class SystemObservationEvent(BaseEvent):
    observation_type: str
    content: str
    severity: str

@dataclass
class SEALAdaptationEvent(BaseEvent):
    iteration: int
    candidates_generated: int
    edits_accepted: int
    top_reward: float

@dataclass
class ArchitectureDiagramEvent(BaseEvent):
    diagram_type: str
    nodes: List[Dict]
    edges: List[Dict]
    zones: List[str]

class EventStream:
    def __init__(self, log_path: str = 'backend/asi/event_stream_log.jsonl'):
        self.log_path = log_path
        self.lock = threading.Lock()
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)

    def emit(self, event: BaseEvent) -> str:
        event_id = str(uuid.uuid4())
        data = asdict(event)
        data['event_id'] = event_id
        data['event_type'] = event.__class__.__name__
        if not getattr(event, 'timestamp', None):
            data['timestamp'] = time.time()
            
        with self.lock:
            with open(self.log_path, 'a') as f:
                f.write(json.dumps(data) + '\n')
        return event_id

    def get_events(self, event_type: str = None, since_timestamp: float = None, limit: int = 100) -> List[Dict]:
        events = []
        if not os.path.exists(self.log_path):
            return events
        with self.lock:
            with open(self.log_path, 'r') as f:
                for line in f:
                    try:
                        evt = json.loads(line)
                        if event_type and evt.get('event_type') != event_type:
                            continue
                        if since_timestamp and evt.get('timestamp', 0) < since_timestamp:
                            continue
                        events.append(evt)
                    except:
                        pass
        return events[-limit:] if limit > 0 else events

    def get_latest(self, n: int = 10) -> List[Dict]:
        return self.get_events(limit=n)

    def replay(self, start_index: int = 0, end_index: int = None) -> List[Dict]:
        events = self.get_events(limit=0)
        return events[start_index:end_index] if end_index else events[start_index:]

    def search(self, query: str) -> List[Dict]:
        results = []
        events = self.get_events(limit=0)
        query = query.lower()
        for evt in events:
            if query in json.dumps(evt).lower():
                results.append(evt)
        return results

    def get_agent_history(self, agent_id: str) -> List[Dict]:
        events = self.get_events(event_type='AgentActionEvent', limit=0)
        return [e for e in events if e.get('agent_id') == agent_id]

    def get_stats(self) -> Dict[str, Any]:
        events = self.get_events(limit=0)
        stats = {
            'total_events': len(events),
            'events_by_type': {},
            'agents_active': set(),
            'last_event_time': events[-1].get('timestamp') if events else None
        }
        for evt in events:
            evt_type = evt.get('event_type')
            stats['events_by_type'][evt_type] = stats['events_by_type'].get(evt_type, 0) + 1
            if evt_type == 'AgentActionEvent':
                stats['agents_active'].add(evt.get('agent_id'))
        
        stats['agents_active'] = list(stats['agents_active'])
        return stats

    def clear(self) -> None:
        with self.lock:
            if os.path.exists(self.log_path):
                os.remove(self.log_path)

def inject_event_stream_prompt(system_prompt: str) -> str:
    return system_prompt + "\n[SYSTEM INJECT] Event stream is tracking all Agent, Tool, and Execution actions."
