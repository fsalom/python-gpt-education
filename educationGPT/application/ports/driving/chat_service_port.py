from abc import ABC, abstractmethod

from educationGPT.domain.entities.chat import ChatCommandData


class ChatServicePort(ABC):
    @abstractmethod
    def handle_command(self, command: ChatCommandData) -> str:
        """Process a chat command and return assistant response."""
        raise NotImplementedError