from abc import ABC, abstractmethod
from typing import List

from educationGPT.domain.entities.chat import ChatMessage


class ConversationRepositoryPort(ABC):
    @abstractmethod
    def get_history(self, user_id: str) -> List[ChatMessage]:
        """Retrieve the chat history for a user."""
        raise NotImplementedError

    @abstractmethod
    def save_history(self, user_id: str, history: List[ChatMessage]) -> None:
        """Save the chat history for a user."""
        raise NotImplementedError