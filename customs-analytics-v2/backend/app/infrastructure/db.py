import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

# Load environment variables (defaults to .env)
load_dotenv()

# We expect an asyncpg URL for async SQLAlchemy operations
# Example: postgresql+asyncpg://postgres:postgres@localhost:5434/customs_v2_db
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+asyncpg://postgres:postgres@localhost:5434/customs_v2_db"
)

# Create the async SQLAlchemy engine
# pool_pre_ping ensures connections are alive before using them
engine = create_async_engine(
    DATABASE_URL, 
    echo=False,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

# Create the configured AsyncSession class
AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Base class for declarative models
Base = declarative_base()

async def get_db_session() -> AsyncSession:
    """
    Dependency function for FastAPI to yield a database session.
    Automatically closes the session after use.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
