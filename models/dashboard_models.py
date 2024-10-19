from sqlalchemy import Column, Integer, String, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Hotels(Base):
    __tablename__ = "hotels"
    __table_args__ = {"schema": "buttler"}  # Specify your schema name here


    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    Address = Column(String)
    Description = Column(String)


class Users(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "buttler"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    hotel_id = Column(Integer)
    access_level = Column(Integer)
    position = Column(String)
    is_active = Column(Boolean)


class Customers(Base):
    __tablename__ = "customers"
    __table_args__ = {"schema": "buttler"}

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer)
    name = Column(String)
    phone_number = Column(String, index=True)
    room_number = Column(Integer)
    booked_date = Column(String)
    checkin_date = Column(String)
    checkout_date = Column(String)
    description = Column(String)
    language = Column(String)
    special_info = Column(String)
    is_active = Column(Boolean)


class Information(Base):
    __tablename__ = "information"
    __table_args__ = {"schema": "buttler"}

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer)
    criteria = Column(String)
    description = Column(String)
    information = Column(String)
    filename = Column(String)


class DailyInformation(Base):
    __tablename__ = "daily_information"
    __table_args__ = {"schema": "buttler"}

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer)
    criteria = Column(String)
    description = Column(String)
    information = Column(String)
    filename = Column(String)


class Marketing(Base):
    __tablename__ = "marketing"
    __table_args__ = {"schema": "buttler"}

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer)
    criteria = Column(String)
    description = Column(String)
    filename = Column(String)
    trigger_point = Column(String)
    is_active = Column(Boolean)


class Actions(Base):
    __tablename__ = "actions"
    __table_args__ = {"schema": "buttler"}

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer)
    function = Column(String)
    name = Column(String)
    description = Column(String)
    fields = Column(JSON)  # Store as JSON to handle dynamic fields
    is_active = Column(Boolean)


class Orders(Base):
    __tablename__ = "orders"
    __table_args__ = {"schema": "buttler"}

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer)
    function = Column(String)
    name = Column(String)
    description = Column(String)
    fields = Column(JSON)  # Store as JSON to handle dynamic fields
    status = Column(Integer)
    special_notes = Column(String)
