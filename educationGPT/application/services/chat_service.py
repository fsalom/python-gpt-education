from educationGPT.application.ports.driving.chat_service_port import ChatServicePort
from educationGPT.application.ports.driven.conversation_repository_port import ConversationRepositoryPort
from educationGPT.application.ports.driven.gpt_client_port import GPTClientPort
from educationGPT.domain.entities.chat import ChatCommandData, ChatMessage
from educationGPT.application.ports.driven.prompt_repository_port import PromptConfigurationRepositoryPort


class ChatService(ChatServicePort):
    def __init__(
        self,
        conversation_repo: ConversationRepositoryPort,
        gpt_client: GPTClientPort,
        prompt_config_repo: PromptConfigurationRepositoryPort,
    ):
        self.conversation_repo = conversation_repo
        self.gpt_client = gpt_client
        self.prompt_config_repo = prompt_config_repo

    def handle_command(self, cmd: ChatCommandData) -> str:
        history = self.conversation_repo.get_history(cmd.user_id)
        if not history:
            base_prompt = self.prompt_config_repo.load_prompt(cmd.user_id)
            if base_prompt:
                history.append(ChatMessage(role="system", content=base_prompt))
        history.append(cmd.message)
        assistant_reply = self.gpt_client.send_messages(history)
        history.append(ChatMessage(role="assistant", content=assistant_reply))
        self.conversation_repo.save_history(cmd.user_id, history)
        return assistant_reply