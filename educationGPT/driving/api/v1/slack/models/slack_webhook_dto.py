from typing import Optional

from pydantic import BaseModel, Field


class SlackWebhookDTO(BaseModel):
    slack_channel_id: str
    pr_url: str
    metadata: Optional[dict] = Field(default_factory=dict)
