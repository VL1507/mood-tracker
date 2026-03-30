from pydantic import BaseModel


class UserRefreshResponse(BaseModel):
    access_token: str
