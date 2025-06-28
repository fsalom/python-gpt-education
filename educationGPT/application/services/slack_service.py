from educationGPT.application.ports.driven.slack_repository_port import SlackRepositoryPort
from educationGPT.application.ports.driving.slack_service_port import SlackServicePort
from educationGPT.domain.entities.slack import SlackMessageData


class SlackService(SlackServicePort):
    def __init__(self, slack_repository_port: SlackRepositoryPort):
        self.slack_repository_port = slack_repository_port

    def process_webhook(self, slack_message_data: SlackMessageData) -> None:
        self.slack_repository_port.send_message(**slack_message_data.to_dict())
