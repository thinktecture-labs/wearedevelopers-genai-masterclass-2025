# This file makes the tools directory a Python package
from .employee_tools import get_employee_id
from .booking_tools import book_slot

__all__ = ["get_employee_id", "book_slot"]
