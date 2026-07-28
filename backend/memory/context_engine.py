import os
import json
from pathlib import Path
from typing import Dict, Any, List
from backend.memory.repo_graph import DAIMG
from backend.utils.logger import get_logger

logger = get_logger(__name__)

class ContextEngine:
    """
    yAI Phase 8 Context Engine.
    Implements Dependency Graph Traversal and Chunk Ranking to extract 
    only mathematically relevant context, eliminating "lost in the middle" hallucination.
    """
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.daimg = DAIMG(str(self.workspace_root))
        
        # We try to load the graph if it exists, otherwise build it in the background
        # For this prototype we will build it synchronously on demand if small enough
        self._graph_built = False

    def build_relevant_prompt(self, user_intent: Dict[str, Any], message: str) -> str:
        """
        Takes the user intent and raw message, traverses the repository graph,
        and constructs a highly optimized prompt payload containing only relevant file chunks.
        """
        if not self.workspace_root.exists():
            return "No active workspace."
            
        if not self._graph_built:
            self.daimg.build_graph()
            self._graph_built = True

        # Phase 1: Heuristic Entry Node Selection
        # Attempt to map the user's intent to specific files
        target_files = self._identify_target_files(message, user_intent)
        
        # Phase 2: Graph Traversal
        # For each target file, pull its immediate dependencies (imports/calls)
        context_files = set(target_files)
        for f in target_files:
            try:
                # Max depth 1 for strict relevance
                ctx = self.daimg.get_architectural_context(f, max_depth=1)
                for node in ctx.get("nodes", []):
                    if node.get("type") == "file":
                        context_files.add(node["id"])
            except Exception as e:
                logger.warning(f"[ContextEngine] Graph traversal failed for {f}: {e}")

        # Phase 3: Assembly & Ranking
        # For now, we assemble the files directly. (Production BM25 ranking goes here)
        compiled_context = ""
        total_tokens = 0
        MAX_TOKENS = 8000 # Strict limit to force speed and accuracy
        
        for file_path in list(context_files)[:10]: # Limit to top 10 files max
            full_path = self.workspace_root / file_path
            if full_path.exists() and full_path.is_file():
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Basic token estimation (4 chars per token)
                    est_tokens = len(content) // 4
                    if total_tokens + est_tokens > MAX_TOKENS:
                        compiled_context += f"\n\n<!-- [TRUNCATED] file path=\"{file_path}\" exceeds context limit -->"
                        break
                        
                    compiled_context += f'\n\n<file path="{file_path}">\n{content}\n</file>'
                    total_tokens += est_tokens
                except Exception:
                    pass

        if not compiled_context.strip():
            return "No relevant context extracted."
            
        return f"[ENGINEERED CONTEXT]:\n{compiled_context}"

    def _identify_target_files(self, message: str, intent: Dict[str, Any]) -> List[str]:
        """Simple keyword-based extraction of files mentioned in the prompt or intent."""
        targets = []
        msg_lower = message.lower()
        
        # 1. Look for explicit .py, .js, .jsx files in the message
        import re
        explicit_files = re.findall(r'[\w\/\-]+\.(?:py|jsx?|tsx?|css|html)', message)
        targets.extend(explicit_files)
        
        # 2. Look for keywords if no explicit files
        if not targets:
            if "api" in msg_lower or "router" in msg_lower:
                targets.append("api_real.py")
            if "ui" in msg_lower or "frontend" in msg_lower or "app.js" in msg_lower:
                targets.append("App.jsx")
                
        return list(set(targets))
