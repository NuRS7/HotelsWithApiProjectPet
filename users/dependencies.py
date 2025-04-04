from datetime import datetime, timezone
from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError
from users.models import Users
from config import settings
from users.repository import UserRepository


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_424_FAILED_DEPENDENCY)
    return token


async def get_current_user(token:str =Depends(get_token)): #get token функцияга зависит
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    expire: str = payload.get("exp")
    if not expire or datetime.fromtimestamp(int(expire), tz=timezone.utc) < datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user_id : str = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user = await UserRepository.find_one_or_none(id =int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user


async def get_current_admin_user(current_user: Users = Depends(get_current_user)):
    # if current_user.role !="admin":
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return current_user
