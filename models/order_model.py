from psycopg2.extensions import JSONB
from sqlalchemy import Column, Integer, String, DateTime, func, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

# Define the Order model
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    criteria = Column(String, nullable=False)
    customer_details = Column(JSONB)  # New JSONB column for customer details
    status = Column(String)  # New column for order status
    created_at = Column(TIMESTAMP, server_default=func.now())  # Created at timestamp with default value
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
