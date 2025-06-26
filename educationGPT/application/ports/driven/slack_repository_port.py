from abc import ABC, abstractmethod
from typing import Any, Dict, List

from educationGPT.domain.entities.slack import Block


class SlackRepositoryPort(ABC):
    @abstractmethod
    def send_message(
            self, slack_channel_id: str, pr_url: str, metadata: Dict[Any, Any]
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def open_dm(self, user_id: str) -> str:
        """Open (or get) a DM channel ID for the given user."""
        raise NotImplementedError

    @abstractmethod
    def send_text(self, channel_id: str, text: str) -> None:
        """Send a plain text message to a Slack channel or DM."""
        raise NotImplementedError
