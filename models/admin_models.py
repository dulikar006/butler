from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone_number = Column(String, index=True)
    room_number = Column(Integer)
    checkout_date = Column(String)


class UploadedFile(Base):
    __tablename__ = "uploaded_files"

    id = Column(Integer, primary_key=True, index=True)
    criteria = Column(String)
    description = Column(String)
    information = Column(String)
    filename = Column(String)


class Brochure(Base):
    __tablename__ = "brochures"

    id = Column(Integer, primary_key=True, index=True)
    criteria = Column(String)
    description = Column(String)
    filename = Column(String)


class Action(Base):
    __tablename__ = "actions"

    id = Column(Integer, primary_key=True, index=True)
    function = Column(String)
    name = Column(String)
    description = Column(String)
    fields = Column(JSON)  # Store as JSON to handle dynamic fields
