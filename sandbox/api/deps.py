from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select # Import select explicitly

from app.core.db import get_db
from app.auth import security, schemas
from app.auth.models import User # Import the model

# OAuth2 scheme definition
# tokenUrl should point to your token endpoint (e.g., "/auth/token")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> User:
    """
    Dependency to get the current authenticated user.
    Decodes the JWT token and fetches the user from the database.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = security.decode_access_token(token)
    if token_data is None or token_data.email is None:
        raise credentials_exception

    # Fetch user from database based on email in token
    query = select(User).where(User.email == token_data.email)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception
    # You might add checks here, e.g., if user.is_active:
    if not user.is_active:
         raise HTTPException(status_code=400, detail="Inactive user")
    return user

# Dependency for getting the current active user (often used together)
async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    # This function primarily exists to be explicitly used in route signatures
    # making it clear that an *active* user is required.
    # The active check is already in get_current_user, but this adds semantic clarity.
    # If further active-specific checks were needed, they'd go here.
    return current_user
