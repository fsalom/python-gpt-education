from abc import ABC, abstractmethod

from educationGPT.domain.entities.slack import SlackMessageData


class SlackServicePort(ABC):
    @abstractmethod
    def process_webhook(self, slack_message_data: SlackMessageData) -> None:
        raise NotImplementedError
