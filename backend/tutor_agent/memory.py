import json
from typing import List, Dict, Any, Optional
import redis
import chromadb
from backend.tutor_agent.config import settings

class TutorMemoryStore:
    def __init__(self):
        self.redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
        try:
            self.chroma_client = chromadb.HttpClient(host=settings.CHROMADB_HOST, port=settings.CHROMADB_PORT)
            self.chroma_collection = self.chroma_client.get_or_create_collection(name="tutor_knowledge_base")
        except Exception:
            self.chroma_client = None
            self.chroma_collection = None

    def store_session_context(self, session_id: str, context_data: Dict[str, Any], ttl_seconds: int = 86400) -> None:
        key = f"tutor_session:{session_id}"
        self.redis_client.setex(key, ttl_seconds, json.dumps(context_data))

    def get_session_context(self, session_id: str) -> Optional[Dict[str, Any]]:
        key = f"tutor_session:{session_id}"
        data = self.redis_client.get(key)
        if data:
            return json.loads(data)
        return None

    def add_knowledge_doc(self, doc_id: str, document: str, metadata: Dict[str, Any]) -> None:
        if self.chroma_collection:
            self.chroma_collection.add(
                documents=[document],
                metadatas=[metadata],
                ids=[doc_id]
            )

    def query_knowledge_base(self, query_text: str, n_results: int = 3) -> List[str]:
        if self.chroma_collection:
            results = self.chroma_collection.query(
                query_texts=[query_text],
                n_results=n_results
            )
            documents = results.get("documents", [[]])
            return documents[0] if documents else []
        return []
