from typing import Dict, Any, TypedDict
from langgraph.graph import StateGraph, END
from backend.tutor_agent.models import TutorRequest, TutorResponse
from backend.tutor_agent.tutor_agent import TutorAgent
from backend.tutor_agent.memory import TutorMemoryStore

class WorkflowState(TypedDict):
    request: TutorRequest
    response: TutorResponse
    error: str

def build_tutor_workflow(tutor_agent: TutorAgent):
    workflow = StateGraph(WorkflowState)

    async def retrieve_context_node(state: WorkflowState) -> Dict[str, Any]:
        req = state["request"]
        docs = tutor_agent.memory_store.query_knowledge_base(req.user_prompt)
        return {"request": req}

    async def generate_explanation_node(state: WorkflowState) -> Dict[str, Any]:
        req = state["request"]
        res = await tutor_agent.process(req)
        return {"response": res}

    workflow.add_node("retrieve_context", retrieve_context_node)
    workflow.add_node("generate_explanation", generate_explanation_node)

    workflow.set_entry_point("retrieve_context")
    workflow.add_edge("retrieve_context", "generate_explanation")
    workflow.add_edge("generate_explanation", END)

    return workflow.compile()
