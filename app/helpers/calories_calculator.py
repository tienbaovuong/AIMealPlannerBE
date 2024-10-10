from datetime import datetime 
from app.dto.auth_dto import UserResponseData
from app.models.user_account import Gender


def calories_calculator(user: UserResponseData):
    # TODO: Implement the calories calculator based on user's information
    calories_per_day = 0
    user_age = datetime.now().year - user.date_of_birth.year
    if user.gender == Gender.MALE:
        calories_per_day = (10 * user.weight) + (6.25 * user.height) - (5 * user_age) + 5
    elif user.gender == Gender.FEMALE:
        calories_per_day = (10 * user.weight) + (6.25 * user.height) - (5 * user_age) - 161
    return calories_per_day