from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field


class KnowledgeLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class Subject(str, Enum):
    MATHEMATICS = "Mathematics"
    PHYSICS = "Physics"
    CHEMISTRY = "Chemistry"
    BIOLOGY = "Biology"
    COMPUTER_SCIENCE = "Computer Science"
    ARTIFICIAL_INTELLIGENCE = "Artificial Intelligence"
    PROGRAMMING = "Programming"
    ELECTRONICS = "Electronics"


class QuizQuestion(BaseModel):
    id: str
    question: str
    options: List[str]
    correct_option_index: int
    explanation: str


class LessonBreakdown(BaseModel):
    subject: Subject
    topic: str
    subtopics: List[str]
    estimated_time_minutes: int
    learning_objectives: List[str]


class TutorRequest(BaseModel):
    learner_id: str
    subject: Subject
    topic: str
    user_prompt: str
    knowledge_level: Optional[KnowledgeLevel] = KnowledgeLevel.BEGINNER
    include_quiz: bool = True
    session_id: Optional[str] = None


class TutorResponse(BaseModel):
    session_id: str
    learner_id: str
    subject: Subject
    topic: str
    knowledge_level: KnowledgeLevel
    explanation: str
    step_by_step_reasoning: List[str]
    practical_examples: List[str]
    lesson_plan: Optional[LessonBreakdown] = None
    quiz: Optional[List[QuizQuestion]] = None
    retrieved_context: List[str] = Field(default_factory=list)
