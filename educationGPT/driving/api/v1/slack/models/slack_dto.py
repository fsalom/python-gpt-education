from pydantic import BaseModel


class SlackDTO(BaseModel):
    name: str
