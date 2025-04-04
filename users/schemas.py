
from pydantic import BaseModel, EmailStr


class SchemasAuth(BaseModel):
    email : EmailStr
    password : str