from pydantic import BaseModel
from datetime import datetime


class Travel(BaseModel):
    """Travels parsed from Viajando channel"""

    origin: str
    destination: str
    transport: str
    section: str
    date_time: datetime
    day_of_week: str
    seat: int

    def __repr__(self) -> str:
        out = f"From {self.origin} to {self.destination} at {self.transport}"
        return out
