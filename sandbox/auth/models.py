from sqlalchemy import Column, Integer, String, Boolean
from sandbox.core.db import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True), # Tells SQLAlchemy to handle Python UUID objects
        primary_key=True,
        default=uuid.uuid4, # Generate a new UUID v4 as the default value
        unique=True,
        nullable=False,
        index=True
    )
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
