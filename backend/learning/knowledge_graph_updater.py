import os
import json
import uuid
import re
from typing import Dict, Any, List

class KnowledgeGraphUpdater:
    """Maintain and update the PrismAI knowledge graph with new information."""
    def __init__(self):
        self.graph_path = os.path.join(os.path.dirname(__file__), 'knowledge_graph.json')
        self.graph = self._load_graph()

    def _load_graph(self) -> Dict[str, Any]:
        if os.path.exists(self.graph_path):
            with open(self.graph_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"nodes": {}, "edges": {}}

    def _save_graph(self):
        os.makedirs(os.path.dirname(self.graph_path), exist_ok=True)
        with open(self.graph_path, 'w', encoding='utf-8') as f:
            json.dump(self.graph, f, indent=4)

    def add_node(self, name: str, node_type: str, properties: Dict[str, Any]) -> str:
        for nid, n in self.graph["nodes"].items():
            if n["name"] == name and n["type"] == node_type:
                return nid
        node_id = str(uuid.uuid4())
        self.graph["nodes"][node_id] = {"name": name, "type": node_type, "properties": properties}
        self._save_graph()
        return node_id

    def add_edge(self, from_node: str, to_node: str, edge_type: str, properties: Dict[str, Any] = {}) -> str:
        edge_id = f"{from_node}-{edge_type}-{to_node}"
        self.graph["edges"][edge_id] = {
            "from": from_node,
            "to": to_node,
            "type": edge_type,
            "properties": properties
        }
        self._save_graph()
        return edge_id

    def update_node(self, node_id: str, properties: Dict[str, Any]) -> bool:
        if node_id in self.graph["nodes"]:
            self.graph["nodes"][node_id]["properties"].update(properties)
            self._save_graph()
            return True
        return False

    def deprecate_node(self, node_id: str, replaced_by: str = None) -> bool:
        if node_id in self.graph["nodes"]:
            self.graph["nodes"][node_id]["properties"]["deprecated"] = True
            if replaced_by:
                self.add_edge(node_id, replaced_by, "DEPRECATED_BY")
            self._save_graph()
            return True
        return False

    def find_related(self, node_name: str, depth: int = 2) -> List[Dict[str, Any]]:
        related = []
        target_id = None
        for nid, n in self.graph["nodes"].items():
            if n["name"] == node_name:
                target_id = nid
                break
        if not target_id:
            return related
        for eid, e in self.graph["edges"].items():
            if e["from"] == target_id:
                to_node = self.graph["nodes"].get(e["to"])
                if to_node:
                    related.append({"name": to_node["name"], "relation": e["type"], "distance": 1})
            elif e["to"] == target_id:
                from_node = self.graph["nodes"].get(e["from"])
                if from_node:
                    related.append({"name": from_node["name"], "relation": e["type"] + "_REVERSE", "distance": 1})
        return related

    def get_alternatives(self, node_name: str) -> List[Dict[str, Any]]:
        alternatives = []
        related = self.find_related(node_name, depth=1)
        for r in related:
            if "ALTERNATIVE_TO" in r["relation"]:
                alternatives.append({"name": r["name"], "pros": "Unknown", "cons": "Unknown"})
        return alternatives

    def detect_deprecated(self, text: str) -> List[str]:
        deprecated = []
        for nid, n in self.graph["nodes"].items():
            if n["properties"].get("deprecated") and re.search(r'\b' + re.escape(n["name"]) + r'\b', text, re.IGNORECASE):
                deprecated.append(n["name"])
        return deprecated

    def get_graph_summary(self) -> Dict[str, Any]:
        by_type = {}
        for n in self.graph["nodes"].values():
            by_type[n["type"]] = by_type.get(n["type"], 0) + 1
        return {
            "total_nodes": len(self.graph["nodes"]),
            "total_edges": len(self.graph["edges"]),
            "by_type": by_type
        }

def inject_knowledge_graph_prompt(system_prompt: str, task: str = '') -> str:
    return system_prompt + "\n\n[Knowledge Graph Online: Provides context for tech stack relationships.]"
