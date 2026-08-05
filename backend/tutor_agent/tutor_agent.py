import uuid
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from backend.tutor_agent.base_agent import BaseAgent
from backend.tutor_agent.models import TutorRequest, TutorResponse, KnowledgeLevel, QuizQuestion, LessonBreakdown, Subject
from backend.tutor_agent.memory import TutorMemoryStore
from backend.tutor_agent.database import LearnerProfile, LearningInteraction, LearnerProgress

class TutorAgent(BaseAgent):
    def __init__(self, memory_store: TutorMemoryStore):
        super().__init__(agent_id="tutor-agent-v1", name="LOT AI Senior Tutor Agent", domain="Education & Pedagogy")
        self.memory_store = memory_store

    async def process(self, request: TutorRequest) -> TutorResponse:
        session_id = request.session_id or f"sess-{uuid.uuid4().hex[:8]}"
        
        # 1. Retrieve prior context & vector RAG docs
        retrieved_docs = self.memory_store.query_knowledge_base(request.user_prompt)
        session_ctx = self.memory_store.get_session_context(session_id) or {}

        # 2. Synthesize pedagogical explanation & reasoning
        reasoning = [
            f"Analyzed query for subject '{request.subject.value}' at {request.knowledge_level.value} level.",
            f"Decomposed topic '{request.topic}' into core fundamental principles.",
            "Formulated intuitive real-world analogies suitable for the target mastery tier."
        ]
        
        examples = [
            f"Real-world application of {request.topic} in modern engineering.",
            f"Interactive problem-solving demonstration for {request.subject.value}."
        ]

        explanation_text = (
            f"### Educational Guide: {request.topic} ({request.knowledge_level.value.capitalize()} Tier)\n\n"
            f"**Core Concept Overview**:\n"
            f"{request.topic} forms a cornerstone principle in {request.subject.value}. "
            f"To understand this effectively, we start from first principles and build towards advanced mastery.\n\n"
            f"**Detailed Breakdown**:\n"
            f"1. **Foundations**: Understanding the fundamental laws and mathematical/logical formulations.\n"
            f"2. **Applications**: Bridging abstract theory with practical industry implementations."
        )

        lesson_plan = LessonBreakdown(
            subject=request.subject,
            topic=request.topic,
            subtopics=[f"Introduction to {request.topic}", f"Core Mechanics of {request.topic}", "Advanced Problem Solving"],
            estimated_time_minutes=25,
            learning_objectives=[f"Master core concepts of {request.topic}", f"Apply {request.topic} in practical scenarios"]
        )

        quiz = []
        if request.include_quiz:
            quiz.append(QuizQuestion(
                id=f"q-{uuid.uuid4().hex[:6]}",
                question=f"What is the primary objective of studying {request.topic} in {request.subject.value}?",
                options=[
                    f"To understand fundamental mechanics of {request.topic}",
                    "To ignore first principles",
                    "To skip problem solving",
                    "None of the above"
                ],
                correct_option_index=0,
                explanation=f"Understanding fundamental mechanics is critical for mastering {request.topic}."
            ))

        response = TutorResponse(
            session_id=session_id,
            learner_id=request.learner_id,
            subject=request.subject,
            topic=request.topic,
            knowledge_level=request.knowledge_level,
            explanation=explanation_text,
            step_by_step_reasoning=reasoning,
            practical_examples=examples,
            lesson_plan=lesson_plan,
            quiz=quiz,
            retrieved_context=retrieved_docs
        )

        # 3. Store session state in Redis
        self.memory_store.store_session_context(session_id, {
            "last_topic": request.topic,
            "last_subject": request.subject.value,
            "knowledge_level": request.knowledge_level.value
        })

        return response

    def save_interaction_log(self, db: Session, response: TutorResponse, prompt: str) -> None:
        interaction = LearningInteraction(
            id=f"int-{uuid.uuid4().hex[:10]}",
            learner_id=response.learner_id,
            subject=response.subject.value,
            topic=response.topic,
            prompt=prompt,
            explanation=response.explanation,
            quiz_data=[q.model_dump() for q in response.quiz] if response.quiz else None,
            difficulty_level=response.knowledge_level.value
        )
        db.add(interaction)
        db.commit()

    def get_status(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "domain": self.domain,
            "status": "active"
        }
