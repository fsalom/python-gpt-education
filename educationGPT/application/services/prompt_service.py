from educationGPT.application.ports.driving.prompt_service_port import PromptConfigurationServicePort
from educationGPT.application.ports.driven.prompt_repository_port import PromptConfigurationRepositoryPort


class PromptConfigurationService(PromptConfigurationServicePort):
    def __init__(self, repo: PromptConfigurationRepositoryPort):
        self.repo = repo

    def set_prompt(self, user_id: str, prompt: str) -> None:
        self.repo.save_prompt(user_id, prompt)

    def get_prompt(self, user_id: str) -> str:
        return self.repo.load_prompt(user_id)