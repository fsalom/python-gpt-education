from typing import Dict, Any

from educationGPT.domain.entities.slack import SlackMessageData


class SlackAPIMapper:
    @staticmethod
    def from_json_to_entity(data: Dict[str, Any]) -> SlackMessageData:
        return SlackMessageData(**data)
