import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text  # Import the text function
from models.order_model import Order


class OrderManager:

    def __init__(self):
        self.DATABASE_URL = os.environ['postgres_url']
        # Use async engine
        self.engine = create_async_engine(self.DATABASE_URL, echo=True)
        # Use AsyncSession instead of regular sessionmaker
        self.SessionLocal = sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            class_=AsyncSession
        )

    async def get_session(self):
        """Create a new session asynchronously."""
        async with self.SessionLocal() as session:
            yield session

    async def store_table_row(self, name: str, description: str, criteria: str):
        """Store a new row in the PostgreSQL table asynchronously."""
        async with self.SessionLocal() as session:
            new_row = Order(name=name, description=description, criteria=criteria)
            session.add(new_row)
            await session.commit()

    async def get_table_data(self):
        """Retrieve all rows from the PostgreSQL table asynchronously."""
        async with self.SessionLocal() as session:
            result = await session.execute(text("SELECT * FROM orders"))  # Use text() for the query
            rows = result.scalars().all()
            return rows

    async def delete_all_rows(self):
        """Delete all rows from the PostgreSQL table asynchronously."""
        async with self.SessionLocal() as session:
            await session.execute(text("DELETE FROM orders"))  # Use text() for the query
            await session.commit()

    async def get_next_id(self):
        """Get the next available ID (auto-incremented in PostgreSQL) asynchronously."""
        async with self.SessionLocal() as session:
            # Fetch the count using a text query
            result = await session.execute(text("SELECT COUNT(*) FROM orders"))
            count = result.scalar()  # Get the scalar result
            return count + 1
