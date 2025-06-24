from pydantic import BaseModel


class SlackResponseDTO(BaseModel):
    name: str
