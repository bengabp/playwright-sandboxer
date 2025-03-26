# app/api/deps.py
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session # Changed import
from sqlalchemy import select

from sandbox.core.db import get_db # Imports SessionLocal implicitly
from sandbox.auth import security, schemas
from sandbox.auth.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# Make function synchronous
def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)] # Changed type hint
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = security.decode_access_token(token)
    if token_data is None or token_data.email is None:
        raise credentials_exception

    # Fetch user from database (NO await)
    query = select(User).where(User.email == token_data.email)
    # Execute synchronously
    user = db.execute(query).scalar_one_or_none() # Simplified execution for scalar

    if user is None:
        raise credentials_exception
    if not user.is_active:
         raise HTTPException(status_code=400, detail="Inactive user")
    return user

# Make function synchronous
def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    # This dependency simply relies on the now-synchronous get_current_user
    return current_user