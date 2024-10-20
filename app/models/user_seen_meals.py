from datetime import datetime
from typing import List
from pymongo import ASCENDING, IndexModel

from app.models.base import RootModel

class UserSeenMeals(RootModel):
    class Collection:
        name = "user_seen_meals"
        indexes = [
            IndexModel(
                [
                    ("user_id", ASCENDING),
                ],
                unique=True,
            )
        ]

    user_id: str
    seen_meals: List[str]

    @staticmethod
    async def find_one_or_create(user_id: str) -> "UserSeenMeals":
        user_seen_meals = await UserSeenMeals.find_one({"user_id": user_id})
        if not user_seen_meals:
            user_seen_meals = UserSeenMeals(user_id=user_id, seen_meals=[], created_at=datetime.now(), updated_at=datetime.now())
            user_seen_meals = await user_seen_meals.save()
        return user_seen_meals
