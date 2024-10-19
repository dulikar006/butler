import os

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from models.dashboard_models import Hotels, Users, Customers, Information, DailyInformation, Marketing, Actions, Orders


class DashboardUpdateManager:

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

    # Helper function for upsert
    async def upsert(self, session, model, values, index_elements):
        stmt = insert(model).values(values)
        update_stmt = stmt.on_conflict_do_update(
            index_elements=index_elements,  # List of columns to check for conflict
            set_=values  # In case of conflict, update with the same values
        )
        await session.execute(update_stmt)
        await session.commit()

    # Hotels DB Operations
    async def upsert_hotel(self, session: AsyncSession, name: str, address: str, description: str):
        values = {"name": name, "address": address, "description": description}
        await self.upsert(session, Hotels, values, index_elements=["name"])

    # Users DB Operations
    async def upsert_user(self, session: AsyncSession, name: str, hotel_id: int, access_level: int, position: str,
                          is_active: bool):
        values = {
            "name": name,
            "hotel_id": hotel_id,
            "access_level": access_level,
            "position": position,
            "is_active": is_active
        }
        await self.upsert(session, Users, values, index_elements=["name", "hotel_id"])

    # Customers DB Operations
    async def upsert_customer(self, session: AsyncSession, name: str, phone_number: str, room_number: int,
                              booked_date: str,
                              checkin_date: str, checkout_date: str, description: str, language: str, special_info: str,
                              is_active: bool):
        values = {
            "name": name, "phone_number": phone_number, "room_number": room_number,
            "booked_date": booked_date, "checkin_date": checkin_date, "checkout_date": checkout_date,
            "description": description, "language": language, "special_info": special_info, "is_active": is_active
        }
        await self.upsert(session, Customers, values, index_elements=["name", "room_number", "phone_number"])

    # Information DB Operations
    async def upsert_information(self, session: AsyncSession, hotel_id: int, criteria: str, description: str,
                                 information: str, filename: str):
        values = {
            "hotel_id": hotel_id, "criteria": criteria, "description": description,
            "information": information, "filename": filename
        }
        await self.upsert(session, Information, values, index_elements=["hotel_id", "criteria"])

    # Daily Information DB Operations
    async def upsert_daily_information(self, session: AsyncSession, hotel_id: int, criteria: str, description: str,
                                       information: str, filename: str):
        values = {
            "hotel_id": hotel_id, "criteria": criteria, "description": description,
            "information": information, "filename": filename
        }
        await self.upsert(session, DailyInformation, values, index_elements=["hotel_id", "criteria"])

    # Marketing DB Operations
    async def upsert_marketing(self, session: AsyncSession, hotel_id: int, criteria: str, description: str,
                               filename: str, trigger_point: str, is_active: bool):
        values = {
            "hotel_id": hotel_id, "criteria": criteria, "description": description,
            "filename": filename, "trigger_point": trigger_point, "is_active": is_active
        }
        await self.upsert(session, Marketing, values, index_elements=["hotel_id", "criteria"])

    # Actions DB Operations
    async def upsert_action(self, session: AsyncSession, hotel_id: int, function: str, name: str, description: str,
                            fields: list, is_active: bool):
        field_list = [
            {"detail": detail, "example": example, "mandatory_optional": mandatory}
            for detail, example, mandatory in zip(fields["details"], fields["examples"], fields["mandatory_optional"])
        ]
        values = {
            "hotel_id": hotel_id, "function": function, "name": name, "description": description,
            "fields": field_list, "is_active": is_active
        }
        await self.upsert(session, Actions, values, index_elements=["hotel_id", "function", "name"])

    # Orders DB Operations
    async def upsert_order(self, session: AsyncSession, hotel_id: int, function: str, name: str, description: str,
                           fields: list, status: int, special_notes: str):
        values = {
            "hotel_id": hotel_id, "function": function, "name": name, "description": description,
            "fields": fields, "status": status, "special_notes": special_notes
        }
        await self.upsert(session, Orders, values, index_elements=["hotel_id", "function", "name"])
