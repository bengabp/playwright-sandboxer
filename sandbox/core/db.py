from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.core.config import settings
import logging

# Configure logging to see SQL statements if needed (optional)
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Create the async engine
# pool_recycle helps prevent connection issues on long-idle connections
# echo=True will log SQL statements - useful for debugging, disable in production
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False, # Set to True for debugging SQL
    pool_recycle=3600 # Recycle connections every hour
)

# Create the async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False # Important for FastAPI background tasks
)

# Base class for SQLAlchemy models
Base = declarative_base()

# Dependency to get DB session
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close() # Ensure session is closed
