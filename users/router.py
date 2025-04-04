
from fastapi import APIRouter, HTTPException, Response, status, Depends

from users.dependencies import get_current_user, get_current_admin_user
from users.models import Users
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
    access_token = create_access_token({"sub":str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return {"access_token": access_token}



@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")


@router.get("/me")
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user


@router.get("/all")
async def read_users_me(current_user:Users = Depends(get_current_admin_user)):
    return await UserRepository.find_all()
