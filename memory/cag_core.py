import chromadb
from chromadb.config import Settings
import uuid
import datetime

class GlobalMemoryMesh:
    """
    Continuous Augmented Generation (CAG) Core.
    Acts as the persistent, global brain for all 34 yAI Agents.
    """
    def __init__(self, persist_directory="./.yai_memory"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(
            name="yai_global_mesh",
            metadata={"hnsw:space": "cosine"}
        )

    def log_thought(self, agent_role: str, content: str, context_tags: list = None):
        """
        Agents use this to proactively write their thoughts/actions to the global memory.
        """
        doc_id = str(uuid.uuid4())
        timestamp = datetime.datetime.now().isoformat()
        
        metadata = {
            "agent": agent_role,
            "timestamp": timestamp,
        }
        
        if context_tags:
            metadata["tags"] = ",".join(context_tags)

        self.collection.add(
            documents=[content],
            metadatas=[metadata],
            ids=[doc_id]
        )
        print(f"[{agent_role}] Thought committed to Global CAG Mesh.")

    def recall_context(self, query: str, n_results: int = 3, filter_by_agent: str = None):
        """
        Agents use this to dynamically retrieve relevant past experiences before generating code or plans.
        """
        where_clause = {}
        if filter_by_agent:
            where_clause = {"agent": filter_by_agent}

        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where_clause if where_clause else None
        )
        
        # Format the output context
        retrieved_memories = []
        if results and results.get('documents') and len(results['documents']) > 0:
            docs = results['documents'][0]
            metas = results['metadatas'][0]
            for i in range(len(docs)):
                retrieved_memories.append(f"[Past Thought from {metas[i]['agent']} at {metas[i]['timestamp']}]: {docs[i]}")
                
        return retrieved_memories

# Singleton instance for the OS
memory_core = GlobalMemoryMesh()
