from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.tutor_agent.models import TutorRequest, TutorResponse
from backend.tutor_agent.tutor_agent import TutorAgent
from backend.tutor_agent.dependencies import get_tutor_agent
from backend.tutor_agent.database import get_db

router = APIRouter(prefix="/tutor", tags=["Tutor Agent"])


@router.post("/explain", response_model=TutorResponse, status_code=status.HTTP_200_OK)
async def generate_explanation(
    request: TutorRequest,
    agent: TutorAgent = Depends(get_tutor_agent),
    db: Session = Depends(get_db)
):
    try:
        response = await agent.process(request)
        agent.save_interaction_log(db, response, prompt=request.user_prompt)
        return response
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Tutor Agent execution failed: {str(exc)}"
        )


@router.get("/status")
def get_agent_status(agent: TutorAgent = Depends(get_tutor_agent)):
    return agent.get_status()
