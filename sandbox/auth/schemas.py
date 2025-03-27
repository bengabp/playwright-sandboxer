from pydantic import BaseModel, EmailStr, ConfigDict, UUID4

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: EmailStr | None = None

class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str

class TokenRequest(UserBase):
    password: str

class User(UserBase):
    id: UUID4
    is_active: bool
    model_config = ConfigDict(from_attributes=True)
