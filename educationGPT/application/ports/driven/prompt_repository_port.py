from abc import ABC, abstractmethod


class PromptConfigurationRepositoryPort(ABC):
    @abstractmethod
    def save_prompt(self, user_id: str, prompt: str) -> None:
        """Persist the base prompt for a specific user."""
        raise NotImplementedError

    @abstractmethod
    def load_prompt(self, user_id: str) -> str:
        """Load the base prompt for a specific user."""
        raise NotImplementedError