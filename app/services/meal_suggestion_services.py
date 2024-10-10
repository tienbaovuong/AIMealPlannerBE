import logging
from typing import List

from app.helpers.exceptions import NotFoundException, BadRequestException, PermissionDeniedException
from app.langchain_helpers.custom_query_retriever import vector_store, retriever
from app.models.user_seen_meals import UserSeenMeals
from app.services.account_services import AuthService
from app.helpers.calories_calculator import calories_calculator

_logger = logging.getLogger(__name__)

class MealSuggestionService:
    @staticmethod
    async def llm_suggestion_meal(user_id: str) -> List[dict]:
        # Preprocess
        user = await AuthService.get_user_by_id(user_id)
        user_seen_meals = await UserSeenMeals.find_one_or_create(user_id)
        exclude_ids = user_seen_meals.seen_meals
        calories = calories_calculator(user)
        query = f"Find meal for the user, their allergies are {user.allergies} and their calories limit are {calories}"

        # Retrieval
        meals = await retriever.ainvoke(query, exclude_ids=exclude_ids)

        # Parse
        parse_meals = []
        for meal in meals:
            parse_meal = meal.metadata
            parse_meal["id"] = meal.id
            parse_meals.append(parse_meal)
            user_seen_meals.seen_meals.append(meal.id)

        await user_seen_meals.save()
        return parse_meals
    
    @staticmethod
    async def suggestion_meal():
        meals = await vector_store.asimilarity_search(query="", k=3)
        parse_meals = []
        for meal in meals:
            parse_meal = meal.metadata
            parse_meal["id"] = meal.id
            parse_meals.append(parse_meal)
        return parse_meals

    @staticmethod
    async def get_meal_recipe_by_id(meal_id: str) -> dict:
        meal = await vector_store.asimilarity_search(query="", k=1, filter=[{"query": {"ids": {"values": [meal_id]}}}])
        if not meal:
            raise NotFoundException("Meal not found")
        meal_with_id = meal[0].metadata
        meal_with_id["id"] = meal[0].id
        return meal_with_id
