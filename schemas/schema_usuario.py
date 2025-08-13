from pydantic import BaseModel

class LoginIn(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: str
    username: str
    class Config:
        from_attributes = True
