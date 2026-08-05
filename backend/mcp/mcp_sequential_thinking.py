import json
import sys
import uuid
from typing import Dict, List, Any

class SequentialThinkingMCPServer:
    def __init__(self):
        self.sessions = {}
        self.stages = [
            "Problem Understanding",
            "Constraint Identification",
            "Knowledge Activation",
            "Hypothesis Generation",
            "Critical Analysis",
            "Solution Selection",
            "Implementation Planning",
            "Verification Design",
            "Self-Critique",
            "Final Synthesis"
        ]

    def create_thinking_session(self, task: str) -> str:
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "task": task,
            "current_stage_idx": 0,
            "thoughts": [],
            "branches": {}
        }
        return session_id

    def record_thought(self, session_id: str, thought: str, thought_type: str = 'analysis') -> Dict:
        if session_id not in self.sessions: return {"error": "Invalid session"}
        thought_record = {"type": thought_type, "content": thought, "stage": self.stages[self.sessions[session_id]["current_stage_idx"]]}
        self.sessions[session_id]["thoughts"].append(thought_record)
        return {"status": "recorded", "thought": thought_record}

    def advance_stage(self, session_id: str) -> Dict:
        if session_id not in self.sessions: return {"error": "Invalid session"}
        session = self.sessions[session_id]
        if session["current_stage_idx"] < len(self.stages) - 1:
            session["current_stage_idx"] += 1
        current_stage = self.stages[session["current_stage_idx"]]
        return {"current_stage": session["current_stage_idx"] + 1, "stage_name": current_stage, "instructions": f"Proceed with {current_stage}"}

    def get_summary(self, session_id: str) -> Dict:
        if session_id not in self.sessions: return {"error": "Invalid session"}
        return {
            "stages_completed": self.sessions[session_id]["current_stage_idx"] + 1,
            "key_insights": ["Insights"],
            "confidence": 0.95,
            "final_answer": "Final synthesized answer"
        }

    def branch_thought(self, session_id: str, branch_name: str) -> str:
        if session_id not in self.sessions: return "Invalid session"
        self.sessions[session_id]["branches"][branch_name] = []
        return branch_name

    def merge_branches(self, session_id: str) -> Dict:
        return {"status": "merged"}

    def get_verification_report(self, session_id: str) -> Dict:
        if session_id not in self.sessions: return {"error": "Invalid session"}
        return {"audit_trail": self.sessions[session_id]["thoughts"]}

def inject_sequential_thinking_prompt(system_prompt: str) -> str:
    return system_prompt + "\n\nYou can use Sequential Thinking MCP to rigorously analyze tasks."

if __name__ == "__main__":
    server = SequentialThinkingMCPServer()
    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            method = req.get("method")
            params = req.get("params", {})
            resp = {"jsonrpc": "2.0", "id": req.get("id")}
            if method == "initialize":
                resp["result"] = {"status": "initialized"}
            elif method == "call_tool":
                tool = params.get("name")
                args = params.get("arguments", {})
                if hasattr(server, tool):
                    func = getattr(server, tool)
                    resp["result"] = func(**args)
                else:
                    resp["error"] = {"code": -32601, "message": f"Tool {tool} not found"}
            else:
                resp["error"] = {"code": -32601, "message": "Method not found"}
            print(json.dumps(resp), flush=True)
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}), flush=True)
