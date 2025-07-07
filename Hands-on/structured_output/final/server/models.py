from typing import List
from pydantic import BaseModel, Field


class Query(BaseModel):
    query: str


class FlightSearch(BaseModel):
    departure_airport: str
    destination_airport: str
    departure_date: str
    return_date: str
    number_of_persons: int
    airlines: List[str]
    booking_class: str = Field(default='economy')
