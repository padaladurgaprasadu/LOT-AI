import datetime
from typing import Generator
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Text, Float, ForeignKey, JSON
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from backend.tutor_agent.config import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class LearnerProfile(Base):
    __tablename__ = "learner_profiles"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    knowledge_level = Column(String, default="beginner")
    preferred_subjects = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    interactions = relationship("LearningInteraction", back_populates="learner")
    progress_records = relationship("LearnerProgress", back_populates="learner")


class LearningInteraction(Base):
    __tablename__ = "learning_interactions"

    id = Column(String, primary_key=True, index=True)
    learner_id = Column(String, ForeignKey("learner_profiles.id"), nullable=False)
    subject = Column(String, nullable=False)
    topic = Column(String, nullable=False)
    prompt = Column(Text, nullable=False)
    explanation = Column(Text, nullable=False)
    quiz_data = Column(JSON, nullable=True)
    difficulty_level = Column(String, default="beginner")
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    learner = relationship("LearnerProfile", back_populates="interactions")


class LearnerProgress(Base):
    __tablename__ = "learner_progress"

    id = Column(String, primary_key=True, index=True)
    learner_id = Column(String, ForeignKey("learner_profiles.id"), nullable=False)
    subject = Column(String, nullable=False)
    topic = Column(String, nullable=False)
    mastery_score = Column(Float, default=0.0)
    completed_lessons = Column(Integer, default=0)
    last_studied = Column(DateTime, default=datetime.datetime.utcnow)

    learner = relationship("LearnerProfile", back_populates="progress_records")


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
