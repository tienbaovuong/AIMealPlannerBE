import logging
import hashlib
from datetime import datetime
from beanie import PydanticObjectId
from pymongo.errors import DuplicateKeyError

from app.models.user_account import UserAccount
from app.dto.auth_dto import SignUpRequest, UserResponseData
from app.helpers.exceptions import NotFoundException, BadRequestException, PermissionDeniedException
from app.helpers.auth_helpers import login_token

_logger = logging.getLogger(__name__)


class AuthService:
    @staticmethod
    async def login(email: str, password: str) -> UserAccount:
        user = await UserAccount.find_one({"email": email})
        if not user:
            raise PermissionDeniedException("Wrong email or password")
        if user.password != hashlib.sha256(password.encode()).hexdigest():
            raise PermissionDeniedException("Wrong email or password")
        access_token = login_token(str(user.id))
        _logger.info(f"User logged in: {user.name}")
        return access_token
    
    @staticmethod
    async def signup(request: SignUpRequest) -> UserAccount:
        new_user = UserAccount(
            name=request.name,
            email=request.email,
            password=hashlib.sha256(request.password.encode()).hexdigest(),
            weight=request.weight,
            height=request.height,
            age=request.age,
            gender=request.gender,
            allergies=request.allergies,
            dietary_preferences=request.dietary_preferences,
            profile_picture=request.profile_picture,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        try:
            await new_user.save()
        except DuplicateKeyError:
            raise BadRequestException("Email already registered")
        _logger.info(f"New user created: {new_user.name}")
        return new_user
    
    @staticmethod
    async def get_user_by_id(user_id: str) -> UserResponseData:
        user = await UserAccount.find_one({"_id": PydanticObjectId(user_id)}).project(UserResponseData)
        if not user:
            raise NotFoundException(f"User not found")
        return user
    
    @staticmethod
    async def edit_user(user_id: str, request: dict):
        user = await UserAccount.find_one({"_id": PydanticObjectId(user_id)})
        if not user:
            raise NotFoundException(f"User not found")
        
        # Update query
        request.update({"updated_at": datetime.now()})
        await user.update({"$set": request})