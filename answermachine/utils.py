from datetime import datetime
from typing import NamedTuple

UserStatus = NamedTuple(
    "UserStatus", name=str, was_online=datetime, expires_datetime=datetime
)
