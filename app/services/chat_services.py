import logging
from typing import List

from app.dto.chat_dto import ChatResponseData
from app.helpers.exceptions import NotFoundException, BadRequestException, PermissionDeniedException
from app.langchain_helpers.custom_query_retriever import retriever
from app.models.chat_history import ChatHistory, MessageType
from app.services.account_services import AuthService
from app.helpers.calories_calculator import calories_calculator
from app.langchain_helpers.chat_with_template import get_chat_response, stream_chat_response, get_chat_intentions

_logger = logging.getLogger(__name__)

class ChatService:

    @staticmethod
    async def get_history(user_id: str) -> List[ChatResponseData]:
        return await ChatHistory.get_all_by_user_id(user_id)
    
    @staticmethod
    async def save_history(user_id: str, messages: List[dict]):
        for message in messages:
            await ChatHistory.create(
                user_id=user_id,
                message=message["message"],
                message_type=message["messageType"],
            )
    
    @staticmethod
    async def chat_suggestion(user_id: str, user_message: str) -> List[dict]:
        # Get chat intention
        intention = await get_chat_intentions(user_message)
        _logger.info(f"Intention: {intention}")

        # Check intention
        if intention != "MEAL_SUGGESTION":
            return [
                ChatResponseData(
                    message="Sorry, I can only help you with meal suggestion",
                    messageType=MessageType.BOT_TEXT,
                ).dict(),
                ChatResponseData(
                    message="Try 'I want to eat something with cabbage' or 'Spicy food for dinner'",
                    messageType=MessageType.BOT_TEXT,
                ).dict()
            ]

        # Preprocess
        user = await AuthService.get_user_by_id(user_id)
        calories = calories_calculator(user)
        query = f"Find meal for the user, their allergies are {user.allergies} and their calories limit are {calories}, user request: {user_message}"

        # Retrieval
        meals = await retriever.ainvoke(query)

        # Parse
        parse_meals = []
        meal_titles = ""
        for meal in meals:
            parse_meals.append(meal.metadata)
            meal_titles += meal.metadata["title"] + "; "

        # Get chat response
        response = await get_chat_response(user_message, meal_titles)

        # Format response
        return_msg = []
        return_msg.append(
            ChatResponseData(
                message=response,
                messageType=MessageType.BOT_TEXT,
            ).dict()
        )
        for meal in parse_meals:
            return_msg.append(
                ChatResponseData(
                    message=meal,
                    messageType=MessageType.BOT_DETAIL,
                ).dict()
            )
        
        return return_msg
    
    @staticmethod
    async def chat_stream_response(user_id: str, user_message: str):
        # Get chat intention
        intention = await get_chat_intentions(user_message)
        _logger.info(f"Intention: {intention}")

        # Check intention
        if intention != "MEAL_SUGGESTION":
            yield ChatResponseData(
                    message="Sorry, I can only help you with meal suggestion",
                    messageType=MessageType.BOT_TEXT,
                ).dict()
            yield ChatResponseData(
                    message="Try 'I want to eat something with cabbage' or 'Spicy food for dinner'",
                    messageType=MessageType.BOT_TEXT,
                ).dict()
            return

        # Preprocess
        user = await AuthService.get_user_by_id(user_id)
        calories = calories_calculator(user)
        query = f"Find meal for the user, their allergies are {user.allergies} and their calories limit are {calories}, user request: {user_message}"

        # Retrieval
        meals = await retriever.ainvoke(query)

        # Parse
        parse_meals = []
        meal_titles = ""
        for meal in meals:
            parse_meals.append(meal.metadata)
            meal_titles += meal.metadata["title"] + "; "

        # Get chat response
        async for response in stream_chat_response(user_message, meal_titles):
            yield ChatResponseData(
                message=response,
                messageType=MessageType.BOT_TEXT,
            ).dict()

        for meal in parse_meals:
            yield ChatResponseData(
                    message=meal,
                    messageType=MessageType.BOT_DETAIL,
                ).dict()


