from fastapi import APIRouter, Depends, Form
from starlette import status
from starlette.responses import JSONResponse

from educationGPT.application.ports.driving.slack_service_port import SlackServicePort
from educationGPT.application.ports.driving.chat_service_port import ChatServicePort
from educationGPT.application.services.chat_service import ChatService
from educationGPT.driven.db.in_memory_conversation_repository import InMemoryConversationRepository
from educationGPT.driven.gpt.openai_client_adapter import OpenAIClientAdapter
from educationGPT.application.ports.driving.prompt_service_port import PromptConfigurationServicePort
from educationGPT.application.services.prompt_service import PromptConfigurationService
from educationGPT.driven.db.in_memory_prompt_configuration_repository import InMemoryPromptConfigurationRepository
from educationGPT.application.ports.driven.slack_repository_port import SlackRepositoryPort
from educationGPT.driven.slack.adapter import SlackRepositoryAdapter
from educationGPT.driving.api.v1.slack.models.slack_response_dto import SlackResponseDTO
from educationGPT.driving.api.v1.slack.models.slack_webhook_dto import SlackWebhookDTO
from educationGPT.driving.api.v1.slack.models.slack_slash_command_dto import SlackSlashCommandDTO
from educationGPT.driving.api.v1.slack.slack_api_mapper import SlackAPIMapper

slack_router = APIRouter()


@slack_router.post('/slack',
                   tags=['slack'],
                   status_code=201,
                   response_model=SlackWebhookDTO,
                   responses={
                       400: {'model': str},
                       500: {'model': str}
                   })
def webhook(request: SlackWebhookDTO,
            service: SlackServicePort = Depends()) -> SlackResponseDTO:
    slack_info = SlackAPIMapper.from_json_to_entity(request)
    service.process_webhook(slack_info)
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content={})


def get_chat_service() -> ChatServicePort:
    conv_repo = InMemoryConversationRepository()
    gpt_client = OpenAIClientAdapter()
    prompt_repo = InMemoryPromptConfigurationRepository()
    return ChatService(conv_repo, gpt_client, prompt_repo)


@slack_router.post('/slack/command',
                   tags=['slack'],
                   status_code=200)
def slash_command(
    command: str = Form(...),
    text: str = Form(...),
    user_id: str = Form(...),
    channel_id: str = Form(...),
    chat_service: ChatServicePort = Depends(get_chat_service),
    prompt_service: PromptConfigurationServicePort = Depends(
        lambda: PromptConfigurationService(InMemoryPromptConfigurationRepository())
    ),
    slack_repo: SlackRepositoryPort = Depends(lambda: SlackRepositoryAdapter()),
) -> JSONResponse:
    dto = SlackSlashCommandDTO(
        command=command,
        text=text,
        user_id=user_id,
        channel_id=channel_id,
    )
    # configure base prompt
    if dto.command == '/prompt':
        prompt_service.set_prompt(dto.user_id, dto.text)
        return JSONResponse(
            status_code=200,
            content={'response_type': 'ephemeral', 'text': 'Prompt guardado correctamente.'},
        )
    # get status recommendation
    if dto.command in ['/estado', '/state']:
        response_text = chat_service.handle_command(
            SlackAPIMapper.from_slash_to_entity(dto)
        )
        return JSONResponse(
            status_code=200,
            content={'response_type': 'ephemeral', 'text': response_text},
        )
    return JSONResponse(
        status_code=400,
        content={'response_type': 'ephemeral', 'text': 'Comando desconocido.'},
    )


@slack_router.post('/slack/remind/{user_id}', tags=['slack'], status_code=200)
def remind_user(
    user_id: str,
    prompt_service: PromptConfigurationServicePort = Depends(
        lambda: PromptConfigurationService(InMemoryPromptConfigurationRepository())
    ),
    slack_repo: SlackRepositoryPort = Depends(lambda: SlackRepositoryAdapter()),
) -> JSONResponse:
    base_prompt = prompt_service.get_prompt(user_id)
    if base_prompt:
        text = (
            f"¡Hola! Este es tu recordatorio diario. Por favor, indica cómo vas trabajando."
            f"\n\nRecordatorio inicial: {base_prompt}"
        )
    else:
        text = (
            "¡Hola! Este es tu recordatorio diario. Por favor, indica cómo vas trabajando."
        )
    dm_channel = slack_repo.open_dm(user_id)
    slack_repo.send_text(dm_channel, text)
    return JSONResponse(status_code=200, content={'status': 'recordatorio enviado'})
