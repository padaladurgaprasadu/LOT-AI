from abc import ABC, abstractmethod
from typing import Any, Dict
from pydantic import BaseModel


class BaseAgent(ABC):
    def __init__(self, agent_id: str, name: str, domain: str):
        self.agent_id = agent_id
        self.name = name
        self.domain = domain

    @abstractmethod
    async def process(self, request: BaseModel) -> BaseModel:
        pass

    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        pass
