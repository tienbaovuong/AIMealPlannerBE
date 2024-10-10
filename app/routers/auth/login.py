from fastapi import APIRouter, Depends

from app.dto.common import BaseResponse
from app.dto.auth_dto import LoginRequest, LoginResponseData, LoginResponse, SignUpRequest, UserResponse, EditRequest
from app.services.account_services import AuthService
from app.helpers.auth_helpers import get_current_user

router = APIRouter(tags=['Auth'], prefix="/account")


@router.post(
    '/login',
    response_model=LoginResponse
)
async def user_login(
    data: LoginRequest
):
    access_token = await AuthService.login(
        email=data.email, 
        password=data.password
    )
    return LoginResponse(
        message='Logged in',
        data=LoginResponseData(access_token=access_token)
    )


@router.post(
    '/signup',
    response_model=BaseResponse
)
async def user_signup(
    data: SignUpRequest
):
    await AuthService.signup(
        request=data
    )
    return BaseResponse(
        message='Succeed',
        error_code=0
    )


@router.get(
    '/profile',
    response_model=UserResponse
)
async def get_user(
    user_id: str = Depends(get_current_user),
):
    user = await AuthService.get_user_by_id(user_id)
    return UserResponse(
        message='Succeed',
        data=user
    )


@router.put(
    '/edit',
    response_model=BaseResponse
)
async def edit_current_user(
    edit_request: EditRequest,
    user_id: str = Depends(get_current_user),
):
    await AuthService.edit_user(user_id, edit_request.dict())
    return BaseResponse(
        message='Edited user profiled successfully',
    )

