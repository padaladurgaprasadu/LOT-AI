import json
from typing import List, Dict, Any
from backend.utils.logger import get_logger

logger = get_logger(__name__)

class FeedbackEngine:
    """
    yAI Pillar 10: Self-Improving Intelligence (RLHF Feedback Loop)
    Records user corrections, runtime failures, and agent mistakes.
    Injects these corrections into future prompts (RAG for behavior correction).
    """
    def __init__(self):
        try:
            from backend.memory.chroma_client import ChromaClient
            self.chroma = ChromaClient()
            self.collection_name = "yai_feedback_loop"
            
            # Ensure collection exists
            if hasattr(self.chroma, "client") and self.chroma.client is not None:
                self.collection = self.chroma.client.get_or_create_collection(self.collection_name)
            else:
                self.collection = None
        except Exception as e:
            logger.error(f"[FeedbackEngine] Failed to initialize ChromaDB: {e}")
            self.collection = None

    def record_correction(self, agent_key: str, original_output: str, corrected_output: str, context: str):
        """
        Stores a correction pair in the vector database.
        """
        if not self.collection:
            logger.warning("[FeedbackEngine] ChromaDB not available. Cannot store correction.")
            return

        import uuid
        correction_id = str(uuid.uuid4())
        
        document = f"CONTEXT: {context}\nORIGINAL MISTAKE:\n{original_output}\nCORRECTED OUTPUT:\n{corrected_output}"
        
        try:
            self.collection.add(
                documents=[document],
                metadatas=[{"agent_key": agent_key, "type": "user_correction"}],
                ids=[correction_id]
            )
            logger.info(f"[FeedbackEngine] Recorded correction for agent {agent_key}")
        except Exception as e:
            logger.error(f"[FeedbackEngine] Failed to add correction to ChromaDB: {e}")

    def get_relevant_corrections(self, agent_key: str, current_prompt: str, top_k: int = 2) -> str:
        """
        Retrieves past corrections relevant to the current prompt to prevent repeating mistakes.
        """
        if not self.collection:
            return ""

        try:
            results = self.collection.query(
                query_texts=[current_prompt],
                n_results=top_k,
                where={"agent_key": agent_key}
            )
            
            if not results or not results.get("documents") or not results["documents"][0]:
                return ""
                
            docs = results["documents"][0]
            if not docs:
                return ""
                
            header = "⚠️ PREVIOUS MISTAKES & CORRECTIONS TO LEARN FROM ⚠️\n"
            return header + "\n\n---\n\n".join(docs)
            
        except Exception as e:
            logger.error(f"[FeedbackEngine] Failed to retrieve corrections: {e}")
            return ""

    def inject_corrections(self, agent_key: str, system_prompt: str, user_request: str) -> str:
        """
        Takes the base system prompt and appends any relevant past corrections.
        """
        corrections = self.get_relevant_corrections(agent_key, user_request)
        if corrections:
            logger.info(f"[FeedbackEngine] Injected past corrections for {agent_key}")
            return f"{system_prompt}\n\n{corrections}"
        return system_prompt
