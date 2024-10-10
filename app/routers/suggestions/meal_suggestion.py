from fastapi import APIRouter, Depends, Query

from app.dto.common import BaseResponseData
from app.helpers.auth_helpers import get_current_user
from app.helpers.exceptions import BadRequestException
from app.services.meal_suggestion_services import MealSuggestionService

router = APIRouter(tags=['Meal suggestion'], prefix='/suggestions')


@router.get(
    '/with_llm',
    response_model=BaseResponseData,
)
async def get_suggestion_meal_with_llm(
    user_id: str = Depends(get_current_user)
):
    suggested_meals = await MealSuggestionService.llm_suggestion_meal(user_id)

    return BaseResponseData(
        message="Get list meal successfully",
        data=BaseResponseData(
            data=suggested_meals
        )
    )

@router.get(
    '/without_llm',
    response_model=BaseResponseData,
)
async def get_suggestion_meal(
    user_id: str = Depends(get_current_user)
):
    meals = await MealSuggestionService.suggestion_meal()

    return BaseResponseData(
        message="Get list meal successfully",
        data=BaseResponseData(
            data=meals
        )
    )

@router.get(
    '/recipe/{meal_id}',
    response_model=BaseResponseData,
)
async def get_meal_recipe_by_id(
    meal_id: str,
    user_id: str = Depends(get_current_user)
):
    meal = await MealSuggestionService.get_meal_recipe_by_id(meal_id)
    return BaseResponseData(
        message="Get meal recipe successfully",
        data=BaseResponseData(
            data=meal
        )
    )