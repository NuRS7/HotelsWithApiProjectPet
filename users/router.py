
from fastapi import APIRouter, HTTPException

from users.schemas import SchemasUser
from users.repository import UserRepository
from users.auth import get_password_hash

router = APIRouter(

    prefix="/auth",
    tags=["auth && Юзеры"],
)



@router.post("/register")
async def register(user_data: SchemasUser):
    existing_user = await UserRepository.find_one_or_none(email=user_data.email) #тексеремиз емайлды бар ма жок па
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    else:
        hashed_password =get_password_hash(user_data.password)
        await UserRepository.add(email=user_data.email, hashed_password=hashed_password)




