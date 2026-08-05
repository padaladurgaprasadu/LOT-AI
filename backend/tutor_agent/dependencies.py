from backend.tutor_agent.memory import TutorMemoryStore
from backend.tutor_agent.tutor_agent import TutorAgent

memory_store_instance = TutorMemoryStore()
tutor_agent_instance = TutorAgent(memory_store=memory_store_instance)

def get_tutor_agent() -> TutorAgent:
    return tutor_agent_instance
