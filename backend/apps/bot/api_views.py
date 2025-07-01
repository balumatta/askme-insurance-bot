import traceback
from fastapi import Request, status
from fastapi.responses import JSONResponse
import logging

from backend.apps.bot.controller import BotController
from backend.apps.bot.serializer import GenerateAnswerInputSerializer
from backend.apps.bot.status_codes import BotStatusCodes

logger = logging.getLogger(__name__)


class BotAPIView:
    def __init__(self):
        pass

    async def generate_answer(self, request: Request):
        data = await request.json()
        try:
            GenerateAnswerInputSerializer(**data)
        except Exception as e:
            traceback.print_exc()
            response = f'Something went wrong while generating answer. Reason - {str(e)}'
            return JSONResponse(content=response, status_code=status.HTTP_412_PRECONDITION_FAILED)

        answer = await BotController().generate_answer(data)
        if not answer:
            response = f'Something went wrong while generating answer'
            return JSONResponse(content=response, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response = BotStatusCodes.ANSWER_GENERATED
        response['answer_info'] = answer
        return JSONResponse(content=response, status_code=status.HTTP_200_OK)
