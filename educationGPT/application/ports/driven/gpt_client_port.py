from abc import ABC, abstractmethod
from typing import List

from educationGPT.domain.entities.chat import ChatMessage


class GPTClientPort(ABC):
    @abstractmethod
    def send_messages(self, messages: List[ChatMessage]) -> str:
        """Send chat messages to a language model and return the assistant reply."""
        raise NotImplementedError