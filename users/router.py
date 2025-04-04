
from fastapi import APIRouter, HTTPException, Response
from starlette import status

from users.schemas import SchemasAuth
from users.repository import UserRepository
from users.auth import get_password_hash, verify_password, authenticate_user, create_access_token

router = APIRouter(

    prefix="/auth",
    tags=["auth && Юзеры"],
)



@router.post("/register")
async def register(user_data: SchemasAuth):
    existing_user = await UserRepository.find_one_or_none(email=user_data.email) #тексеремиз емайлды бар ма жок па
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    else:
        hashed_password =get_password_hash(user_data.password)
        await UserRepository.add(email=user_data.email, hashed_password=hashed_password)

@router.post("/login")
async def login(response: Response,user_data: SchemasAuth):
    # user = UserRepository.find_one_or_none(email=user_data.email)
    # if not user:
    #     raise HTTPException(status_code=400, detail="Email not registered")
    # else:
    #     password_valid = verify_password(user_data.password, user_data.password)
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    access_token = create_access_token({"sub":user.id})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return access_token
