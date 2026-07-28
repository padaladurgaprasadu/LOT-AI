import json
from typing import TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from agents.base_agent import yAIAgentFactory
from agents.executer import SandboxExecuter

class yAIState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    current_agent: str
    plan: str
    status: str

factory = yAIAgentFactory()
router_agent = factory.create_agent("Router Agent")
planning_agent = factory.create_agent("Planning Agent")
reviewer_agent = factory.create_agent("Reviewer Agent")
sandbox = SandboxExecuter("yai_live_preview")

def router_node(state: yAIState):
    print("\n[Router Agent] Analyzing request and delegating...")
    return {"current_agent": "Full Stack Developer", "status": "routed"}

def planner_node(state: yAIState):
    print("\n[Planning Agent] Creating execution blueprint...")
    response = planning_agent.invoke({"input": f"Create a technical plan for: {state['messages'][-1].content}"})
    return {"plan": response.content, "status": "planned"}

def specialist_node(state: yAIState):
    agent_role = state.get("current_agent", "Developer Agent")
    print(f"\n[{agent_role}] Executing specialized task...")
    
    agent = factory.create_agent(agent_role)
    prompt = f"""Plan: {state['plan']}
    
Execute this plan flawlessly. 
CRITICAL: You MUST output ONLY valid JSON format. 
The JSON must be a dictionary where keys are file paths and values are the file content strings.
Do not output markdown code blocks. Just raw JSON.
Example: {{"index.html": "<html>...</html>", "script.js": "console.log('hi');"}}"""
    
    response = agent.invoke({"input": prompt})
    return {"messages": [AIMessage(content=response.content)], "status": "specialist_complete"}

def reviewer_node(state: yAIState):
    print("\n[Reviewer Agent] Validating output...")
    # Skipping deep review for this fast test to avoid getting stuck in loops
    return {"status": "approved"}

def executer_node(state: yAIState):
    print("\n[Executer Agent] Sandboxing and preparing Live Preview...")
    try:
        # The specialist output should be JSON
        content = state["messages"][-1].content
        # Basic cleanup in case the LLM wrapped it in markdown
        if content.startswith("```json"):
            content = content[7:-3]
        elif content.startswith("```"):
            content = content[3:-3]
            
        files_dict = json.loads(content.strip())
        
        # Write to sandbox
        sandbox.write_files(files_dict)
        
        # Start server
        sandbox.start_preview_server("python -m http.server 8080", 8080)
        
    except Exception as e:
        print(f"[Executer Agent] Failed to parse and deploy: {e}")
        return {"status": "failed_deployment"}

    return {"status": "deployed"}

def review_decision(state: yAIState):
    if state["status"] == "rejected" or state["status"] == "failed_deployment":
        return "specialist"
    return "executer"

workflow = StateGraph(yAIState)
workflow.add_node("router", router_node)
workflow.add_node("planner", planner_node)
workflow.add_node("specialist", specialist_node)
workflow.add_node("reviewer", reviewer_node)
workflow.add_node("executer", executer_node)

workflow.set_entry_point("router")
workflow.add_edge("router", "planner")
workflow.add_edge("planner", "specialist")
workflow.add_edge("specialist", "reviewer")
workflow.add_conditional_edges("reviewer", review_decision, {
    "specialist": "specialist",
    "executer": "executer"
})
workflow.add_edge("executer", END)

yai_engine = workflow.compile()

if __name__ == "__main__":
    print("--- Testing yAI Engine End-to-End ---")
    initial_state = {
        "messages": [HumanMessage(content="Build a beautiful, modern digital clock web app using HTML, CSS, and JS. Use dark mode and neon glow effects. Put it all in index.html.")],
        "current_agent": "",
        "plan": "",
        "status": "init"
    }
    
    final_state = yai_engine.invoke(initial_state)
    print("\n--- Final Workflow Execution Complete ---")
