import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker

from models.dashboard_models import Hotels, Users, Customers, Information, DailyInformation, Marketing, Actions, Orders


class DashboardManager:

    def __init__(self):
        # Define the async engine for PostgreSQL
        self.DASHBOARD_DATABASE_URL = os.environ['postgres_url']
        self.engine = create_async_engine(self.DASHBOARD_DATABASE_URL, echo=True)
        # Create a sessionmaker for async sessions
        self.AsyncSessionLocal = sessionmaker(
            bind=self.engine, class_=AsyncSession, expire_on_commit=False
        )

    # Dependency for getting the database session
    async def get_db_session(self):
        async with self.AsyncSessionLocal() as session:
            yield session

    # Hotels DB Operations
    async def fetch_all_hotels(self, session: AsyncSession, limit=100):
        query = select(Hotels).limit(limit)
        result = await session.execute(query)
        hotels = result.scalars().all()
        return hotels

    async def add_hotel(self, session: AsyncSession, name: str, address: str, description: str):
        new_hotel = Hotels(name=name, address=address, description=description)
        session.add(new_hotel)
        await session.commit()
        await session.refresh(new_hotel)
        return new_hotel

    # Users DB Operations
    async def fetch_all_users(self, session: AsyncSession, limit=100):
        query = select(Users).limit(limit)
        result = await session.execute(query)
        users = result.scalars().all()
        return users

    async def add_user(self, session: AsyncSession, name: str, hotel_id: int, access_level: int, position: str,
                       is_active: bool):
        new_user = Users(name=name, hotel_id=hotel_id, access_level=access_level, position=position,
                         is_active=is_active)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

    # Customers DB Operations
    async def fetch_all_customers(self, session: AsyncSession, limit=100):
        query = select(Customers).limit(limit)
        result = await session.execute(query)
        customers = result.scalars().all()
        return customers

    async def add_customer(self, session: AsyncSession, name: str, hotel_id: int, phone_number: str, room_number: int,
                           booked_date: str,
                           checkin_date: str, checkout_date: str, description: str, language: str, special_info: str,
                           is_active: bool):
        new_customer = Customers(
            name=name, phone_number=phone_number, room_number=room_number, booked_date=booked_date,
            checkin_date=checkin_date, checkout_date=checkout_date, description=description,
            language=language, special_info=special_info, is_active=is_active
        )
        session.add(new_customer)
        await session.commit()
        await session.refresh(new_customer)
        return new_customer

    # Information DB Operations
    async def fetch_all_information(self, session: AsyncSession, limit=100):
        query = select(Information).limit(limit)
        result = await session.execute(query)
        information = result.scalars().all()
        return information

    async def add_information(self, session: AsyncSession, hotel_id: int, criteria: str, description: str,
                              information: str, filename: str):
        new_information = Information(hotel_id=hotel_id, criteria=criteria, description=description,
                                      information=information, filename=filename)
        session.add(new_information)
        await session.commit()
        await session.refresh(new_information)
        return new_information

    # Daily Information DB Operations
    async def fetch_all_daily_information(self, session: AsyncSession, limit=100):
        query = select(DailyInformation).limit(limit)
        result = await session.execute(query)
        daily_information = result.scalars().all()
        return daily_information

    async def add_daily_information(self, session: AsyncSession, hotel_id: int, criteria: str, description: str,
                                    information: str, filename: str):
        new_daily_information = DailyInformation(
            hotel_id=hotel_id, criteria=criteria, description=description, information=information, filename=filename
        )
        session.add(new_daily_information)
        await session.commit()
        await session.refresh(new_daily_information)
        return new_daily_information

    # Marketing DB Operations
    async def fetch_all_marketing(self, session: AsyncSession, limit=100):
        query = select(Marketing).limit(limit)
        result = await session.execute(query)
        marketing = result.scalars().all()
        return marketing

    async def add_marketing(self, session: AsyncSession, hotel_id: int, criteria: str, description: str, filename: str,
                            trigger_point: str, is_active: bool):
        new_marketing = Marketing(
            hotel_id=hotel_id, criteria=criteria, description=description, filename=filename,
            trigger_point=trigger_point, is_active=is_active
        )
        session.add(new_marketing)
        await session.commit()
        await session.refresh(new_marketing)
        return new_marketing

    # Actions DB Operations
    async def fetch_all_actions(self, session: AsyncSession, limit=100):
        query = select(Actions).limit(limit)
        result = await session.execute(query)
        actions = result.scalars().all()
        return actions

    async def add_action(self, session: AsyncSession, hotel_id: int, function: str, name: str, description: str,
                         fields: list, is_active: bool):
        field_list = [
            {"detail": detail, "example": example, "mandatory_optional": mandatory}
            for detail, example, mandatory in zip(fields["details"], fields["examples"], fields["mandatory_optional"])
        ]
        new_action = Actions(
            hotel_id=hotel_id, function=function, name=name, description=description, fields=field_list,
            is_active=is_active
        )
        session.add(new_action)
        await session.commit()
        await session.refresh(new_action)
        return new_action

    # Orders DB Operations
    async def fetch_all_orders(self, session: AsyncSession, limit=100):
        query = select(Orders).limit(limit)
        result = await session.execute(query)
        orders = result.scalars().all()
        return orders

    async def add_order(self, session: AsyncSession, hotel_id: int, function: str, name: str, description: str,
                        fields: list, status: int, special_notes: str):
        new_order = Orders(
            hotel_id=hotel_id, function=function, name=name, description=description, fields=fields, status=status,
            special_notes=special_notes
        )
        session.add(new_order)
        await session.commit()
        await session.refresh(new_order)
        return new_order
