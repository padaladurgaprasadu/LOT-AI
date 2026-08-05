import pytest
import asyncio
from backend.tutor_agent.models import TutorRequest, Subject, KnowledgeLevel
from backend.tutor_agent.memory import TutorMemoryStore
from backend.tutor_agent.tutor_agent import TutorAgent


@pytest.fixture
def mock_memory_store(mocker):
    store = mocker.MagicMock(spec=TutorMemoryStore)
    store.query_knowledge_base.return_value = ["Sample textbook doc"]
    store.get_session_context.return_value = {}
    return store


@pytest.mark.asyncio
async def test_tutor_agent_process(mock_memory_store):
    agent = TutorAgent(memory_store=mock_memory_store)
    req = TutorRequest(
        learner_id="learner-123",
        subject=Subject.COMPUTER_SCIENCE,
        topic="Data Structures",
        user_prompt="Explain binary search trees",
        knowledge_level=KnowledgeLevel.BEGINNER,
        include_quiz=True
    )
    res = await agent.process(req)

    assert res.learner_id == "learner-123"
    assert res.subject == Subject.COMPUTER_SCIENCE
    assert res.topic == "Data Structures"
    assert "Binary" in res.explanation or "Data Structures" in res.explanation
    assert len(res.quiz) == 1
    assert res.quiz[0].correct_option_index == 0
