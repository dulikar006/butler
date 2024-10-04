import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker

from models.admin_models import Customer, UploadedFile, Brochure, Action


class AdminManager:

    def __init__(self):
        # Define the async engine for PostgreSQL
        self.DATABASE_URL = os.environ['postgres_url']
        self.engine = create_async_engine(self.DATABASE_URL, echo=True)
        # Create a sessionmaker for async sessions
        self.AsyncSessionLocal = sessionmaker(
            bind=self.engine, class_=AsyncSession, expire_on_commit=False
        )

    # Dependency for getting the database session
    async def get_db_session(self):
        async with self.AsyncSessionLocal() as session:
            yield session

    # Customers DB Operations
    async def fetch_all_customers(self, session: AsyncSession, limit=100):
        query = select(Customer).limit(limit)
        result = await session.execute(query)
        customers = result.scalars().all()
        return customers

    async def add_customer(self, session: AsyncSession, name: str, phone_number: str, room_number: int,
                           checkout_date: str):
        new_customer = Customer(name=name, phone_number=phone_number, room_number=room_number,
                                checkout_date=checkout_date)
        session.add(new_customer)
        await session.commit()
        await session.refresh(new_customer)
        return new_customer

    # Uploaded Files DB Operations
    async def upload_file(self, session: AsyncSession, criteria: str, description: str, information: str, filename: str):
        new_file = UploadedFile(criteria=criteria, description=description, information=information, filename=filename)
        session.add(new_file)
        await session.commit()
        await session.refresh(new_file)
        return new_file

    # Brochures DB Operations
    async def upload_brochures(self, session: AsyncSession, criteria: str, description: str, filename: str):
        new_brochure = Brochure(criteria=criteria, description=description, filename=filename)
        session.add(new_brochure)
        await session.commit()
        await session.refresh(new_brochure)
        return new_brochure

    # Actions DB Operations
    async def add_action(self, session: AsyncSession, function: str, name: str, description: str, fields: list):
        field_list = [
            {"detail": detail, "example": example, "mandatory_optional": mandatory}
            for detail, example, mandatory in zip(fields["details"], fields["examples"], fields["mandatory_optional"])
        ]
        new_action = Action(function=function, name=name, description=description, fields=field_list)
        session.add(new_action)
        await session.commit()
        await session.refresh(new_action)
        return new_action
