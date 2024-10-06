from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.admin_manager import AdminManager
from database.postgres_manager import PostgresManager
from database.redis_cache_manager import RedisCacheManager


def check_eligibility(phone_number):
    rcm = RedisCacheManager()
    rcm.connect()

    customer_details = rcm.is_customer(phone_number)
    if customer_details:
        return customer_details[0]

    order_manager = PostgresManager()

    customer_details = order_manager.get_customer(phone_number)
    if customer_details:
        rcm.add_is_customer(phone_number, customer_details)
        return customer_details
