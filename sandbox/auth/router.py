# app/auth/router.py
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session # Changed import
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from sandbox.core.db import get_db
from sandbox.auth import schemas, security, models
from sandbox.api.deps import get_current_active_user

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

# Make function synchronous
@router.post("/token", response_model=schemas.Token)
def login_for_access_token( # Changed from async def
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)] # Changed type hint
):
    query = select(models.User).where(models.User.email == form_data.username)
    # NO await
    user = db.execute(query).scalar_one_or_none()

    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
         raise HTTPException(status_code=400, detail="Inactive user")

    access_token = security.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Make function synchronous
@router.post("/register", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def register_user( # Changed from async def
    user_in: schemas.UserCreate,
    db: Annotated[Session, Depends(get_db)] # Changed type hint
):
    query = select(models.User).where(models.User.email == user_in.email)
    # NO await
    existing_user = db.execute(query).scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    hashed_password = security.get_password_hash(user_in.password)
    db_user = models.User(
        email=user_in.email,
        hashed_password=hashed_password,
        is_active=True
    )

    db.add(db_user)
    try:
        # NO await
        db.commit()
        # NO await
        db.refresh(db_user)
    except IntegrityError:
        # NO await needed for rollback
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered (race condition)",
        )
    except Exception:
        # NO await needed for rollback
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not register user",
        )
    return db_user

# Make function synchronous
@router.get("/users/me", response_model=schemas.User)
def read_users_me( # Changed from async def
    current_user: Annotated[models.User, Depends(get_current_active_user)]
):
    return current_user