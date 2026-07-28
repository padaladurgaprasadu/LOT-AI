from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agents.base_agent import yAIAgentFactory
import sys

sys.stdout.reconfigure(encoding='utf-8')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

factory = yAIAgentFactory()
tutor_agent = factory.create_agent("Tutor Agent")

class TutorRequest(BaseModel):
    query: str
    history: list = []

@app.post("/api/tutor")
async def chat_tutor(request: TutorRequest):
    try:
        response = tutor_agent.invoke({"input": request.query})
        content = response.content if hasattr(response, 'content') else str(response)
        return {"response": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
