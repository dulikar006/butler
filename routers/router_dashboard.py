from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.dashboard_manager import DashboardManager  # Assuming you have this in the same directory
from models.dashboard_models import Hotels, Users, Customers, Information, DailyInformation, Marketing, Actions, Orders


# Create an instance of DashboardManager
dashboard_manager = DashboardManager()

# Create the FastAPI router
router = APIRouter(prefix="/dashboard")


# Define request schemas for Hotels
class HotelCreate(BaseModel):
    name: str
    address: str
    description: str


class HotelUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None


# Request schemas for Users
class UserCreate(BaseModel):
    name: str
    hotel_id: int
    access_level: int
    position: str
    is_active: bool


class UserUpdate(BaseModel):
    name: Optional[str] = None
    hotel_id: Optional[int] = None
    access_level: Optional[int] = None
    position: Optional[str] = None
    is_active: Optional[bool] = None


# Add more request schemas similarly for Customers, Information, etc.
# Example for Customers
class CustomerCreate(BaseModel):
    name: str
    hotel_id: int
    phone_number: str
    room_number: int
    booked_date: str
    checkin_date: str
    checkout_date: str
    description: str
    language: str
    special_info: str
    is_active: bool


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    hotel_id: Optional[int] = None
    phone_number: Optional[str] = None
    room_number: Optional[int] = None
    booked_date: Optional[str] = None
    checkin_date: Optional[str] = None
    checkout_date: Optional[str] = None
    description: Optional[str] = None
    language: Optional[str] = None
    special_info: Optional[str] = None
    is_active: Optional[bool] = None


class InformationCreate(BaseModel):
    hotel_id: int
    criteria: str
    description: str
    information: str
    filename: Optional[str] = None


class InformationUpdate(BaseModel):
    hotel_id: Optional[int] = None
    criteria: Optional[str] = None
    description: Optional[str] = None
    information: Optional[str] = None
    filename: Optional[str] = None


class MarketingCreate(BaseModel):
    hotel_id: int
    criteria: str
    description: str
    filename: Optional[str] = None
    trigger_point: Optional[str] = None
    is_active: bool


class MarketingUpdate(BaseModel):
    hotel_id: Optional[int] = None
    criteria: Optional[str] = None
    description: Optional[str] = None
    filename: Optional[str] = None
    trigger_point: Optional[str] = None
    is_active: Optional[bool] = None


class DailyInformationCreate(BaseModel):
    hotel_id: int
    criteria: str
    description: str
    information: str
    filename: Optional[str] = None


class DailyInformationUpdate(BaseModel):
    hotel_id: Optional[int] = None
    criteria: Optional[str] = None
    description: Optional[str] = None
    information: Optional[str] = None
    filename: Optional[str] = None


class ActionsCreate(BaseModel):
    hotel_id: int
    function: str
    name: str
    description: str
    fields: dict
    is_active: bool


class ActionsUpdate(BaseModel):
    hotel_id: Optional[int] = None
    function: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    fields: Optional[dict] = None
    is_active: Optional[bool] = None


class OrdersCreate(BaseModel):
    hotel_id: int
    function: str
    name: str
    description: str
    fields: dict
    status: int
    special_notes: Optional[str] = None


class OrdersUpdate(BaseModel):
    hotel_id: Optional[int] = None
    function: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    fields: Optional[dict] = None
    status: Optional[int] = None
    special_notes: Optional[str] = None


# Dependency to get the session
async def get_session():
    async for session in dashboard_manager.get_db_session():
        yield session


# Routes for Hotels
@router.get("/hotels", response_model=List[HotelCreate])
async def get_hotels(limit: int = 100, session: AsyncSession = Depends(get_session)):
    return await dashboard_manager.fetch_all_hotels(session, limit=limit)


@router.post("/hotels", response_model=HotelCreate)
async def create_hotel(hotel: HotelCreate, session: AsyncSession = Depends(get_session)):
    return await dashboard_manager.add_hotel(session, name=hotel.name, address=hotel.address,
                                             description=hotel.description)


@router.put("/hotels/{hotel_id}", response_model=HotelCreate)
async def update_hotel(hotel_id: int, hotel: HotelUpdate, session: AsyncSession = Depends(get_session)):
    query = select(Hotels).filter_by(id=hotel_id)
    result = await session.execute(query)
    existing_hotel = result.scalar_one_or_none()
    if not existing_hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")

    # Update fields
    if hotel.name:
        existing_hotel.name = hotel.name
    if hotel.address:
        existing_hotel.address = hotel.address
    if hotel.description:
        existing_hotel.description = hotel.description

    await session.commit()
    await session.refresh(existing_hotel)
    return existing_hotel


# Routes for Users
@router.get("/users", response_model=List[UserCreate])
async def get_users(limit: int = 100, session: AsyncSession = Depends(get_session)):
    return await dashboard_manager.fetch_all_users(session, limit=limit)


@router.post("/users", response_model=UserCreate)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    return await dashboard_manager.add_user(session,
                                            name=user.name,
                                            hotel_id=user.hotel_id,
                                            access_level=user.access_level,
                                            position=user.position,
                                            is_active=user.is_active)


@router.put("/users/{user_id}", response_model=UserCreate)
async def update_user(user_id: int, user: UserUpdate, session: AsyncSession = Depends(get_session)):
    query = select(Users).filter_by(id=user_id)
    result = await session.execute(query)
    existing_user = result.scalar_one_or_none()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update fields
    if user.name:
        existing_user.name = user.name
    if user.hotel_id:
        existing_user.hotel_id = user.hotel_id
    if user.access_level:
        existing_user.access_level = user.access_level
    if user.position:
        existing_user.position = user.position
    if user.is_active is not None:
        existing_user.is_active = user.is_active

    await session.commit()
    await session.refresh(existing_user)
    return existing_user


# Similarly, create routes for Customers, Information, DailyInformation, Marketing, Actions, Orders

# Example: Routes for Customers
@router.get("/customers", response_model=List[CustomerCreate])
async def get_customers(limit: int = 100, session: AsyncSession = Depends(get_session)):
    return await dashboard_manager.fetch_all_customers(session, limit=limit)


@router.post("/customers", response_model=CustomerCreate)
async def create_customer(customer: CustomerCreate, session: AsyncSession = Depends(get_session)):
    return await dashboard_manager.add_customer(session,
                                                name=customer.name,
                                                hotel_id=customer.hotel_id,
                                                phone_number=customer.phone_number,
                                                room_number=customer.room_number,
                                                booked_date=customer.booked_date,
                                                checkin_date=customer.checkin_date,
                                                checkout_date=customer.checkout_date,
                                                description=customer.description,
                                                language=customer.language,
                                                special_info=customer.special_info,
                                                is_active=customer.is_active)


@router.put("/customers/{customer_id}", response_model=CustomerCreate)
async def update_customer(customer_id: int, customer: CustomerUpdate, session: AsyncSession = Depends(get_session)):
    query = select(Customers).filter_by(id=customer_id)
    result = await session.execute(query)
    existing_customer = result.scalar_one_or_none()
    if not existing_customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Update fields
    if customer.name:
        existing_customer.name = customer.name
    if customer.hotel_id:
        existing_customer.hotel_id = customer.hotel_id
    if customer.phone_number:
        existing_customer.phone_number = customer.phone_number
    if customer.room_number:
        existing_customer.room_number = customer.room_number
    if customer.booked_date:
        existing_customer.booked_date = customer.booked_date
    if customer.checkin_date:
        existing_customer.checkin_date = customer.checkin_date
    if customer.checkout_date:
        existing_customer.checkout_date = customer.checkout_date
    if customer.description:
        existing_customer.description = customer.description
    if customer.language:
        existing_customer.language = customer.language
    if customer.special_info:
        existing_customer.special_info = customer.special_info
    if customer.is_active is not None:
        existing_customer.is_active = customer.is_active

    await session.commit()
    await session.refresh(existing_customer)
    return existing_customer


@router.get("/information", response_model=List[InformationCreate])
async def get_information(limit: int = 100, session: AsyncSession = Depends(get_session)):
    return await dashboard_manager.fetch_all_information(session, limit=limit)


@router.post("/information", response_model=InformationCreate)
async def create_information(info: InformationCreate, session: AsyncSession = Depends(get_session)):
    return await dashboard_manager.add_information(session,
                                                   hotel_id=info.hotel_id,
                                                   criteria=info.criteria,
                                                   description=info.description,
                                                   information=info.information,
                                                   filename=info.filename)


@router.put("/information/{information_id}", response_model=InformationCreate)
async def update_information(information_id: int, info: InformationUpdate,
                             session: AsyncSession = Depends(get_session)):
    query = select(Information).filter_by(id=information_id)
    result = await session.execute(query)
    existing_info = result.scalar_one_or_none()
    if not existing_info:
        raise HTTPException(status_code=404, detail="Information not found")

    # Update fields
    if info.hotel_id:
        existing_info.hotel_id = info.hotel_id
    if info.criteria:
        existing_info.criteria = info.criteria
    if info.description:
        existing_info.description = info.description
    if info.information:
        existing_info.information = info.information
    if info.filename:
        existing_info.filename = info.filename

    await session.commit()
    await session.refresh(existing_info)
    return existing_info


@router.get("/marketing", response_model=List[MarketingCreate])
async def get_marketing(limit: int = 100, session: AsyncSession = Depends(get_session)):
    return await dashboard_manager.fetch_all_marketing(session, limit=limit)


@router.post("/marketing", response_model=MarketingCreate)
async def create_marketing(marketing: MarketingCreate, session: AsyncSession = Depends(get_session)):
    return await dashboard_manager.add_marketing(session,
                                                 hotel_id=marketing.hotel_id,
                                                 criteria=marketing.criteria,
                                                 description=marketing.description,
                                                 filename=marketing.filename,
                                                 trigger_point=marketing.trigger_point,
                                                 is_active=marketing.is_active)


@router.put("/marketing/{marketing_id}", response_model=MarketingCreate)
async def update_marketing(marketing_id: int, marketing: MarketingUpdate, session: AsyncSession = Depends(get_session)):
    query = select(Marketing).filter_by(id=marketing_id)
    result = await session.execute(query)
    existing_marketing = result.scalar_one_or_none()
    if not existing_marketing:
        raise HTTPException(status_code=404, detail="Marketing record not found")

    # Update fields
    if marketing.hotel_id:
        existing_marketing.hotel_id = marketing.hotel_id
    if marketing.criteria:
        existing_marketing.criteria = marketing.criteria
    if marketing.description:
        existing_marketing.description = marketing.description
    if marketing.filename:
        existing_marketing.filename = marketing.filename
    if marketing.trigger_point:
        existing_marketing.trigger_point = marketing.trigger_point
    if marketing.is_active is not None:
        existing_marketing.is_active = marketing.is_active

    await session.commit()
    await session.refresh(existing_marketing)
    return existing_marketing


@router.get("/daily_information", response_model=List[DailyInformationCreate])
async def get_daily_information(limit: int = 100, session: AsyncSession = Depends(get_session)):
    return await dashboard_manager.fetch_all_daily_information(session, limit=limit)


@router.post("/daily_information", response_model=DailyInformationCreate)
async def create_daily_information(info: DailyInformationCreate, session: AsyncSession = Depends(get_session)):
    return await dashboard_manager.add_daily_information(session,
                                                         hotel_id=info.hotel_id,
                                                         criteria=info.criteria,
                                                         description=info.description,
                                                         information=info.information,
                                                         filename=info.filename)


@router.put("/daily_information/{daily_information_id}", response_model=DailyInformationCreate)
async def update_daily_information(daily_information_id: int, info: DailyInformationUpdate,
                                   session: AsyncSession = Depends(get_session)):
    query = select(DailyInformation).filter_by(id=daily_information_id)
    result = await session.execute(query)
    existing_info = result.scalar_one_or_none()
    if not existing_info:
        raise HTTPException(status_code=404, detail="Daily Information not found")

    # Update fields
    if info.hotel_id:
        existing_info.hotel_id = info.hotel_id
    if info.criteria:
        existing_info.criteria = info.criteria
    if info.description:
        existing_info.description = info.description
    if info.information:
        existing_info.information = info.information
    if info.filename:
        existing_info.filename = info.filename

    await session.commit()
    await session.refresh(existing_info)
    return existing_info


@router.get("/actions", response_model=List[ActionsCreate])
async def get_actions(limit: int = 100, session: AsyncSession = Depends(get_session)):
    return await dashboard_manager.fetch_all_actions(session, limit=limit)


@router.post("/actions", response_model=ActionsCreate)
async def create_actions(action: ActionsCreate, session: AsyncSession = Depends(get_session)):
    return await dashboard_manager.add_action(session,
                                              hotel_id=action.hotel_id,
                                              function=action.function,
                                              name=action.name,
                                              description=action.description,
                                              fields=action.fields,
                                              is_active=action.is_active)


@router.put("/actions/{action_id}", response_model=ActionsCreate)
async def update_action(action_id: int, action: ActionsUpdate, session: AsyncSession = Depends(get_session)):
    query = select(Actions).filter_by(id=action_id)
    result = await session.execute(query)
    existing_action = result.scalar_one_or_none()
    if not existing_action:
        raise HTTPException(status_code=404, detail="Action not found")

    # Update fields
    if action.hotel_id:
        existing_action.hotel_id = action.hotel_id
    if action.function:
        existing_action.function = action.function
    if action.name:
        existing_action.name = action.name
    if action.description:
        existing_action.description = action.description
    if action.fields is not None:
        existing_action.fields = action.fields
    if action.is_active is not None:
        existing_action.is_active = action.is_active

    await session.commit()
    await session.refresh(existing_action)
    return existing_action


@router.get("/orders", response_model=List[OrdersCreate])
async def get_orders(limit: int = 100, session: AsyncSession = Depends(get_session)):
    return await dashboard_manager.fetch_all_orders(session, limit=limit)


@router.post("/orders", response_model=OrdersCreate)
async def create_orders(order: OrdersCreate, session: AsyncSession = Depends(get_session)):
    return await dashboard_manager.add_order(session,
                                             hotel_id=order.hotel_id,
                                             function=order.function,
                                             name=order.name,
                                             description=order.description,
                                             fields=order.fields,
                                             status=order.status,
                                             special_notes=order.special_notes)


@router.put("/orders/{order_id}", response_model=OrdersCreate)
async def update_order(order_id: int, order: OrdersUpdate, session: AsyncSession = Depends(get_session)):
    query = select(Orders).filter_by(id=order_id)
    result = await session.execute(query)
    existing_order = result.scalar_one_or_none()
    if not existing_order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Update fields
    if order.hotel_id:
        existing_order.hotel_id = order.hotel_id
    if order.function:
        existing_order.function = order.function
    if order.name:
        existing_order.name = order.name
    if order.description:
        existing_order.description = order.description
    if order.fields is not None:
        existing_order.fields = order.fields
    if order.status is not None:
        existing_order.status = order.status
    if order.special_notes:
        existing_order.special_notes = order.special_notes

    await session.commit()
    await session.refresh(existing_order)
    return existing_order
