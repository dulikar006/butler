# from typing import Generator
#
# from mock import Mock
#
#
# class DB(Mock):
#     @staticmethod
#     def get_number():
#         return 5
#
#
# def get_db() -> Generator:
#     """
#     Function to use as a Dependency in the FastAPI endpoints.
#     Returns an inicialized DataBase object to be used inside
#     the endpoint functions.
#
#     Returns
#     -------
#     - Generator: data base generator
#     """
#     # Replace this with ths DB connection
#     db = DB()
#     try:
#         yield db
#     finally:
#         db.close()
