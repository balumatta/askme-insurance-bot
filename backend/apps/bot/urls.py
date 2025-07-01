from fastapi import APIRouter

from backend.apps.bot.api_views import BotAPIView

api_router = APIRouter()

##################################################################################################################################
bot_view = BotAPIView()
api_router.add_api_route(path="/api/bot/ask", endpoint=bot_view.generate_answer, methods=['GET'])
