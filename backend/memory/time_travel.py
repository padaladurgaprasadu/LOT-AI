import os
import json
import uuid
from datetime import datetime
from backend.memory.chroma_client import ChromaClient

class TimeTravelEngine:
    """
    Semantic Time-Travel Git
    Replaces traditional Git with Vector-based natural language rollbacks.
    Allows users to say 'Revert the UI to yesterday but keep the Stripe backend'.
    """
    def __init__(self):
        self.memory_client = ChromaClient()
        # Fallback to ephemeral if the persistent collection fails
        try:
            self.snapshots = self.memory_client.client.get_or_create_collection("time_travel_snapshots", embedding_function=self.memory_client.embedding_fn)
        except Exception:
            self.snapshots = self.memory_client.client.get_or_create_collection("time_travel_snapshots")

    def snapshot_workspace(self, workspace_path: str, intent: str) -> str:
        """
        Takes a snapshot of all files in the workspace and stores them in ChromaDB.
        """
        snapshot_id = f"snap-{str(uuid.uuid4())[:8]}"
        files_data = {}
        
        # Serialize workspace files
        for root, _, files in os.walk(workspace_path):
            for file in files:
                if file.endswith((".py", ".js", ".html", ".css", ".json", ".md", ".tsx", ".jsx")):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, workspace_path)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            files_data[rel_path] = f.read()
                    except Exception:
                        pass
                        
        serialized_state = json.dumps(files_data)
        timestamp = datetime.utcnow().isoformat()
        
        # Store in Vector DB
        document = f"Intent: {intent}\nTimestamp: {timestamp}\nState: {serialized_state}"
        self.snapshots.add(
            documents=[document],
            metadatas=[{"intent": intent, "timestamp": timestamp}],
            ids=[snapshot_id]
        )
        print(f"[TimeTravel] Workspace snapshot {snapshot_id} saved to Vector Memory.")
        return snapshot_id

    def rollback_workspace(self, workspace_path: str, semantic_query: str) -> bool:
        """
        Searches ChromaDB for a past snapshot matching the user's natural language query.
        Hot-swaps the files in the workspace with the historical state.
        """
        print(f"[TimeTravel] Searching memory for rollback target: '{semantic_query}'...")
        try:
            results = self.snapshots.query(
                query_texts=[semantic_query],
                n_results=1
            )
            
            if results and results["documents"] and len(results["documents"][0]) > 0:
                doc = results["documents"][0][0]
                # Extract the JSON state
                state_str = doc.split("State: ")[1]
                files_data = json.loads(state_str)
                
                # Hot-swap the files
                for rel_path, content in files_data.items():
                    full_path = os.path.join(workspace_path, rel_path)
                    os.makedirs(os.path.dirname(full_path), exist_ok=True)
                    with open(full_path, "w", encoding="utf-8") as f:
                        f.write(content)
                        
                print(f"[TimeTravel] Successfully reverted workspace to historical state matching '{semantic_query}'.")
                return True
            else:
                print("[TimeTravel] No matching historical snapshot found.")
                return False
        except Exception as e:
            print(f"[TimeTravel] Rollback failed: {e}")
            return False
