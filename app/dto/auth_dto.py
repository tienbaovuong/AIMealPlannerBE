from datetime import datetime, date
from pydantic import BaseModel
from typing import Optional, List

from app.dto.common import BaseResponseData
from app.models.user_account import Gender

class LoginRequest(BaseModel):
    email: str
    password: str

class SignUpRequest(BaseModel):
    name: str
    password: str
    email: str
    weight: Optional[float]
    height: Optional[float]
    age: date
    gender: Optional[Gender]
    allergies: List[str]
    dietary_preferences: List[str]
    profile_picture: Optional[str]

class EditRequest(BaseModel):
    name: str
    weight: Optional[float]
    height: Optional[float]
    age: date
    gender: Optional[Gender]
    allergies: List[str]
    dietary_preferences: List[str]
    profile_picture: Optional[str]

class LoginResponseData(BaseModel):
    access_token: str

class LoginResponse(BaseResponseData):
    data: LoginResponseData

class UserResponseData(BaseModel):
    name: str
    email: str
    weight: Optional[float]
    height: Optional[float]
    age: date
    gender: Optional[Gender]
    allergies: List[str]
    dietary_preferences: List[str]
    profile_picture: Optional[str]
    created_at: datetime
    updated_at: datetime

class UserResponse(BaseResponseData):
    data: UserResponseData