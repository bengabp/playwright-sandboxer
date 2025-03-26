from sqlalchemy import Column, String, DateTime
from sqlalchemy import Enum as SQLEnum
from sandbox.core.db import Base
from sandbox.core.config import settings
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sandbox.core.enums import SandboxStatus


class Sandbox(Base):
    __tablename__ = "sandboxes"

    id = Column(
        # Use the generic UUID type first, or PostgreSQL specific if preferred
        # UUID(as_uuid=True),
        UUID(as_uuid=True), # Tells SQLAlchemy to handle Python UUID objects
        primary_key=True,
        default=uuid.uuid4, # Generate a new UUID v4 as the default value
        unique=True,
        nullable=False,
        index=True
    )
    created_at = Column(
        DateTime,
        nullable=False,
        default=settings.datetime_now
    )
    twitter_account_id = Column(
        String,
        unique=False, index=True, nullable=True
    )
    status = Column(
        SQLEnum(
            SandboxStatus, # Your Python Enum
            name="sandbox_status_enum", # Optional but good practice: name for potential native type
            values_callable=lambda obj: [e.value for e in obj], # Helps SQLAlchemy validate input values
            native_enum=False # *** Store as VARCHAR ***
        ),
        nullable=False,
        default=SandboxStatus.default(), # Use the default value from the enum
        server_default=SandboxStatus.default().value # Set DB-level default to the string value
    )