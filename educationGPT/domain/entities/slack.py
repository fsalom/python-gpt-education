from typing import Optional

from pydantic import Field


class SlackMessageData():
    slack_channel_id: str
    pr_url: str
    metadata: Optional[dict] = Field(default_factory=dict)


class Type():
    type: str


class Text(Type):
    text: str


class Accessory(Type):
    image_url: str
    alt_text: str


class Block():
    """
    [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": ":tada: ¡Aquí tienes los días de oficina! :tada:",
            },
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Responsable*\n{manager_first_name}\n*Fecha del mensaje:*\n{date}\n"
                f"Para cualquier cambio sobre los dias de la oficina o duda de justificantes, vacaciones, Sesame, Pyxis coméntalo con tu responsable :smile:",
            },
            "accessory": {
                "type": "image",
                "image_url": "https://rudo.fra1.digitaloceanspaces.com/rudo/media/image/Captura%20de%20Pantalla%202022-06-07%20a%20las%209.23.46.png",
                "alt_text": "Oficina",
            },
        },
    ]
    """

    type: str
    text: Optional[Text] = Field(None)
    accessory: Optional[Accessory] = Field(None)
