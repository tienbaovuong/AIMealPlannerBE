from datetime import datetime
from typing import Optional, List
from pymongo import ASCENDING, IndexModel

from app.models.base import RootModel, RootEnum

class Gender(str, RootEnum):
    MALE = "MALE"
    FEMALE = "FEMALE"

class UserAccount(RootModel):
    class Collection:
        name = "user_account"
        indexes = [
            IndexModel(
                [
                    ("email", ASCENDING),
                ],
                unique=True,
            )
        ]

    name: str
    email: str
    #hash password before put in db / best do it from FE
    password: str
    weight: Optional[float] # kg
    height: Optional[float] # cm
    date_of_birth: datetime #YYYY-MM-DD
    gender: Optional[Gender] # MALE, FEMALE or OTHER(null)
    allergies: List[str]
    dietary_preferences: List[str]
    profile_picture: Optional[str] # Profile id
