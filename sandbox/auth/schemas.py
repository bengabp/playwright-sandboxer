from pydantic import BaseModel, EmailStr, ConfigDict

# --- Token Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: EmailStr | None = None
    # If using ID instead of email in token:
    # user_id: int | None = None

# --- User Schemas ---
class UserBase(BaseModel):
    email: EmailStr

# Schema for creating a user (received in request body)
class UserCreate(UserBase):
    password: str

# Schema for reading/returning user data (never include password)
class User(UserBase):
    id: int
    is_active: bool
    # Add other fields exposed via API here

    # Pydantic V2 config for ORM mode
    model_config = ConfigDict(from_attributes=True)
