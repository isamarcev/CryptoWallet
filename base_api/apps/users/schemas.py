

from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    password2: str
