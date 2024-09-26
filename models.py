from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


# class Mode(str, Enum):
#     """
#     Enum of tha aviable input
#     """
#
#     addition = "SUM"
#     subtraction = "SUB"
#     multiplication = "PROD"
#     all = "ALL"
#
#
# class Results(BaseModel):
#     addition: Optional[int] = None
#     subtraction: Optional[int] = None
#     multiplication: Optional[int] = None
#
#
# class Compute(BaseModel):
#     db_number: int
#     results: Results
#
#
# class Compute_all(BaseModel):
#     db_number: int
#     results: List[Results]
