
from pydantic import BaseModel, EmailStr


class SchemasUser(BaseModel):
    email : EmailStr
    password : str