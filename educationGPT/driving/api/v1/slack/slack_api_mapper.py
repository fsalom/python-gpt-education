from typing import Dict, Any

from educationGPT.domain.entities.slack import SlackMessageData
from educationGPT.driving.api.v1.slack.models.slack_slash_command_dto import SlackSlashCommandDTO
from educationGPT.domain.entities.chat import ChatCommandData, ChatMessage


class SlackAPIMapper:
    @staticmethod
    def from_json_to_entity(data: Dict[str, Any]) -> SlackMessageData:
        return SlackMessageData(**data)

    @staticmethod
    def from_slash_to_entity(data: SlackSlashCommandDTO) -> ChatCommandData:
        return ChatCommandData(
            user_id=data.user_id,
            channel_id=data.channel_id,
            message=ChatMessage(role='user', content=data.text),
        )
