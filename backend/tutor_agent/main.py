from fastapi import FastAPI
from backend.tutor_agent.config import settings
from backend.tutor_agent.database import init_db
from backend.tutor_agent.api import router as tutor_router

app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(tutor_router, prefix=settings.API_V1_STR)

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": settings.PROJECT_NAME}
