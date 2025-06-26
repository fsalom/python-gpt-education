from abc import ABC, abstractmethod


class PromptConfigurationServicePort(ABC):
    @abstractmethod
    def set_prompt(self, user_id: str, prompt: str) -> None:
        """Configure the base prompt for a specific user."""
        raise NotImplementedError

    @abstractmethod
    def get_prompt(self, user_id: str) -> str:
        """Retrieve the configured base prompt for a specific user."""
        raise NotImplementedError