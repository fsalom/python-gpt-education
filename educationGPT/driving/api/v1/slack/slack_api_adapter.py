from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse

from educationGPT.driving.api.v1.slack.models.slack_response_dto import SlackResponseDTO
from educationGPT.driving.api.v1.slack.models.slack_webhook_dto import SlackWebhookDTO
from educationGPT.driving.api.v1.slack.slack_api_mapper import SlackAPIMapper

slack_router = APIRouter()


@slack_router.post('/examples', tags=['examples'], status_code=201, response_model=SlackWebhookDTO,
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
