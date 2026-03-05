from pydantic import BaseModel, EmailStr


class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str


class UserRegisterResponse(BaseModel):
    access_token: str
